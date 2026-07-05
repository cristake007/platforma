# apps/tasks/apps.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/tasks/apps.py`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `backend`
- Size: 148 bytes
- Source SHA-256: `aba4a1b2a991fb9321cfc31d78ee623470d761e517f949113b65b8bd56015aec`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tasks"
```
