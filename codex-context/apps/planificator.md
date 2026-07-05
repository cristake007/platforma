# App context: planificator

Generated: `2026-07-05T22:30:50`

Local instructions: `apps/planificator/AGENTS.md`. They define app contracts and the smallest workflow-specific file set.

Use this app guide to select exact file-level context. Do not load all files listed here unless the task truly affects all of them.

## Routing

- Backend behavior: start with `models.py`, `urls.py`, `views.py`, `forms.py`, `services.py`, `selectors.py`, or `validators.py` only if present and relevant.
- UI behavior: start with the exact template/static context file.
- Tests: read only tests related to the changed behavior.
- Migrations: read only for model/schema changes or migration debugging.

## Backend files

| Real file | Context file |
|---|---|
| `apps/planificator/__init__.py` | [`files/apps/planificator/__init__.py.md`](../files/apps/planificator/__init__.py.md) |
| `apps/planificator/admin.py` | [`files/apps/planificator/admin.py.md`](../files/apps/planificator/admin.py.md) |
| `apps/planificator/apps.py` | [`files/apps/planificator/apps.py.md`](../files/apps/planificator/apps.py.md) |
| `apps/planificator/constants.py` | [`files/apps/planificator/constants.py.md`](../files/apps/planificator/constants.py.md) |
| `apps/planificator/file_handlers.py` | [`files/apps/planificator/file_handlers.py.md`](../files/apps/planificator/file_handlers.py.md) |
| `apps/planificator/forms.py` | [`files/apps/planificator/forms.py.md`](../files/apps/planificator/forms.py.md) |
| `apps/planificator/management/__init__.py` | [`files/apps/planificator/management/__init__.py.md`](../files/apps/planificator/management/__init__.py.md) |
| `apps/planificator/management/commands/__init__.py` | [`files/apps/planificator/management/commands/__init__.py.md`](../files/apps/planificator/management/commands/__init__.py.md) |
| `apps/planificator/management/commands/purge_expired_schedule_generations.py` | [`files/apps/planificator/management/commands/purge_expired_schedule_generations.py.md`](../files/apps/planificator/management/commands/purge_expired_schedule_generations.py.md) |
| `apps/planificator/models.py` | [`files/apps/planificator/models.py.md`](../files/apps/planificator/models.py.md) |
| `apps/planificator/presentation.py` | [`files/apps/planificator/presentation.py.md`](../files/apps/planificator/presentation.py.md) |
| `apps/planificator/scheduler.py` | [`files/apps/planificator/scheduler.py.md`](../files/apps/planificator/scheduler.py.md) |
| `apps/planificator/selectors.py` | [`files/apps/planificator/selectors.py.md`](../files/apps/planificator/selectors.py.md) |
| `apps/planificator/services.py` | [`files/apps/planificator/services.py.md`](../files/apps/planificator/services.py.md) |
| `apps/planificator/settings_store.py` | [`files/apps/planificator/settings_store.py.md`](../files/apps/planificator/settings_store.py.md) |
| `apps/planificator/urls.py` | [`files/apps/planificator/urls.py.md`](../files/apps/planificator/urls.py.md) |
| `apps/planificator/validators.py` | [`files/apps/planificator/validators.py.md`](../files/apps/planificator/validators.py.md) |
| `apps/planificator/views.py` | [`files/apps/planificator/views.py.md`](../files/apps/planificator/views.py.md) |
| `apps/planificator/word_matching.py` | [`files/apps/planificator/word_matching.py.md`](../files/apps/planificator/word_matching.py.md) |
| `apps/planificator/wp_course_updater.py` | [`files/apps/planificator/wp_course_updater.py.md`](../files/apps/planificator/wp_course_updater.py.md) |
| `apps/planificator/xml_export.py` | [`files/apps/planificator/xml_export.py.md`](../files/apps/planificator/xml_export.py.md) |

## Template files

| Real file | Context file |
|---|---|
| `apps/planificator/templates/planificator/actualizeaza_cursuri.html` | [`files/apps/planificator/templates/planificator/actualizeaza_cursuri.html.md`](../files/apps/planificator/templates/planificator/actualizeaza_cursuri.html.md) |
| `apps/planificator/templates/planificator/generator_perioade.html` | [`files/apps/planificator/templates/planificator/generator_perioade.html.md`](../files/apps/planificator/templates/planificator/generator_perioade.html.md) |
| `apps/planificator/templates/planificator/includes/actions.html` | [`files/apps/planificator/templates/planificator/includes/actions.html.md`](../files/apps/planificator/templates/planificator/includes/actions.html.md) |
| `apps/planificator/templates/planificator/includes/messages.html` | [`files/apps/planificator/templates/planificator/includes/messages.html.md`](../files/apps/planificator/templates/planificator/includes/messages.html.md) |
| `apps/planificator/templates/planificator/includes/result_table.html` | [`files/apps/planificator/templates/planificator/includes/result_table.html.md`](../files/apps/planificator/templates/planificator/includes/result_table.html.md) |
| `apps/planificator/templates/planificator/includes/settings.html` | [`files/apps/planificator/templates/planificator/includes/settings.html.md`](../files/apps/planificator/templates/planificator/includes/settings.html.md) |
| `apps/planificator/templates/planificator/includes/upload.html` | [`files/apps/planificator/templates/planificator/includes/upload.html.md`](../files/apps/planificator/templates/planificator/includes/upload.html.md) |
| `apps/planificator/templates/planificator/istoric.html` | [`files/apps/planificator/templates/planificator/istoric.html.md`](../files/apps/planificator/templates/planificator/istoric.html.md) |
| `apps/planificator/templates/planificator/word_converter.html` | [`files/apps/planificator/templates/planificator/word_converter.html.md`](../files/apps/planificator/templates/planificator/word_converter.html.md) |
| `apps/planificator/templates/planificator/xml_formatter.html` | [`files/apps/planificator/templates/planificator/xml_formatter.html.md`](../files/apps/planificator/templates/planificator/xml_formatter.html.md) |

## Static files

| Real file | Context file |
|---|---|
| `apps/planificator/static/planificator/course_updater.js` | [`files/apps/planificator/static/planificator/course_updater.js.md`](../files/apps/planificator/static/planificator/course_updater.js.md) |
| `apps/planificator/static/planificator/generator.js` | [`files/apps/planificator/static/planificator/generator.js.md`](../files/apps/planificator/static/planificator/generator.js.md) |
| `apps/planificator/static/planificator/word_converter.js` | [`files/apps/planificator/static/planificator/word_converter.js.md`](../files/apps/planificator/static/planificator/word_converter.js.md) |
| `apps/planificator/static/planificator/xml_formatter.js` | [`files/apps/planificator/static/planificator/xml_formatter.js.md`](../files/apps/planificator/static/planificator/xml_formatter.js.md) |

## Test files

| Real file | Context file |
|---|---|
| `apps/planificator/tests.py` | [`files/apps/planificator/tests.py.md`](../files/apps/planificator/tests.py.md) |
| `apps/planificator/tests_course_updater.py` | [`files/apps/planificator/tests_course_updater.py.md`](../files/apps/planificator/tests_course_updater.py.md) |
| `apps/planificator/tests_scheduler.py` | [`files/apps/planificator/tests_scheduler.py.md`](../files/apps/planificator/tests_scheduler.py.md) |
| `apps/planificator/tests_word_converter.py` | [`files/apps/planificator/tests_word_converter.py.md`](../files/apps/planificator/tests_word_converter.py.md) |
| `apps/planificator/tests_xml_export.py` | [`files/apps/planificator/tests_xml_export.py.md`](../files/apps/planificator/tests_xml_export.py.md) |

## Migration files

| Real file | Context file |
|---|---|
| `apps/planificator/migrations/__init__.py` | [`files/apps/planificator/migrations/__init__.py.md`](../files/apps/planificator/migrations/__init__.py.md) |
| `apps/planificator/migrations/0001_initial.py` | [`files/apps/planificator/migrations/0001_initial.py.md`](../files/apps/planificator/migrations/0001_initial.py.md) |
| `apps/planificator/migrations/0002_schedulegeneration_appsetting_user_and_more.py` | [`files/apps/planificator/migrations/0002_schedulegeneration_appsetting_user_and_more.py.md`](../files/apps/planificator/migrations/0002_schedulegeneration_appsetting_user_and_more.py.md) |
| `apps/planificator/migrations/0003_schedulegeneration_source_file_data.py` | [`files/apps/planificator/migrations/0003_schedulegeneration_source_file_data.py.md`](../files/apps/planificator/migrations/0003_schedulegeneration_source_file_data.py.md) |
| `apps/planificator/migrations/0004_alter_appsetting_options.py` | [`files/apps/planificator/migrations/0004_alter_appsetting_options.py.md`](../files/apps/planificator/migrations/0004_alter_appsetting_options.py.md) |
| `apps/planificator/migrations/0005_alter_appsetting_options.py` | [`files/apps/planificator/migrations/0005_alter_appsetting_options.py.md`](../files/apps/planificator/migrations/0005_alter_appsetting_options.py.md) |

