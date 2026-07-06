# Planificator App Instructions

## Scope and workflows

This app owns schedule generation/history/export, Word matching, XML export, and WordPress course-date updates.

These are separate workflows sharing permissions, input utilities, settings, and app navigation.

## Read before editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md` for UI/template work.
- This file.
- Only the files for the selected workflow.

Use `codex-context/apps/planificator.md` only when a path is unknown.

Do not read every converter and updater file for a task confined to one workflow.

## Minimal routing

- Schedule generation/history/export: `forms.py`, `file_handlers.py`, `scheduler.py`, `services.py`, `selectors.py`, `presentation.py`, affected views/templates/static, then `tests.py` or `tests_scheduler.py`.
- Word matching/conversion: `word_matching.py`, relevant forms/views/template/JavaScript, then `tests_word_converter.py`.
- XML conversion: `xml_export.py`, relevant forms/views/template/JavaScript, then `tests_xml_export.py`.
- WordPress course updater: `wp_course_updater.py`, validators, affected views/template/JavaScript, then `tests_course_updater.py`.
- Persisted settings or generation models: `models.py`, `settings_store.py` or selectors/services, focused tests, then relevant migrations.
- Expiry cleanup: the model plus `management/commands/purge_expired_schedule_generations.py` and cleanup tests.

## Domain and security contracts

- Enforce workflow-specific permissions already represented by view mixins and model permissions.
- Persisted generations and settings are owner-scoped.
- Foreign or expired generation access must follow existing 404/error behavior.
- Uploaded CSV/XLSX/DOCX and JSON are untrusted.
- Keep size, extension, schema, date, and index validation server-side.
- Preserve schedule constraints and stable export contracts.
- Neutralize spreadsheet formulas in generated files.
- WordPress URL handling must keep the existing public HTTP(S), DNS, redirect, and bounded-network protections.
- Do not persist secrets from the updater.
- Store only non-secret settings explicitly supported by `settings_store.py`.
- Use services for generation/persistence.
- Keep JSON endpoints method-restricted, CSRF-protected, and consistent in error shape.

## Reuse and UI standards

- Reuse existing generator includes before adding markup to the main template.
- Reuse existing message, action, table, and upload patterns.
- Large result and matching tables must remain horizontally usable on narrow screens.
- Preserve sticky columns/headers and native scrolling where present.
- Use sharp bordered panels and compact settings rows.
- Avoid rounded card-heavy generator/settings layouts.
- JavaScript coordinates uploads, previews, and downloads only; server validation remains authoritative.

## Focused checks

```powershell
python manage.py test apps.planificator.tests_scheduler
python manage.py test apps.planificator.tests_word_converter
python manage.py test apps.planificator.tests_xml_export
python manage.py test apps.planificator.tests_course_updater
python manage.py test apps.planificator
```

Use the smallest matching module. Use the full app command only for cross-workflow changes.
