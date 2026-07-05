# Source snapshot

## `apps/media_library/selectors.py`

Size: 690 B

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
