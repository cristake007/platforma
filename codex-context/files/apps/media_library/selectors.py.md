# apps/media_library/selectors.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/media_library/selectors.py`
- App: `media_library`
- App guide: `codex-context/apps/media_library.md`
- Role: `backend`
- Size: 690 bytes
- Source SHA-256: `9f36c113db4a969399b11ff39616adc35e99a3e9cc194c947b81cf4b9f724ef9`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.shortcuts import get_object_or_404

from .models import MediaAsset


def list_owned_media_assets(*, user):
    return MediaAsset.objects.filter(owner=user).order_by("-created_at", "name")


def get_owned_media_asset(*, user, asset_id) -> MediaAsset:
    return get_object_or_404(MediaAsset, owner=user, pk=asset_id)


def get_owned_media_assets_by_ids(*, user, asset_ids, for_update: bool = False) -> dict[str, MediaAsset]:
    normalized_ids = {str(asset_id) for asset_id in asset_ids}
    assets = MediaAsset.objects.filter(owner=user, pk__in=normalized_ids)
    if for_update:
        assets = assets.select_for_update()
    return {str(asset.pk): asset for asset in assets}
```
