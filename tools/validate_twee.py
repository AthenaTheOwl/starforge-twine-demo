#!/usr/bin/env python3
"""Validate the Starforge Twine/SugarCube source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from twee_utils import initialized_variables, parse_passages, passage_links, used_variables


REQUIRED = {"StoryData", "StoryTitle", "StoryInit", "Start"}


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    args = parser.parse_args()

    source = args.source.resolve()
    repo = Path(__file__).resolve().parents[1]
    passages = parse_passages(source)
    names: dict[str, tuple[Path, int]] = {}
    errors: list[str] = []

    for passage in passages:
        if passage.name in names:
            first_path, first_line = names[passage.name]
            errors.append(
                f"duplicate passage {passage.name!r}: {rel(first_path, repo)}:{first_line} and "
                f"{rel(passage.path, repo)}:{passage.line}"
            )
        names[passage.name] = (passage.path, passage.line)

    missing_required = sorted(REQUIRED - set(names))
    for name in missing_required:
        errors.append(f"missing required passage: {name}")

    story_data = next((passage for passage in passages if passage.name == "StoryData"), None)
    if story_data is not None:
        try:
            payload = json.loads(story_data.body)
        except json.JSONDecodeError as exc:
            errors.append(f"StoryData JSON invalid: {exc}")
        else:
            if payload.get("format") != "SugarCube":
                errors.append("StoryData format must be SugarCube")
            if payload.get("start") != "Start":
                errors.append("StoryData start must be Start")
            if not payload.get("ifid"):
                errors.append("StoryData ifid is required")

    for passage in passages:
        for target in passage_links(passage.body):
            if target not in names:
                errors.append(f"{rel(passage.path, repo)}:{passage.line}: missing link target {target!r}")

    initialized = initialized_variables(passages)
    used = used_variables(passages)
    missing_vars = sorted(used - initialized)
    for variable in missing_vars:
        errors.append(f"variable ${variable} used before StoryInit initialization")

    if errors:
        print("twee validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"twee validation passed: {len(passages)} passages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
