# Source snapshot

## `apps/media_library/AGENTS.md`

Size: 2.0 KB

````markdown
# Media Library App Instructions

## Scope and Integration

This app owns private reusable raster/SVG assets, upload validation and sanitization, owner-scoped delivery, and safe deletion. `diplome` consumes these assets in layouts and generated PDFs.

## Minimal Routing

- Upload/input rules: `forms.py`, `validators.py`, `services.py`, then the matching tests in `tests.py`.
- Listing/content/delete endpoints: `urls.py`, `views.py`, `selectors.py`, `services.py`, then endpoint tests.
- Storage/file lifecycle: `models.py`, `storage.py`, `signals.py`, `services.py`, then storage/deletion tests.
- Library UI: `templates/media_library/library.html`, `static/media_library/library.css`, and view/form context only if needed.
- Diploma integration: inspect only the importing `diplome` service/renderer and its relevant tests.
- Unknown path only: `codex-context/apps/media_library.md`.

## Domain and Security Contracts

- Assets are private and owner-scoped. Never expose storage paths or serve a foreign asset.
- Treat filenames, MIME types, dimensions, and client metadata as untrusted. Canonicalized validator output is the data persisted by the service.
- Preserve raster re-encoding and restrictive SVG sanitization/response headers. Do not weaken URL, script, style, entity, or active-content rejection.
- File/database writes and cleanup must remain consistent on failure.
- An asset referenced by an owned diploma layout cannot be deleted. Keep the narrow `diplome` dependency in the deletion service; do not duplicate layout parsing.
- State changes are POST-only and CSRF-protected; cross-owner object routes return 404.

## Frontend Contract

- The library page extends `layouts/base.html` and uses shared semantic tokens.
- App CSS is for preview geometry only; colors and controls come from the global daisyUI theme.
- Keep `apps/media_library/**/*.{html,py,js}` registered as a Tailwind source in `theme/static_src/src/styles.css`.

## Focused Check

```powershell
python manage.py test apps.media_library
```
````
