#!/usr/bin/env python3
"""Run deterministic release gates for the Twine demo repo."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build"
REPORT_DIRS = [ROOT / "test-results", ROOT / "playwright-report"]


def run(label: str, command: list[str]) -> int:
    print(f"\n== {label} ==")
    print("+ " + " ".join(command))
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def clean_generated_artifacts() -> None:
    if BUILD_DIR.exists():
        for path in BUILD_DIR.iterdir():
            if path.name != ".gitkeep":
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
    else:
        BUILD_DIR.mkdir()
    (BUILD_DIR / ".gitkeep").touch()

    for path in REPORT_DIRS:
        if path.exists():
            shutil.rmtree(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="Remove build and Playwright reports before running.")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate Twine source from the sibling public Act 1 corpus before validating.")
    args = parser.parse_args()

    if args.clean:
        clean_generated_artifacts()

    failures = 0
    if args.regenerate:
        failures += 1 if run("Full Act 1 route generation", [sys.executable, "tools/generate_full_act1.py"]) else 0

    checks = [
        ("Twee validation", [sys.executable, "tools/validate_twee.py", "src/passages"]),
        (
            "Story graph validation",
            [
                sys.executable,
                "tools/story_graph.py",
                "--fail-on-dead-ends",
                "--fail-on-missing-targets",
                "src/passages",
            ],
        ),
        ("Public-scope validation", [sys.executable, "tools/validate_public_scope.py"]),
        ("Tweego build", ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "tools/build_release.ps1"]),
        ("Playwright smoke", ["npx.cmd", "playwright", "test"]),
    ]

    for label, command in checks:
        failures += 1 if run(label, command) else 0

    if failures:
        print(f"\nrelease gate failed: {failures} check(s) failed")
        return 1

    print("\nrelease gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
