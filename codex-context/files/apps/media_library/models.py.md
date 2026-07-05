# Source snapshot

## `apps/media_library/models.py`

Size: 2.0 KB

```python
import uuid
from pathlib import Path

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from .storage import PrivateMediaStorage


private_media_storage = PrivateMediaStorage()


def media_asset_upload_to(instance, _filename: str) -> str:
    extension = instance.extension.lstrip(".")
    return f"media_library/{instance.owner_id}/{instance.pk}.{extension}"


class MediaAsset(models.Model):
    class Kind(models.TextChoices):
        RASTER = "raster", "Imagine raster"
        SVG = "svg", "SVG"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="media_library_assets",
    )
    name = models.CharField(max_length=160)
    original_filename = models.CharField(max_length=255)
    file = models.FileField(
        upload_to=media_asset_upload_to,
        storage=private_media_storage,
        max_length=500,
    )
    kind = models.CharField(max_length=16, choices=Kind.choices)
    extension = models.CharField(max_length=8)
    mime_type = models.CharField(max_length=64)
    size_bytes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    width_px = models.PositiveIntegerField(null=True, blank=True)
    height_px = models.PositiveIntegerField(null=True, blank=True)
    sha256 = models.CharField(max_length=64, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", "name")
        indexes = [
            models.Index(fields=("owner", "-created_at"), name="media_owner_created"),
            models.Index(fields=("owner", "name"), name="media_owner_name"),
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def safe_download_name(self) -> str:
        return f"{Path(self.original_filename).stem}{self.extension}"
```
