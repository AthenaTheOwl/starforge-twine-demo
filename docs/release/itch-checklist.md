# Itch Checklist

- Run `python tools/check_release.py --clean --regenerate` in the local cluster,
  or `python tools/check_release.py --clean` in a standalone checkout with
  generated source already committed.
- Confirm `build/index.html` exists.
- Confirm generated size is reasonable for HTML upload.
- Upload `build/` as an HTML game.
- Mark the upload playable in browser.
- Smoke test the live itch page before announcement.
