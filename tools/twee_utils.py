#!/usr/bin/env python3
"""Small Twee parser used by Starforge Twine validation tools."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


HEADER_RE = re.compile(r"^::\s+(.+?)\s*$")
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
SET_RE = re.compile(r"<<set\s+\$(\w+)\s*=")
VAR_RE = re.compile(r"\$(\w+)")


@dataclass(frozen=True)
class Passage:
    name: str
    body: str
    path: Path
    line: int


def parse_passages(root: Path) -> list[Passage]:
    passages: list[Passage] = []
    for path in sorted(root.rglob("*.twee")):
        current_name: str | None = None
        current_line = 0
        current_body: list[str] = []
        for line_num, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = HEADER_RE.match(line)
            if match:
                if current_name is not None:
                    passages.append(Passage(current_name, "\n".join(current_body).strip(), path, current_line))
                current_name = match.group(1).split("[", 1)[0].strip()
                current_line = line_num
                current_body = []
            elif current_name is not None:
                current_body.append(line)
        if current_name is not None:
            passages.append(Passage(current_name, "\n".join(current_body).strip(), path, current_line))
    return passages


def link_target(markup: str) -> str:
    if "->" in markup:
        return markup.rsplit("->", 1)[1].strip()
    if "<-" in markup:
        return markup.split("<-", 1)[0].strip()
    return markup.strip()


def passage_links(body: str) -> list[str]:
    return [link_target(match.group(1)) for match in LINK_RE.finditer(body)]


def initialized_variables(passages: list[Passage]) -> set[str]:
    values: set[str] = set()
    for passage in passages:
        if passage.name == "StoryInit":
            values.update(SET_RE.findall(passage.body))
    return values


def used_variables(passages: list[Passage]) -> set[str]:
    values: set[str] = set()
    for passage in passages:
        if passage.name != "StoryData":
            values.update(VAR_RE.findall(passage.body))
    return values
