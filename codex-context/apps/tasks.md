# App context: tasks

Generated: `2026-07-05T22:50:42`

Local instructions: `apps/tasks/AGENTS.md`. They define app contracts and the smallest workflow-specific file set.

Use this app guide to select exact file-level context. Do not load all files listed here unless the task truly affects all of them.

## Routing

- Backend behavior: start with `models.py`, `urls.py`, `views.py`, `forms.py`, `services.py`, `selectors.py`, or `validators.py` only if present and relevant.
- UI behavior: start with the exact template/static context file.
- Tests: read only tests related to the changed behavior.
- Migrations: read only for model/schema changes or migration debugging.

## Backend files

| Real file | Context file |
|---|---|
| `apps/tasks/__init__.py` | [`files/apps/tasks/__init__.py.md`](../files/apps/tasks/__init__.py.md) |
| `apps/tasks/admin.py` | [`files/apps/tasks/admin.py.md`](../files/apps/tasks/admin.py.md) |
| `apps/tasks/apps.py` | [`files/apps/tasks/apps.py.md`](../files/apps/tasks/apps.py.md) |
| `apps/tasks/forms.py` | [`files/apps/tasks/forms.py.md`](../files/apps/tasks/forms.py.md) |
| `apps/tasks/IMPLEMENTATION_PLAN.md` | [`files/apps/tasks/IMPLEMENTATION_PLAN.md.md`](../files/apps/tasks/IMPLEMENTATION_PLAN.md.md) |
| `apps/tasks/models.py` | [`files/apps/tasks/models.py.md`](../files/apps/tasks/models.py.md) |
| `apps/tasks/selectors.py` | [`files/apps/tasks/selectors.py.md`](../files/apps/tasks/selectors.py.md) |
| `apps/tasks/services.py` | [`files/apps/tasks/services.py.md`](../files/apps/tasks/services.py.md) |
| `apps/tasks/signals.py` | [`files/apps/tasks/signals.py.md`](../files/apps/tasks/signals.py.md) |
| `apps/tasks/urls.py` | [`files/apps/tasks/urls.py.md`](../files/apps/tasks/urls.py.md) |
| `apps/tasks/validators.py` | [`files/apps/tasks/validators.py.md`](../files/apps/tasks/validators.py.md) |
| `apps/tasks/views.py` | [`files/apps/tasks/views.py.md`](../files/apps/tasks/views.py.md) |

## Template files

| Real file | Context file |
|---|---|
| `apps/tasks/templates/tasks/board_form.html` | [`files/apps/tasks/templates/tasks/board_form.html.md`](../files/apps/tasks/templates/tasks/board_form.html.md) |
| `apps/tasks/templates/tasks/board_kanban.html` | [`files/apps/tasks/templates/tasks/board_kanban.html.md`](../files/apps/tasks/templates/tasks/board_kanban.html.md) |
| `apps/tasks/templates/tasks/board_list.html` | [`files/apps/tasks/templates/tasks/board_list.html.md`](../files/apps/tasks/templates/tasks/board_list.html.md) |
| `apps/tasks/templates/tasks/board_settings.html` | [`files/apps/tasks/templates/tasks/board_settings.html.md`](../files/apps/tasks/templates/tasks/board_settings.html.md) |
| `apps/tasks/templates/tasks/hub.html` | [`files/apps/tasks/templates/tasks/hub.html.md`](../files/apps/tasks/templates/tasks/hub.html.md) |
| `apps/tasks/templates/tasks/includes/form_fields.html` | [`files/apps/tasks/templates/tasks/includes/form_fields.html.md`](../files/apps/tasks/templates/tasks/includes/form_fields.html.md) |
| `apps/tasks/templates/tasks/includes/messages.html` | [`files/apps/tasks/templates/tasks/includes/messages.html.md`](../files/apps/tasks/templates/tasks/includes/messages.html.md) |
| `apps/tasks/templates/tasks/includes/timer.html` | [`files/apps/tasks/templates/tasks/includes/timer.html.md`](../files/apps/tasks/templates/tasks/includes/timer.html.md) |
| `apps/tasks/templates/tasks/task_form.html` | [`files/apps/tasks/templates/tasks/task_form.html.md`](../files/apps/tasks/templates/tasks/task_form.html.md) |

## Static files

| Real file | Context file |
|---|---|
| `apps/tasks/static/tasks/tasks.js` | [`files/apps/tasks/static/tasks/tasks.js.md`](../files/apps/tasks/static/tasks/tasks.js.md) |

## Test files

| Real file | Context file |
|---|---|
| `apps/tasks/tests.py` | [`files/apps/tasks/tests.py.md`](../files/apps/tasks/tests.py.md) |

## Migration files

| Real file | Context file |
|---|---|
| `apps/tasks/migrations/__init__.py` | [`files/apps/tasks/migrations/__init__.py.md`](../files/apps/tasks/migrations/__init__.py.md) |
| `apps/tasks/migrations/0001_initial.py` | [`files/apps/tasks/migrations/0001_initial.py.md`](../files/apps/tasks/migrations/0001_initial.py.md) |

