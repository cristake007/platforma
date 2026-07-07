# Django app: media_library

Migrations are excluded by default. Tests are included unless `--no-tests` is used.

## `apps/media_library/__init__.py`

Size: 1 B

```python

```

## `apps/media_library/admin.py`

Size: 438 B

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

## `apps/media_library/AGENTS.md`

Size: 2.4 KB

````markdown
# Media Library App Instructions

## Scope and integration

This app owns private reusable raster/SVG assets, upload validation and sanitization, owner-scoped delivery, and safe deletion.

`diplome` consumes these assets in layouts and generated PDFs.

## Read before editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md` for UI/template work.
- This file.
- Only the files for the selected workflow.

Use `codex-context/apps/media_library.md` only when a path is unknown.

## Minimal routing

- Upload/input rules: `forms.py`, `validators.py`, `services.py`, then matching tests in `tests.py`.
- Listing/content/delete endpoints: `urls.py`, `views.py`, `selectors.py`, `services.py`, then endpoint tests.
- Storage/file lifecycle: `models.py`, `storage.py`, `signals.py`, `services.py`, then storage/deletion tests.
- Library UI: `templates/media_library/library.html`, `static/media_library/library.css`, and view/form context only if needed.
- Diploma integration: inspect only the importing `diplome` service/renderer and relevant tests.

## Domain and security contracts

- Assets are private and owner-scoped.
- Never expose storage paths or serve a foreign asset.
- Treat filenames, MIME types, dimensions, and client metadata as untrusted.
- Canonicalized validator output is the data persisted by the service.
- Preserve raster re-encoding and restrictive SVG sanitization/response headers.
- File/database writes and cleanup must remain consistent on failure.
- An asset referenced by an owned diploma layout cannot be deleted.
- Keep the narrow `diplome` dependency in the deletion service.
- Do not duplicate layout parsing.
- State changes are POST-only and CSRF-protected.
- Cross-owner object routes return 404.

## Reuse and UI standards

- Reuse the existing upload, asset-grid, delete, empty-state, and message patterns.
- The library page extends `layouts/base.html` and uses shared semantic tokens.
- App CSS is for preview geometry only.
- Colors and controls come from the global daisyUI theme.
- Keep sharp bordered upload/list areas instead of decorative rounded cards.
- Disable upload actions until required client-side prerequisites exist, while keeping server validation authoritative.
- Keep `apps/media_library/**/*.{html,py,js}` registered as a Tailwind source in `theme/static_src/src/styles.css`.

## Focused check

```powershell
python manage.py test apps.media_library
```
````

## `apps/media_library/apps.py`

Size: 229 B

```python
from django.apps import AppConfig


class MediaLibraryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.media_library"

    def ready(self):
        from . import signals  # noqa: F401

```

## `apps/media_library/forms.py`

Size: 1.2 KB

```python
from pathlib import Path

from django import forms

from .validators import validate_and_prepare_media


class MediaAssetUploadForm(forms.Form):
    name = forms.CharField(
        max_length=160,
        required=False,
        label="Nume în bibliotecă",
        widget=forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Opțional"}),
    )
    file = forms.FileField(
        label="Fișier",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "file-input file-input-bordered w-full",
                "accept": ".svg,.png,.jpg,.jpeg,.webp,image/svg+xml,image/png,image/jpeg,image/webp",
                "x-on:change": "fileName = $event.target.files[0]?.name || ''",
            }
        ),
    )

    def clean_name(self):
        return " ".join(self.cleaned_data.get("name", "").split())

    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]
        self.prepared_media = validate_and_prepare_media(uploaded_file)
        uploaded_file.seek(0)
        return uploaded_file

    def resolved_name(self) -> str:
        return self.cleaned_data["name"] or Path(self.cleaned_data["file"].name).stem[:160] or "Fișier media"
```

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

## `apps/media_library/services.py`

Size: 3.1 KB

```python
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
```

## `apps/media_library/signals.py`

Size: 334 B

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

## `apps/media_library/static/media_library/library.css`

Size: 302 B

```css
.media-asset-preview {
    position: relative;
    width: 100%;
    min-height: 0;
    flex: 0 0 auto;
    overflow: hidden;
    aspect-ratio: 4 / 3;
}

.media-asset-preview img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    padding: 0.75rem;
    object-fit: contain;
}
```

## `apps/media_library/storage.py`

Size: 518 B

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

## `apps/media_library/templates/media_library/includes/asset_grid.html`

Size: 8.1 KB

```html
<div id="media-asset-panel" class="border border-base-300 bg-base-100">
    <div class="flex items-center justify-between border-b border-base-300 px-5 py-4">
        <h2 class="font-semibold text-base-content">Fișierele mele</h2>
        <span class="badge badge-ghost">{{ assets|length }}</span>
    </div>
    {% if assets %}
        <div class="grid grid-cols-2 gap-4 p-5 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
            {% for asset in assets %}
                <article class="flex h-full flex-col overflow-hidden border border-base-300 bg-base-100" x-data>
                    <button
                        type="button"
                        class="group media-asset-preview relative block w-full shrink-0 cursor-pointer overflow-hidden bg-base-200 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
                        aria-label="Deschide {{ asset.name }}"
                        title="Deschide"
                        x-on:click="$refs.previewDialog.showModal()"
                    >
                        <img src="{% url 'media_library:content' asset.pk %}" alt="{{ asset.name }}">
                        <span class="absolute inset-0 flex items-center justify-center bg-neutral/35 opacity-0 transition-opacity duration-150 group-hover:opacity-100 group-focus-visible:opacity-100" aria-hidden="true">
                            <span class="flex h-10 w-10 items-center justify-center rounded-full bg-base-100/90 text-base-content shadow">
                                <svg class="h-5 w-5" viewBox="0 0 16 16" fill="currentColor" focusable="false">
                                    <path d="M6.5 12a5.5 5.5 0 1 1 4.389-2.185l3.148 3.148a.75.75 0 0 1-1.06 1.06l-3.148-3.148A5.475 5.475 0 0 1 6.5 12Zm0-1.5a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z"/>
                                    <path d="M6.5 4a.5.5 0 0 1 .5.5V6h1.5a.5.5 0 0 1 0 1H7v1.5a.5.5 0 0 1-1 0V7H4.5a.5.5 0 0 1 0-1H6V4.5a.5.5 0 0 1 .5-.5Z"/>
                                </svg>
                            </span>
                        </span>
                    </button>
                    <div class="flex flex-1 flex-col gap-3 p-3">
                        <div class="grid h-10 min-w-0 grid-rows-2 content-start">
                            <h3 class="h-5 truncate text-sm font-semibold leading-5 text-base-content" title="{{ asset.name }}">{{ asset.name }}</h3>
                            <p class="h-5 truncate text-xs leading-5 text-muted" title="{{ asset.original_filename }}">{{ asset.original_filename }}</p>
                        </div>
                        <div class="mt-auto flex min-h-7 items-center justify-between gap-2">
                            <span class="badge badge-outline h-7">{{ asset.extension|upper }}</span>
                            <button
                                type="button"
                                class="btn btn-error btn-outline btn-square btn-sm shrink-0"
                                aria-label="Șterge {{ asset.name }}"
                                title="Șterge"
                                x-on:click="$refs.deleteDialog.showModal()"
                            >
                                <svg class="h-4 w-4" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" focusable="false">
                                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6Z"/>
                                    <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1 0-2H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1ZM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118ZM2.5 3h11V2h-11v1Z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                    <dialog x-ref="previewDialog" class="modal" aria-labelledby="preview-media-{{ asset.pk }}-title">
                        <div class="modal-box max-w-5xl rounded-none border border-base-300 bg-base-100 p-0 shadow-xl">
                            <form method="dialog">
                                <button class="btn btn-ghost btn-sm btn-circle absolute right-3 top-3 z-10 bg-base-100/80" aria-label="Închide">✕</button>
                            </form>
                            <div class="border-b border-base-300 px-5 py-4 pr-14">
                                <h3 id="preview-media-{{ asset.pk }}-title" class="truncate text-lg font-semibold text-base-content" title="{{ asset.name }}">{{ asset.name }}</h3>
                                <p class="truncate text-sm text-muted" title="{{ asset.original_filename }}">{{ asset.original_filename }}</p>
                            </div>
                            <div class="flex max-h-[70vh] items-center justify-center bg-base-200 p-4">
                                <img
                                    src="{% url 'media_library:content' asset.pk %}"
                                    alt="{{ asset.name }}"
                                    class="max-h-[64vh] max-w-full object-contain"
                                >
                            </div>
                        </div>
                        <form method="dialog" class="modal-backdrop"><button>Închide</button></form>
                    </dialog>
                    <dialog x-ref="deleteDialog" class="modal" aria-labelledby="delete-media-{{ asset.pk }}-title">
                        <div class="modal-box max-w-md rounded-box border border-base-300 bg-base-100 shadow-xl">
                            <form method="dialog">
                                <button class="btn btn-ghost btn-sm btn-circle absolute right-3 top-3" aria-label="Închide">✕</button>
                            </form>
                            <h3 id="delete-media-{{ asset.pk }}-title" class="pr-8 text-lg font-semibold text-base-content">Șterge fișierul?</h3>
                            <p class="mt-3 text-sm text-muted">
                                Fișierul „{{ asset.name }}” va fi eliminat din biblioteca media dacă nu este folosit într-un template de diplomă.
                            </p>
                            <div class="modal-action">
                                <form method="dialog">
                                    <button class="btn btn-ghost btn-sm">Anulează</button>
                                </form>
                                <form
                                    method="post"
                                    action="{% url 'media_library:delete' asset.pk %}"
                                    hx-post="{% url 'media_library:delete' asset.pk %}"
                                    hx-target="#media-asset-panel"
                                    hx-swap="outerHTML"
                                >
                                    {% csrf_token %}
                                    <button type="submit" class="btn btn-error btn-sm">
                                        <svg class="h-4 w-4" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" focusable="false">
                                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6Z"/>
                                            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1 0-2H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1ZM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118ZM2.5 3h11V2h-11v1Z"/>
                                        </svg>
                                        Șterge
                                    </button>
                                </form>
                            </div>
                        </div>
                        <form method="dialog" class="modal-backdrop"><button>Închide</button></form>
                    </dialog>
                </article>
            {% endfor %}
        </div>
    {% else %}
        <div class="p-10 text-center text-sm text-muted">Biblioteca este goală.</div>
    {% endif %}
</div>
```

## `apps/media_library/templates/media_library/includes/delete_response.html`

Size: 108 B

```html
{% include "media_library/includes/messages.html" %}
{% include "media_library/includes/asset_grid.html" %}
```

## `apps/media_library/templates/media_library/includes/library_content.html`

Size: 318 B

```html
<div id="media-library-content" class="space-y-6">
    {% include "media_library/includes/messages.html" %}

    <div class="grid gap-6 lg:grid-cols-[22rem_minmax(0,1fr)]">
        {% include "media_library/includes/upload_form.html" %}
        {% include "media_library/includes/asset_grid.html" %}
    </div>
</div>
```

## `apps/media_library/templates/media_library/includes/messages.html`

Size: 754 B

```html
<div
    id="media-library-messages"
    class="toast toast-top toast-end z-50{% if not messages %} hidden{% endif %}"
    aria-live="polite"
    aria-atomic="true"
    {% if messages %}x-data="{ visible: true }" x-init="setTimeout(() => visible = false, 4000)" x-show="visible" x-transition.opacity.duration.500ms{% endif %}
    {% if messages_oob %}hx-swap-oob="true"{% endif %}
>
    {% if messages %}
        {% for message in messages %}
            <div class="alert {% if message.tags == 'error' %}alert-error{% else %}alert-success{% endif %} py-2 text-sm shadow-lg" role="{% if message.tags == 'error' %}alert{% else %}status{% endif %}">
                <span>{{ message }}</span>
            </div>
        {% endfor %}
    {% endif %}
</div>
```

## `apps/media_library/templates/media_library/includes/upload_form.html`

Size: 1.5 KB

```html
<form
    method="post"
    enctype="multipart/form-data"
    class="space-y-4 border border-base-300 bg-base-100 p-5"
    hx-post="{% url 'media_library:index' %}"
    hx-target="#media-library-content"
    hx-swap="outerHTML"
    x-data="{ fileName: '', uploading: false }"
    x-on:submit="uploading = true"
>
    {% csrf_token %}
    <div>
        <h2 class="font-semibold text-base-content">Adaugă fișier</h2>
        <p class="mt-1 text-xs text-muted">SVG static sigur, PNG, JPG, JPEG sau WEBP. Maximum 10 MB.</p>
    </div>
    {% if form.non_field_errors %}<div class="alert alert-error py-2 text-sm">{{ form.non_field_errors }}</div>{% endif %}
    {% for field in form %}
        <label class="form-control w-full">
            <span class="label"><span class="label-text font-medium">{{ field.label }}</span></span>
            {% if field.name == "file" %}
                <div class="space-y-2">
                    {{ field }}
                    <p class="min-h-4 text-xs text-muted" x-text="fileName"></p>
                </div>
            {% else %}
                {{ field }}
            {% endif %}
            {% for error in field.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
    {% endfor %}
    <button type="submit" class="btn btn-primary btn-sm w-full" x-bind:disabled="!fileName || uploading">
        <span class="loading loading-spinner loading-xs" x-show="uploading" style="display: none;" aria-hidden="true"></span>
        Încarcă în bibliotecă
    </button>
</form>
```

## `apps/media_library/templates/media_library/library.html`

Size: 800 B

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Bibliotecă media | Platforma TUVTK{% endblock %}

{% block page_styles %}
<link rel="stylesheet" href="{% static 'media_library/library.css' %}">
{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl space-y-6">
    <header class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Operațiuni</li><li>Bibliotecă media</li></ul></div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Bibliotecă media</h1>
            <p class="mt-1 text-sm text-muted">Încarcă o singură dată imagini reutilizabile în template-urile de diplomă.</p>
        </div>
    </header>

    {% include "media_library/includes/library_content.html" %}
</section>
{% endblock %}
```

## `apps/media_library/tests.py`

Size: 22.3 KB

```python
import json
import tempfile
from copy import deepcopy
from datetime import date
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from apps.diplome.models import Participant, ParticipantList
from apps.diplome.pdf_renderer import render_diploma_pdf
from apps.diplome.services import create_diploma_template, update_diploma_template_layout

from .forms import MediaAssetUploadForm
from .models import MediaAsset
from .services import create_media_asset


SAFE_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" data-name="Illustrator Layer">
<defs><linearGradient id="brand"><stop offset="0" stop-color="#164194"/></linearGradient></defs>
<g data-name="Artwork"><rect x="2" y="2" width="96" height="96" fill="url(#brand)"/></g>
<circle cx="50" cy="50" r="20" fill="#ffffff"/>
</svg>"""

ILLUSTRATOR_STYLE_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" data-name="Logo">
<style type="text/css">.st0{fill:#164194}.st1{fill:none;stroke:#d41131;stroke-width:4}</style>
<g class="st0" data-name="Brand"><rect width="100" height="100"/></g>
<path class="st1" d="M10 10 L90 90"/>
<circle cx="50" cy="50" r="20" style="fill:rgb(255,255,255)"/>
</svg>"""


class MediaLibraryTests(TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.settings_override = override_settings(PRIVATE_MEDIA_ROOT=self.temp_directory.name)
        self.settings_override.enable()
        self.user = get_user_model().objects.create_user(username="media-owner", password="test-password")
        self.other_user = get_user_model().objects.create_user(username="other-media-owner", password="test-password")
        self.client.force_login(self.user)

    def tearDown(self):
        self.settings_override.disable()
        self.temp_directory.cleanup()

    def _png_upload(self, name="logo.png"):
        output = BytesIO()
        Image.new("RGBA", (32, 20), (22, 65, 148, 255)).save(output, format="PNG")
        return SimpleUploadedFile(name, output.getvalue(), content_type="image/png")

    def _create_asset(self, *, owner=None, upload=None, name="Logo"):
        upload = upload or self._png_upload()
        form = MediaAssetUploadForm(data={"name": name}, files={"file": upload})
        self.assertTrue(form.is_valid(), form.errors)
        return create_media_asset(
            owner=owner or self.user,
            uploaded_file=form.cleaned_data["file"],
            name=form.resolved_name(),
            prepared_media=form.prepared_media,
        )

    def _create_template(self):
        return create_diploma_template(
            owner=self.user,
            data={
                "name": "Template cu logo",
                "category": "General",
                "description": "",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )

    def test_upload_reencodes_raster_and_stores_it_in_private_storage(self):
        response = self.client.post(
            reverse("media_library:index"),
            {"name": "Logo TUVTK", "file": self._png_upload()},
        )

        self.assertRedirects(response, reverse("media_library:index"))
        asset = MediaAsset.objects.get()
        self.assertEqual(asset.owner, self.user)
        self.assertEqual(asset.mime_type, "image/png")
        self.assertEqual((asset.width_px, asset.height_px), (32, 20))
        self.assertTrue(asset.file.name.startswith(f"media_library/{self.user.pk}/"))
        self.assertTrue(asset.file.storage.exists(asset.file.name))

    def test_htmx_upload_returns_refreshed_library_partial(self):
        response = self.client.post(
            reverse("media_library:index"),
            {"name": "Logo HTMX", "file": self._png_upload()},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        asset = MediaAsset.objects.get()
        self.assertEqual(asset.owner, self.user)
        self.assertContains(response, 'id="media-library-content"')
        self.assertContains(response, 'id="media-library-messages"')
        self.assertContains(response, "x-transition.opacity.duration.500ms")
        self.assertContains(response, "Fișierul a fost adăugat în biblioteca media.")
        self.assertContains(response, "Logo HTMX")
        self.assertContains(response, 'hx-target="#media-library-content"')
        self.assertNotContains(response, "<title>")

    def test_htmx_upload_validation_error_returns_partial_with_errors(self):
        response = self.client.post(
            reverse("media_library:index"),
            {"file": SimpleUploadedFile("notes.txt", b"not an image", content_type="text/plain")},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(MediaAsset.objects.exists())
        self.assertContains(response, 'id="media-library-content"')
        self.assertContains(response, 'hx-target="#media-library-content"')

    def test_library_asset_cards_use_htmx_delete_icon_button(self):
        asset = self._create_asset(name="Logo de șters")

        response = self.client.get(reverse("media_library:index"))

        self.assertContains(response, 'x-ref="previewDialog"')
        self.assertContains(response, 'x-on:click="$refs.previewDialog.showModal()"', count=1)
        self.assertContains(response, 'aria-label="Deschide Logo de șters"')
        self.assertContains(response, 'cursor-pointer')
        self.assertContains(response, 'group-hover:opacity-100')
        self.assertContains(response, 'id="preview-media-{}-title"'.format(asset.pk))
        self.assertContains(response, 'modal-box max-w-5xl rounded-none')
        self.assertContains(response, 'max-h-[64vh] max-w-full object-contain')
        self.assertNotContains(response, 'target="_blank"')
        self.assertNotContains(response, 'btn btn-outline btn-square btn-sm shrink-0" aria-label="Deschide')
        self.assertContains(response, 'hx-post="{}"'.format(reverse("media_library:delete", kwargs={"asset_id": asset.pk})))
        self.assertContains(response, 'hx-target="#media-asset-panel"')
        self.assertContains(response, 'aria-label="Șterge Logo de șters"')
        self.assertContains(response, 'viewBox="0 0 16 16"')
        self.assertContains(response, 'focusable="false"')
        self.assertContains(response, 'class="modal"')
        self.assertContains(response, "Șterge fișierul?")
        self.assertContains(response, "Anulează")

    def test_htmx_delete_owned_asset_returns_refreshed_asset_panel(self):
        deleted_asset = self._create_asset(name="Logo vechi")
        remaining_asset = self._create_asset(name="Logo rămas")

        response = self.client.post(
            reverse("media_library:delete", kwargs={"asset_id": deleted_asset.pk}),
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(MediaAsset.objects.filter(pk=deleted_asset.pk).exists())
        self.assertTrue(MediaAsset.objects.filter(pk=remaining_asset.pk).exists())
        self.assertContains(response, 'id="media-library-messages"')
        self.assertContains(response, 'hx-swap-oob="true"')
        self.assertContains(response, "Fișierul a fost șters din biblioteca media.")
        self.assertContains(response, 'id="media-asset-panel"')
        self.assertContains(response, "Logo rămas")
        self.assertNotContains(response, "Logo vechi")
        self.assertContains(response, 'hx-target="#media-asset-panel"')
        self.assertNotContains(response, "<title>")

    def test_htmx_delete_foreign_asset_is_owner_scoped(self):
        foreign_asset = self._create_asset(owner=self.other_user, name="Logo străin")

        response = self.client.post(
            reverse("media_library:delete", kwargs={"asset_id": foreign_asset.pk}),
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(MediaAsset.objects.filter(pk=foreign_asset.pk).exists())

    def test_json_asset_list_requires_login(self):
        self.client.logout()

        response = self.client.get(reverse("media_library:api_assets"))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_json_asset_list_returns_only_owned_assets(self):
        own_asset = self._create_asset(name="Logo propriu")
        self._create_asset(owner=self.other_user, name="Logo străin")

        response = self.client.get(reverse("media_library:api_assets"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual([asset["id"] for asset in payload["assets"]], [str(own_asset.pk)])
        self.assertEqual(payload["assets"][0]["kind"], "raster")
        self.assertEqual(payload["assets"][0]["mimeType"], "image/png")
        self.assertEqual(payload["assets"][0]["sizeBytes"], own_asset.size_bytes)

    def test_cross_owner_assets_are_not_returned_by_json_list(self):
        foreign_asset = self._create_asset(owner=self.other_user, name="Logo străin")

        response = self.client.get(reverse("media_library:api_assets"))

        self.assertEqual(response.status_code, 200)
        returned_ids = {asset["id"] for asset in response.json()["assets"]}
        self.assertNotIn(str(foreign_asset.pk), returned_ids)

    def test_json_upload_requires_login(self):
        self.client.logout()

        response = self.client.post(
            reverse("media_library:api_upload"),
            {"name": "Logo", "file": self._png_upload()},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))
        self.assertFalse(MediaAsset.objects.exists())

    def test_json_upload_creates_validated_asset(self):
        response = self.client.post(
            reverse("media_library:api_upload"),
            {"name": "Logo TUVTK", "file": self._png_upload()},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        asset = MediaAsset.objects.get()
        self.assertTrue(payload["success"])
        self.assertEqual(payload["asset"]["id"], str(asset.pk))
        self.assertEqual(payload["asset"]["name"], "Logo TUVTK")
        self.assertEqual(payload["asset"]["kind"], "raster")
        self.assertEqual((payload["asset"]["width"], payload["asset"]["height"]), (32, 20))
        self.assertEqual(
            payload["asset"]["url"],
            reverse("media_library:content", kwargs={"asset_id": asset.pk}),
        )

    def test_json_upload_rejects_unsafe_svg(self):
        response = self.client.post(
            reverse("media_library:api_upload"),
            {
                "name": "Nesigur",
                "file": SimpleUploadedFile(
                    "unsafe.svg",
                    b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>',
                    content_type="image/svg+xml",
                ),
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        self.assertIn("file", response.json()["errors"])
        self.assertFalse(MediaAsset.objects.exists())

    def test_json_upload_rejects_unsupported_file(self):
        response = self.client.post(
            reverse("media_library:api_upload"),
            {"file": SimpleUploadedFile("notes.txt", b"not an image", content_type="text/plain")},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("file", response.json()["errors"])
        self.assertFalse(MediaAsset.objects.exists())

    def test_json_upload_response_does_not_expose_storage_paths(self):
        response = self.client.post(
            reverse("media_library:api_upload"),
            {"file": self._png_upload()},
        )

        self.assertEqual(response.status_code, 200)
        asset = MediaAsset.objects.get()
        serialized_response = json.dumps(response.json())
        self.assertNotIn(asset.file.name, serialized_response)
        self.assertNotIn(self.temp_directory.name, serialized_response)
        self.assertNotIn("original_filename", response.json()["asset"])

    def test_safe_svg_is_canonicalized_and_served_with_restrictive_headers(self):
        asset = self._create_asset(
            upload=SimpleUploadedFile("brand.svg", SAFE_SVG, content_type="image/svg+xml")
        )

        response = self.client.get(reverse("media_library:content", kwargs={"asset_id": asset.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/svg+xml")
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertIn("default-src 'none'", response["Content-Security-Policy"])
        stored = b"".join(response.streaming_content)
        self.assertIn(b"<linearGradient", stored)
        self.assertNotIn(b"data-name", stored)
        self.assertNotIn(b"<script", stored)

    def test_safe_illustrator_css_is_converted_to_presentation_attributes(self):
        asset = self._create_asset(
            upload=SimpleUploadedFile("illustrator.svg", ILLUSTRATOR_STYLE_SVG)
        )

        with asset.file.open("rb") as stored_file:
            stored = stored_file.read()

        self.assertNotIn(b"<style", stored)
        self.assertNotIn(b"class=", stored)
        self.assertNotIn(b" style=", stored)
        self.assertIn(b'fill="#164194"', stored)
        self.assertIn(b'stroke="#d41131"', stored)
        self.assertIn(b'fill="rgb(255,255,255)"', stored)

    def test_unsafe_svg_constructs_are_rejected(self):
        unsafe_documents = {
            "script": b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>',
            "foreign object": b'<svg xmlns="http://www.w3.org/2000/svg"><foreignObject/></svg>',
            "event": b'<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"><path d="M0 0"/></svg>',
            "external image": b'<svg xmlns="http://www.w3.org/2000/svg"><image href="https://example.com/a.png"/></svg>',
            "data url": b'<svg xmlns="http://www.w3.org/2000/svg"><path fill="data:image/png;base64,AA" d="M0 0"/></svg>',
            "style": b'<svg xmlns="http://www.w3.org/2000/svg"><style>path{fill:red}</style></svg>',
            "style external url": b'<svg xmlns="http://www.w3.org/2000/svg"><style>.st0{fill:url(https://example.com/a.svg)}</style><path class="st0" d="M0 0"/></svg>',
            "style data url": b'<svg xmlns="http://www.w3.org/2000/svg"><path style="fill:url(data:image/svg+xml,x)" d="M0 0"/></svg>',
            "style import": b'<svg xmlns="http://www.w3.org/2000/svg"><style>@import url(https://example.com/a.css);</style></svg>',
            "style animation": b'<svg xmlns="http://www.w3.org/2000/svg"><style>.st0{animation:spin 1s}</style><path class="st0" d="M0 0"/></svg>',
            "animation": b'<svg xmlns="http://www.w3.org/2000/svg"><animate attributeName="x"/></svg>',
            "dtd": b'<!DOCTYPE svg [<!ENTITY x "boom">]><svg xmlns="http://www.w3.org/2000/svg"/>',
        }
        for label, content in unsafe_documents.items():
            with self.subTest(label=label):
                form = MediaAssetUploadForm(
                    data={"name": label},
                    files={"file": SimpleUploadedFile("unsafe.svg", content)},
                )
                self.assertFalse(form.is_valid())
                self.assertIn("file", form.errors)

    def test_content_and_delete_are_owner_scoped(self):
        asset = self._create_asset(owner=self.other_user)

        self.assertEqual(
            self.client.get(reverse("media_library:content", kwargs={"asset_id": asset.pk})).status_code,
            404,
        )
        self.assertEqual(
            self.client.post(reverse("media_library:delete", kwargs={"asset_id": asset.pk})).status_code,
            404,
        )
        self.assertTrue(MediaAsset.objects.filter(pk=asset.pk).exists())

    def test_asset_used_by_template_cannot_be_deleted(self):
        asset = self._create_asset()
        template = self._create_template()
        layout = deepcopy(template.layout_json)
        layout["elements"].append(
            {
                "id": "logo",
                "type": "image",
                "label": "Logo",
                "x_mm": 10,
                "y_mm": 10,
                "width_mm": 30,
                "height_mm": 20,
                "rotation": 0,
                "zIndex": 100,
                "locked": False,
                "visible": True,
                "style": {"fit": "contain", "opacity": 1},
                "assetId": str(asset.pk),
                "alt": "Logo",
            }
        )
        template.layout_json = layout
        template.save(update_fields=("layout_json",))

        response = self.client.post(reverse("media_library:delete", kwargs={"asset_id": asset.pk}))

        self.assertRedirects(response, reverse("media_library:index"))
        self.assertTrue(MediaAsset.objects.filter(pk=asset.pk).exists())

    def test_asset_used_by_custom_icon_cannot_be_deleted(self):
        asset = self._create_asset(name="Icon personalizat")
        template = self._create_template()
        layout = deepcopy(template.layout_json)
        layout["elements"].append({
            "id": "custom_icon",
            "type": "icon",
            "label": "Icon personalizat",
            "x_mm": 10,
            "y_mm": 10,
            "width_mm": 15,
            "height_mm": 15,
            "rotation": 0,
            "zIndex": 100,
            "locked": False,
            "visible": True,
            "style": {"color": "#164194", "opacity": 1},
            "iconName": "award",
            "assetId": str(asset.pk),
            "alt": "Icon personalizat",
        })
        template.layout_json = layout
        template.save(update_fields=("layout_json",))

        response = self.client.post(reverse("media_library:delete", kwargs={"asset_id": asset.pk}))

        self.assertRedirects(response, reverse("media_library:index"))
        self.assertTrue(MediaAsset.objects.filter(pk=asset.pk).exists())

    def test_unused_asset_and_its_private_file_are_deleted(self):
        asset = self._create_asset()
        stored_name = asset.file.name
        storage = asset.file.storage

        response = self.client.post(reverse("media_library:delete", kwargs={"asset_id": asset.pk}))

        self.assertRedirects(response, reverse("media_library:index"))
        self.assertFalse(MediaAsset.objects.filter(pk=asset.pk).exists())
        self.assertFalse(storage.exists(stored_name))

    def test_editor_rejects_foreign_asset_id_and_exposes_owned_assets(self):
        own_asset = self._create_asset(name="Logo propriu")
        foreign_asset = self._create_asset(owner=self.other_user, name="Logo străin")
        template = self._create_template()
        editor_url = reverse("diplome:template_editor", kwargs={"template_id": template.pk})

        editor_response = self.client.get(editor_url)
        self.assertContains(editor_response, str(own_asset.pk))
        self.assertNotContains(editor_response, str(foreign_asset.pk))

        layout = deepcopy(template.layout_json)
        layout["elements"].append(
            {
                "id": "foreign_logo",
                "type": "image",
                "label": "Logo",
                "x_mm": 10,
                "y_mm": 10,
                "width_mm": 30,
                "height_mm": 20,
                "rotation": 0,
                "zIndex": 100,
                "locked": False,
                "visible": True,
                "style": {"fit": "contain", "opacity": 1},
                "assetId": str(foreign_asset.pk),
                "alt": "Logo",
            }
        )
        response = self.client.post(editor_url, {"layout_json": json.dumps(layout)})

        self.assertEqual(response.status_code, 400)
        template.refresh_from_db()
        self.assertNotIn("foreign_logo", {element["id"] for element in template.layout_json["elements"]})

    def test_raster_and_svg_assets_are_rendered_in_generated_pdf(self):
        raster = self._create_asset(name="Logo raster")
        svg = self._create_asset(
            name="Logo vectorial",
            upload=SimpleUploadedFile("brand.svg", SAFE_SVG, content_type="image/svg+xml"),
        )
        template = self._create_template()
        layout = deepcopy(template.layout_json)
        for index, asset in enumerate((raster, svg), start=1):
            layout["elements"].append(
                {
                    "id": f"media_{index}",
                    "type": "image",
                    "label": asset.name,
                    "x_mm": 10 + index * 35,
                    "y_mm": 10,
                    "width_mm": 30,
                    "height_mm": 20,
                    "rotation": 0,
                    "zIndex": 100 + index,
                    "locked": False,
                    "visible": True,
                    "style": {"fit": "contain", "opacity": 1},
                    "assetId": str(asset.pk),
                    "alt": asset.name,
                }
            )
        layout["elements"].append({
            "id": "custom_icon",
            "type": "icon",
            "label": "Icon raster",
            "x_mm": 120,
            "y_mm": 10,
            "width_mm": 20,
            "height_mm": 20,
            "rotation": 0,
            "zIndex": 110,
            "locked": False,
            "visible": True,
            "style": {"color": "#164194", "opacity": 1},
            "iconName": "award",
            "assetId": str(raster.pk),
            "alt": "Icon raster",
        })
        template = update_diploma_template_layout(
            owner=self.user,
            template_id=template.pk,
            layout=layout,
        )
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="Curs",
            source_file_name="participanti.xlsx",
        )
        participant = Participant.objects.create(
            owner=self.user,
            participant_list=participant_list,
            full_name="Ana Popescu",
            date_of_birth=date(1990, 4, 12),
            place_of_birth="Brașov",
            certificate_number="CERT-1",
            source_row=2,
        )

        pdf = render_diploma_pdf(template=template, participant=participant)

        self.assertTrue(pdf.startswith(b"%PDF"))
```

## `apps/media_library/urls.py`

Size: 623 B

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

## `apps/media_library/validators.py`

Size: 14.1 KB

```python
import hashlib
import re
import warnings
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree

from defusedxml import ElementTree as DefusedElementTree
from defusedxml.common import DefusedXmlException
from django.core.exceptions import ValidationError
from PIL import Image, ImageOps, UnidentifiedImageError
import tinycss2


MAX_MEDIA_FILE_BYTES = 10 * 1024 * 1024
MAX_SVG_FILE_BYTES = 2 * 1024 * 1024
MAX_RASTER_PIXELS = 40_000_000
MAX_RASTER_DIMENSION = 10_000
MAX_SVG_ELEMENTS = 2_000
MAX_SVG_DEPTH = 32
SVG_NAMESPACE = "http://www.w3.org/2000/svg"

RASTER_FORMATS = {
    ".png": ("PNG", "image/png"),
    ".jpg": ("JPEG", "image/jpeg"),
    ".jpeg": ("JPEG", "image/jpeg"),
    ".webp": ("WEBP", "image/webp"),
}
SUPPORTED_EXTENSIONS = {*RASTER_FORMATS, ".svg"}

SVG_ALLOWED_TAG_ATTRIBUTES = {
    "svg": {"viewBox", "width", "height", "preserveAspectRatio"},
    "g": set(),
    "path": {"d", "pathLength"},
    "rect": {"x", "y", "width", "height", "rx", "ry"},
    "circle": {"cx", "cy", "r"},
    "ellipse": {"cx", "cy", "rx", "ry"},
    "line": {"x1", "y1", "x2", "y2"},
    "polyline": {"points"},
    "polygon": {"points"},
    "defs": set(),
    "linearGradient": {
        "x1", "y1", "x2", "y2", "gradientUnits", "gradientTransform", "spreadMethod",
    },
    "radialGradient": {
        "cx", "cy", "r", "fx", "fy", "fr", "gradientUnits", "gradientTransform", "spreadMethod",
    },
    "stop": {"offset", "stop-color", "stop-opacity"},
}
SVG_GLOBAL_ATTRIBUTES = {
    "id", "transform", "opacity", "fill", "fill-opacity", "fill-rule", "clip-rule",
    "stroke", "stroke-width", "stroke-opacity", "stroke-linecap", "stroke-linejoin",
    "stroke-miterlimit", "stroke-dasharray", "stroke-dashoffset", "vector-effect",
    "stop-color", "stop-opacity",
}
SVG_STRIPPED_METADATA_ATTRIBUTES = {"data-name"}
SVG_SAFE_CSS_PROPERTIES = {
    "fill", "fill-opacity", "fill-rule", "clip-rule", "opacity", "stop-color", "stop-opacity",
    "stroke", "stroke-width", "stroke-opacity", "stroke-linecap", "stroke-linejoin",
    "stroke-miterlimit", "stroke-dasharray", "stroke-dashoffset", "vector-effect",
}
SVG_INTERNAL_URL_RE = re.compile(r"^url\(#[A-Za-z_][A-Za-z0-9_.:-]{0,127}\)$")
SVG_ID_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.:-]{0,127}$")
SVG_CLASS_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]{0,127}$")
SVG_CLASS_SELECTOR_RE = re.compile(r"^\.[A-Za-z_][A-Za-z0-9_-]{0,127}$")
SVG_COLOR_FUNCTION_RE = re.compile(r"^(?:rgb|rgba|hsl|hsla)\([^()]{1,128}\)$", re.IGNORECASE)
UNSAFE_VALUE_RE = re.compile(r"(?:javascript\s*:|data\s*:|https?\s*:|//)", re.IGNORECASE)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


@dataclass(frozen=True)
class PreparedMedia:
    content: bytes
    extension: str
    kind: str
    mime_type: str
    width_px: int | None
    height_px: int | None
    sha256: str


def _read_upload(uploaded_file) -> tuple[bytes, str]:
    original_name = Path(uploaded_file.name or "").name
    extension = Path(original_name).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValidationError("Sunt acceptate doar fișiere SVG, PNG, JPG, JPEG și WEBP.")
    limit = MAX_SVG_FILE_BYTES if extension == ".svg" else MAX_MEDIA_FILE_BYTES
    content = uploaded_file.read(limit + 1)
    if not content:
        raise ValidationError("Fișierul este gol.")
    if len(content) > limit:
        limit_mb = limit // (1024 * 1024)
        raise ValidationError(f"Fișierul depășește limita de {limit_mb} MB.")
    return content, extension


def _prepare_raster(content: bytes, extension: str) -> PreparedMedia:
    expected_format, mime_type = RASTER_FORMATS[extension]
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(content)) as source:
                if source.format != expected_format:
                    raise ValidationError("Extensia nu corespunde conținutului imaginii.")
                if getattr(source, "n_frames", 1) != 1:
                    raise ValidationError("Imaginile animate nu sunt acceptate.")
                width, height = source.size
                if (
                    width < 1
                    or height < 1
                    or width > MAX_RASTER_DIMENSION
                    or height > MAX_RASTER_DIMENSION
                    or width * height > MAX_RASTER_PIXELS
                ):
                    raise ValidationError("Dimensiunile imaginii depășesc limitele acceptate.")
                source.load()
                image = ImageOps.exif_transpose(source)
                has_alpha = "A" in image.getbands() or "transparency" in image.info
                image = image.convert("RGBA" if has_alpha and expected_format != "JPEG" else "RGB")
                output = BytesIO()
                if expected_format == "JPEG":
                    image.save(output, format="JPEG", quality=95, optimize=True)
                elif expected_format == "PNG":
                    image.save(output, format="PNG", optimize=True)
                else:
                    image.save(output, format="WEBP", quality=95, method=6)
    except ValidationError:
        raise
    except (Image.DecompressionBombError, Image.DecompressionBombWarning, UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValidationError("Fișierul nu este o imagine validă și sigură.") from exc

    sanitized = output.getvalue()
    return PreparedMedia(
        content=sanitized,
        extension=extension,
        kind="raster",
        mime_type=mime_type,
        width_px=width,
        height_px=height,
        sha256=hashlib.sha256(sanitized).hexdigest(),
    )


def _svg_local_name(qualified_name: str) -> tuple[str, str | None]:
    if qualified_name.startswith("{"):
        namespace, local_name = qualified_name[1:].split("}", 1)
        return local_name, namespace
    return qualified_name, None


def _validate_svg_style_value(value: str) -> str:
    value = value.strip()
    if not value or len(value) > 20_000 or CONTROL_RE.search(value) or UNSAFE_VALUE_RE.search(value):
        raise ValidationError("SVG-ul conține o valoare CSS nesigură.")
    lowered = value.lower()
    if "url(" in lowered and not SVG_INTERNAL_URL_RE.fullmatch(value):
        raise ValidationError("Stilurile SVG pot folosi doar referințe interne către gradienți.")
    if "(" in value and not SVG_INTERNAL_URL_RE.fullmatch(value) and not SVG_COLOR_FUNCTION_RE.fullmatch(value):
        raise ValidationError("SVG-ul conține o funcție CSS neacceptată.")
    return value


def _parse_safe_declarations(content) -> dict[str, str]:
    declarations = {}
    for item in tinycss2.parse_declaration_list(content, skip_comments=True, skip_whitespace=True):
        if item.type == "error":
            raise ValidationError("SVG-ul conține CSS invalid.")
        if item.type != "declaration" or item.lower_name not in SVG_SAFE_CSS_PROPERTIES or item.important:
            raise ValidationError("SVG-ul conține o declarație CSS neacceptată.")
        declarations[item.lower_name] = _validate_svg_style_value(tinycss2.serialize(item.value))
    return declarations


def _sanitize_svg_styles(root) -> None:
    class_rules = []
    for parent in root.iter():
        for child in list(parent):
            tag_name, namespace = _svg_local_name(child.tag)
            if tag_name != "style":
                continue
            if namespace not in {None, SVG_NAMESPACE} or set(child.attrib) - {"type"}:
                raise ValidationError("Elementul SVG style conține atribute neacceptate.")
            if child.attrib.get("type", "text/css").lower() != "text/css":
                raise ValidationError("Elementul SVG style trebuie să conțină CSS.")
            rules = tinycss2.parse_stylesheet(child.text or "", skip_comments=True, skip_whitespace=True)
            for rule in rules:
                if rule.type == "error":
                    raise ValidationError("SVG-ul conține CSS invalid.")
                if rule.type != "qualified-rule":
                    raise ValidationError("Regulile CSS de tip @import, font sau animație nu sunt acceptate.")
                selectors = {
                    selector.strip().removeprefix(".")
                    for selector in tinycss2.serialize(rule.prelude).split(",")
                    if selector.strip()
                }
                serialized_selectors = [selector.strip() for selector in tinycss2.serialize(rule.prelude).split(",")]
                if not serialized_selectors or any(
                    not SVG_CLASS_SELECTOR_RE.fullmatch(selector) for selector in serialized_selectors
                ):
                    raise ValidationError("Sunt acceptați doar selectori CSS simpli de clasă în SVG.")
                class_rules.append((selectors, _parse_safe_declarations(rule.content)))
            parent.remove(child)

    for element in root.iter():
        class_value = element.attrib.pop("class", "").strip()
        inline_style = element.attrib.pop("style", None)
        classes = class_value.split() if class_value else []
        if any(not SVG_CLASS_RE.fullmatch(class_name) for class_name in classes):
            raise ValidationError("SVG-ul conține un nume de clasă CSS invalid.")
        applied = {}
        matched_classes = set()
        for selectors, declarations in class_rules:
            matching = selectors.intersection(classes)
            if matching:
                matched_classes.update(matching)
                applied.update(declarations)
        if set(classes) - matched_classes:
            raise ValidationError("SVG-ul conține o clasă CSS fără o regulă sigură asociată.")
        if inline_style is not None:
            applied.update(_parse_safe_declarations(inline_style))
        for property_name, value in applied.items():
            element.set(property_name, value)


def _validate_svg_tree(root) -> None:
    root_name, root_namespace = _svg_local_name(root.tag)
    if root_name != "svg" or root_namespace not in {None, SVG_NAMESPACE}:
        raise ValidationError("Fișierul trebuie să aibă un element rădăcină SVG valid.")

    ids = set()
    internal_references = set()
    stack = [(root, 1)]
    element_count = 0
    while stack:
        element, depth = stack.pop()
        element_count += 1
        if element_count > MAX_SVG_ELEMENTS or depth > MAX_SVG_DEPTH:
            raise ValidationError("Structura SVG este prea complexă.")
        tag_name, namespace = _svg_local_name(element.tag)
        if namespace not in {None, SVG_NAMESPACE} or tag_name not in SVG_ALLOWED_TAG_ATTRIBUTES:
            raise ValidationError(f"Elementul SVG «{tag_name}» nu este acceptat.")
        if element.text and CONTROL_RE.search(element.text):
            raise ValidationError("SVG-ul conține caractere de control nepermise.")
        if element.text and element.text.strip():
            raise ValidationError("Conținutul text nu este acceptat în SVG.")
        if element.tail and element.tail.strip():
            raise ValidationError("Conținutul text nu este acceptat în SVG.")

        allowed_attributes = SVG_GLOBAL_ATTRIBUTES | SVG_ALLOWED_TAG_ATTRIBUTES[tag_name]
        for qualified_attribute, value in list(element.attrib.items()):
            attribute, attribute_namespace = _svg_local_name(qualified_attribute)
            if attribute_namespace is not None:
                raise ValidationError("Atributele SVG cu namespace nu sunt acceptate.")
            lowered = attribute.lower()
            if lowered.startswith("on") or lowered in {"style", "href"}:
                raise ValidationError(f"Atributul SVG «{attribute}» nu este acceptat.")
            if len(value) > 20_000 or CONTROL_RE.search(value) or UNSAFE_VALUE_RE.search(value):
                raise ValidationError("SVG-ul conține o valoare de atribut nesigură.")
            if attribute in SVG_STRIPPED_METADATA_ATTRIBUTES:
                del element.attrib[qualified_attribute]
                continue
            if attribute not in allowed_attributes:
                raise ValidationError(f"Atributul SVG «{attribute}» nu este acceptat.")
            if "url(" in value.lower():
                if not SVG_INTERNAL_URL_RE.fullmatch(value.strip()):
                    raise ValidationError("SVG-ul poate folosi doar referințe interne către gradienți.")
                internal_references.add(value.strip()[5:-1])
            if attribute == "id":
                if not SVG_ID_RE.fullmatch(value) or value in ids:
                    raise ValidationError("SVG-ul conține un identificator invalid sau duplicat.")
                ids.add(value)
        stack.extend((child, depth + 1) for child in reversed(list(element)))

    if not internal_references.issubset(ids):
        raise ValidationError("SVG-ul conține o referință internă inexistentă.")


def _prepare_svg(content: bytes) -> PreparedMedia:
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValidationError("Fișierul SVG trebuie să fie codificat UTF-8.") from exc
    if re.search(r"<!\s*(?:DOCTYPE|ENTITY)", text, re.IGNORECASE):
        raise ValidationError("Declarațiile DTD și ENTITY nu sunt acceptate în SVG.")
    try:
        root = DefusedElementTree.fromstring(
            text,
            forbid_dtd=True,
            forbid_entities=True,
            forbid_external=True,
        )
    except (DefusedXmlException, ElementTree.ParseError, ValueError) as exc:
        raise ValidationError("Fișierul SVG nu este valid sau conține XML nesigur.") from exc
    _sanitize_svg_styles(root)
    _validate_svg_tree(root)
    ElementTree.register_namespace("", SVG_NAMESPACE)
    sanitized = ElementTree.tostring(root, encoding="utf-8", xml_declaration=True)
    return PreparedMedia(
        content=sanitized,
        extension=".svg",
        kind="svg",
        mime_type="image/svg+xml",
        width_px=None,
        height_px=None,
        sha256=hashlib.sha256(sanitized).hexdigest(),
    )


def validate_and_prepare_media(uploaded_file) -> PreparedMedia:
    content, extension = _read_upload(uploaded_file)
    if extension == ".svg":
        return _prepare_svg(content)
    return _prepare_raster(content, extension)
```

## `apps/media_library/views.py`

Size: 4.7 KB

```python
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from .forms import MediaAssetUploadForm
from .selectors import get_owned_media_asset, list_owned_media_assets
from .services import create_media_asset, delete_media_asset, serialize_media_assets


def _json_form_errors(form) -> dict[str, list[str]]:
    return {
        field: [error["message"] for error in errors]
        for field, errors in form.errors.get_json_data().items()
    }


class MediaLibraryView(LoginRequiredMixin, View):
    template_name = "media_library/library.html"
    partial_template_name = "media_library/includes/library_content.html"

    def _is_htmx(self, request) -> bool:
        return request.headers.get("HX-Request") == "true"

    def _render(self, request, *, form, assets, status=200):
        template_name = self.partial_template_name if self._is_htmx(request) else self.template_name
        return render(
            request,
            template_name,
            {"form": form, "assets": assets},
            status=status,
        )

    def get(self, request):
        return self._render(
            request,
            form=MediaAssetUploadForm(),
            assets=list_owned_media_assets(user=request.user),
        )

    def post(self, request):
        form = MediaAssetUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return self._render(
                request,
                form=form,
                assets=list_owned_media_assets(user=request.user),
                status=200 if self._is_htmx(request) else 400,
            )
        create_media_asset(
            owner=request.user,
            uploaded_file=form.cleaned_data["file"],
            name=form.resolved_name(),
            prepared_media=form.prepared_media,
        )
        messages.success(request, "Fișierul a fost adăugat în biblioteca media.")
        if self._is_htmx(request):
            return self._render(
                request,
                form=MediaAssetUploadForm(),
                assets=list_owned_media_assets(user=request.user),
            )
        return redirect("media_library:index")


class MediaAssetListApiView(LoginRequiredMixin, View):
    def get(self, request):
        assets = serialize_media_assets(list_owned_media_assets(user=request.user))
        return JsonResponse({"assets": assets})


class MediaAssetUploadApiView(LoginRequiredMixin, View):
    def post(self, request):
        form = MediaAssetUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse(
                {"success": False, "errors": _json_form_errors(form)},
                status=400,
            )
        asset = create_media_asset(
            owner=request.user,
            uploaded_file=form.cleaned_data["file"],
            name=form.resolved_name(),
            prepared_media=form.prepared_media,
        )
        return JsonResponse({
            "success": True,
            "asset": serialize_media_assets([asset])[0],
        })


class MediaAssetContentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        asset = get_owned_media_asset(user=request.user, asset_id=kwargs["asset_id"])
        response = FileResponse(
            asset.file.open("rb"),
            content_type=asset.mime_type,
            as_attachment=False,
            filename=asset.safe_download_name,
        )
        response["X-Content-Type-Options"] = "nosniff"
        response["Cache-Control"] = "private, max-age=3600"
        if asset.kind == asset.Kind.SVG:
            response["Content-Security-Policy"] = "default-src 'none'; style-src 'none'; sandbox"
        return response


class MediaAssetDeleteView(LoginRequiredMixin, View):
    partial_template_name = "media_library/includes/delete_response.html"

    def _is_htmx(self, request) -> bool:
        return request.headers.get("HX-Request") == "true"

    def post(self, request, *args, **kwargs):
        try:
            delete_media_asset(owner=request.user, asset_id=kwargs["asset_id"])
        except ValidationError as exc:
            messages.error(request, exc.messages[0])
        else:
            messages.success(request, "Fișierul a fost șters din biblioteca media.")
        if self._is_htmx(request):
            return render(
                request,
                self.partial_template_name,
                {"assets": list_owned_media_assets(user=request.user), "messages_oob": True},
            )
        return redirect("media_library:index")
```
