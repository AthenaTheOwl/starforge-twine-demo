# Verification scope — October 18, 2026

The source validators and Tweego build passed: 71 passages, 68 playable and
reachable passages, no missing targets and no explicit dead-letter markers.
Four Chromium smoke paths passed: route map, prologue-to-first-chapter,
optional scene and final main chapter. The public story source was unchanged.

The existing browser report directory was locked on this Windows checkout.
The release gate now accepts `--browser-output` so a fresh evidence directory
can be used without deleting another run's reports:

```powershell
python tools/check_release.py --browser-output C:\path\to\fresh-proof-directory
```

The flag changes evidence storage only. It does not skip the browser or
alter the story. The default release command remains available.

Reachability and four smoke paths do not prove every passage, save/load case
or browser layout. For an AI Product Team experiment, propose one additional
behavioral smoke with an observable expected state, then compare its failure
signal with the existing suite. Keep the task bounded and preserve the
published prose. A review report cannot replace an executed browser check.
