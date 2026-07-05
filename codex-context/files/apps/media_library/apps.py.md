# apps/media_library/apps.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/media_library/apps.py`
- App: `media_library`
- App guide: `codex-context/apps/media_library.md`
- Role: `backend`
- Size: 229 bytes
- Source SHA-256: `b7c8b062f73a84eb8c4a2ad1e01e4d7871a36c688ffbcbf3b96ba15a5b552e7c`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.apps import AppConfig


class MediaLibraryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.media_library"

    def ready(self):
        from . import signals  # noqa: F401
```
