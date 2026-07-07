# HTMX and Alpine.js Implementation Plan

## Low-Priority Planning Artifact

- Read this file only for migration planning or historical status.
- Do not read it for ordinary bug fixes, UI polish, tests, or app-local implementation.
- For coding work, start with `AGENTS.md`, then the target app `AGENTS.md`, then exact source files.

## Status

Completed:

- Shared HTMX and Alpine baseline.
- Flota conversion baseline.
- Media Library conversion.
- Tasks static pages and lists.
- Tasks Kanban partial refresh work.
- Diplome ordinary pages, generation, and imports.
- Planificator generator and history.

Next:

- Phase 8 — Planificator XML and Word Converter Workflows.

## Phase 8 Focus

Read only:

- `apps/planificator/AGENTS.md`
- `apps/planificator/views.py`
- `apps/planificator/templates/planificator/xml_formatter.html`
- `apps/planificator/templates/planificator/word_converter.html`
- `apps/planificator/static/planificator/xml_formatter.js`
- `apps/planificator/static/planificator/word_converter.js`
- `apps/planificator/tests_xml_export.py`
- `apps/planificator/tests_word_converter.py`

Checks:

- `./install.sh test apps.planificator.tests_xml_export`
- `./install.sh test apps.planificator.tests_word_converter`
- `git diff --check`

## Later Phases

Phase 9:

- Planificator Course Updater.
- Start from `apps/planificator/AGENTS.md`.

Phase 10:

- Diplome Template Preview and Editor.
- Start from `apps/diplome/AGENTS.md`.

Phase 11:

- Cleanup and context refresh after staged migration work.
