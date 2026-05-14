# Architecture Map

`starforge-twine-demo` is the full Act 1 single-HTML browser adaptation in the
Starforge portfolio cluster.

## Boundaries

- Public source is read from `../starforge-narrative-tools/prose/act1`.
- Generated Twine source lives in `src/passages`, with hand-owned CSS/JS in
  `src/styles` and `src/scripts`.
- `tools/generate_full_act1.py` regenerates the route from the public Act 1
  prose files.
- Tweego compiles the source to `build/index.html`.
- Python validators enforce source shape, graph integrity, and public scope.
- Playwright verifies the generated HTML through real browser clicks.
- Generated output stays out of git.

## Data Flow

1. Released Act 1 source files are parsed into main chapters and optional
   lettered scenes.
2. The generator emits `StoryData`, `StoryTitle`, `StoryInit`, route map, main
   chapter passages, optional passages, and an explicit Act 1 ending.
3. Validators inspect the generated Twine source before build.
4. Tweego emits `build/index.html`.
5. Playwright opens the built file through a local server and follows route-map,
   spine, optional-scene, and ending smoke paths.

## Related Repos

- `starforge-narrative-tools`: source/tooling proof.
- `starforge-renpy-demo`: visual-novel proof.
- `starforge-rpg-prototype`: Godot systems proof.
- `starforge-choicescript-demo`: stat-forward choice proof.
