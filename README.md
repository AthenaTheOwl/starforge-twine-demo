# starforge-twine-demo

Act 1 opens on a chapter called "Floors Not Thrones" and closes on one called
"The Receipt." In between: a debt clock, an exit writ, a name given not owned.
The whole route — 71 passages, prologue to receipt — compiles into one 1.6 MB HTML
file you can open with a double-click. No server, no install, no save file on
anyone else's disk.

## What it does

[Starforge Canticles](https://www.royalroad.com/fiction/149065/starforge-canticles)
is a serialized speculative-fiction novel by Cessnya Lin. This repo takes the
released Act 1 prose and pours it into a Twine/SugarCube interactive-fiction page:
20 main chapters plus a spread of lettered optional scenes (medical autonomy,
crew meal dynamics, a coffee ritual, asking for what you need), all reachable from
one route map.

Twine is the fast path. It is the lightest of the four engine demos in the
cluster — a single self-contained HTML file proves the prose works as something
you click through, before anyone builds the visual novel, the Godot prototype, or
the stat-forward ChoiceScript route. The generator owns the routing; the validators
make sure every passage is reachable and nothing links into the dark.

## Try it

The release gate is the honest demo: it builds the page from source and walks a
real browser through it. One command runs the whole thing.

```powershell
python tools\check_release.py
```

```
twee validation passed: 71 passages
story graph validation passed: 68 playable passages, 68 reachable
public-scope validation passed
Twine playtest audit
- playable passages: 68
- reachable passages: 68
- route-map links: 65
- graph links: 273
- dead-letter marker hits: 0
playtest audit passed
Built build\index.html
  4 passed (4.4s)
release gate passed
```

68 reachable out of 68, zero dead-letter hits. Every door in the route opens onto
a room, and every room has a way out — which is more than the story's miners can
say. For a clean strict local proof run, use
`python tools\check_release.py --clean --fail-on-generated`.
In the local five-repo cluster, use
`python tools\check_release.py --clean --fail-on-generated --regenerate` to
regenerate from `../starforge-narrative-tools/prose/act1` before validation.

## How to play

Open the live demo (or `build/index.html` locally) in any modern browser. The
game is a single self-contained Twine/SugarCube HTML file: no server, no install.

- click **Begin Act 1** to start the route, or **Open Act 1 route map** to jump
  by chapter.
- choices are the in-passage links; click one to advance.
- the left sidebar has **SAVES** (save/load slots, browser-local) and
  **RESTART**. The back/forward arrows step through visited passages.

## Live demo

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

## Layout

What ships and what stays out:

- `src/passages/` — Twee/SugarCube source, hand-owned CSS/JS alongside
- `tools/generate_full_act1.py` — the source-to-route generator
- the Python validators (twee shape, graph integrity, public scope) and the
  playtest/path audit
- Playwright smoke tests, repo-brain and spec docs

Out of the repo: the generated `build/`, Playwright reports, Node dependencies,
unreleased later-act prose, and engine SDKs that have nothing to do with Twine.

## See also

Part of the Starforge cluster — same Act 1 prose, four different playable shapes:

- [starforge-narrative-tools](https://github.com/AthenaTheOwl/starforge-narrative-tools) — the public Act 1 corpus this demo regenerates from, plus the conversion and validation tooling
- [starforge-renpy-demo](https://github.com/AthenaTheOwl/starforge-renpy-demo) — the same Act 1 as a Ren'Py visual novel
- [starforge-rpg-prototype](https://github.com/AthenaTheOwl/starforge-rpg-prototype) — the Godot RPG-systems take on the route
- [starforge-choicescript-demo](https://github.com/AthenaTheOwl/starforge-choicescript-demo) — the full Act 1 as a stat-forward ChoiceScript route

## License

MIT. See [LICENSE](LICENSE).
</content>
</invoke>
