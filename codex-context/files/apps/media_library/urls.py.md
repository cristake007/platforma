# apps/media_library/urls.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/media_library/urls.py`
- App: `media_library`
- App guide: `codex-context/apps/media_library.md`
- Role: `backend`
- Size: 623 bytes
- Source SHA-256: `326e8f9b2d4c4b93b3815eba940cae08e72331dbb415bcd57863e7993ed5f455`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.urls import path

from .views import (
    MediaAssetContentView,
    MediaAssetDeleteView,
    MediaAssetListApiView,
    MediaAssetUploadApiView,
    MediaLibraryView,
)


app_name = "media_library"

urlpatterns = [
    path("", MediaLibraryView.as_view(), name="index"),
    path("api/assets/", MediaAssetListApiView.as_view(), name="api_assets"),
    path("api/assets/upload/", MediaAssetUploadApiView.as_view(), name="api_upload"),
    path("<uuid:asset_id>/continut/", MediaAssetContentView.as_view(), name="content"),
    path("<uuid:asset_id>/sterge/", MediaAssetDeleteView.as_view(), name="delete"),
]
```
