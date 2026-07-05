# App context: media_library

Generated: `2026-07-05T22:50:42`

Local instructions: `apps/media_library/AGENTS.md`. They define app contracts and the smallest workflow-specific file set.

Use this app guide to select exact file-level context. Do not load all files listed here unless the task truly affects all of them.

## Routing

- Backend behavior: start with `models.py`, `urls.py`, `views.py`, `forms.py`, `services.py`, `selectors.py`, or `validators.py` only if present and relevant.
- UI behavior: start with the exact template/static context file.
- Tests: read only tests related to the changed behavior.
- Migrations: read only for model/schema changes or migration debugging.

## Backend files

| Real file | Context file |
|---|---|
| `apps/media_library/__init__.py` | [`files/apps/media_library/__init__.py.md`](../files/apps/media_library/__init__.py.md) |
| `apps/media_library/admin.py` | [`files/apps/media_library/admin.py.md`](../files/apps/media_library/admin.py.md) |
| `apps/media_library/apps.py` | [`files/apps/media_library/apps.py.md`](../files/apps/media_library/apps.py.md) |
| `apps/media_library/forms.py` | [`files/apps/media_library/forms.py.md`](../files/apps/media_library/forms.py.md) |
| `apps/media_library/models.py` | [`files/apps/media_library/models.py.md`](../files/apps/media_library/models.py.md) |
| `apps/media_library/selectors.py` | [`files/apps/media_library/selectors.py.md`](../files/apps/media_library/selectors.py.md) |
| `apps/media_library/services.py` | [`files/apps/media_library/services.py.md`](../files/apps/media_library/services.py.md) |
| `apps/media_library/signals.py` | [`files/apps/media_library/signals.py.md`](../files/apps/media_library/signals.py.md) |
| `apps/media_library/storage.py` | [`files/apps/media_library/storage.py.md`](../files/apps/media_library/storage.py.md) |
| `apps/media_library/urls.py` | [`files/apps/media_library/urls.py.md`](../files/apps/media_library/urls.py.md) |
| `apps/media_library/validators.py` | [`files/apps/media_library/validators.py.md`](../files/apps/media_library/validators.py.md) |
| `apps/media_library/views.py` | [`files/apps/media_library/views.py.md`](../files/apps/media_library/views.py.md) |

## Template files

| Real file | Context file |
|---|---|
| `apps/media_library/templates/media_library/library.html` | [`files/apps/media_library/templates/media_library/library.html.md`](../files/apps/media_library/templates/media_library/library.html.md) |

## Static files

| Real file | Context file |
|---|---|
| `apps/media_library/static/media_library/library.css` | [`files/apps/media_library/static/media_library/library.css.md`](../files/apps/media_library/static/media_library/library.css.md) |

## Test files

| Real file | Context file |
|---|---|
| `apps/media_library/tests.py` | [`files/apps/media_library/tests.py.md`](../files/apps/media_library/tests.py.md) |

## Migration files

| Real file | Context file |
|---|---|
| `apps/media_library/migrations/__init__.py` | [`files/apps/media_library/migrations/__init__.py.md`](../files/apps/media_library/migrations/__init__.py.md) |
| `apps/media_library/migrations/0001_initial.py` | [`files/apps/media_library/migrations/0001_initial.py.md`](../files/apps/media_library/migrations/0001_initial.py.md) |

