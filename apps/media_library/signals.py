from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import MediaAsset


@receiver(post_delete, sender=MediaAsset)
def delete_media_asset_file(sender, instance: MediaAsset, **_kwargs) -> None:
    del sender
    if instance.file:
        instance.file.storage.delete(instance.file.name)
