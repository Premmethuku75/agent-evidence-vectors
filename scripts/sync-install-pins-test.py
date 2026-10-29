#!/usr/bin/env python3
"""Tests for scripts/sync-install-pins.py."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sync_install_pins", HERE / "sync-install-pins.py")
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

README = (
    "uv add agent-evidence-vectors==0.26.0 and pip install probityai==0.1.0\n"
    "go install x/cmd/aee-verify@v0.26.0\n"
    "[r](https://github.com/o/agent-evidence-vectors/releases/tag/v0.26.0)\n"
    "uses: probityai/agent-evidence-vectors@v0.22.0\n"
)


class SyncTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs" / "guides").mkdir(parents=True)
        (self.root / "README.md").write_text(README)
        (self.root / "DISTRIBUTION.md").write_text("git checkout v0.26.0\n")
        (self.root / "docs/guides/runner.md").write_text("uses: p/agent-evidence-vectors@v0.26.0\n")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_check_reports_stale_pages_without_writing(self) -> None:
        stale = mod.sync(self.root, "0.30.0", apply=False)
        self.assertEqual(sorted(stale), ["DISTRIBUTION.md", "README.md", "docs/guides/runner.md"])
        self.assertEqual((self.root / "README.md").read_text(), README)

    def test_apply_moves_this_projects_pins_only(self) -> None:
        mod.sync(self.root, "0.30.0", apply=True)
        text = (self.root / "README.md").read_text()
        self.assertIn("agent-evidence-vectors==0.30.0", text)
        self.assertIn("aee-verify@v0.30.0", text)
        self.assertIn("releases/tag/v0.30.0", text)
        self.assertIn("probityai==0.1.0", text)
        self.assertIn("agent-evidence-vectors@v0.22.0", text)
        self.assertEqual((self.root / "DISTRIBUTION.md").read_text(), "git checkout v0.30.0\n")

    def test_second_run_is_clean(self) -> None:
        mod.sync(self.root, "0.30.0", apply=True)
        self.assertEqual(mod.sync(self.root, "0.30.0", apply=False), [])

    def test_repo_pins_match_published_release(self) -> None:
        version = mod.published_version(mod.ROOT)
        self.assertEqual(mod.sync(mod.ROOT, version, apply=False), [])


if __name__ == "__main__":
    unittest.main()
