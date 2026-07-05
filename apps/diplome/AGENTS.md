# Diplome App Instructions

## Scope and Workflows

This app owns diploma templates and layout JSON, participant-list import, single/bulk PDF generation, downloads, and generation history. It integrates with `media_library` for owned layout assets.

## Minimal Routing

- Template list/create/editor/preview: `urls.py`, `views.py`, `forms.py`, `services.py`, `validators.py`, the exact template/static file, then `tests.py`.
- Participant CSV/XLSX import and mapping: `forms.py`, `services.py`, `views.py`, the exact participant template/JavaScript, then `tests_participants.py`.
- Single generation/download: `forms.py`, `selectors.py`, `services.py`, `pdf_renderer.py`, relevant generation templates, then `tests_generation.py`.
- Bulk generation/history/ZIP: `models.py`, `selectors.py`, `services.py`, relevant batch/history templates, then `tests_bulk_generation.py`.
- Model changes: `models.py`, affected service/selector/tests, then only the relevant migration history.
- Unknown path only: `codex-context/apps/diplome.md`.

Do not open all editor, participant, generation, and history files for a change confined to one workflow.

## Domain Contracts

- All templates, participant records, drafts, generated diplomas, and batches are owner-scoped. Cross-owner access returns 404 or a validation error appropriate to the existing endpoint.
- `validators.py` is the canonical layout JSON contract. Keep browser rendering, PDF rendering, form validation, and stored layout versions compatible.
- Use `services.py` for transactional imports, template mutation, generation, ZIP creation, and history snapshots. Views orchestrate HTTP only.
- Preserve history snapshots when source participants, lists, or templates are deleted.
- Validate participant membership against the selected owned list and validate every media asset through `media_library` ownership services.
- Keep state-changing endpoints POST-only with CSRF protection. Downloads must use owned selectors and safe filenames.

## Frontend Contract

- Standard pages extend `layouts/base.html` and use shared semantic tokens.
- `template_editor.css` may implement editor geometry. Editor chrome must consume global semantic variables.
- Diploma canvas element colors are user-authored document data and may remain literal/stored values; do not confuse them with application theme colors.
- Keep `template_renderer.js` behavior compatible with preview and editor consumers. Server validation remains authoritative.

## Focused Checks

```powershell
python manage.py test apps.diplome.tests
python manage.py test apps.diplome.tests_participants
python manage.py test apps.diplome.tests_generation
python manage.py test apps.diplome.tests_bulk_generation
```

Run only the command matching the changed workflow unless the contract crosses them.
