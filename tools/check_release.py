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
# outputDir in playwright.config.ts; only treated as churn when --browser-output is not used.
DEFAULT_BROWSER_OUTPUT = ROOT / ".gstack" / "playwright-results"


def run(label: str, command: list[str]) -> int:
    print(f"\n== {label} ==")
    print("+ " + " ".join(command))
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def report_dirs(browser_output: Path | None) -> list[Path]:
    # With --browser-output the default directory may hold another (possibly locked) run's
    # evidence, so leave it alone.
    return REPORT_DIRS if browser_output else REPORT_DIRS + [DEFAULT_BROWSER_OUTPUT]


def remove_dirs(paths: list[Path]) -> None:
    for path in paths:
        if path.exists():
            try:
                shutil.rmtree(path)
            except OSError as error:
                print(f"warning: could not remove {path.relative_to(ROOT).as_posix()}: {error}")


def clean_generated_artifacts(paths: list[Path]) -> None:
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

    remove_dirs(paths)


def find_report_artifacts(paths: list[Path]) -> list[Path]:
    return [path for path in paths if path.exists()]


def verify_no_report_artifacts(paths: list[Path]) -> int:
    artifacts = find_report_artifacts(paths)
    if not artifacts:
        return 0

    print("\n== Generated report artifact check ==")
    print("release gate found generated Playwright report artifacts:")
    for path in artifacts:
        print(f"- {path.relative_to(ROOT).as_posix()}")
    print("rerun with --clean to remove known Twine test-report churn")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="Remove build and Playwright reports before running.")
    parser.add_argument("--fail-on-generated", action="store_true", help="Fail if Playwright report artifacts remain after the run; build/index.html is expected output. Pair with --clean when the browser runs, because Playwright always leaves its output directory behind.")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate Twine source from the sibling public Act 1 corpus before validating.")
    parser.add_argument("--skip-browser", action="store_true", help="Skip the Playwright browser smoke. Use only for fast push/PR gates; workflow_dispatch runs the full browser gate.")
    parser.add_argument("--browser-output", type=Path, help="Write browser evidence to this directory instead of the configured default; useful when an older report directory is locked. Playwright deletes this directory before each run, so it must be outside the repo and either new, empty or a previous Playwright output directory; not valid with --skip-browser.")
    args = parser.parse_args()
    if args.skip_browser and args.browser_output:
        parser.error("--browser-output has no effect with --skip-browser")
    browser_output = args.browser_output.resolve() if args.browser_output else None
    if browser_output and (browser_output.is_relative_to(ROOT) or ROOT.is_relative_to(browser_output)):
        parser.error("--browser-output must be outside the repo; Playwright deletes that directory before each run")
    if browser_output and browser_output.exists():
        if not browser_output.is_dir():
            parser.error("--browser-output must be a directory")
        if any(browser_output.iterdir()) and not (browser_output / ".last-run.json").exists():
            parser.error(
                "--browser-output must be a new or empty directory, or one Playwright wrote before "
                "(it holds .last-run.json); Playwright deletes that directory before each run"
            )
    generated_dirs = report_dirs(browser_output)

    if args.clean:
        clean_generated_artifacts(generated_dirs)

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
        ("Playtest path/dead-letter audit", [sys.executable, "tools/playtest_audit.py"]),
        ("Tweego build", ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "tools/build_release.ps1"]),
    ]
    if not args.skip_browser:
        browser_command = ["npx.cmd", "playwright", "test"]
        if browser_output:
            browser_command.extend(["--output", str(browser_output)])
        checks.append(("Playwright smoke", browser_command))

    for label, command in checks:
        failures += 1 if run(label, command) else 0
    if args.clean:
        remove_dirs(generated_dirs)
    if args.fail_on_generated:
        failures += verify_no_report_artifacts(generated_dirs)

    if failures:
        print(f"\nrelease gate failed: {failures} check(s) failed")
        return 1

    print("\nrelease gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
