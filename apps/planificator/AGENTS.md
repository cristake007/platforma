# Planificator App Instructions

## Scope and Workflows

This app owns schedule generation/history/export, Word matching, XML export, and WordPress course-date updates. These are separate workflows sharing permissions, input utilities, settings, and app navigation.

## Minimal Routing

- Schedule generation/history/export: `forms.py`, `file_handlers.py`, `scheduler.py`, `services.py`, `selectors.py`, `presentation.py`, affected views/templates/static, then `tests.py` or `tests_scheduler.py`.
- Word matching/conversion: `word_matching.py`, relevant forms/views/template/JavaScript, then `tests_word_converter.py`.
- XML conversion: `xml_export.py`, relevant forms/views/template/JavaScript, then `tests_xml_export.py`.
- WordPress course updater: `wp_course_updater.py`, validators, affected views/template/JavaScript, then `tests_course_updater.py`.
- Persisted settings or generation models: `models.py`, `settings_store.py` or selectors/services, focused tests, then relevant migrations.
- Expiry cleanup: the model plus `management/commands/purge_expired_schedule_generations.py` and cleanup tests.
- Unknown path only: `codex-context/apps/planificator.md`.

Do not read every converter and updater file for a task confined to one workflow.

## Domain and Security Contracts

- Enforce the workflow-specific permissions already represented by the view mixins and model permissions.
- Persisted generations and settings are owner-scoped. Foreign or expired generation access must follow existing 404/error behavior.
- Uploaded CSV/XLSX/DOCX and JSON are untrusted. Keep size, extension, schema, date, and index validation server-side.
- Preserve schedule constraints and stable export contracts. Neutralize spreadsheet formulas in generated files.
- WordPress URLs must remain public HTTP(S) destinations after DNS resolution and redirects; preserve SSRF defenses and bounded network behavior.
- Do not persist secrets from the updater. Store only the non-secret settings explicitly supported by `settings_store.py`.
- Use services for generation/persistence and keep JSON endpoints method-restricted, CSRF-protected, and consistent in error shape.

## Frontend Contract

- Pages extend `layouts/base.html` and use the shared semantic theme tokens.
- Keep large result and matching tables horizontally usable on narrow screens; preserve sticky columns/headers and native scrolling where present.
- JavaScript coordinates uploads, previews, and downloads but does not replace server validation.
- Reuse the existing generator includes before adding markup to the main template.

## Focused Checks

```powershell
python manage.py test apps.planificator.tests_scheduler
python manage.py test apps.planificator.tests_word_converter
python manage.py test apps.planificator.tests_xml_export
python manage.py test apps.planificator.tests_course_updater
python manage.py test apps.planificator
```

Use the smallest matching module; use the full app command only for cross-workflow changes.
