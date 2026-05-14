# Decision Ledger

## D-001 - Keep Twine Separate

Decision: Twine is its own repo, not a folder inside Ren'Py or Godot.

Reason: Twine proves a different portfolio claim: low-friction browser
interactive fiction with a single HTML artifact.

## D-002 - Use Tweego/SugarCube

Decision: Source is Twee 3 compiled by Tweego to SugarCube 2.

Reason: This keeps the demo source-controlled and deterministic while still
shipping as plain browser HTML.

## D-003 - No Runtime Agent Framework

Decision: Agentic work stays in development workflow, not the player runtime.

Reason: The demo is a deterministic playable artifact. Runtime agents would
increase complexity without improving the core proof.

## D-004 - Build Output Is Generated

Decision: `build/` is ignored and rebuilt by `tools/check_release.py`.

Reason: The source and reproducible gate are more valuable than committing a
derived HTML file at this stage.
