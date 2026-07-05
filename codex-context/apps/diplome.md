# App context: diplome

Generated: `2026-07-05T21:21:12`

Local instructions: `apps/diplome/AGENTS.md`. They define app contracts and the smallest workflow-specific file set.

Use this app guide to select exact file-level context. Do not load all files listed here unless the task truly affects all of them.

## Routing

- Backend behavior: start with `models.py`, `urls.py`, `views.py`, `forms.py`, `services.py`, `selectors.py`, or `validators.py` only if present and relevant.
- UI behavior: start with the exact template/static context file.
- Tests: read only tests related to the changed behavior.
- Migrations: read only for model/schema changes or migration debugging.

## Backend files

| Real file | Context file |
|---|---|
| `apps/diplome/__init__.py` | [`files/apps/diplome/__init__.py.md`](../files/apps/diplome/__init__.py.md) |
| `apps/diplome/admin.py` | [`files/apps/diplome/admin.py.md`](../files/apps/diplome/admin.py.md) |
| `apps/diplome/apps.py` | [`files/apps/diplome/apps.py.md`](../files/apps/diplome/apps.py.md) |
| `apps/diplome/forms.py` | [`files/apps/diplome/forms.py.md`](../files/apps/diplome/forms.py.md) |
| `apps/diplome/models.py` | [`files/apps/diplome/models.py.md`](../files/apps/diplome/models.py.md) |
| `apps/diplome/pdf_renderer.py` | [`files/apps/diplome/pdf_renderer.py.md`](../files/apps/diplome/pdf_renderer.py.md) |
| `apps/diplome/selectors.py` | [`files/apps/diplome/selectors.py.md`](../files/apps/diplome/selectors.py.md) |
| `apps/diplome/services.py` | [`files/apps/diplome/services.py.md`](../files/apps/diplome/services.py.md) |
| `apps/diplome/urls.py` | [`files/apps/diplome/urls.py.md`](../files/apps/diplome/urls.py.md) |
| `apps/diplome/validators.py` | [`files/apps/diplome/validators.py.md`](../files/apps/diplome/validators.py.md) |
| `apps/diplome/views.py` | [`files/apps/diplome/views.py.md`](../files/apps/diplome/views.py.md) |

## Template files

| Real file | Context file |
|---|---|
| `apps/diplome/templates/diplome/batch_detail.html` | [`files/apps/diplome/templates/diplome/batch_detail.html.md`](../files/apps/diplome/templates/diplome/batch_detail.html.md) |
| `apps/diplome/templates/diplome/generation_index.html` | [`files/apps/diplome/templates/diplome/generation_index.html.md`](../files/apps/diplome/templates/diplome/generation_index.html.md) |
| `apps/diplome/templates/diplome/generation_preview.html` | [`files/apps/diplome/templates/diplome/generation_preview.html.md`](../files/apps/diplome/templates/diplome/generation_preview.html.md) |
| `apps/diplome/templates/diplome/history_index.html` | [`files/apps/diplome/templates/diplome/history_index.html.md`](../files/apps/diplome/templates/diplome/history_index.html.md) |
| `apps/diplome/templates/diplome/participant_import.html` | [`files/apps/diplome/templates/diplome/participant_import.html.md`](../files/apps/diplome/templates/diplome/participant_import.html.md) |
| `apps/diplome/templates/diplome/participant_import_mapping.html` | [`files/apps/diplome/templates/diplome/participant_import_mapping.html.md`](../files/apps/diplome/templates/diplome/participant_import_mapping.html.md) |
| `apps/diplome/templates/diplome/participant_import_preview.html` | [`files/apps/diplome/templates/diplome/participant_import_preview.html.md`](../files/apps/diplome/templates/diplome/participant_import_preview.html.md) |
| `apps/diplome/templates/diplome/participant_import_sheet.html` | [`files/apps/diplome/templates/diplome/participant_import_sheet.html.md`](../files/apps/diplome/templates/diplome/participant_import_sheet.html.md) |
| `apps/diplome/templates/diplome/participant_list.html` | [`files/apps/diplome/templates/diplome/participant_list.html.md`](../files/apps/diplome/templates/diplome/participant_list.html.md) |
| `apps/diplome/templates/diplome/participant_list_detail.html` | [`files/apps/diplome/templates/diplome/participant_list_detail.html.md`](../files/apps/diplome/templates/diplome/participant_list_detail.html.md) |
| `apps/diplome/templates/diplome/placeholder.html` | [`files/apps/diplome/templates/diplome/placeholder.html.md`](../files/apps/diplome/templates/diplome/placeholder.html.md) |
| `apps/diplome/templates/diplome/template_editor.html` | [`files/apps/diplome/templates/diplome/template_editor.html.md`](../files/apps/diplome/templates/diplome/template_editor.html.md) |
| `apps/diplome/templates/diplome/template_form.html` | [`files/apps/diplome/templates/diplome/template_form.html.md`](../files/apps/diplome/templates/diplome/template_form.html.md) |
| `apps/diplome/templates/diplome/template_list.html` | [`files/apps/diplome/templates/diplome/template_list.html.md`](../files/apps/diplome/templates/diplome/template_list.html.md) |
| `apps/diplome/templates/diplome/template_preview.html` | [`files/apps/diplome/templates/diplome/template_preview.html.md`](../files/apps/diplome/templates/diplome/template_preview.html.md) |

## Static files

| Real file | Context file |
|---|---|
| `apps/diplome/static/diplome/generation.js` | [`files/apps/diplome/static/diplome/generation.js.md`](../files/apps/diplome/static/diplome/generation.js.md) |
| `apps/diplome/static/diplome/participant_import.js` | [`files/apps/diplome/static/diplome/participant_import.js.md`](../files/apps/diplome/static/diplome/participant_import.js.md) |
| `apps/diplome/static/diplome/participant_mapping.js` | [`files/apps/diplome/static/diplome/participant_mapping.js.md`](../files/apps/diplome/static/diplome/participant_mapping.js.md) |
| `apps/diplome/static/diplome/template_editor.css` | [`files/apps/diplome/static/diplome/template_editor.css.md`](../files/apps/diplome/static/diplome/template_editor.css.md) |
| `apps/diplome/static/diplome/template_editor.js` | [`files/apps/diplome/static/diplome/template_editor.js.md`](../files/apps/diplome/static/diplome/template_editor.js.md) |
| `apps/diplome/static/diplome/template_preview.js` | [`files/apps/diplome/static/diplome/template_preview.js.md`](../files/apps/diplome/static/diplome/template_preview.js.md) |
| `apps/diplome/static/diplome/template_renderer.js` | [`files/apps/diplome/static/diplome/template_renderer.js.md`](../files/apps/diplome/static/diplome/template_renderer.js.md) |

## Test files

| Real file | Context file |
|---|---|
| `apps/diplome/tests.py` | [`files/apps/diplome/tests.py.md`](../files/apps/diplome/tests.py.md) |
| `apps/diplome/tests_bulk_generation.py` | [`files/apps/diplome/tests_bulk_generation.py.md`](../files/apps/diplome/tests_bulk_generation.py.md) |
| `apps/diplome/tests_generation.py` | [`files/apps/diplome/tests_generation.py.md`](../files/apps/diplome/tests_generation.py.md) |
| `apps/diplome/tests_participants.py` | [`files/apps/diplome/tests_participants.py.md`](../files/apps/diplome/tests_participants.py.md) |

## Migration files

| Real file | Context file |
|---|---|
| `apps/diplome/migrations/__init__.py` | [`files/apps/diplome/migrations/__init__.py.md`](../files/apps/diplome/migrations/__init__.py.md) |
| `apps/diplome/migrations/0001_initial.py` | [`files/apps/diplome/migrations/0001_initial.py.md`](../files/apps/diplome/migrations/0001_initial.py.md) |
| `apps/diplome/migrations/0002_millimeter_coordinate_system.py` | [`files/apps/diplome/migrations/0002_millimeter_coordinate_system.py.md`](../files/apps/diplome/migrations/0002_millimeter_coordinate_system.py.md) |
| `apps/diplome/migrations/0003_diplomatemplate_category_and_more.py` | [`files/apps/diplome/migrations/0003_diplomatemplate_category_and_more.py.md`](../files/apps/diplome/migrations/0003_diplomatemplate_category_and_more.py.md) |
| `apps/diplome/migrations/0004_participant_list_import.py` | [`files/apps/diplome/migrations/0004_participant_list_import.py.md`](../files/apps/diplome/migrations/0004_participant_list_import.py.md) |
| `apps/diplome/migrations/0005_participant_import_mapping.py` | [`files/apps/diplome/migrations/0005_participant_import_mapping.py.md`](../files/apps/diplome/migrations/0005_participant_import_mapping.py.md) |
| `apps/diplome/migrations/0006_generated_diploma.py` | [`files/apps/diplome/migrations/0006_generated_diploma.py.md`](../files/apps/diplome/migrations/0006_generated_diploma.py.md) |
| `apps/diplome/migrations/0007_diploma_generation_batch.py` | [`files/apps/diplome/migrations/0007_diploma_generation_batch.py.md`](../files/apps/diplome/migrations/0007_diploma_generation_batch.py.md) |
| `apps/diplome/migrations/0008_history_snapshots_allow_source_deletion.py` | [`files/apps/diplome/migrations/0008_history_snapshots_allow_source_deletion.py.md`](../files/apps/diplome/migrations/0008_history_snapshots_allow_source_deletion.py.md) |
| `apps/diplome/migrations/0009_participantimportdraft_source_sheets_json.py` | [`files/apps/diplome/migrations/0009_participantimportdraft_source_sheets_json.py.md`](../files/apps/diplome/migrations/0009_participantimportdraft_source_sheets_json.py.md) |

