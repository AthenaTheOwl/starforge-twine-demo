#!/usr/bin/env python3
"""Deterministic playtest audit for the Twine/SugarCube route."""

from __future__ import annotations

import re
import sys
from collections import deque
from pathlib import Path

from twee_utils import parse_passages, passage_links


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "passages"
SPECIAL = {"StoryData", "StoryTitle", "StoryInit"}
QUEUE_MARKERS = re.compile(r"\b(TODO|FIXME|DEAD[- ]?LETTER|PLAYTEST[- ]?QUEUE|BALANCE[- ]?QUEUE)\b|\bBUG:", re.IGNORECASE)


def reachable_from_start(graph: dict[str, list[str]]) -> set[str]:
    reached: set[str] = set()
    queue: deque[str] = deque(["Start"])
    while queue:
        current = queue.popleft()
        if current in reached or current not in graph:
            continue
        reached.add(current)
        queue.extend(graph[current])
    return reached


def main() -> int:
    passages = parse_passages(SOURCE)
    playable = [passage for passage in passages if passage.name not in SPECIAL]
    graph = {passage.name: passage_links(passage.body) for passage in playable}
    names = set(graph)
    errors: list[str] = []
    warnings: list[str] = []

    for source, targets in graph.items():
        for target in targets:
            if target not in names:
                errors.append(f"{source}: missing target {target}")

    reachable = reachable_from_start(graph)
    for name in sorted(names - reachable):
        errors.append(f"unreachable passage: {name}")

    route_map = next((passage for passage in playable if passage.name == "Act 1 Route Map"), None)
    route_map_links = passage_links(route_map.body) if route_map else []
    if len(route_map_links) < 60:
        errors.append(f"route map exposes only {len(route_map_links)} routes; expected at least 60 Act 1 routes")

    ending_count = sum(1 for passage in playable if "ending" in passage.name.lower() or "Act 1 complete" in passage.body)
    if ending_count == 0:
        errors.append("no ending passage detected")

    marker_hits = []
    for passage in playable:
        for line_no, line in enumerate(passage.body.splitlines(), start=1):
            if QUEUE_MARKERS.search(line):
                marker_hits.append(f"{passage.name}:{line_no}: {line.strip()}")

    if marker_hits:
        warnings.extend(marker_hits)

    print("Twine playtest audit")
    print(f"- playable passages: {len(playable)}")
    print(f"- reachable passages: {len(reachable)}")
    print(f"- route-map links: {len(route_map_links)}")
    print(f"- graph links: {sum(len(targets) for targets in graph.values())}")
    print(f"- dead-letter marker hits: {len(marker_hits)}")

    if warnings:
        print("\nDead-letter queue:")
        for warning in warnings[:40]:
            print(f"- {warning}")
        if len(warnings) > 40:
            print(f"- ... {len(warnings) - 40} more marker hit(s)")

    if errors:
        print("\nplaytest audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("playtest audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

