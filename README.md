# No. 17 - starforge-twine-demo

[Starforge Canticles](https://www.royalroad.com/fiction/149065/starforge-canticles)
is a serialized speculative-fiction novel by Cessnya Lin. This repo adapts the
full released Act 1 route into a Twine/SugarCube browser demo.

The repo is intentionally separate from the Ren'Py and Godot versions. Twine
proves a fast, single-HTML interactive-fiction path; it is not the visual novel,
RPG systems prototype, or stat-forward ChoiceScript build.

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

The release gate validates the Act 1 route, compiles with Tweego, and runs
Playwright smoke paths through the generated HTML. In the local five-repo
cluster, use `python tools\check_release.py --clean --regenerate` to regenerate
from `../starforge-narrative-tools/prose/act1` before validation.

## Cleanup boundary

Included:

- `src/passages/` Twee/SugarCube source
- `tools/generate_full_act1.py` source-to-route generator
- story CSS/JS
- deterministic Python validators
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
