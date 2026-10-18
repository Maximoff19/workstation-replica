#!/usr/bin/env python3
"""Stage an existing reviewed replica for publication, never the live HOME tree."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--skill", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    if (root / "snapshot").exists() or (root / "dist").exists():
        parser.error("Refusing to overwrite an existing staged snapshot or release")
    skill = args.skill.resolve()
    source = skill / "scripts/replica.py"
    spec = importlib.util.spec_from_file_location("replica", source)
    replica = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(replica)
    manifest, files = replica.load(args.bundle)
    # Only the validated manifest payload is materialized. Do not extract arbitrary ZIP paths.
    for name, data in files.items():
        path = root / "snapshot/payload" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(manifest["files"][name]["mode"])
    (root / "snapshot/manifest.json").write_bytes(replica.encoded(manifest))
    for name in ("SKILL.md", "scripts/replica.py", "scripts/test_replica.py", "references/source-notes.md", "references/runtime-setup.md"):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(skill / name, path)
    dist = root / "dist"
    dist.mkdir()
    release = dist / "workstation-replica.zip"
    shutil.copyfile(args.bundle, release)
    checksum = hashlib.sha256(release.read_bytes()).hexdigest()
    (dist / "SHA256SUMS").write_text(checksum + "  workstation-replica.zip\n")
    with zipfile.ZipFile(release) as archive:
        if archive.read("replica.py") != source.read_bytes():
            raise ValueError("Release tool differs from the reviewed source")
    print(json.dumps({"root": str(root), "payload_files": len(files), "sha256": checksum}, indent=2))


if __name__ == "__main__":
    main()
