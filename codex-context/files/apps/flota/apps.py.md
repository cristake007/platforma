# apps/flota/apps.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/flota/apps.py`
- App: `flota`
- App guide: `codex-context/apps/flota.md`
- Role: `backend`
- Size: 148 bytes
- Source SHA-256: `07aa2b08af28840e97fe1e1c73a78112452f20b388f8d5723147930f8bcb1ef8`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.apps import AppConfig


class FlotaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.flota"
```
