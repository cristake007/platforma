# core/apps.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `core/apps.py`
- App: none
- Role: `core`
- Size: 152 bytes
- Source SHA-256: `d5a6861b4953f86d3ce217c55dfb520c4d43d0d3a07e7092d323995f17ec60aa`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from . import signals  # noqa: F401
```
