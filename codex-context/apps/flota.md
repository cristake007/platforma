# App context: flota

Generated: `2026-07-05T22:50:42`

Local instructions: `apps/flota/AGENTS.md`. They define app contracts and the smallest workflow-specific file set.

Use this app guide to select exact file-level context. Do not load all files listed here unless the task truly affects all of them.

## Routing

- Backend behavior: start with `models.py`, `urls.py`, `views.py`, `forms.py`, `services.py`, `selectors.py`, or `validators.py` only if present and relevant.
- UI behavior: start with the exact template/static context file.
- Tests: read only tests related to the changed behavior.
- Migrations: read only for model/schema changes or migration debugging.

## Backend files

| Real file | Context file |
|---|---|
| `apps/flota/__init__.py` | [`files/apps/flota/__init__.py.md`](../files/apps/flota/__init__.py.md) |
| `apps/flota/admin.py` | [`files/apps/flota/admin.py.md`](../files/apps/flota/admin.py.md) |
| `apps/flota/apps.py` | [`files/apps/flota/apps.py.md`](../files/apps/flota/apps.py.md) |
| `apps/flota/forms.py` | [`files/apps/flota/forms.py.md`](../files/apps/flota/forms.py.md) |
| `apps/flota/IMPLEMENTATION_PLAN.md` | [`files/apps/flota/IMPLEMENTATION_PLAN.md.md`](../files/apps/flota/IMPLEMENTATION_PLAN.md.md) |
| `apps/flota/models.py` | [`files/apps/flota/models.py.md`](../files/apps/flota/models.py.md) |
| `apps/flota/selectors.py` | [`files/apps/flota/selectors.py.md`](../files/apps/flota/selectors.py.md) |
| `apps/flota/services.py` | [`files/apps/flota/services.py.md`](../files/apps/flota/services.py.md) |
| `apps/flota/urls.py` | [`files/apps/flota/urls.py.md`](../files/apps/flota/urls.py.md) |
| `apps/flota/validators.py` | [`files/apps/flota/validators.py.md`](../files/apps/flota/validators.py.md) |
| `apps/flota/views.py` | [`files/apps/flota/views.py.md`](../files/apps/flota/views.py.md) |

## Template files

| Real file | Context file |
|---|---|
| `apps/flota/templates/flota/includes/deadline_badge.html` | [`files/apps/flota/templates/flota/includes/deadline_badge.html.md`](../files/apps/flota/templates/flota/includes/deadline_badge.html.md) |
| `apps/flota/templates/flota/includes/form_fields.html` | [`files/apps/flota/templates/flota/includes/form_fields.html.md`](../files/apps/flota/templates/flota/includes/form_fields.html.md) |
| `apps/flota/templates/flota/includes/messages.html` | [`files/apps/flota/templates/flota/includes/messages.html.md`](../files/apps/flota/templates/flota/includes/messages.html.md) |
| `apps/flota/templates/flota/index.html` | [`files/apps/flota/templates/flota/index.html.md`](../files/apps/flota/templates/flota/index.html.md) |
| `apps/flota/templates/flota/maintenance_form.html` | [`files/apps/flota/templates/flota/maintenance_form.html.md`](../files/apps/flota/templates/flota/maintenance_form.html.md) |
| `apps/flota/templates/flota/maintenance_type_form.html` | [`files/apps/flota/templates/flota/maintenance_type_form.html.md`](../files/apps/flota/templates/flota/maintenance_type_form.html.md) |
| `apps/flota/templates/flota/maintenance_type_list.html` | [`files/apps/flota/templates/flota/maintenance_type_list.html.md`](../files/apps/flota/templates/flota/maintenance_type_list.html.md) |
| `apps/flota/templates/flota/vehicle_detail.html` | [`files/apps/flota/templates/flota/vehicle_detail.html.md`](../files/apps/flota/templates/flota/vehicle_detail.html.md) |
| `apps/flota/templates/flota/vehicle_form.html` | [`files/apps/flota/templates/flota/vehicle_form.html.md`](../files/apps/flota/templates/flota/vehicle_form.html.md) |

## Static files

| Real file | Context file |
|---|---|
| `apps/flota/static/flota/flota.js` | [`files/apps/flota/static/flota/flota.js.md`](../files/apps/flota/static/flota/flota.js.md) |

## Test files

| Real file | Context file |
|---|---|
| `apps/flota/tests.py` | [`files/apps/flota/tests.py.md`](../files/apps/flota/tests.py.md) |

## Migration files

| Real file | Context file |
|---|---|
| `apps/flota/migrations/__init__.py` | [`files/apps/flota/migrations/__init__.py.md`](../files/apps/flota/migrations/__init__.py.md) |
| `apps/flota/migrations/0001_initial.py` | [`files/apps/flota/migrations/0001_initial.py.md`](../files/apps/flota/migrations/0001_initial.py.md) |
| `apps/flota/migrations/0002_seed_maintenance_types.py` | [`files/apps/flota/migrations/0002_seed_maintenance_types.py.md`](../files/apps/flota/migrations/0002_seed_maintenance_types.py.md) |

