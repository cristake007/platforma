# App context: dashboard

Generated: `2026-07-05T22:30:50`

Local instructions: `apps/dashboard/AGENTS.md`. They define app contracts and the smallest workflow-specific file set.

Use this app guide to select exact file-level context. Do not load all files listed here unless the task truly affects all of them.

## Routing

- Backend behavior: start with `models.py`, `urls.py`, `views.py`, `forms.py`, `services.py`, `selectors.py`, or `validators.py` only if present and relevant.
- UI behavior: start with the exact template/static context file.
- Tests: read only tests related to the changed behavior.
- Migrations: read only for model/schema changes or migration debugging.

## Backend files

| Real file | Context file |
|---|---|
| `apps/dashboard/__init__.py` | [`files/apps/dashboard/__init__.py.md`](../files/apps/dashboard/__init__.py.md) |
| `apps/dashboard/apps.py` | [`files/apps/dashboard/apps.py.md`](../files/apps/dashboard/apps.py.md) |
| `apps/dashboard/urls.py` | [`files/apps/dashboard/urls.py.md`](../files/apps/dashboard/urls.py.md) |
| `apps/dashboard/views.py` | [`files/apps/dashboard/views.py.md`](../files/apps/dashboard/views.py.md) |

## Template files

| Real file | Context file |
|---|---|
| `apps/dashboard/templates/dashboard/index.html` | [`files/apps/dashboard/templates/dashboard/index.html.md`](../files/apps/dashboard/templates/dashboard/index.html.md) |

## Test files

| Real file | Context file |
|---|---|
| `apps/dashboard/tests.py` | [`files/apps/dashboard/tests.py.md`](../files/apps/dashboard/tests.py.md) |

## Migration files

| Real file | Context file |
|---|---|
| `apps/dashboard/migrations/__init__.py` | [`files/apps/dashboard/migrations/__init__.py.md`](../files/apps/dashboard/migrations/__init__.py.md) |

