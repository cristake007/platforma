# Media Library App Instructions

## Scope and integration

This app owns private reusable raster/SVG assets, upload validation and sanitization, owner-scoped delivery, and safe deletion.

`diplome` consumes these assets in layouts and generated PDFs.

## Read before editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md` for UI/template work.
- This file.
- Only the files for the selected workflow.

Use `codex-context/apps/media_library.md` only when a path is unknown.

## Minimal routing

- Upload/input rules: `forms.py`, `validators.py`, `services.py`, then matching tests in `tests.py`.
- Listing/content/delete endpoints: `urls.py`, `views.py`, `selectors.py`, `services.py`, then endpoint tests.
- Storage/file lifecycle: `models.py`, `storage.py`, `signals.py`, `services.py`, then storage/deletion tests.
- Library UI: `templates/media_library/library.html`, `static/media_library/library.css`, and view/form context only if needed.
- Diploma integration: inspect only the importing `diplome` service/renderer and relevant tests.

## Domain and security contracts

- Assets are private and owner-scoped.
- Never expose storage paths or serve a foreign asset.
- Treat filenames, MIME types, dimensions, and client metadata as untrusted.
- Canonicalized validator output is the data persisted by the service.
- Preserve raster re-encoding and restrictive SVG sanitization/response headers.
- File/database writes and cleanup must remain consistent on failure.
- An asset referenced by an owned diploma layout cannot be deleted.
- Keep the narrow `diplome` dependency in the deletion service.
- Do not duplicate layout parsing.
- State changes are POST-only and CSRF-protected.
- Cross-owner object routes return 404.

## Reuse and UI standards

- Reuse the existing upload, asset-grid, delete, empty-state, and message patterns.
- The library page extends `layouts/base.html` and uses shared semantic tokens.
- App CSS is for preview geometry only.
- Colors and controls come from the global daisyUI theme.
- Keep sharp bordered upload/list areas instead of decorative rounded cards.
- Disable upload actions until required client-side prerequisites exist, while keeping server validation authoritative.
- Keep `apps/media_library/**/*.{html,py,js}` registered as a Tailwind source in `theme/static_src/src/styles.css`.

## Focused check

```powershell
python manage.py test apps.media_library
```
