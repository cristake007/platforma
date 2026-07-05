from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import transaction
from django.urls import reverse

from .models import MediaAsset
from .selectors import get_owned_media_asset, get_owned_media_assets_by_ids


def create_media_asset(*, owner, uploaded_file, name: str, prepared_media) -> MediaAsset:
    original_filename = Path(uploaded_file.name or "upload").name[:255]
    asset = MediaAsset(
        owner=owner,
        name=name,
        original_filename=original_filename,
        kind=prepared_media.kind,
        extension=prepared_media.extension,
        mime_type=prepared_media.mime_type,
        size_bytes=len(prepared_media.content),
        width_px=prepared_media.width_px,
        height_px=prepared_media.height_px,
        sha256=prepared_media.sha256,
    )
    stored_name = ""
    try:
        with transaction.atomic():
            asset.file.save(
                f"{asset.pk}{prepared_media.extension}",
                ContentFile(prepared_media.content),
                save=False,
            )
            stored_name = asset.file.name
            asset.full_clean()
            asset.save()
    except Exception:
        if stored_name:
            asset.file.storage.delete(stored_name)
        raise
    return asset


def extract_layout_asset_ids(layout: dict) -> set[str]:
    return {
        element["assetId"]
        for element in layout.get("elements", [])
        if element.get("type") in {"image", "background", "icon"} and element.get("assetId")
    }


def require_owned_layout_assets(*, owner, layout: dict, for_update: bool = False) -> dict[str, MediaAsset]:
    asset_ids = extract_layout_asset_ids(layout)
    assets = get_owned_media_assets_by_ids(
        user=owner,
        asset_ids=asset_ids,
        for_update=for_update,
    )
    missing = asset_ids - set(assets)
    if missing:
        raise ValidationError("Layout-ul conține fișiere media inexistente sau care aparțin altui utilizator.")
    return assets


def serialize_media_assets(assets) -> list[dict]:
    return [
        {
            "id": str(asset.pk),
            "name": asset.name,
            "kind": asset.kind,
            "url": reverse("media_library:content", kwargs={"asset_id": asset.pk}),
            "mimeType": asset.mime_type,
            "width": asset.width_px,
            "height": asset.height_px,
            "sizeBytes": asset.size_bytes,
        }
        for asset in assets
    ]


def delete_media_asset(*, owner, asset_id) -> None:
    from apps.diplome.models import DiplomaTemplate

    with transaction.atomic():
        layouts = DiplomaTemplate.objects.select_for_update().filter(owner=owner).values_list(
            "layout_json",
            flat=True,
        )
        asset = get_owned_media_asset(user=owner, asset_id=asset_id)
        for layout in layouts:
            if str(asset.pk) in extract_layout_asset_ids(layout):
                raise ValidationError("Fișierul este folosit într-un template de diplomă și nu poate fi șters.")
        asset.delete()
