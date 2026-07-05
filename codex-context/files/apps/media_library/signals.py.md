# apps/media_library/signals.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/media_library/signals.py`
- App: `media_library`
- App guide: `codex-context/apps/media_library.md`
- Role: `backend`
- Size: 334 bytes
- Source SHA-256: `02d650b01af5736a9f3fa506e8e88d8bb78f70aed60a000db3c9a8d3db3575c1`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import MediaAsset


@receiver(post_delete, sender=MediaAsset)
def delete_media_asset_file(sender, instance: MediaAsset, **_kwargs) -> None:
    del sender
    if instance.file:
        instance.file.storage.delete(instance.file.name)
```
