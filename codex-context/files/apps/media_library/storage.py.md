# apps/media_library/storage.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/media_library/storage.py`
- App: `media_library`
- App guide: `codex-context/apps/media_library.md`
- Role: `backend`
- Size: 518 bytes
- Source SHA-256: `a2287ed0913226a56068c4c0b10299dec2775a0f19a33260f842ced23e46c721`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class PrivateMediaStorage(FileSystemStorage):
    def __init__(self):
        super().__init__(base_url=None)

    @property
    def base_location(self):
        return settings.PRIVATE_MEDIA_ROOT

    @property
    def location(self):
        return os.path.abspath(self.base_location)

    @property
    def base_url(self):
        return None
```
