#!/usr/bin/env python3
"""Generate a full Act 1 Twine route from the public Act 1 prose files."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
import textwrap


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "starforge-narrative-tools" / "prose" / "act1"
OUT = ROOT / "src" / "passages"


@dataclass(frozen=True)
class Scene:
    path: Path
    stem: str
    number: int
    letter: str
    title: str
    passage: str


def title_from_stem(stem: str) -> str:
    text = re.sub(r"^\d+[a-z]?_", "", stem)
    return text.replace("_", " ").title()


def scene_from_path(path: Path) -> Scene | None:
    if path.name == "act1_combined.md":
        return None
    match = re.match(r"^(\d+)([a-z]?)_", path.stem)
    if not match:
        return None
    number = int(match.group(1))
    letter = match.group(2)
    title = title_from_stem(path.stem)
    suffix = f"{number:02d}{letter}" if letter else f"{number:02d}"
    passage = f"Act1 {suffix} {title}"
    return Scene(path, path.stem, number, letter, title, passage)


def load_scenes() -> tuple[list[Scene], dict[int, list[Scene]]]:
    scenes = [scene for path in sorted(SOURCE.glob("*.md")) if (scene := scene_from_path(path))]
    main = [scene for scene in scenes if not scene.letter]
    optional: dict[int, list[Scene]] = {}
    for scene in scenes:
        if scene.letter:
            optional.setdefault(scene.number, []).append(scene)
    for values in optional.values():
        values.sort(key=lambda scene: scene.letter)
    return main, optional


def prose_html(path: Path) -> str:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    paragraphs: list[str] = []
    block: list[str] = []
    for line in lines:
        if line.strip() == "---":
            if block:
                paragraphs.append(" ".join(block))
                block = []
            paragraphs.append("<hr>")
            continue
        if not line.strip():
            if block:
                paragraphs.append(" ".join(block))
                block = []
            continue
        normalized = line.replace("\u00a0", " ").replace("\ufeff", "").strip()
        block.append(normalized)
    if block:
        paragraphs.append(" ".join(block))

    rendered: list[str] = []
    for paragraph in paragraphs:
        if paragraph == "<hr>":
            rendered.append(paragraph)
        else:
            rendered.append(f"<p>{escape(paragraph)}</p>")
    return "\n".join(rendered)


def link(label: str, target: str) -> str:
    return f"* [[{label}->{target}]]"


def write_storydata() -> None:
    (OUT / "00_storydata.twee").write_text(
        textwrap.dedent(
            """\
            :: StoryTitle
            Starforge Canticles: Act 1

            :: StoryData
            {
              "ifid": "5F9D381B-DF63-4F9A-8825-2F55004D1C8A",
              "format": "SugarCube",
              "format-version": "2.37.3",
              "start": "Start",
              "zoom": 1
            }
            """
        ),
        encoding="utf-8",
    )


def write_init(scene_count: int, optional_count: int) -> None:
    (OUT / "01_storyinit.twee").write_text(
        textwrap.dedent(
            f"""\
            :: StoryInit
            <<set $trust = 0>>
            <<set $resolve = 0>>
            <<set $lattice_attention = 0>>
            <<set $debt_pressure = 1>>
            <<set $chapter_count = {scene_count}>>
            <<set $optional_scene_count = {optional_count}>>
            """
        ),
        encoding="utf-8",
    )


def write_route(main: list[Scene], optional: dict[int, list[Scene]]) -> None:
    first = main[0].passage
    route_lines = [
        ":: Start",
        "Starforge Canticles: Act 1",
        "",
        "by Cessnya Lin",
        "",
        "Full Act 1 is routed here as a browser-playable Twine/SugarCube build.",
        "",
        "The spine follows every released Act 1 main chapter. Lettered scenes are exposed as branch choices at the relevant chapter.",
        "",
        link("Begin Act 1", first),
        link("Open Act 1 route map", "Act 1 Route Map"),
        "",
        ":: Act 1 Route Map",
        "Choose any routed Act 1 scene.",
        "",
    ]
    for scene in main:
        route_lines.append(link(f"Chapter {scene.number:02d}: {scene.title}", scene.passage))
        for extra in optional.get(scene.number, []):
            route_lines.append(link(f"Optional {scene.number:02d}{extra.letter}: {extra.title}", extra.passage))
    route_lines.append("")
    route_lines.append(":: Act 1 Ending")
    route_lines.append("Ending: Act 1 route complete.")
    (OUT / "10_act1_route.twee").write_text("\n".join(route_lines) + "\n", encoding="utf-8")


def write_scenes(main: list[Scene], optional: dict[int, list[Scene]]) -> None:
    passages: list[str] = []
    next_main = {scene.number: main[index + 1] if index + 1 < len(main) else None for index, scene in enumerate(main)}
    for scene in main:
        passages.append(f":: {scene.passage}")
        passages.append(f"<h1>Chapter {scene.number:02d}: {escape(scene.title)}</h1>")
        passages.append(f'<p class="source-note">Source: {escape(scene.path.name)}</p>')
        passages.append('<div class="scene-prose">')
        passages.append(prose_html(scene.path))
        passages.append("</div>")
        passages.append("")
        passages.append("Where does the route go next?")
        for extra in optional.get(scene.number, []):
            passages.append(link(f"Read optional scene {scene.number:02d}{extra.letter}: {extra.title}", extra.passage))
        target = next_main[scene.number].passage if next_main[scene.number] else "Act 1 Ending"
        label = f"Continue to Chapter {next_main[scene.number].number:02d}: {next_main[scene.number].title}" if next_main[scene.number] else "Finish Act 1"
        passages.append(link(label, target))
        passages.append(link("Return to route map", "Act 1 Route Map"))
        passages.append("")

        extras = optional.get(scene.number, [])
        for index, extra in enumerate(extras):
            passages.append(f":: {extra.passage}")
            passages.append(f"<h1>Optional {extra.number:02d}{extra.letter}: {escape(extra.title)}</h1>")
            passages.append(f'<p class="source-note">Source: {escape(extra.path.name)}</p>')
            passages.append('<div class="scene-prose">')
            passages.append(prose_html(extra.path))
            passages.append("</div>")
            passages.append("")
            if index + 1 < len(extras):
                next_extra = extras[index + 1]
                passages.append(link(f"Continue to optional scene {next_extra.number:02d}{next_extra.letter}: {next_extra.title}", next_extra.passage))
            target = next_main[scene.number].passage if next_main[scene.number] else "Act 1 Ending"
            label = f"Continue to Chapter {next_main[scene.number].number:02d}: {next_main[scene.number].title}" if next_main[scene.number] else "Finish Act 1"
            passages.append(link(label, target))
            passages.append(link("Return to route map", "Act 1 Route Map"))
            passages.append("")

    (OUT / "20_act1_scenes.twee").write_text("\n".join(passages), encoding="utf-8")


def main() -> int:
    main_scenes, optional = load_scenes()
    if not main_scenes:
        print(f"no Act 1 scenes found at {SOURCE}")
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    for path in OUT.glob("*.twee"):
        path.unlink()
    write_storydata()
    write_init(len(main_scenes), sum(len(values) for values in optional.values()))
    write_route(main_scenes, optional)
    write_scenes(main_scenes, optional)
    print(f"generated {len(main_scenes)} main scenes and {sum(len(values) for values in optional.values())} optional scenes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
