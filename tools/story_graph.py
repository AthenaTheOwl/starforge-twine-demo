#!/usr/bin/env python3
"""Validate the Starforge Twine passage graph."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from twee_utils import parse_passages, passage_links


SPECIAL = {"StoryData", "StoryTitle", "StoryInit"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--fail-on-dead-ends", action="store_true")
    parser.add_argument("--fail-on-missing-targets", action="store_true")
    args = parser.parse_args()

    passages = parse_passages(args.source.resolve())
    graph = {passage.name: passage_links(passage.body) for passage in passages if passage.name not in SPECIAL}
    bodies = {passage.name: passage.body for passage in passages if passage.name not in SPECIAL}
    names = set(graph)
    errors: list[str] = []

    for source, targets in graph.items():
        for target in targets:
            if target not in names and args.fail_on_missing_targets:
                errors.append(f"{source}: missing target {target}")

    reachable: set[str] = set()
    queue: deque[str] = deque(["Start"])
    while queue:
        current = queue.popleft()
        if current in reachable or current not in graph:
            continue
        reachable.add(current)
        queue.extend(graph[current])

    unreachable = sorted(names - reachable)
    for name in unreachable:
        errors.append(f"unreachable passage: {name}")

    if args.fail_on_dead_ends:
        for name, targets in sorted(graph.items()):
            if not targets and not name.lower().startswith(("ending", "epilogue")) and "ending:" not in bodies[name].lower():
                errors.append(f"dead-end passage is not marked as an ending: {name}")

    if errors:
        print("story graph validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"story graph validation passed: {len(names)} playable passages, {len(reachable)} reachable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
