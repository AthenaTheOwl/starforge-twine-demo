# Acceptance

The Twine demo reaches P0/P1 when:

- `python tools/check_release.py` passes.
- `build/index.html` is produced by Tweego.
- Playwright reaches the Act 1 route map, main spine, a representative optional
  scene, and the Act 1 ending.
- Public-scope validation passes.
- README explains how to build and run locally.

The release claim is:

> Browser-playable full Act 1 Twine/SugarCube route with deterministic
> validation, reproducible source generation, a Tweego single-HTML build, and
> browser smoke coverage.
