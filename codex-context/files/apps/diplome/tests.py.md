# Source snapshot

## `apps/diplome/tests.py`

Size: 30.2 KB

Redacted secret-like assignments: 2

```python
import json
from copy import deepcopy

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.media_library.models import MediaAsset

from .forms import DiplomaTemplateCreateForm
from .models import DiplomaGenerationBatch, DiplomaTemplate, ParticipantList
from .pdf_renderer import _fitted_box
from .services import build_default_layout, create_diploma_template
from .validators import MAX_LAYOUT_JSON_BYTES, validate_layout_json
from .views import DRAFT_TEMPLATE_IDS_SESSION_KEY


class DiplomaTemplateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="diploma-owner",
            password=<redacted>
            first_name="Ana",
            last_name="Operator",
        )
        cls.other_user = get_user_model().objects.create_user(
            username="other-owner",
            password=<redacted>
        )

    def setUp(self):
        self.client.force_login(self.user)

    def create_template(
        self,
        *,
        owner=None,
        name="Diplomă absolvire",
        category="General",
        with_sample_layout=False,
    ):
        template = create_diploma_template(
            owner=owner or self.user,
            data={
                "name": name,
                "category": category,
                "description": "Template pentru cursuri",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        if with_sample_layout:
            template.layout_json = build_default_layout()
            template.full_clean()
            template.save(update_fields=("layout_json", "updated_at"))
        return template

    def create_media_asset(self, *, owner=None, name="Logo"):
        asset = MediaAsset(
            owner=owner or self.user,
            name=name,
            original_filename="logo.png",
            kind=MediaAsset.Kind.RASTER,
            extension=".png",
            mime_type="image/png",
            size_bytes=128,
            width_px=32,
            height_px=20,
            sha256="a" * 64,
        )
        asset.file.name = f"media_library/tests/{asset.pk}.png"
        asset.save()
        return asset

    def append_media_element(self, layout, asset, *, element_id="logo"):
        layout["elements"].append({
            "id": element_id,
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
            "alt": asset.name,
        })

    def test_all_diploma_pages_require_login(self):
        template = self.create_template()
        routes = (
            reverse("diplome:list_index"),
            reverse("diplome:template_list"),
            reverse("diplome:template_create"),
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            reverse("diplome:template_preview", kwargs={"template_id": template.pk}),
            reverse("diplome:generation_index"),
            reverse("diplome:history_index"),
        )
        self.client.logout()
        for url in routes:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login")))

    def test_user_can_create_template_with_blank_layout(self):
        response = self.client.post(
            reverse("diplome:template_create"),
            {
                "name": "Diplomă Inspector SSM",
                "category": "  SSM   avansat  ",
                "description": "Model A4 pentru absolvire",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )

        template = DiplomaTemplate.objects.get()
        self.assertRedirects(
            response,
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
        )
        self.assertEqual(template.owner, self.user)
        self.assertEqual(template.category, "SSM avansat")
        self.assertEqual(template.page_width_mm, 297)
        self.assertEqual(template.page_height_mm, 210)
        self.assertEqual(template.grid_size_mm, 1)
        self.assertEqual(template.major_grid_size_mm, 10)
        self.assertEqual(template.layout_json["version"], 2)
        self.assertEqual(template.layout_json["page"]["width_mm"], 297)
        self.assertEqual(template.layout_json["page"]["height_mm"], 210)
        self.assertEqual(template.layout_json["page"]["grid_mm"], 1)
        self.assertEqual(template.layout_json["guides"], {"vertical": [], "horizontal": []})
        self.assertEqual(template.layout_json["elements"], [])
        self.assertIn(
            str(template.pk),
            self.client.session[DRAFT_TEMPLATE_IDS_SESSION_KEY],
        )

    def test_nonempty_save_finalizes_new_template_draft(self):
        self.client.post(
            reverse("diplome:template_create"),
            {
                "name": "Template finalizat",
                "category": "General",
                "description": "",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        template = DiplomaTemplate.objects.get()
        layout = build_default_layout()

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["isDraft"])
        self.assertNotIn(
            str(template.pk),
            self.client.session.get(DRAFT_TEMPLATE_IDS_SESSION_KEY, []),
        )
    def test_empty_save_keeps_new_template_as_draft(self):
        self.client.post(
            reverse("diplome:template_create"),
            {
                "name": "Template încă gol",
                "category": "General",
                "description": "",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        template = DiplomaTemplate.objects.get()

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(template.layout_json)},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["isDraft"])
        self.assertIn(
            str(template.pk),
            self.client.session[DRAFT_TEMPLATE_IDS_SESSION_KEY],
        )

    def test_ajax_discard_deletes_new_template_draft(self):
        self.client.post(
            reverse("diplome:template_create"),
            {
                "name": "Template abandonat",
                "category": "General",
                "description": "",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        template = DiplomaTemplate.objects.get()

        response = self.client.post(
            reverse("diplome:template_delete", kwargs={"template_id": template.pk}),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            HTTP_ACCEPT="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertFalse(DiplomaTemplate.objects.filter(pk=template.pk).exists())
        self.assertNotIn(
            str(template.pk),
            self.client.session.get(DRAFT_TEMPLATE_IDS_SESSION_KEY, []),
        )
        list_response = self.client.get(reverse("diplome:template_list"))
        self.assertNotContains(list_response, "Template-ul a fost creat.")

    def test_create_form_does_not_validate_an_incomplete_model_instance(self):
        form = DiplomaTemplateCreateForm(data={
            "name": "Diplomă Inspector SSM",
            "category": "SSM",
            "description": "Model cu diacritice pentru Brașov",
            "page_size": "A4",
            "orientation": "landscape",
        })

        self.assertTrue(form.is_valid(), form.errors)
        self.assertNotIn("layout_json", form.errors)

    def test_template_list_only_contains_owned_templates(self):
        own = self.create_template(name="Template propriu")
        other = self.create_template(owner=self.other_user, name="Template străin")

        response = self.client.get(reverse("diplome:template_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/template_list.html")
        self.assertContains(response, own.name)
        self.assertNotContains(response, other.name)

    def test_template_list_filters_by_owned_category(self):
        ssm = self.create_template(name="Template SSM", category="SSM")
        psi = self.create_template(name="Template PSI", category="PSI")
        other = self.create_template(
            owner=self.other_user,
            name="Template străin",
            category="Categorie privată",
        )

        response = self.client.get(reverse("diplome:template_list"), {"category": "SSM"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ssm.name)
        self.assertNotContains(response, psi.name)
        self.assertNotContains(response, other.name)
        self.assertContains(response, "SSM")
        self.assertNotContains(response, "Categorie privată")

    def test_user_can_open_own_editor_and_navigation_is_active(self):
        template = self.create_template()

        response = self.client.get(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/template_editor.html")
        self.assertContains(
            response,
            f"<title>Editor {template.name} | Platforma TUVTK</title>",
            html=True,
        )
        self.assertContains(response, "diplome/template_editor.js")
        self.assertContains(response, 'data-sidebar-start-collapsed="true"')
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, reverse("diplome:list_index"))
        self.assertContains(response, reverse("diplome:generation_index"))
        self.assertContains(response, reverse("diplome:history_index"))
        self.assertContains(response, 'data-action="undo"')
        self.assertContains(response, 'data-action="redo"')
        self.assertContains(response, 'id="editor-guide-position"')
        self.assertContains(response, 'id="editor-confirm-dialog"')
        self.assertContains(response, 'data-table-columns')
        self.assertContains(response, 'data-action="open-icon-media-picker"')

    def test_editor_page_includes_media_api_urls(self):
        template = self.create_template()

        response = self.client.get(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'data-media-assets-api-url="{reverse("media_library:api_assets")}"')
        self.assertContains(response, f'data-media-assets-upload-url="{reverse("media_library:api_upload")}"')

    def test_editor_includes_owned_media_assets(self):
        template = self.create_template()
        asset = self.create_media_asset(name="Logo propriu")

        response = self.client.get(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk})
        )

        self.assertContains(response, str(asset.pk))
        self.assertContains(response, "Logo propriu")

    def test_editor_does_not_include_foreign_media_assets(self):
        template = self.create_template()
        foreign_asset = self.create_media_asset(owner=self.other_user, name="Logo străin")

        response = self.client.get(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk})
        )

        self.assertNotContains(response, str(foreign_asset.pk))
        self.assertNotContains(response, "Logo străin")

    def test_cross_owner_template_routes_return_404(self):
        template = self.create_template(owner=self.other_user)
        editor_url = reverse("diplome:template_editor", kwargs={"template_id": template.pk})
        routes = (
            ("get", editor_url, None),
            ("get", reverse("diplome:template_preview", kwargs={"template_id": template.pk}), None),
            ("post", editor_url, {"layout_json": json.dumps(build_default_layout())}),
            ("post", reverse("diplome:template_delete", kwargs={"template_id": template.pk}), {}),
        )
        for method, url, data in routes:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url, data or {})
                self.assertEqual(response.status_code, 404)

    def test_valid_layout_json_saves(self):
        template = self.create_template(with_sample_layout=True)
        layout = deepcopy(template.layout_json)
        full_name = next(item for item in layout["elements"] if item["id"] == "full_name")
        full_name["x_mm"] = 72
        full_name["style"]["color"] = "#d41131"

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        template.refresh_from_db()
        saved = next(item for item in template.layout_json["elements"] if item["id"] == "full_name")
        self.assertEqual(saved["x_mm"], 72)
        self.assertEqual(saved["style"]["color"], "#d41131")

    def test_editor_saves_custom_guides(self):
        template = self.create_template()
        layout = deepcopy(template.layout_json)
        layout["guides"] = {"vertical": [10, 148], "horizontal": [25, 105]}

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        template.refresh_from_db()
        self.assertEqual(
            template.layout_json["guides"],
            {"vertical": [10, 148], "horizontal": [25, 105]},
        )

    def test_legacy_layout_without_guides_is_normalized(self):
        layout = build_default_layout()
        layout.pop("guides")

        normalized = validate_layout_json(layout)

        self.assertEqual(normalized["guides"], {"vertical": [], "horizontal": []})

    def test_guides_are_sorted_deduplicated_and_page_bounded(self):
        layout = build_default_layout()
        layout["guides"] = {"vertical": [148, 10, 10], "horizontal": [105, 25]}

        normalized = validate_layout_json(layout)

        self.assertEqual(normalized["guides"]["vertical"], [10, 148])
        invalid = deepcopy(layout)
        invalid["guides"]["vertical"] = [298]
        with self.assertRaises(ValidationError):
            validate_layout_json(invalid)

    def test_legacy_typography_is_normalized_with_defaults(self):
        layout = build_default_layout()
        element = next(item for item in layout["elements"] if item["type"] == "text")
        for key in ("lineHeight", "letterSpacing", "textTransform"):
            element["style"].pop(key)

        normalized = validate_layout_json(layout)
        style = next(item for item in normalized["elements"] if item["id"] == element["id"])["style"]

        self.assertEqual(style["lineHeight"], 1.18)
        self.assertEqual(style["letterSpacing"], 0)
        self.assertEqual(style["textTransform"], "none")

    def test_typography_values_are_normalized_and_validated(self):
        layout = build_default_layout()
        element = next(item for item in layout["elements"] if item["type"] == "variable")
        element["style"].update({
            "lineHeight": 1.5,
            "letterSpacing": 2,
            "textTransform": "uppercase",
        })
        normalized = validate_layout_json(layout)
        style = next(item for item in normalized["elements"] if item["id"] == element["id"])["style"]
        self.assertEqual(style["lineHeight"], 1.5)
        self.assertEqual(style["letterSpacing"], 2.0)
        self.assertEqual(style["textTransform"], "uppercase")

        invalid_values = {
            "lineHeight": 3.1,
            "letterSpacing": 21,
            "textTransform": "capitalize",
        }
        for key, value in invalid_values.items():
            with self.subTest(key=key):
                invalid = deepcopy(layout)
                next(item for item in invalid["elements"] if item["id"] == element["id"])["style"][key] = value
                with self.assertRaises(ValidationError):
                    validate_layout_json(invalid)

    def test_list_element_validates_and_rejects_unsafe_items(self):
        layout = build_default_layout()
        list_element = {
            "id": "requirements",
            "type": "list",
            "label": "Cerințe",
            "x_mm": 20,
            "y_mm": 80,
            "width_mm": 120,
            "height_mm": 40,
            "rotation": 0,
            "zIndex": 100,
            "locked": False,
            "visible": True,
            "style": {
                "fontFamily": "Inter",
                "fontSize": 14,
                "bold": False,
                "italic": False,
                "underline": False,
                "color": "#111827",
                "align": "left",
                "lineHeight": 1.2,
                "letterSpacing": 0,
                "textTransform": "none",
                "listType": "bullet",
                "indent_mm": 5,
            },
            "items": ["Primul punct", "Al doilea punct"],
        }
        layout["elements"].append(list_element)

        normalized = validate_layout_json(layout)
        self.assertEqual(normalized["elements"][-1]["items"], list_element["items"])

        too_many = deepcopy(layout)
        too_many["elements"][-1]["items"] = [f"Punct {index}" for index in range(21)]
        with self.assertRaises(ValidationError):
            validate_layout_json(too_many)
        for unsafe in ("<b>HTML</b>", "javascript:alert(1)", "https://example.com"):
            with self.subTest(unsafe=unsafe):
                invalid = deepcopy(layout)
                invalid["elements"][-1]["items"] = [unsafe]
                with self.assertRaises(ValidationError):
                    validate_layout_json(invalid)

    def test_editor_saves_typography_and_list_elements(self):
        template = self.create_template(with_sample_layout=True)
        layout = deepcopy(template.layout_json)
        layout["elements"][0]["style"].update({
            "lineHeight": 1.4,
            "letterSpacing": 1.5,
            "textTransform": "lowercase",
        })
        list_style = {
            **layout["elements"][0]["style"],
            "listType": "number",
            "indent_mm": 5,
        }
        layout["elements"].append({
            "id": "agenda", "type": "list", "label": "Agendă",
            "x_mm": 10, "y_mm": 10, "width_mm": 80, "height_mm": 40,
            "rotation": 0, "zIndex": 101, "locked": False, "visible": True,
            "style": list_style, "items": ["Introducere", "Evaluare"],
        })

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        template.refresh_from_db()
        self.assertEqual(template.layout_json["elements"][-1]["type"], "list")

    def test_editor_rejects_invalid_typography_with_400(self):
        template = self.create_template(with_sample_layout=True)
        layout = deepcopy(template.layout_json)
        layout["elements"][0]["style"]["lineHeight"] = 0.5

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 400)

    def test_background_stretch_is_valid(self):
        asset = self.create_media_asset()
        layout = build_default_layout()
        layout["elements"].append({
            "id": "background", "type": "background", "label": "Fundal",
            "x_mm": 0, "y_mm": 0, "width_mm": 297, "height_mm": 210,
            "rotation": 0, "zIndex": 0, "locked": True, "visible": True,
            "style": {"fit": "stretch", "opacity": 1},
            "assetId": str(asset.pk), "alt": "",
        })

        self.assertEqual(validate_layout_json(layout)["elements"][-1]["style"]["fit"], "stretch")
        self.assertEqual(
            _fitted_box(
                source_width=100,
                source_height=50,
                x=0,
                y=0,
                width=297,
                height=210,
                fit="stretch",
            ),
            (0, 0, 297, 210),
        )

    def test_layout_with_owned_asset_id_saves(self):
        template = self.create_template()
        asset = self.create_media_asset()
        layout = deepcopy(template.layout_json)
        self.append_media_element(layout, asset)

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        template.refresh_from_db()
        saved = next(element for element in template.layout_json["elements"] if element["id"] == "logo")
        self.assertEqual(saved["assetId"], str(asset.pk))

    def test_custom_icon_asset_validates_and_saves(self):
        template = self.create_template()
        asset = self.create_media_asset(name="Icon personalizat")
        layout = deepcopy(template.layout_json)
        layout["elements"].append({
            "id": "custom_icon",
            "type": "icon",
            "label": "Icon personalizat",
            "x_mm": 20,
            "y_mm": 20,
            "width_mm": 15,
            "height_mm": 15,
            "rotation": 0,
            "zIndex": 110,
            "locked": False,
            "visible": True,
            "style": {"color": "#164194", "opacity": 0.8},
            "iconName": "award",
            "assetId": str(asset.pk),
            "alt": "Icon personalizat",
        })

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        template.refresh_from_db()
        saved = next(element for element in template.layout_json["elements"] if element["id"] == "custom_icon")
        self.assertEqual(saved["assetId"], str(asset.pk))
        self.assertEqual(saved["iconName"], "award")

    def test_table_content_and_styles_save(self):
        template = self.create_template(with_sample_layout=True)
        layout = deepcopy(template.layout_json)
        table = next(element for element in layout["elements"] if element["type"] == "table")
        table["columns"] = ["Curs", "Ore"]
        table["rows"] = [["SSM", "80"], ["PSI", "40"]]
        table["style"].update({
            "fontSize": 16,
            "bold": True,
            "align": "left",
            "borderColor": "#d41131",
            "headerBackground": "#f3f4f6",
        })

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        template.refresh_from_db()
        saved = next(element for element in template.layout_json["elements"] if element["type"] == "table")
        self.assertEqual(saved["columns"], ["Curs", "Ore"])
        self.assertEqual(saved["rows"], [["SSM", "80"], ["PSI", "40"]])
        self.assertEqual(saved["style"]["borderColor"], "#d41131")

    def test_layout_with_foreign_asset_id_fails(self):
        template = self.create_template()
        foreign_asset = self.create_media_asset(owner=self.other_user)
        original_layout = deepcopy(template.layout_json)
        layout = deepcopy(original_layout)
        self.append_media_element(layout, foreign_asset, element_id="foreign_logo")

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        template.refresh_from_db()
        self.assertEqual(template.layout_json, original_layout)

    def test_invalid_layout_json_is_rejected_without_modifying_template(self):
        template = self.create_template(with_sample_layout=True)
        original = deepcopy(template.layout_json)
        cases = []

        invalid_type = deepcopy(original)
        invalid_type["elements"][0]["type"] = "video"
        cases.append(("element type", json.dumps(invalid_type)))

        invalid_variable = deepcopy(original)
        next(item for item in invalid_variable["elements"] if item["type"] == "variable")["variable"] = "email"
        cases.append(("variable", json.dumps(invalid_variable)))

        invalid_color = deepcopy(original)
        next(item for item in invalid_color["elements"] if item["type"] == "text")["style"]["color"] = "navy"
        cases.append(("color", json.dumps(invalid_color)))

        invalid_geometry = deepcopy(original)
        invalid_geometry["elements"][0]["x_mm"] = -1
        cases.append(("geometry", json.dumps(invalid_geometry)))

        unsafe_html = deepcopy(original)
        next(item for item in unsafe_html["elements"] if item["type"] == "text")["text"] = "<script>alert(1)</script>"
        cases.append(("unsafe html", json.dumps(unsafe_html)))

        duplicate_id = deepcopy(original)
        duplicate_id["elements"][1]["id"] = duplicate_id["elements"][0]["id"]
        cases.append(("duplicate id", json.dumps(duplicate_id)))

        cases.append(("oversized", "x" * (MAX_LAYOUT_JSON_BYTES + 1)))

        url = reverse("diplome:template_editor", kwargs={"template_id": template.pk})
        for label, payload in cases:
            with self.subTest(label=label):
                response = self.client.post(url, {"layout_json": payload})
                self.assertEqual(response.status_code, 400)
                self.assertFalse(response.json()["success"])
                template.refresh_from_db()
                self.assertEqual(template.layout_json, original)

    def test_version_one_pixel_layout_is_converted_to_millimeters(self):
        metric_layout = build_default_layout()
        pixel_layout = deepcopy(metric_layout)
        pixel_layout["version"] = 1
        pixel_layout["page"] = {
            "size": "A4",
            "orientation": "landscape",
            "width": 1123,
            "height": 794,
            "gridSize": 10,
            "background": None,
        }
        for element in pixel_layout["elements"]:
            element["x"] = round(element.pop("x_mm") * 1123 / 297)
            element["y"] = round(element.pop("y_mm") * 794 / 210)
            element["width"] = round(element.pop("width_mm") * 1123 / 297)
            element["height"] = round(element.pop("height_mm") * 794 / 210)

        converted = validate_layout_json(pixel_layout)

        self.assertEqual(converted["version"], 2)
        self.assertEqual(converted["page"]["width_mm"], 297)
        self.assertEqual(converted["page"]["height_mm"], 210)
        self.assertNotIn("x", converted["elements"][0])
        self.assertIn("x_mm", converted["elements"][0])

    def test_preview_renders_sample_participant_data(self):
        template = self.create_template()

        response = self.client.get(
            reverse("diplome:template_preview", kwargs={"template_id": template.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/template_preview.html")
        self.assertContains(response, 'data-sidebar-start-collapsed="true"')
        self.assertEqual(response.context["sample_participant"]["full_name"], "Andrei Popescu")
        self.assertEqual(response.context["sample_participant"]["date_of_birth"], "12.04.1990")
        self.assertEqual(response.context["sample_participant"]["place_of_birth"], "Brașov")
        self.assertEqual(response.context["sample_participant"]["certificate_number"], "TTK-2026-001")
        self.assertContains(response, "Andrei Popescu")
        self.assertContains(response, "TTK-2026-001")

    def test_delete_is_post_only(self):
        template = self.create_template()
        url = reverse("diplome:template_delete", kwargs={"template_id": template.pk})

        self.assertEqual(self.client.get(url).status_code, 405)
        response = self.client.post(url)

        self.assertRedirects(response, reverse("diplome:template_list"))
        self.assertFalse(DiplomaTemplate.objects.filter(pk=template.pk).exists())

    def test_used_template_delete_preserves_batch_history_snapshot(self):
        template = self.create_template()
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="Lista cu istoric",
            source_file_name="istoric.csv",
        )
        DiplomaGenerationBatch.objects.create(
            owner=self.user,
            participant_list=participant_list,
            template=template,
            participant_list_name=participant_list.name,
            template_name=template.name,
            output_folder=f"diplomas/{self.user.pk}/batch-test",
        )

        response = self.client.post(
            reverse("diplome:template_delete", kwargs={"template_id": template.pk}),
            follow=True,
        )

        self.assertRedirects(response, reverse("diplome:template_list"))
        self.assertContains(response, "Template-ul a fost șters.")
        self.assertFalse(DiplomaTemplate.objects.filter(pk=template.pk).exists())
        batch = DiplomaGenerationBatch.objects.get()
        self.assertIsNone(batch.template_id)
        self.assertEqual(batch.template_display_name, "Diplomă absolvire")
```
