# apps/diplome/tests_generation.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/diplome/tests_generation.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `test`
- Size: 15685 bytes
- Source SHA-256: `e3304ee1262a55e94e4b225852217269a4e60f6017f564be2c0d773947ffdf4c`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import tempfile
from html import escape
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import GeneratedDiploma, Participant, ParticipantList
from .services import build_default_layout, create_diploma_template, generate_single_diploma


class DiplomaGenerationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._media_directory = tempfile.TemporaryDirectory()
        cls._media_override = override_settings(MEDIA_ROOT=cls._media_directory.name)
        cls._media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls._media_override.disable()
        cls._media_directory.cleanup()

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username="generation-owner",
            password="test-password",
        )
        cls.other_user = user_model.objects.create_user(
            username="generation-other",
            password="test-password",
        )
        cls.participant_list = ParticipantList.objects.create(
            owner=cls.user,
            name="Grupa SSM iulie",
            course_name="Inspector SSM",
            source_file_name="participanti.csv",
            participant_count=2,
        )
        cls.participant = Participant.objects.create(
            owner=cls.user,
            participant_list=cls.participant_list,
            full_name="Ana Șerban",
            date_of_birth="1990-04-12",
            place_of_birth="Brașov",
            certificate_number="CERT/2026 001",
            source_row=2,
        )
        cls.other_participant = Participant.objects.create(
            owner=cls.user,
            participant_list=cls.participant_list,
            full_name="Ion Ionescu",
            date_of_birth="1991-05-13",
            place_of_birth="Sibiu",
            certificate_number="CERT-002",
            source_row=3,
        )
        cls.template = create_diploma_template(
            owner=cls.user,
            data={
                "name": "Diplomă SSM",
                "category": "SSM",
                "description": "Template de test",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        cls.foreign_list = ParticipantList.objects.create(
            owner=cls.other_user,
            name="Lista altui utilizator",
            source_file_name="foreign.csv",
            participant_count=1,
        )
        cls.foreign_participant = Participant.objects.create(
            owner=cls.other_user,
            participant_list=cls.foreign_list,
            full_name="Participant străin",
            date_of_birth="1988-01-02",
            place_of_birth="Cluj-Napoca",
            certificate_number="FOREIGN-001",
            source_row=2,
        )
        cls.foreign_template = create_diploma_template(
            owner=cls.other_user,
            data={
                "name": "Template străin",
                "category": "General",
                "description": "",
                "page_size": "A4",
                "orientation": "portrait",
            },
        )

    def setUp(self):
        self.client.force_login(self.user)

    def selection_payload(self, **overrides):
        payload = {
            "participant_list": str(self.participant_list.pk),
            "participant": str(self.participant.pk),
            "template": str(self.template.pk),
        }
        payload.update(overrides)
        return payload

    def preview_url(self):
        return f"{reverse('diplome:generation_preview')}?{urlencode(self.selection_payload())}"

    def generate_record(self):
        return generate_single_diploma(
            owner=self.user,
            participant_list_id=self.participant_list.pk,
            participant_id=self.participant.pk,
            template_id=self.template.pk,
        )

    def test_pdf_generation_supports_typography_and_list_elements(self):
        layout = build_default_layout(
            page_size=self.template.page_size,
            orientation=self.template.orientation,
        )
        title = next(element for element in layout["elements"] if element["type"] == "text")
        title["style"].update({
            "lineHeight": 1.35,
            "letterSpacing": 1.25,
            "textTransform": "uppercase",
        })
        layout["elements"].append({
            "id": "pdf_list",
            "type": "list",
            "label": "Listă PDF",
            "x_mm": 20,
            "y_mm": 110,
            "width_mm": 90,
            "height_mm": 35,
            "rotation": 0,
            "zIndex": 95,
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
                "letterSpacing": 0.5,
                "textTransform": "none",
                "listType": "number",
                "indent_mm": 5,
            },
            "items": ["Primul punct", "Al doilea punct"],
        })
        self.template.layout_json = layout
        self.template.save(update_fields=("layout_json", "updated_at"))

        generated = self.generate_record()

        with generated.pdf_file.open("rb") as pdf_file:
            self.assertEqual(pdf_file.read(5), b"%PDF-")

    def test_generation_pages_require_login(self):
        generated = self.generate_record()
        routes = (
            ("get", reverse("diplome:generation_index"), None),
            ("get", self.preview_url(), None),
            ("post", reverse("diplome:generation_create"), self.selection_payload()),
            (
                "get",
                reverse(
                    "diplome:generation_download",
                    kwargs={"generated_diploma_id": generated.pk},
                ),
                None,
            ),
        )
        self.client.logout()
        for method, url, data in routes:
            with self.subTest(url=url):
                response = getattr(self.client, method)(url, data or {})
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login")))

    def test_generation_index_lists_only_owned_templates_and_lists(self):
        response = self.client.get(reverse("diplome:generation_index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.participant_list.name)
        self.assertContains(response, self.template.name)
        self.assertNotContains(response, self.foreign_list.name)
        self.assertNotContains(response, self.foreign_template.name)

    def test_generation_index_restores_preview_selection_from_query_string(self):
        response = self.client.get(
            reverse("diplome:generation_index"),
            self.selection_payload(),
        )

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertEqual(str(form["participant_list"].value()), str(self.participant_list.pk))
        self.assertEqual(str(form["participant"].value()), str(self.participant.pk))
        self.assertEqual(str(form["template"].value()), str(self.template.pk))

    def test_generation_index_renders_single_select_participant_table(self):
        response = self.client.get(reverse("diplome:generation_index"))

        self.assertContains(response, "data-participant-table")
        self.assertContains(
            response,
            f'data-participant-id="{self.participant.pk}"',
        )
        self.assertContains(response, 'type="radio"', count=2)

    def test_multiple_participants_are_rejected(self):
        payload = self.selection_payload()
        payload["participant"] = [
            str(self.participant.pk),
            str(self.other_participant.pk),
        ]

        response = self.client.post(reverse("diplome:generation_create"), payload)

        self.assertEqual(response.status_code, 400)
        self.assertFormError(
            response.context["form"],
            "participant",
            "Selectează un singur participant.",
        )
        self.assertFalse(GeneratedDiploma.objects.exists())

    def test_participant_must_belong_to_selected_owned_list(self):
        second_list = ParticipantList.objects.create(
            owner=self.user,
            name="Altă listă",
            source_file_name="alta.csv",
            participant_count=0,
        )
        response = self.client.post(
            reverse("diplome:generation_index"),
            self.selection_payload(participant_list=str(second_list.pk)),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "participant",
            "Participantul nu aparține listei selectate.",
        )

    def test_cross_owner_objects_cannot_be_used_for_generation(self):
        cases = (
            {"participant_list": str(self.foreign_list.pk)},
            {"participant": str(self.foreign_participant.pk)},
            {"template": str(self.foreign_template.pk)},
        )
        for override in cases:
            with self.subTest(override=override):
                response = self.client.post(
                    reverse("diplome:generation_create"),
                    self.selection_payload(**override),
                )
                self.assertEqual(response.status_code, 400)
                self.assertTrue(response.context["form"].errors)
        self.assertFalse(GeneratedDiploma.objects.exists())

    def test_preview_renders_real_participant_values(self):
        response = self.client.get(self.preview_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/generation_preview.html")
        self.assertContains(response, self.participant.full_name)
        self.assertContains(response, "12.04.1990")
        self.assertContains(response, self.participant.place_of_birth)
        self.assertContains(response, self.participant.certificate_number)
        self.assertContains(response, self.template.name)
        self.assertContains(response, self.participant_list.name)
        self.assertContains(
            response,
            f'{reverse("diplome:generation_index")}?'
            f'{escape(response.context["selection_query"])}',
            count=2,
        )

    def test_preview_rejects_malformed_or_cross_owner_selection(self):
        malformed = self.client.get(
            reverse("diplome:generation_preview"),
            {
                "participant_list": "invalid",
                "participant": self.participant.pk,
                "template": self.template.pk,
            },
        )
        foreign = self.client.get(
            reverse("diplome:generation_preview"),
            self.selection_payload(template=str(self.foreign_template.pk)),
        )

        self.assertEqual(malformed.status_code, 404)
        self.assertEqual(foreign.status_code, 404)

    def test_generate_single_diploma_stores_pdf_and_snapshot(self):
        response = self.client.post(
            reverse("diplome:generation_create"),
            self.selection_payload(),
        )

        generated = GeneratedDiploma.objects.get()
        self.assertEqual(response.status_code, 302)
        self.assertIn(f"generated={generated.pk}", response.url)
        self.assertEqual(generated.owner, self.user)
        self.assertEqual(generated.participant_name, self.participant.full_name)
        self.assertEqual(
            generated.certificate_number,
            self.participant.certificate_number,
        )
        self.assertTrue(generated.pdf_file.storage.exists(generated.pdf_file.name))
        self.assertTrue(
            generated.pdf_file.name.startswith(
                f"diplomas/{self.user.pk}/{self.participant_list.pk}/"
            )
        )
        with generated.pdf_file.open("rb") as pdf_file:
            self.assertEqual(pdf_file.read(5), b"%PDF-")

    def test_download_returns_owned_pdf_with_safe_filename(self):
        generated = self.generate_record()
        response = self.client.get(
            reverse(
                "diplome:generation_download",
                kwargs={"generated_diploma_id": generated.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("attachment;", response["Content-Disposition"])
        self.assertIn("diploma_cert_2026_001_ana_serban.pdf", response["Content-Disposition"])
        self.assertEqual(b"".join(response.streaming_content)[:5], b"%PDF-")

    def test_cross_owner_download_returns_404(self):
        generated = generate_single_diploma(
            owner=self.other_user,
            participant_list_id=self.foreign_list.pk,
            participant_id=self.foreign_participant.pk,
            template_id=self.foreign_template.pk,
        )

        response = self.client.get(
            reverse(
                "diplome:generation_download",
                kwargs={"generated_diploma_id": generated.pk},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_source_records_can_be_deleted_without_losing_pdf_history(self):
        generated = self.generate_record()
        stored_name = generated.pdf_file.name

        template_response = self.client.post(
            reverse(
                "diplome:template_delete",
                kwargs={"template_id": self.template.pk},
            )
        )
        list_response = self.client.post(
            reverse(
                "diplome:participant_list_delete",
                kwargs={"participant_list_id": self.participant_list.pk},
            )
        )

        self.assertRedirects(template_response, reverse("diplome:template_list"))
        self.assertRedirects(list_response, reverse("diplome:list_index"))
        generated.refresh_from_db()
        self.assertIsNone(generated.template_id)
        self.assertIsNone(generated.participant_list_id)
        self.assertIsNone(generated.participant_id)
        self.assertEqual(generated.template_name, "Diplomă SSM")
        self.assertEqual(generated.participant_list_name, "Grupa SSM iulie")
        self.assertTrue(generated.pdf_file.storage.exists(stored_name))
        download = self.client.get(
            reverse(
                "diplome:generation_download",
                kwargs={"generated_diploma_id": generated.pk},
            )
        )
        self.assertEqual(download.status_code, 200)
        self.assertEqual(b"".join(download.streaming_content)[:5], b"%PDF-")

    def test_invalid_selection_returns_form_errors(self):
        response = self.client.post(reverse("diplome:generation_create"), {})

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.context["form"].errors)
        self.assertFalse(GeneratedDiploma.objects.exists())

    def test_generation_navigation_is_active_on_preview(self):
        response = self.client.get(self.preview_url())

        self.assertContains(
            response,
            f'href="{reverse("diplome:generation_index")}" class="active font-semibold" aria-current="page"',
        )
```
