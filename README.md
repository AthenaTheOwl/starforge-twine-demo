# No. 17 - starforge-twine-demo

[Starforge Canticles](https://www.royalroad.com/fiction/149065/starforge-canticles)
is a serialized speculative-fiction novel by Cessnya Lin. This repo adapts the
full released Act 1 route into a Twine/SugarCube browser demo.

The repo is intentionally separate from the Ren'Py and Godot versions. Twine
proves a fast, single-HTML interactive-fiction path; it is not the visual novel,
RPG systems prototype, or stat-forward ChoiceScript build.

## How to play

Open the live demo (or `build/index.html` locally) in any modern browser. The
game is a single self-contained Twine/SugarCube HTML file: no server, no install.

- click **Begin Act 1** to start the route, or **Open Act 1 route map** to jump
  by chapter.
- choices are the in-passage links; click one to advance.
- the left sidebar has **SAVES** (save/load slots, browser-local) and
  **RESTART**. The back/forward arrows step through visited passages.

## live demo

Deployed as a Vercel static site. `vercel.json` sets the output directory to
`build`, and the compiled `build/index.html` is committed, so no build step
runs on Vercel.

Deploy steps:

1. go to https://vercel.com/new
2. import `AthenaTheOwl/starforge-twine-demo`
3. leave the framework preset as **Other** (`vercel.json` handles output dir;
   no build command needed).
4. click **Deploy**.

<!-- live-url: https://__REPLACE_WITH_VERCEL_URL__.vercel.app -->

## Run locally

```powershell
pwsh .\tools\bootstrap_tweego.ps1
npm install
npm run build
python -m http.server 8000 --directory build
```

Open `http://localhost:8000/index.html`.

## Validate

```powershell
python tools\check_release.py
```

The release gate validates the Act 1 route, audits path/dead-letter coverage,
compiles with Tweego, and runs Playwright smoke paths through the generated
HTML. For a clean strict local proof run, use
`python tools\check_release.py --clean --fail-on-generated`.
In the local five-repo cluster, use
`python tools\check_release.py --clean --fail-on-generated --regenerate` to
regenerate from `../starforge-narrative-tools/prose/act1` before validation.

## Cleanup boundary

Included:

- `src/passages/` Twee/SugarCube source
- `tools/generate_full_act1.py` source-to-route generator
- story CSS/JS
- deterministic Python validators
- deterministic playtest/path audit
- Playwright smoke tests
- repo-brain and spec docs

Excluded:

- generated `build/`
- Playwright reports
- Node dependencies
- unreleased later-act prose/spec content
- engine SDKs unrelated to Twine

## See also

Part of the Starforge cluster:

- [starforge-narrative-tools](https://github.com/AthenaTheOwl/starforge-narrative-tools) - public Act 1 corpus + conversion/validation tooling
- [starforge-renpy-demo](https://github.com/AthenaTheOwl/starforge-renpy-demo) - Act 1 Ren'Py narrative demo copy
- [starforge-rpg-prototype](https://github.com/AthenaTheOwl/starforge-rpg-prototype) - Act 1 Godot RPG prototype copy
- [starforge-choicescript-demo](https://github.com/AthenaTheOwl/starforge-choicescript-demo) - full Act 1 ChoiceScript route
