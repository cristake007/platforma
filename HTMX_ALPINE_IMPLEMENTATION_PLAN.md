# HTMX and Alpine.js Implementation Plan

This plan migrates the project toward HTMX and Alpine.js without turning the
application into a SPA and without replacing working custom JavaScript in one
large pass. The order matters: install the shared foundation first, convert
low-risk CRUD/list pages next, then handle custom interactive workflows after
their surrounding pages are stable.

The shared foundation and the first Flota conversion pass are complete, so they
are not repeated as active implementation phases below.

## Ground Rules

- Keep Django templates and PostgreSQL as the source of truth.
- Use HTMX for server-rendered partial updates, form submissions, table/list
  refreshes, small polling/refresh needs, and targeted swaps.
- Use Alpine.js for local-only UI state: toggles, dialogs, filters, disclosure
  panels, selected-row state, loading flags, and small reactive counters.
- Keep validation, authorization, ownership checks, and persistence server-side.
- Preserve native links/forms as fallbacks wherever practical.
- Keep state-changing requests POST-only with CSRF protection.
- Do not rewrite heavy custom JavaScript until the workflow is specifically in
  scope.
- Add focused tests for partial-response behavior when a view gains HTMX support.

## Completed Baseline

Already implemented:

1. Shared HTMX and Alpine package dependencies, script loading, CSRF request
   handling, frontend rules, and shell/dashboard script-contract tests.
2. Flota HTMX partial responses for fleet filters, pagination, vehicle
   archive/restore, and maintenance-type archive flows.
3. Flota Alpine confirmation state for archive/restore actions.
4. Flota deadline badge refresh after HTMX swaps.
5. Focused Flota tests for partial responses and preserved native behavior.

## Flota Follow-Up Improvements

Goal: improve the completed Flota pass without reworking the whole app.

Files:

1. `apps/flota/views.py`
2. `apps/flota/templates/flota/includes/fleet_panel.html`
3. `apps/flota/templates/flota/includes/vehicle_detail_panel.html`
4. `apps/flota/templates/flota/includes/maintenance_type_panel.html`
5. `apps/flota/static/flota/flota.js`
6. `apps/flota/tests.py`

Tasks:

1. Replace the subtle filter spinner with a clearly visible loading state:
   disabled controls, `aria-busy`, an obvious table-level loading row or overlay,
   and focused tests for the rendered loading hooks.
2. Use `hx-sync` on the fleet filter form so rapid typing or select changes
   replace stale requests instead of queueing outdated table refreshes.
3. Add active filter chips with one-click removal while preserving the normal
   query-string fallback.
4. Consider an Alpine disclosure for the filter panel on narrow screens if the
   filter grid takes too much vertical space.
5. Add archive/restore actions from the fleet list only if row-level partials can
   keep ownership, CSRF, confirmation, and fallback behavior straightforward.
6. Consider HTMX out-of-band message swaps if a future flow needs global message
   updates outside the swapped panel.
7. Add manual browser QA under slow network throttling for filter loading state,
   archive confirmation, refresh/back navigation, and narrow-screen layout.

Checks:

1. `.\install.ps1 test apps.flota`
2. `.\install.ps1 check`
3. Manual browser check with network throttling.
4. `git diff --check`

## Phase 3: Media Library

Goal: convert the small upload/list/delete workflow before larger consumers use
it.

Files:

1. `apps/media_library/AGENTS.md`
2. `apps/media_library/views.py`
3. `apps/media_library/urls.py`
4. `apps/media_library/forms.py`
5. `apps/media_library/templates/media_library/library.html`
6. New partial templates under `apps/media_library/templates/media_library/includes/`
   if needed.
7. `apps/media_library/tests.py`

Tasks:

1. Add HTMX upload handling that returns the refreshed upload form, messages,
   and asset grid as partial HTML.
2. Add HTMX delete handling for owned assets.
3. Use Alpine for local upload filename/preview/loading state only.
4. Keep JSON API endpoints for existing `diplome` editor integration.
5. Preserve private asset serving and ownership behavior.

Checks:

1. `.\install.ps1 test apps.media_library`
2. `.\install.ps1 check`
3. `git diff --check`

## Phase 4: Tasks Static Pages and Lists

Goal: convert non-Kanban task workflows before touching drag-and-drop behavior.

Files:

1. `apps/tasks/AGENTS.md`
2. `apps/tasks/views.py`
3. `apps/tasks/urls.py`
4. `apps/tasks/forms.py`
5. `apps/tasks/templates/tasks/includes/messages.html`
6. `apps/tasks/templates/tasks/includes/form_fields.html`
7. `apps/tasks/templates/tasks/includes/timer.html`
8. `apps/tasks/templates/tasks/hub.html`
9. `apps/tasks/templates/tasks/board_list.html`
10. `apps/tasks/templates/tasks/board_settings.html`
11. `apps/tasks/templates/tasks/board_form.html`
12. `apps/tasks/templates/tasks/task_form.html`
13. `apps/tasks/static/tasks/tasks.js`
14. `apps/tasks/tests.py`

Tasks:

1. Add HTMX filtering for board/task lists.
2. Add HTMX form handling for settings actions where the page can refresh a
   local section.
3. Use Alpine for dialogs, confirm state, local form sections, and loading flags.
4. Keep timers in existing JS unless replacing them is isolated and lower risk.
5. Preserve server-side permission behavior and native form fallbacks.

Checks:

1. `.\install.ps1 test apps.tasks`
2. `.\install.ps1 check`
3. `git diff --check`

## Phase 5: Tasks Kanban

Goal: integrate HTMX around Kanban without breaking drag-and-drop.

Files:

1. `apps/tasks/views.py`
2. `apps/tasks/templates/tasks/board_kanban.html`
3. New partial templates under `apps/tasks/templates/tasks/includes/` if needed.
4. `apps/tasks/static/tasks/tasks.js`
5. `apps/tasks/tests.py`

Tasks:

1. Keep drag-and-drop movement in custom JS initially.
2. Convert task creation and archive/restore flows to HTMX partial refreshes.
3. Evaluate whether board state polling can become `hx-trigger` polling or remain
   custom JSON polling.
4. Ensure swapped cards still have required drag/drop attributes and version
   fields.
5. Preserve native fallback forms for task movement.

Checks:

1. `.\install.ps1 test apps.tasks`
2. Manual browser check: drag/drop, create task, archive task, refresh/back.
3. `git diff --check`

## Phase 6: Diplome Lists, Generation, and Imports

Goal: convert ordinary diploma pages while leaving the editor intact.

Files:

1. `apps/diplome/AGENTS.md`
2. `apps/diplome/views.py`
3. `apps/diplome/urls.py`
4. `apps/diplome/forms.py`
5. `apps/diplome/templates/diplome/template_list.html`
6. `apps/diplome/templates/diplome/template_form.html`
7. `apps/diplome/templates/diplome/history_index.html`
8. `apps/diplome/templates/diplome/batch_detail.html`
9. `apps/diplome/templates/diplome/generation_index.html`
10. `apps/diplome/templates/diplome/generation_preview.html`
11. `apps/diplome/templates/diplome/participant_list.html`
12. `apps/diplome/templates/diplome/participant_list_detail.html`
13. `apps/diplome/templates/diplome/participant_import.html`
14. `apps/diplome/templates/diplome/participant_import_sheet.html`
15. `apps/diplome/templates/diplome/participant_import_mapping.html`
16. `apps/diplome/templates/diplome/participant_import_preview.html`
17. `apps/diplome/static/diplome/generation.js`
18. `apps/diplome/static/diplome/participant_import.js`
19. `apps/diplome/static/diplome/participant_mapping.js`
20. `apps/diplome/tests.py`
21. `apps/diplome/tests_generation.py`
22. `apps/diplome/tests_bulk_generation.py`
23. `apps/diplome/tests_participants.py`

Tasks:

1. Add HTMX partial refreshes for template list, participant list, history, and
   batch detail actions.
2. Use HTMX only where downloads and redirects are not the primary response.
3. Use Alpine for selection state, local filtering, confirm dialogs, and import
   form UI.
4. Keep generation/download validation and output server-owned.
5. Preserve owner scoping and history snapshot behavior.

Checks:

1. `.\install.ps1 test apps.diplome.tests`
2. `.\install.ps1 test apps.diplome.tests_participants`
3. `.\install.ps1 test apps.diplome.tests_generation`
4. `.\install.ps1 test apps.diplome.tests_bulk_generation`
5. Use only the focused command matching the edited workflow when possible.
6. `git diff --check`

## Phase 7: Planificator Generator and History

Goal: convert the schedule generator shell and history before the JSON-heavy
converter/updater workflows.

Files:

1. `apps/planificator/AGENTS.md`
2. `apps/planificator/views.py`
3. `apps/planificator/urls.py`
4. `apps/planificator/forms.py`
5. `apps/planificator/templates/planificator/generator_perioade.html`
6. `apps/planificator/templates/planificator/includes/upload.html`
7. `apps/planificator/templates/planificator/includes/settings.html`
8. `apps/planificator/templates/planificator/includes/result_table.html`
9. `apps/planificator/templates/planificator/includes/actions.html`
10. `apps/planificator/templates/planificator/includes/messages.html`
11. `apps/planificator/templates/planificator/istoric.html`
12. `apps/planificator/static/planificator/generator.js`
13. `apps/planificator/tests.py`
14. `apps/planificator/tests_scheduler.py`

Tasks:

1. Add HTMX support around generator form errors, messages, and result sections
   where it does not interfere with file download/export flows.
2. Use Alpine for local month selection, holiday rows, upload filename state, and
   step UI where it reduces custom JavaScript.
3. Keep result tables horizontally scrollable.
4. Preserve schedule export response behavior.

Checks:

1. `.\install.ps1 test apps.planificator.tests`
2. `.\install.ps1 test apps.planificator.tests_scheduler`
3. `.\install.ps1 check`
4. `git diff --check`

## Phase 8: Planificator XML and Word Converter Workflows

Goal: migrate JSON/download workflows only after their boundaries are mapped.

Files:

1. `apps/planificator/views.py`
2. `apps/planificator/templates/planificator/xml_formatter.html`
3. `apps/planificator/templates/planificator/word_converter.html`
4. `apps/planificator/static/planificator/xml_formatter.js`
5. `apps/planificator/static/planificator/word_converter.js`
6. `apps/planificator/tests_xml_export.py`
7. `apps/planificator/tests_word_converter.py`

Tasks:

1. Keep direct file download responses outside HTMX swaps unless using an
   intentional download pattern.
2. Convert preview/error sections to HTMX only if the endpoint can return HTML
   partials without weakening the JSON contract used by existing code.
3. Use Alpine for file labels, preview selection, and loading state.
4. Preserve untrusted file validation and neutralization behavior.

Checks:

1. `.\install.ps1 test apps.planificator.tests_xml_export`
2. `.\install.ps1 test apps.planificator.tests_word_converter`
3. `git diff --check`

## Phase 9: Planificator Course Updater

Goal: handle the highest-risk Planificator workflow after the simpler workflows.

Files:

1. `apps/planificator/views.py`
2. `apps/planificator/templates/planificator/actualizeaza_cursuri.html`
3. `apps/planificator/static/planificator/course_updater.js`
4. `apps/planificator/tests_course_updater.py`

Tasks:

1. Preserve SSRF defenses, redirect handling, and secret non-persistence.
2. Keep JSON endpoints if they remain the clearest contract for row-by-row
   updates.
3. Use HTMX for isolated row/status replacement only when the response shape is
   simpler than the current JSON flow.
4. Use Alpine for connection state, input state, progress indicators, and local
   row UI.

Checks:

1. `.\install.ps1 test apps.planificator.tests_course_updater`
2. Manual browser check: connect, fetch dates, update row, disconnect.
3. `git diff --check`

## Phase 10: Diplome Template Preview and Editor

Goal: review the editor last. This is not a first-pass HTMX conversion target.

Files:

1. `apps/diplome/templates/diplome/template_preview.html`
2. `apps/diplome/templates/diplome/template_editor.html`
3. `apps/diplome/static/diplome/template_preview.js`
4. `apps/diplome/static/diplome/template_renderer.js`
5. `apps/diplome/static/diplome/template_editor.js`
6. `apps/diplome/tests.py`

Tasks:

1. Keep `template_renderer.js` compatible with preview, editor, and PDF-related
   assumptions.
2. Do not replace canvas/layout editing state with HTMX.
3. Consider Alpine only for isolated chrome state if it does not conflict with
   editor selection, history, keyboard, pointer, media picker, or save behavior.
4. Consider HTMX only for surrounding shell actions, not the editor layout model.
5. Keep JSON layout validation canonical in server validators.

Checks:

1. `.\install.ps1 test apps.diplome.tests`
2. Manual browser check: create template, edit, media picker, save, preview,
   discard, back/refresh behavior.
3. `git diff --check`

## Phase 11: Cleanup and Context Refresh

Goal: remove dead code and update generated context after the staged migration.

Files:

1. Any app static JS file made obsolete by earlier phases.
2. Any new partial templates created during the migration.
3. `theme/static_src/src/styles.css` if new template/static paths require
   Tailwind `@source` entries.
4. `codex-context/` generated files after context regeneration.

Tasks:

1. Remove unused custom JavaScript only after the replacement behavior is tested.
2. Confirm no app-local colors or duplicate UI tokens were introduced.
3. Confirm all HTMX partials preserve authorization, CSRF, and fallback behavior.
4. Regenerate context from the repository root.

Checks:

1. `.\install.ps1 check`
2. Focused app tests for every app touched in the cleanup.
3. `.\install.ps1 npm run build`
4. `.\install.ps1 context`
5. `git diff --check`
