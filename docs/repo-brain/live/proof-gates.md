# Proof Gates

## Gate 1 - Source Boundary

- Public Act 1 source only.
- No workshop paths, later-act content, engine SDKs, or generated build output.
- Generated route covers every public Act 1 main chapter and lettered optional
  scene from `../starforge-narrative-tools/prose/act1`.

## Gate 2 - Story Shape

- Required passages exist: `StoryData`, `StoryTitle`, `StoryInit`, `Start`.
- `StoryData` is valid JSON and targets SugarCube.
- All variables used by passages are initialized in `StoryInit`.
- Route counts are regenerated from source instead of hand-maintained.

## Gate 3 - Branch Integrity

- All internal links resolve.
- No unreachable playable passages.
- Dead ends are explicit endings.
- The full route map, main spine, optional scenes, and final Act 1 ending are
  reachable.

## Gate 4 - Build

- `tools/build_release.ps1` produces `build/index.html`.
- Tweego version is pinned in `tools/vendor/tweego/VERSION.txt`.
- CI bootstraps Tweego instead of relying on a global install.

## Gate 5 - Browser Smoke

- Playwright loads the generated HTML.
- Start page renders.
- Full route map renders.
- Main spine advances from prologue into chapter 1.
- Representative optional scene opens from the route map.
- Chapter 20 can finish Act 1.
