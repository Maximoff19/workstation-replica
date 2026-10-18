"""Offline tests: never read or modify the actual workstation configuration."""

from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import replica


class ReplicaTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.source = self.base / "source"
        self.target = self.base / "target"
        self.source.mkdir()
        self.target.mkdir()
        self.bundle = self.base / "snapshot.zip"
        self.environment = patch.dict(os.environ, {key: "" for key in replica.OVERRIDES})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.secret = "x" * 32
        self.put(".config/nvim/init.lua", 'vim.g.mapleader = " "\n')
        self.put(".config/nvim/lazy-lock.json", '{"example":{"commit":"123"}}')
        self.put(".config/opencode/opencode.json", json.dumps({
            "agent": {"personal": {"prompt": "Read " + str(self.source / ".agents/skills")}},
            "model": "provider/preserve-existing-model",
            "mcp": {
                "test": {"type": "local", "command": ["/opt/homebrew/bin/engram", "mcp"],
                         "environment": {"API_KEY": self.secret}},
                "argument": {"type": "local", "command": ["npx", "package", 'API_KEY="' + self.secret + '"']},
            },
        }))
        self.put(".config/opencode/tui.json", '{"plugin":["local-ui"]}')
        self.put(".config/opencode/themes/personal.json", '{"theme":{}}')
        self.put(".config/opencode/agents/personal.md", "---\nmode: all\n---\nKeep this prompt.\n")
        self.put(".config/opencode/skills/example/SKILL.md", "---\nname: example\ndescription: Fixture\n---\n# Fixture\n")
        self.put(".config/opencode/skill/legacy/SKILL.md", "---\nname: legacy\ndescription: Fixture\n---\n")
        self.put(".agents/skills/other/SKILL.md", "---\nname: other\ndescription: Fixture\n---\n")
        self.put(".claude/skills/another/SKILL.md", "---\nname: another\ndescription: Fixture\n---\n")
        self.put(replica.UI, '{"theme":"personal","session":"PRIVATE HISTORY","sidebar":"auto"}')
        self.put(".config/ghostty/config", "theme = personal\n")
        self.put(".config/opencode/push-tokens.json", '{"private":"mobile credential"}')
        self.put(".config/opencode/opencode.json.backup-20260101", self.secret)
        self.put(".config/opencode/node_modules/private/index.js", self.secret)

    def put(self, relative, text):
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def export(self):
        return replica.export(self.source, self.bundle, collect_versions=False)

    def restore(self, **kwargs):
        with redirect_stdout(io.StringIO()):
            return replica.restore(self.bundle, self.target, **kwargs)

    def verify(self, **kwargs):
        with redirect_stdout(io.StringIO()):
            return replica.verify(self.bundle, self.target, **kwargs)

    def test_redacts_secrets_excludes_history_and_keeps_themes(self):
        manifest = self.export()
        _, files = replica.load(self.bundle)
        self.assertNotIn(self.secret.encode(), b"".join(files.values()))
        self.assertNotIn(b"PRIVATE HISTORY", b"".join(files.values()))
        self.assertEqual(len(manifest["required_environment"]), 2)
        self.assertTrue(manifest["omissions"])
        self.assertEqual(json.loads(files[".config/opencode/tui.json"])["theme"], "personal")
        self.assertEqual(len(manifest["skills"]), 4)

    def test_export_never_overwrites_bundle(self):
        self.export()
        before = self.bundle.read_bytes()
        with self.assertRaises(ValueError):
            self.export()
        self.assertEqual(before, self.bundle.read_bytes())

    def test_dry_run_does_not_create_config_or_backup(self):
        self.export()
        self.restore()
        self.assertEqual(list(self.target.iterdir()), [])

    def test_restore_backs_up_replaces_and_rewrites_only_documented_paths(self):
        self.export()
        old = self.target / ".config/opencode/agents/old.md"
        old.parent.mkdir(parents=True)
        old.write_text("keep in backup")
        backup = self.restore(apply=True)
        self.assertFalse(old.exists())
        self.assertEqual((backup / ".config/opencode/agents/old.md").read_text(), "keep in backup")
        text = (self.target / ".config/opencode/opencode.json").read_text()
        config = json.loads(text)
        self.assertNotIn(str(self.source), text)
        self.assertIn(str(self.target), text)
        self.assertEqual(config["mcp"]["test"]["command"][0], "engram")
        self.assertEqual(config["model"], "provider/preserve-existing-model")
        self.assertFalse((self.target / ".config/ghostty").exists())
        self.assertTrue(self.verify())

    def test_terminal_is_explicit(self):
        self.export()
        self.restore(apply=True, terminal=True)
        self.assertTrue((self.target / ".config/ghostty/config").exists())
        self.assertTrue(self.verify(terminal=True))

    def test_verify_detects_edits_and_extra_skills(self):
        self.export()
        self.restore(apply=True)
        path = self.target / ".config/opencode/skills/unexpected/SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("unexpected")
        self.assertFalse(self.verify())
        path.unlink()
        (self.target / ".config/nvim/init.lua").write_text("changed")
        self.assertFalse(self.verify())

    def test_symlink_skills_are_materialized(self):
        original = self.source / ".agents/skills/other"
        link = self.source / ".claude/skills/linked"
        link.symlink_to(original, target_is_directory=True)
        self.export()
        self.restore(apply=True)
        destination = self.target / ".claude/skills/linked"
        self.assertFalse(destination.is_symlink())
        self.assertTrue((destination / "SKILL.md").is_file())

    def test_external_symlink_is_rejected(self):
        (self.source / ".agents/skills/external").symlink_to(self.target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "External symlink"):
            self.export()

    def test_directory_cycle_is_rejected(self):
        (self.source / ".agents/skills/cycle").symlink_to(self.source / ".agents/skills", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "cycle"):
            self.export()

    def test_destination_symlink_ancestor_is_rejected(self):
        self.export()
        (self.target / ".config").symlink_to(self.source / ".config", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.restore(apply=True)

    def test_backup_symlink_is_rejected(self):
        self.export()
        (self.target / ".local/state").mkdir(parents=True)
        (self.target / ".local/state/workstation-replica").symlink_to(self.source, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.restore(apply=True)

    def test_corrupt_payload_is_rejected_before_any_write(self):
        self.export()
        replacement = self.base / "corrupt.zip"
        with zipfile.ZipFile(self.bundle) as source, zipfile.ZipFile(replacement, "w") as target:
            for name in source.namelist():
                data = b"corrupted" if name == "payload/.config/nvim/init.lua" else source.read(name)
                target.writestr(name, data)
        self.bundle = replacement
        with self.assertRaisesRegex(ValueError, "checksum"):
            self.restore(apply=True)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_traversal_archive_is_rejected(self):
        with zipfile.ZipFile(self.bundle, "w") as archive:
            archive.writestr("../escape", "bad")
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            replica.load(self.bundle)

    def test_rollback_restores_previous_roots_after_failure(self):
        self.export()
        old = self.target / ".config/nvim/init.lua"
        old.parent.mkdir(parents=True)
        old.write_text("previous config")
        original = Path.write_bytes

        def fail_on_opencode(path, data):
            if path == self.target / ".config/opencode/opencode.json":
                raise OSError("simulated disk failure")
            return original(path, data)

        with patch.object(Path, "write_bytes", fail_on_opencode):
            with self.assertRaises(OSError):
                self.restore(apply=True)
        self.assertEqual(old.read_text(), "previous config")
        self.assertFalse((self.target / ".config/opencode").exists())

    def test_active_config_override_is_not_silently_ignored(self):
        with patch.dict(os.environ, {"XDG_CONFIG_HOME": str(self.source / "custom")}):
            with self.assertRaisesRegex(ValueError, "Non-default"):
                self.export()

    def test_existing_environment_reference_is_preserved(self):
        sanitizer = replica.Sanitizer()
        value = {"apiKey": "{env:EXISTING_KEY}"}
        self.assertEqual(sanitizer.tree(value, "fixture"), value)
        self.assertFalse(sanitizer.variables)

    def test_unquoted_code_identifiers_are_not_credentials(self):
        sanitizer = replica.Sanitizer()
        text = "refresh_token = RefreshToken.for_user(user)"
        self.assertEqual(sanitizer.text(text, "fixture.py"), text)
        self.assertFalse(sanitizer.variables)

    def test_private_key_header_is_rejected_without_echoing_key(self):
        sanitizer = replica.Sanitizer()
        text = "-----BEGIN " + "OPENSSH PRIVATE KEY-----\n" + self.secret
        with self.assertRaisesRegex(ValueError, "Private key detected") as context:
            sanitizer.text(text, "fixture")
        self.assertNotIn(self.secret, str(context.exception))

    def test_scanner_source_does_not_trigger_private_key_detection(self):
        sanitizer = replica.Sanitizer()
        text = Path(replica.__file__).read_text()
        self.assertEqual(sanitizer.text(text, "replica.py"), text)


@unittest.skipUnless(os.environ.get("REPLICA_TEST_BUNDLE"), "Set REPLICA_TEST_BUNDLE for a real snapshot round trip")
class RealSnapshotTests(unittest.TestCase):
    def test_all_managed_roots_restore_and_verify_offline(self):
        bundle = Path(os.environ["REPLICA_TEST_BUNDLE"])
        manifest, _ = replica.load(bundle)
        with tempfile.TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
            home = Path(directory).resolve()
            replica.restore(bundle, home, apply=True, terminal=True)
            self.assertTrue(replica.verify(bundle, home, terminal=True))
            for skill in manifest["skills"]:
                self.assertTrue((home / skill["path"]).is_file())


if __name__ == "__main__":
    unittest.main()
