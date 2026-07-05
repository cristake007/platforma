# apps/media_library/views.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/media_library/views.py`
- App: `media_library`
- App guide: `codex-context/apps/media_library.md`
- Role: `backend`
- Size: 3656 bytes
- Source SHA-256: `2c1d3c2e88744f64d6fea1d5e6930423d1dd2d58c79d48a29e4adff369843292`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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

    def get(self, request):
        return render(
            request,
            self.template_name,
            {"form": MediaAssetUploadForm(), "assets": list_owned_media_assets(user=request.user)},
        )

    def post(self, request):
        form = MediaAssetUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"form": form, "assets": list_owned_media_assets(user=request.user)},
                status=400,
            )
        create_media_asset(
            owner=request.user,
            uploaded_file=form.cleaned_data["file"],
            name=form.resolved_name(),
            prepared_media=form.prepared_media,
        )
        messages.success(request, "Fișierul a fost adăugat în biblioteca media.")
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
    def post(self, request, *args, **kwargs):
        try:
            delete_media_asset(owner=request.user, asset_id=kwargs["asset_id"])
        except ValidationError as exc:
            messages.error(request, exc.messages[0])
        else:
            messages.success(request, "Fișierul a fost șters din biblioteca media.")
        return redirect("media_library:index")
```
