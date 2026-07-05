# apps/media_library/admin.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/media_library/admin.py`
- App: `media_library`
- App guide: `codex-context/apps/media_library.md`
- Role: `backend`
- Size: 438 bytes
- Source SHA-256: `6249ca6522fdc04642191d73781b4ed3aaa0ebf93c1e4929b005b7d80ca549d9`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.contrib import admin

from .models import MediaAsset


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "kind", "mime_type", "size_bytes", "created_at")
    list_filter = ("kind", "mime_type")
    search_fields = ("name", "original_filename", "owner__username")
    readonly_fields = ("id", "sha256", "size_bytes", "width_px", "height_px", "created_at", "updated_at")
```
