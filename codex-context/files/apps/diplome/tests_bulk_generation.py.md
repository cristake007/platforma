# Source snapshot

## `apps/diplome/tests_bulk_generation.py`

Size: 20.1 KB

Redacted secret-like assignments: 2

```python
import tempfile
from io import BytesIO
from unittest.mock import patch
from zipfile import ZipFile

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse

from . import services
from .models import (
    DiplomaGenerationBatch,
    GeneratedDiploma,
    Participant,
    ParticipantList,
)
from .services import (
    create_diploma_template,
    create_generation_batch,
    generate_diploma_batch,
    run_generation_batch,
)


class BulkDiplomaGenerationTests(TestCase):
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
            username="bulk-owner",
            password=<redacted>
        )
        cls.other_user = user_model.objects.create_user(
            username="bulk-other",
            password=<redacted>
        )
        cls.participant_list = ParticipantList.objects.create(
            owner=cls.user,
            name="Grupa vară / 2026",
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
        cls.second_participant = Participant.objects.create(
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
                "name": "Diplomă lot",
                "category": "SSM",
                "description": "",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        cls.foreign_list = ParticipantList.objects.create(
            owner=cls.other_user,
            name="Lista străină",
            source_file_name="foreign.csv",
            participant_count=1,
        )
        cls.foreign_participant = Participant.objects.create(
            owner=cls.other_user,
            participant_list=cls.foreign_list,
            full_name="Participant străin",
            date_of_birth="1985-01-01",
            place_of_birth="Cluj-Napoca",
            certificate_number="OTHER-001",
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

    def bulk_payload(self, **overrides):
        payload = {
            "participant_list": str(self.participant_list.pk),
            "template": str(self.template.pk),
        }
        payload.update(overrides)
        return payload

    def generate_batch(self):
        return generate_diploma_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )

    def test_bulk_and_history_pages_require_login(self):
        batch = self.generate_batch()
        routes = (
            reverse("diplome:generation_index"),
            reverse("diplome:history_index"),
            reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk}),
            reverse("diplome:batch_zip_download", kwargs={"batch_id": batch.pk}),
        )
        self.client.logout()
        for url in routes:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login")))

    def test_user_can_bulk_generate_owned_list_and_template(self):
        response = self.client.post(
            reverse("diplome:generation_bulk_create"),
            self.bulk_payload(),
        )

        batch = DiplomaGenerationBatch.objects.get()
        generated = GeneratedDiploma.objects.filter(batch=batch)
        self.assertRedirects(
            response,
            reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk}),
        )
        self.assertEqual(batch.status, DiplomaGenerationBatch.Status.COMPLETED)
        self.assertEqual(batch.total_count, 2)
        self.assertEqual(batch.success_count, 2)
        self.assertEqual(batch.failed_count, 0)
        self.assertEqual(generated.count(), 2)
        for diploma in generated:
            self.assertTrue(diploma.pdf_file.storage.exists(diploma.pdf_file.name))
            self.assertTrue(diploma.pdf_file.name.startswith(f"{batch.output_folder}/"))

    def test_one_participant_failure_completes_with_errors(self):
        original_renderer = services.render_diploma_pdf

        def render_with_one_failure(*, template, participant):
            if participant.pk == self.second_participant.pk:
                raise RuntimeError("renderer details must not reach the UI")
            return original_renderer(template=template, participant=participant)

        with patch(
            "apps.diplome.services.render_diploma_pdf",
            side_effect=render_with_one_failure,
        ):
            batch = self.generate_batch()

        self.assertEqual(
            batch.status,
            DiplomaGenerationBatch.Status.COMPLETED_WITH_ERRORS,
        )
        self.assertEqual(batch.success_count, 1)
        self.assertEqual(batch.failed_count, 1)
        self.assertEqual(GeneratedDiploma.objects.filter(batch=batch).count(), 1)
        self.assertEqual(batch.error_summary[0]["participant_name"], "Ion Ionescu")
        self.assertNotIn("renderer details", str(batch.error_summary))

    def test_batch_fails_when_no_pdf_is_generated(self):
        with patch(
            "apps.diplome.services.render_diploma_pdf",
            side_effect=RuntimeError("renderer unavailable"),
        ):
            batch = self.generate_batch()

        self.assertEqual(batch.status, DiplomaGenerationBatch.Status.FAILED)
        self.assertEqual(batch.success_count, 0)
        self.assertEqual(batch.failed_count, 2)
        self.assertFalse(GeneratedDiploma.objects.filter(batch=batch).exists())

    def test_batch_startup_failure_is_recorded_as_failed(self):
        with patch(
            "apps.diplome.services.run_generation_batch",
            side_effect=RuntimeError("runner unavailable"),
        ):
            with self.assertRaises(RuntimeError):
                self.generate_batch()

        batch = DiplomaGenerationBatch.objects.get()
        self.assertEqual(batch.status, DiplomaGenerationBatch.Status.FAILED)
        self.assertEqual(batch.failed_count, batch.total_count)
        self.assertEqual(
            batch.error_summary,
            [{"message": "Generarea lotului nu a putut porni."}],
        )

    def test_empty_participant_list_is_rejected(self):
        empty_list = ParticipantList.objects.create(
            owner=self.user,
            name="Listă goală",
            source_file_name="empty.csv",
            participant_count=8,
        )
        response = self.client.post(
            reverse("diplome:generation_bulk_create"),
            self.bulk_payload(participant_list=str(empty_list.pk)),
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Lista selectată nu conține participanți.", status_code=400)
        self.assertFalse(DiplomaGenerationBatch.objects.exists())

    def test_cross_owner_list_and_template_cannot_be_used(self):
        cases = (
            {"participant_list": str(self.foreign_list.pk)},
            {"template": str(self.foreign_template.pk)},
        )
        for override in cases:
            with self.subTest(override=override):
                response = self.client.post(
                    reverse("diplome:generation_bulk_create"),
                    self.bulk_payload(**override),
                )
                self.assertEqual(response.status_code, 400)
        self.assertFalse(DiplomaGenerationBatch.objects.exists())

    def test_cross_owner_batch_detail_and_zip_return_404(self):
        foreign_batch = generate_diploma_batch(
            self.other_user,
            self.foreign_list.pk,
            self.foreign_template.pk,
        )

        detail = self.client.get(
            reverse("diplome:batch_detail", kwargs={"batch_id": foreign_batch.pk})
        )
        archive = self.client.get(
            reverse(
                "diplome:batch_zip_download",
                kwargs={"batch_id": foreign_batch.pk},
            )
        )

        self.assertEqual(detail.status_code, 404)
        self.assertEqual(archive.status_code, 404)

    def test_zip_contains_only_pdfs_from_requested_batch(self):
        batch = self.generate_batch()
        other_batch = self.generate_batch()
        response = self.client.get(
            reverse("diplome:batch_zip_download", kwargs={"batch_id": batch.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/zip")
        self.assertIn("diplome_grupa_vara_2026_", response["Content-Disposition"])
        with ZipFile(BytesIO(response.content)) as archive:
            names = archive.namelist()
        self.assertEqual(len(names), 2)
        self.assertTrue(all(name.endswith(".pdf") for name in names))
        requested_names = {
            diploma.pdf_file.name.rsplit("/", 1)[-1]
            for diploma in GeneratedDiploma.objects.filter(batch=batch)
        }
        other_names = {
            diploma.pdf_file.name.rsplit("/", 1)[-1]
            for diploma in GeneratedDiploma.objects.filter(batch=other_batch)
        }
        self.assertSetEqual(set(names), requested_names)
        self.assertSetEqual(requested_names, other_names)

    def test_history_and_detail_are_owner_scoped(self):
        owned_batch = self.generate_batch()
        foreign_batch = generate_diploma_batch(
            self.other_user,
            self.foreign_list.pk,
            self.foreign_template.pk,
        )

        history = self.client.get(reverse("diplome:history_index"))
        detail = self.client.get(
            reverse("diplome:batch_detail", kwargs={"batch_id": owned_batch.pk})
        )

        self.assertContains(history, self.participant_list.name)
        self.assertNotContains(history, self.foreign_list.name)
        self.assertContains(detail, self.participant.full_name)
        self.assertContains(detail, self.second_participant.full_name)
        self.assertNotContains(detail, self.foreign_participant.full_name)
        self.assertFalse(
            detail.context["generated_diplomas"].filter(batch=foreign_batch).exists()
        )

    def test_history_exposes_accessible_detail_and_zip_icon_actions(self):
        batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )
        batch.success_count = 1
        batch.total_count = 1
        batch.save(update_fields=["success_count", "total_count"])
        generated = GeneratedDiploma.objects.create(
            owner=self.user,
            participant_list=self.participant_list,
            participant=self.participant,
            template=self.template,
            batch=batch,
            certificate_number=self.participant.certificate_number,
            participant_name=self.participant.full_name,
            pdf_file=ContentFile(b"%PDF-1.4", name="diploma-test.pdf"),
        )

        history = self.client.get(reverse("diplome:history_index"))
        detail = self.client.get(
            reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk})
        )

        self.assertContains(history, 'class="table table-xs"')
        self.assertContains(
            history,
            f'href="{reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk})}"',
        )
        self.assertContains(history, 'aria-label="Vezi detaliile lotului"')
        self.assertContains(history, 'class="text-right">Acțiuni</th>')
        self.assertContains(
            history,
            f'action="{reverse("diplome:batch_resume", kwargs={"batch_id": batch.pk})}"',
        )
        self.assertContains(history, 'aria-label="Reia generarea lotului"')
        self.assertContains(history, "text-primary hover:bg-primary/10")
        self.assertContains(
            history,
            f'href="{reverse("diplome:batch_zip_download", kwargs={"batch_id": batch.pk})}"',
        )
        self.assertContains(history, 'aria-label="Descarcă lotul ca arhivă ZIP"')
        self.assertContains(history, "text-success hover:bg-success/10")
        self.assertNotContains(history, ">Detalii</a>")
        self.assertContains(detail, 'class="table table-xs"')
        self.assertContains(detail, 'class="text-right">Acțiuni</th>')
        self.assertContains(
            detail,
            f'href="{reverse("diplome:generation_download", kwargs={"generated_diploma_id": generated.pk})}"',
        )
        self.assertContains(detail, 'aria-label="Descarcă diploma PDF"')
        self.assertContains(detail, "text-success hover:bg-success/10")
        self.assertNotContains(detail, ">Descarcă PDF</a>")

    def test_history_htmx_returns_partial_panel(self):
        owned_batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )
        foreign_batch = create_generation_batch(
            self.other_user,
            self.foreign_list.pk,
            self.foreign_template.pk,
        )

        response = self.client.get(
            reverse("diplome:history_index"),
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/includes/history_panel.html")
        self.assertContains(response, 'id="history-panel"')
        self.assertContains(response, owned_batch.participant_list_display_name)
        self.assertNotContains(response, foreign_batch.participant_list_display_name)
        self.assertNotContains(response, "<title>")

    def test_pending_batch_resume_from_history_htmx_refreshes_history_panel(self):
        batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )

        response = self.client.post(
            reverse("diplome:batch_resume", kwargs={"batch_id": batch.pk}),
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET="history-panel",
        )

        batch.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/includes/history_panel.html")
        self.assertEqual(batch.status, DiplomaGenerationBatch.Status.COMPLETED)
        self.assertContains(response, "Lot finalizat")
        self.assertContains(response, batch.participant_list_display_name)
        self.assertContains(response, batch.get_status_display())
        self.assertNotContains(response, "<title>")

    def test_batch_detail_htmx_and_resume_refresh_detail_panel(self):
        batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )
        detail_url = reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk})

        detail = self.client.get(detail_url, HTTP_HX_REQUEST="true")
        self.assertEqual(detail.status_code, 200)
        self.assertTemplateUsed(detail, "diplome/includes/batch_detail_panel.html")
        self.assertContains(detail, 'id="batch-detail-panel"')
        self.assertContains(detail, "Reia generarea")
        self.assertNotContains(detail, "<title>")

        response = self.client.post(
            reverse("diplome:batch_resume", kwargs={"batch_id": batch.pk}),
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET="batch-detail-panel",
        )

        batch.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/includes/batch_detail_panel.html")
        self.assertEqual(batch.status, DiplomaGenerationBatch.Status.COMPLETED)
        self.assertContains(response, "Lot finalizat")
        self.assertContains(response, batch.get_status_display())
        self.assertNotContains(response, "Reia generarea")
        self.assertContains(response, reverse("diplome:batch_zip_download", kwargs={"batch_id": batch.pk}))

    def test_pending_batch_can_be_resumed(self):
        batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )

        response = self.client.post(
            reverse("diplome:batch_resume", kwargs={"batch_id": batch.pk})
        )

        self.assertRedirects(
            response,
            reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk}),
        )
        batch.refresh_from_db()
        self.assertEqual(batch.status, DiplomaGenerationBatch.Status.COMPLETED)
        self.assertEqual(batch.success_count, 2)
        self.assertEqual(batch.failed_count, 0)

    def test_batch_resume_is_post_only_and_owner_scoped(self):
        owned_batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )
        foreign_batch = create_generation_batch(
            self.other_user,
            self.foreign_list.pk,
            self.foreign_template.pk,
        )

        get_response = self.client.get(
            reverse("diplome:batch_resume", kwargs={"batch_id": owned_batch.pk})
        )
        foreign_response = self.client.post(
            reverse("diplome:batch_resume", kwargs={"batch_id": foreign_batch.pk})
        )

        self.assertEqual(get_response.status_code, 405)
        self.assertEqual(foreign_response.status_code, 404)
        foreign_batch.refresh_from_db()
        self.assertEqual(foreign_batch.status, DiplomaGenerationBatch.Status.PENDING)

    def test_individual_download_still_works_for_batch_pdf(self):
        batch = self.generate_batch()
        generated = GeneratedDiploma.objects.filter(batch=batch).first()
        response = self.client.get(
            reverse(
                "diplome:generation_download",
                kwargs={"generated_diploma_id": generated.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertEqual(b"".join(response.streaming_content)[:5], b"%PDF-")

    def test_run_generation_batch_needs_only_the_batch_id(self):
        batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )

        result = run_generation_batch(batch.pk)

        self.assertEqual(result.status, DiplomaGenerationBatch.Status.COMPLETED)
        self.assertEqual(result.success_count, 2)

    def test_navigation_active_state_for_generation_and_history(self):
        generation = self.client.get(reverse("diplome:generation_index"))
        batch = self.generate_batch()
        history_detail = self.client.get(
            reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk})
        )

        self.assertContains(
            generation,
            f'href="{reverse("diplome:generation_index")}" class="transition-none active font-semibold" aria-current="page"',
        )
        self.assertContains(
            history_detail,
            f'href="{reverse("diplome:history_index")}" class="transition-none active font-semibold" aria-current="page"',
        )
```
