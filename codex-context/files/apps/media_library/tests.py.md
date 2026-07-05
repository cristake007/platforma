# apps/media_library/tests.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/media_library/tests.py`
- App: `media_library`
- App guide: `codex-context/apps/media_library.md`
- Role: `test`
- Size: 18302 bytes
- Source SHA-256: `bc8e356a9041ebaeb82a77b5ef1d0f52382cb9ab46e761f84af215345b464968`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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
