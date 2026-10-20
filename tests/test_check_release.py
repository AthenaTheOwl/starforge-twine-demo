"""Unit tests for tools/check_release.py argument guards and cleanup.

Run with: python -m unittest discover -s tests
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import shutil
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "check_release.py"


def load_module():
    spec = importlib.util.spec_from_file_location("check_release_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CheckReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.repo = self.tmp / "repo"
        (self.repo / "build").mkdir(parents=True)
        self.outside = self.tmp / "outside"
        self.cr = load_module()
        real_root = self.cr.ROOT
        self.cr.ROOT = self.repo
        self.cr.BUILD_DIR = self.repo / "build"
        self.cr.REPORT_DIRS = [self.repo / path.relative_to(real_root) for path in self.cr.REPORT_DIRS]
        self.default_rel = self.cr.DEFAULT_BROWSER_OUTPUT.relative_to(real_root).as_posix()
        self.cr.DEFAULT_BROWSER_OUTPUT = self.repo / self.default_rel
        self.commands = []

        def fake_run(command, **kwargs):
            self.commands.append(command)
            return types.SimpleNamespace(returncode=0)

        patcher = mock.patch.object(self.cr.subprocess, "run", side_effect=fake_run)
        patcher.start()
        self.addCleanup(patcher.stop)

    def main(self, *args):
        out = io.StringIO()
        with mock.patch.object(self.cr.sys, "argv", ["check_release.py", *map(str, args)]):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                try:
                    return self.cr.main(), out.getvalue()
                except SystemExit as exit_:
                    return exit_.code, out.getvalue()

    def playwright_commands(self):
        return [c for c in self.commands if "playwright" in c]

    def test_browser_output_rejected_with_skip_browser(self):
        code, _ = self.main("--skip-browser", "--browser-output", self.outside)
        self.assertEqual(code, 2)
        self.assertEqual(self.commands, [])

    def test_browser_output_inside_repo_rejected(self):
        code, _ = self.main("--browser-output", self.repo / "docs")
        self.assertEqual(code, 2)
        self.assertEqual(self.commands, [])

    def test_browser_output_repo_ancestor_rejected(self):
        code, _ = self.main("--browser-output", self.tmp)
        self.assertEqual(code, 2)
        self.assertEqual(self.commands, [])

    def test_browser_output_non_empty_foreign_directory_rejected(self):
        self.outside.mkdir()
        (self.outside / "notes.txt").write_text("keep me")
        code, _ = self.main("--browser-output", self.outside)
        self.assertEqual(code, 2)
        self.assertEqual(self.commands, [])
        self.assertTrue((self.outside / "notes.txt").exists())

    def test_browser_output_outside_repo_forwarded(self):
        code, _ = self.main("--browser-output", self.outside)
        self.assertEqual(code, 0)
        self.assertEqual(self.playwright_commands(), [["npx.cmd", "playwright", "test", "--output", str(self.outside)]])

    def test_browser_output_previous_playwright_directory_accepted(self):
        self.outside.mkdir()
        (self.outside / ".last-run.json").write_text("{}")
        code, _ = self.main("--browser-output", self.outside)
        self.assertEqual(code, 0)
        self.assertEqual(len(self.playwright_commands()), 1)

    def test_clean_with_browser_output_leaves_default_output_alone(self):
        default = self.cr.DEFAULT_BROWSER_OUTPUT
        default.mkdir(parents=True)
        (default / ".last-run.json").write_text("{}")
        real_rmtree = shutil.rmtree

        def locked_rmtree(path, *args, **kwargs):
            if Path(path) == default:
                raise PermissionError(13, "locked", str(path))
            return real_rmtree(path, *args, **kwargs)

        with mock.patch.object(self.cr.shutil, "rmtree", side_effect=locked_rmtree):
            code, output = self.main("--clean", "--fail-on-generated", "--browser-output", self.outside)
        self.assertEqual(code, 0, output)
        self.assertTrue(default.exists())

    def test_clean_reports_locked_directory_instead_of_crashing(self):
        default = self.cr.DEFAULT_BROWSER_OUTPUT
        default.mkdir(parents=True)

        def locked_rmtree(path, *args, **kwargs):
            raise PermissionError(13, "locked", str(path))

        with mock.patch.object(self.cr.shutil, "rmtree", side_effect=locked_rmtree):
            code, output = self.main("--clean", "--fail-on-generated", "--skip-browser")
        self.assertEqual(code, 1)
        self.assertIn(f"warning: could not remove {self.default_rel}", output)
        self.assertIn(f"- {self.default_rel}", output)

    def test_clean_removes_default_output_without_browser_output(self):
        default = self.cr.DEFAULT_BROWSER_OUTPUT
        default.mkdir(parents=True)
        (default / ".last-run.json").write_text("{}")
        code, output = self.main("--clean", "--fail-on-generated")
        self.assertEqual(code, 0, output)
        self.assertFalse(default.exists())


if __name__ == "__main__":
    unittest.main()
