#!/usr/bin/env python3
"""Portable, reviewed-file replication; no package installs or config execution."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
import zipfile


CORE = (".config/nvim", ".config/opencode", ".agents/skills", ".claude/skills")
TERMINAL = (".config/ghostty", ".config/zellij", ".config/tmux", ".tmux.conf")
UI = ".local/state/opencode/kv.json"
SKILL_ROOTS = (".config/opencode/skills", ".config/opencode/skill", ".agents/skills", ".claude/skills")
SKIP_DIRS = {".git", ".codegraph", "node_modules", "__pycache__", ".venv", "cache", "backups", "profile-versions"}
SKIP_FILES = {".DS_Store", "auth.json", "mcp-auth.json", "credentials.json", "push-tokens.json", "tunnel.json"}
BINARY = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".wasm", ".spl", ".sug", ".ttf", ".otf", ".woff", ".woff2"}
UI_KEYS = {"theme", "sidebar", "thinking_visibility", "timestamps", "tool_details_visibility", "assistant_metadata_visibility", "scrollbar_visible", "diff_wrap_mode", "animations_enabled", "generic_tool_output_visibility", "thinking_mode", "sdd-active-profile-name", "subagents.sidebar.expanded", "file_context_enabled", "sdd-badge-display-mode", "sdd-show-model-badge"}
OVERRIDES = ("XDG_CONFIG_HOME", "XDG_STATE_HOME", "NVIM_APPNAME", "OPENCODE_CONFIG", "OPENCODE_CONFIG_DIR", "OPENCODE_CONFIG_CONTENT", "OPENCODE_TUI_CONFIG")
SECRET_KEY = re.compile(r"^(?:.*[_-])?(?:api[_-]?key|access[_-]?token|refresh[_-]?token|token|password|passwd|secret|authorization|client[_-]?secret)$", re.I)
ASSIGNMENT = re.compile(r"(?i)(\b(?:[\w-]*(?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|passwd|client[_-]?secret)|secret|token|authorization)\s*[:=]\s*)([\"']?)([A-Za-z0-9_./+~=-]{12,})(\2)")
TOKEN = re.compile(r"\b(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9_]{16,}|github_pat_[A-Za-z0-9_]{16,}|AIza[A-Za-z0-9_-]{20,}|Bearer\s+[A-Za-z0-9_./+~=-]{16,})\b", re.I)
LIMIT = 512 * 1024 * 1024


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def excluded(path):
    return (any(p in SKIP_DIRS for p in path.parts) or path.name in SKIP_FILES
            or path.name.startswith(".env") or path.suffix in {".pem", ".key", ".db", ".sqlite", ".sqlite3", ".log", ".pyc"}
            or bool(re.search(r"(?:backup|\.bak(?:$|[.-])|\.tmp(?:$|[.-])|pre-headroom)", path.name, re.I)))


def walk(path, home, omissions, ancestors=()):
    """Follow skill symlinks, but never outside HOME or through a directory cycle."""
    if excluded(path):
        omissions.append(str(path.relative_to(home)))
        return
    real = path.resolve()
    if not real.is_relative_to(home):
        raise ValueError(f"External symlink requires manual review: {path.relative_to(home)}")
    if real in ancestors:
        raise ValueError(f"Symlink cycle: {path.relative_to(home)}")
    if path.is_dir():
        for child in sorted(path.iterdir()):
            yield from walk(child, home, omissions, (*ancestors, real))
    elif path.is_file():
        yield path
    else:
        raise ValueError(f"Broken link or special file: {path.relative_to(home)}")


class Sanitizer:
    def __init__(self):
        self.variables = {}
        self.changed = set()

    def placeholder(self, location):
        key = "REPLICA_" + hashlib.sha256(location.encode()).hexdigest()[:12].upper()
        self.variables[key] = location
        self.changed.add(location.split(" :: ")[0])
        return "{env:" + key + "}"

    def text(self, text, location):
        if re.search(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA |ENCRYPTED )?PRIVATE KEY-----", text):
            raise ValueError(f"Private key detected; refusing export: {location}")
        def assignment(match):
            # Unquoted identifiers such as RefreshToken.for_user are code, not keys.
            if not match[2] and not re.fullmatch(r"[a-fA-F0-9]{32,}", match[3]):
                return match[0]
            return match[1] + match[2] + self.placeholder(location + " :: " + match[1].strip()) + match[4]

        text = ASSIGNMENT.sub(assignment, text)
        text = TOKEN.sub(lambda m: self.placeholder(location + " :: token-" + digest(m[0].encode())[:8]), text)
        return text

    def tree(self, value, location):
        if isinstance(value, dict):
            result = {}
            for key, item in value.items():
                loc = location + " :: " + key
                if SECRET_KEY.match(key) and isinstance(item, str) and item and not re.search(r"\{(?:env|file):|\$\{|os\.getenv|process\.env", item):
                    result[key] = self.placeholder(loc)
                else:
                    result[key] = self.tree(item, loc)
            return result
        if isinstance(value, list):
            return [self.tree(item, location + f" :: {i}") for i, item in enumerate(value)]
        return self.text(value, location) if isinstance(value, str) else value

    def data(self, data, relative):
        try:
            text = data.decode("utf-8")
            if "\x00" in text:
                raise UnicodeError("binary")
        except UnicodeError:
            if Path(relative).suffix.lower() not in BINARY:
                raise ValueError(f"Unreviewed binary type: {relative}") from None
            return data
        # JSONC is scanned as text: comments are preserved, never stripped unsafely.
        if Path(relative).suffix == ".json":
            try:
                value = json.loads(text)
            except json.JSONDecodeError:
                return self.text(text, relative).encode()
            clean = self.tree(value, relative)
            return encoded(clean) if clean != value else data
        return self.text(text, relative).encode()


def versions():
    result = {}
    for command in ("nvim", "opencode", "node", "npm", "bun", "git", "engram", "codegraph", "gentle-ai", "tmux", "zellij", "ghostty", "fish"):
        if not shutil.which(command):
            result[command] = "not installed"
            continue
        try:
            run = subprocess.run([command, "--version" if command != "tmux" else "-V"], capture_output=True, text=True, timeout=8)
            result[command] = (run.stdout or run.stderr).splitlines()[0][:160]
        except (OSError, subprocess.SubprocessError, IndexError):
            result[command] = "version unavailable"
    return result


def skill_index(files):
    skills = []
    for path, data in sorted(files.items()):
        if not path.endswith("/SKILL.md"):
            continue
        text = data.decode("utf-8")
        match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", text)
        if match:
            frontmatter = text.split("---", 2)[1] if text.startswith("---") else ""
            description = re.search(r"(?m)^description:\s*(.*)(?:\n((?:[ \t]+[^\n]*\n?)*))?", frontmatter)
            trigger = " ".join((description[1].strip(" >|\"'") + " " + (description[2] or "")).split()) if description else "See SKILL.md"
            skills.append({"name": match[1].strip(), "path": path, "description": trigger})
    return skills


def export(home, output, collect_versions=True):
    if output.exists():
        raise ValueError("Bundle already exists; choose a new output name")
    if not output.parent.is_dir():
        raise ValueError("Output parent must already exist")
    if any(os.environ.get(key) for key in OVERRIDES):
        raise ValueError("Non-default config environment detected; review XDG/OpenCode overrides before export")
    if any(output.is_relative_to(home / root) for root in (*CORE, *TERMINAL)):
        raise ValueError("Place the bundle outside captured roots")
    files, modes, omissions, roots = {}, {}, [], []
    sanitizer = Sanitizer()
    for root in (*CORE, *TERMINAL):
        source = home / root
        if not source.exists() and not source.is_symlink():
            continue
        roots.append(root)
        for path in walk(source, home, omissions):
            relative = path.relative_to(home).as_posix()
            files[relative] = sanitizer.data(path.read_bytes(), relative)
            modes[relative] = 0o700 if path.stat().st_mode & 0o111 else 0o600
    if not files or not all(root in roots for root in CORE[:2]):
        raise ValueError("Both Neovim and OpenCode configuration are required")
    ui_path = home / UI
    if ui_path.is_file():
        ui = json.loads(ui_path.read_text())
        ui = {k: v for k, v in ui.items() if k in UI_KEYS}
        files[UI], modes[UI] = encoded(sanitizer.tree(ui, UI)), 0o600
        roots.append(UI)
        tui_path = ".config/opencode/tui.json"
        # Do not introduce a second TUI config alongside an existing JSONC file.
        if ui.get("theme") and ".config/opencode/tui.jsonc" not in files:
            tui = json.loads(files.get(tui_path, b"{}"))
            tui.setdefault("theme", ui["theme"])
            files[tui_path], modes[tui_path] = encoded(tui), 0o600
    skills = skill_index(files)
    registry = ["# Installed skill registry", "", "Generated from the captured files. SKILL.md remains authoritative.", "", "Sources: " + ", ".join(SKILL_ROOTS), "", "| Skill | Trigger / description | Scope | Exact path |", "|---|---|---|---|"]
    seen = set()
    for item in skills:
        name = item["name"]
        if name in seen or name.startswith("sdd-") or name in {"_shared", "shared", "skill-registry"}:
            continue
        seen.add(name)
        description = item["description"].replace("|", "\\|")
        registry.append(f"| {name} | {description} | global | ~/{item['path']} |")
    registry_path = ".config/opencode/.atl/skill-registry.md"
    files[registry_path], modes[registry_path] = ("\n".join(registry) + "\n").encode(), 0o600
    config = json.loads(files[".config/opencode/opencode.json"])
    manifest = {"format": 1, "created": datetime.now(timezone.utc).isoformat(), "source_home": str(home), "platform": sys.platform,
                "roots": roots, "versions": versions() if collect_versions else {}, "skills": skills,
                "inline_agents": sorted(config.get("agent", {})), "mcp_servers": sorted(config.get("mcp", {})),
                "required_environment": sanitizer.variables, "sanitized_files": sorted(sanitizer.changed),
                "omissions": sorted(set(omissions)), "registry_count": len(seen),
                "files": {p: {"sha256": digest(data), "mode": modes[p]} for p, data in sorted(files.items())}}
    if sum(map(len, files.values())) > LIMIT:
        raise ValueError("Snapshot exceeds 512 MiB safety limit")
    script = Path(__file__).resolve()
    # Exclusive creation prevents accidental truncation of an existing snapshot.
    with output.open("xb") as stream:
        os.chmod(output, 0o600)
        with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("manifest.json", encoded(manifest))
            archive.writestr("replica.py", script.read_bytes())
            skill = script.parent.parent
            for document in ("SKILL.md", "references/source-notes.md", "references/runtime-setup.md"):
                if (skill / document).is_file():
                    archive.writestr(document, (skill / document).read_bytes())
            for relative, data in sorted(files.items()):
                archive.writestr("payload/" + relative, data)
    return manifest


def safe_relative(value):
    path = PurePosixPath(value)
    if not value or path.is_absolute() or any(p in {"..", "."} for p in path.parts) or "\\" in value or str(path) != value:
        raise ValueError("Unsafe bundle path")
    return path


def load(bundle):
    with zipfile.ZipFile(bundle) as archive:
        infos = archive.infolist()
        if len(infos) > 30000 or sum(i.file_size for i in infos) > LIMIT or len({i.filename for i in infos}) != len(infos):
            raise ValueError("Oversized bundle or duplicate members")
        for info in infos:
            safe_relative(info.filename)
            if stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Archive symlinks are not allowed")
        manifest = json.loads(archive.read("manifest.json"))
        if manifest.get("format") != 1 or not Path(manifest["source_home"]).is_absolute():
            raise ValueError("Unsupported manifest")
        roots = manifest["roots"]
        if len(roots) != len(set(roots)) or any(root not in (*CORE, *TERMINAL, UI) for root in roots):
            raise ValueError("Unexpected managed roots")
        payload = {name[8:] for name in archive.namelist() if name.startswith("payload/")}
        if payload != set(manifest["files"]):
            raise ValueError("Manifest/payload mismatch")
        files = {}
        for name, meta in manifest["files"].items():
            path = safe_relative(name)
            if not any(path == PurePosixPath(root) or PurePosixPath(root) in path.parents for root in roots):
                raise ValueError("Payload outside managed roots")
            if meta["mode"] not in {0o600, 0o700}:
                raise ValueError("Unexpected file permissions")
            data = archive.read("payload/" + name)
            if digest(data) != meta["sha256"]:
                raise ValueError("Payload checksum mismatch: " + name)
            files[name] = data
    return manifest, files


def adapted(files, manifest, home):
    result = {}
    for name, data in files.items():
        if Path(name).suffix.lower() in BINARY:
            result[name] = data
            continue
        text = data.decode("utf-8").replace(manifest["source_home"], str(home))
        if name == ".config/opencode/opencode.json":
            value = json.loads(text)
            for server in value.get("mcp", {}).values():
                command = server.get("command", [])
                if command and command[0].startswith(("/opt/homebrew/bin/", "/usr/local/bin/")):
                    command[0] = Path(command[0]).name
            text = encoded(value).decode()
        if name == ".tmux.conf" and not Path("/opt/homebrew/bin/fish").exists():
            text = text.replace("/opt/homebrew/bin/fish", shutil.which("fish") or "/usr/bin/fish")
        result[name] = text.encode()
    return result


def selected_roots(manifest, terminal):
    return [root for root in manifest["roots"] if terminal or root not in TERMINAL]


def guard_parents(home, path):
    for parent in path.parents:
        if parent == home:
            return
        if parent.is_symlink():
            raise ValueError("Destination ancestor is a symlink: " + str(parent))
    raise ValueError("Destination escaped HOME")


def restore(bundle, home, apply=False, terminal=False):
    manifest, files = load(bundle)
    files = adapted(files, manifest, home)
    roots = selected_roots(manifest, terminal)
    for root in roots:
        guard_parents(home, home / root)
    print(json.dumps({"mode": "apply" if apply else "dry-run", "replace_roots": roots,
                      "required_environment": sorted(manifest["required_environment"])}, indent=2))
    if not apply:
        return None
    if not home.is_dir():
        raise ValueError("Destination HOME must already exist")
    state = home / ".local/state/workstation-replica"
    guard_parents(home, state / "backups")
    if state.is_symlink() or (state / "backups").is_symlink():
        raise ValueError("Backup directory must not be a symlink")
    backup = state / "backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup.mkdir(parents=True, mode=0o700)
    done = []
    try:
        for root in roots:
            target, saved = home / root, backup / root
            target.parent.mkdir(parents=True, exist_ok=True)
            existed = target.exists() or target.is_symlink()
            if existed:
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(target), str(saved))
            done.append((target, saved, existed))
            for name, data in files.items():
                if name != root and not name.startswith(root + "/"):
                    continue
                destination = home / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
                destination.chmod(manifest["files"][name]["mode"])
        print("Backup: " + str(backup))
    except BaseException:
        for target, saved, existed in reversed(done):
            if target.is_dir() and not target.is_symlink():
                shutil.rmtree(target)
            elif target.exists() or target.is_symlink():
                target.unlink()
            if existed:
                shutil.move(str(saved), str(target))
        raise
    return backup


def verify(bundle, home, terminal=False):
    manifest, original = load(bundle)
    files = adapted(original, manifest, home)
    roots = selected_roots(manifest, terminal)
    expected = {p: data for p, data in files.items() if any(p == root or p.startswith(root + "/") for root in roots)}
    failures = []
    for name, data in expected.items():
        target = home / name
        guard_parents(home, target)
        if target.is_symlink() or not target.is_file() or target.read_bytes() != data:
            failures.append("missing/changed: " + name)
    actual = set()
    for root in roots:
        path = home / root
        if path.exists():
            actual.update(p.relative_to(home).as_posix() for p in walk(path, home, []))
    failures.extend("unexpected: " + p for p in sorted(actual - set(expected)))
    print(json.dumps({"checked_files": len(expected), "failures": failures}, indent=2))
    return not failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("export", "inspect", "restore", "verify"))
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--bundle", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--terminal", action="store_true")
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    if args.action == "export":
        if not args.output:
            parser.error("export requires --output")
        manifest = export(home, args.output.expanduser().resolve())
        print(json.dumps({"bundle": str(args.output), "files": len(manifest["files"]), "skill_files": len(manifest["skills"]), "unique_skills": len({s['name'] for s in manifest['skills']}), "indexed_skills": manifest["registry_count"], "sanitized_files": manifest["sanitized_files"], "omitted_paths": len(manifest["omissions"])}, indent=2))
    else:
        if not args.bundle:
            parser.error("this action requires --bundle")
        bundle = args.bundle.expanduser().resolve()
        if args.action == "inspect":
            manifest, _ = load(bundle)
            summary = {k: v for k, v in manifest.items() if k not in {"files", "skills"}}
            summary["skills"] = {"definitions": len(manifest["skills"]), "names": sorted({s["name"] for s in manifest["skills"]})}
            summary["file_count"] = len(manifest["files"])
            print(json.dumps(summary, indent=2))
        elif args.action == "restore":
            if any(bundle.is_relative_to(home / root) for root in (*CORE, *TERMINAL)):
                raise ValueError("Move the bundle outside managed roots before restore")
            restore(bundle, home, args.apply, args.terminal)
        elif not verify(bundle, home, args.terminal):
            return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as error:
        # Do not print file contents or credential values in exceptions.
        detail = str(error) if isinstance(error, ValueError) else "inspect paths/manifest privately"
        print(f"Error: {type(error).__name__}: {detail}", file=sys.stderr)
        sys.exit(2)
