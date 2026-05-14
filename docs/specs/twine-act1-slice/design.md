# Design

## Passage Graph

```text
Start
  -> Act 1 Route Map
  -> Act1 00 Prologue
       -> optional 00a/00b/00c...
       -> Act1 01 ...
       -> ...
       -> Act1 20 ...
       -> Act 1 Ending
```

## Variables

- `$trust`, `$resolve`, `$lattice_attention`, and `$debt_pressure` remain
  initialized for later mechanics passes.
- `$chapter_count` and `$optional_scene_count` record the generated route size.

## Checks

- P0 checks are routing checks, not stat-gated mechanics.
- Each main chapter exposes its optional lettered scenes before continuing.
- Each optional scene can continue to the next optional sibling or rejoin the
  main spine.

## UI

Minimal SugarCube styling. The first release emphasizes readable long-form
prose, route-map navigation, and fast browser loading.
