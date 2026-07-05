# apps/diplome/apps.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/diplome/apps.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `backend`
- Size: 180 bytes
- Source SHA-256: `d16925e6ae77b0155640cb6142ecbd7cfa9608651a82a6edc175dc792058d0a3`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.apps import AppConfig


class DiplomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.diplome"
    verbose_name = "Diplome"
```
