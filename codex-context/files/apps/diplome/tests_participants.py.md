# apps/diplome/tests_participants.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/diplome/tests_participants.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `test`
- Size: 20746 bytes
- Source SHA-256: `f885bce7d403803d39a07d56ed1e886c226c4680e9019673a268668508e93da4`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from datetime import datetime, timedelta
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from openpyxl import Workbook

from .models import (
    DiplomaGenerationBatch,
    Participant,
    ParticipantImportDraft,
    ParticipantList,
)
from .services import (
    PARTICIPANT_DATE_ERROR,
    create_diploma_template,
    parse_participant_upload,
)


def csv_upload(*rows, name="participanti.csv"):
    content = "\n".join(
        (
            "Nume complet;Data nașterii;Locul nașterii;Număr certificat",
            *rows,
        )
    )
    return SimpleUploadedFile(name, content.encode("utf-8"), content_type="text/csv")


def xlsx_upload(*, number_format="DD.MM.YYYY", date_value=None):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(
        ["Nume complet", "Data nașterii", "Locul nașterii", "Număr certificat"]
    )
    worksheet.append(
        [
            "Ana Popescu",
            date_value if date_value is not None else datetime(1990, 4, 12),
            "Brașov",
            "CERT-001",
        ]
    )
    worksheet["B2"].number_format = number_format
    buffer = BytesIO()
    workbook.save(buffer)
    return SimpleUploadedFile(
        "participanti.xlsx",
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def multi_sheet_xlsx_upload():
    workbook = Workbook()
    notes = workbook.active
    notes.title = "Instrucțiuni"
    notes.append(["Această foaie nu conține participanți."])

    headers = [
        "Nume complet",
        "Data nașterii",
        "Locul nașterii",
        "Număr certificat",
    ]
    first = workbook.create_sheet("Grupa 1")
    first.append(headers)
    first.append(["Ana Popescu", datetime(1990, 4, 12), "Brașov", "CERT-001"])
    first["B2"].number_format = "DD.MM.YYYY"

    second = workbook.create_sheet("Grupa 2")
    second.append(headers)
    second.append(["Ion Ionescu", datetime(1991, 5, 13), "Sibiu", "CERT-002"])
    second["B2"].number_format = "DD.MM.YYYY"

    buffer = BytesIO()
    workbook.save(buffer)
    return SimpleUploadedFile(
        "participanti-mai-multe-foi.xlsx",
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def mapping_payload():
    return {
        "column_0": "full_name",
        "column_1": "date_of_birth",
        "column_2": "place_of_birth",
        "column_3": "certificate_number",
    }


class ParticipantImportTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="participant-owner",
            password="test-password",
        )
        cls.other_user = get_user_model().objects.create_user(
            username="participant-other",
            password="test-password",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_participant_pages_require_login(self):
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="Lista permanentă",
            source_file_name="participanti.csv",
        )
        draft = ParticipantImportDraft.objects.create(
            owner=self.user,
            list_name="Import",
            source_file_name="participanti.csv",
            mapping_confirmed=True,
            valid_rows_json=[],
            invalid_rows_json=[],
            warnings_json=[],
            expires_at=timezone.now() + timedelta(hours=1),
        )
        routes = (
            reverse("diplome:list_index"),
            reverse("diplome:participant_import"),
            reverse(
                "diplome:participant_import_sheet", kwargs={"draft_id": draft.pk}
            ),
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
            reverse("diplome:participant_import_preview", kwargs={"draft_id": draft.pk}),
            reverse(
                "diplome:participant_list_detail",
                kwargs={"participant_list_id": participant_list.pk},
            ),
        )
        self.client.logout()
        for url in routes:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login")))

    def test_csv_accepts_only_strict_dd_mm_yyyy_dates(self):
        valid = parse_participant_upload(
            upload=csv_upload("Ana Popescu;12.04.1990;Brașov;CERT-001")
        )
        self.assertEqual(valid["valid_rows"][0]["date_of_birth"], "12.04.1990")

        invalid_dates = ("12/04/1990", "1990-04-12", "1.4.1990", "31.02.1990")
        for value in invalid_dates:
            with self.subTest(value=value):
                parsed = parse_participant_upload(
                    upload=csv_upload(f"Ana Popescu;{value};Brașov;CERT-001")
                )
                self.assertEqual(parsed["valid_rows"], [])
                self.assertIn(PARTICIPANT_DATE_ERROR, parsed["invalid_rows"][0]["errors"])

    def test_excel_date_cell_is_normalized_independently_of_locale_format(self):
        accepted_formats = (
            "DD.MM.YYYY",
            "dd.mm.yyyy;@",
            '[$-ro-RO]dd"."mm"."yyyy',
            r"dd\.mm\.yyyy",
            "YYYY-MM-DD",
            "mm-dd-yy",
        )
        for number_format in accepted_formats:
            with self.subTest(number_format=number_format):
                accepted = parse_participant_upload(
                    upload=xlsx_upload(number_format=number_format)
                )
                self.assertEqual(
                    accepted["valid_rows"][0]["date_of_birth"],
                    "12.04.1990",
                )

    def test_excel_text_date_still_requires_dd_mm_yyyy(self):
        rejected = parse_participant_upload(
            upload=xlsx_upload(date_value="1990-04-12", number_format="@")
        )

        self.assertEqual(rejected["valid_rows"], [])
        self.assertIn(PARTICIPANT_DATE_ERROR, rejected["invalid_rows"][0]["errors"])

    def test_xlsx_import_uses_only_the_selected_visible_sheet(self):
        parsed = parse_participant_upload(
            upload=multi_sheet_xlsx_upload(),
            worksheet_name="Grupa 2",
        )

        self.assertEqual(
            [row["full_name"] for row in parsed["valid_rows"]],
            ["Ion Ionescu"],
        )
        self.assertEqual(parsed["valid_rows"][0]["source_row"], 2)
        self.assertEqual(parsed["invalid_rows"], [])

    def test_multi_sheet_xlsx_prompts_for_a_sheet_before_column_mapping(self):
        response = self.client.post(
            reverse("diplome:participant_import"),
            {
                "list_name": "Grupe separate",
                "first_row_has_headers": "on",
                "source_file": multi_sheet_xlsx_upload(),
            },
        )

        draft = ParticipantImportDraft.objects.get()
        self.assertRedirects(
            response,
            reverse("diplome:participant_import_sheet", kwargs={"draft_id": draft.pk}),
        )
        self.assertEqual(
            [sheet["name"] for sheet in draft.source_sheets_json],
            ["Grupa 1", "Grupa 2"],
        )
        self.assertEqual(draft.source_columns_json, [])
        self.assertEqual(draft.source_rows_json, [])

        selection_page = self.client.get(response.url)
        self.assertContains(selection_page, "Grupa 1")
        self.assertContains(selection_page, "Grupa 2")
        self.assertNotContains(selection_page, "Instrucțiuni")

        selection_response = self.client.post(response.url, {"sheet_index": "1"})
        draft.refresh_from_db()
        self.assertRedirects(
            selection_response,
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
        )
        self.assertEqual(len(draft.source_rows_json), 1)
        self.assertEqual(draft.source_rows_json[0]["values"][0], "Ion Ionescu")

    def test_missing_list_name_uses_application_validation_message(self):
        response = self.client.post(
            reverse("diplome:participant_import"),
            {"source_file": xlsx_upload(), "first_row_has_headers": "on"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Numele listei este obligatoriu.", count=2)
        self.assertContains(response, "data-participant-import-toast")
        self.assertFalse(ParticipantImportDraft.objects.exists())

    def test_upload_creates_preview_draft_without_creating_a_list(self):
        response = self.client.post(
            reverse("diplome:participant_import"),
            {
                "list_name": "  Curs   SSM  ",
                "description": "Grupa iulie",
                "course_name": "Inspector SSM",
                "first_row_has_headers": "on",
                "source_file": csv_upload(
                    "Ana Popescu;12.04.1990;Brașov;CERT-001",
                    "Ion Ionescu;1991-05-13;Sibiu;CERT-002",
                ),
            },
        )

        draft = ParticipantImportDraft.objects.get()
        self.assertRedirects(
            response,
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
        )
        self.assertEqual(draft.owner, self.user)
        self.assertEqual(draft.list_name, "Curs SSM")
        self.assertEqual(len(draft.source_columns_json), 4)
        self.assertEqual(len(draft.source_rows_json), 2)
        self.assertEqual(draft.valid_rows_json, [])
        self.assertEqual(draft.invalid_rows_json, [])
        self.assertFalse(ParticipantList.objects.exists())

        mapping_response = self.client.post(
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
            mapping_payload(),
        )
        draft.refresh_from_db()
        self.assertRedirects(
            mapping_response,
            reverse("diplome:participant_import_preview", kwargs={"draft_id": draft.pk}),
        )
        self.assertEqual(len(draft.valid_rows_json), 1)
        self.assertEqual(len(draft.invalid_rows_json), 1)
        self.assertFalse(ParticipantList.objects.exists())

    def test_confirm_import_creates_permanent_owned_list_and_participants(self):
        upload_response = self.client.post(
            reverse("diplome:participant_import"),
            {
                "list_name": "Grupa iulie",
                "description": "Participanți validați",
                "course_name": "Inspector SSM",
                "first_row_has_headers": "on",
                "source_file": csv_upload(
                    "Ana Popescu;12.04.1990;Brașov;CERT-001",
                    "Ion Ionescu;13.05.1991;Sibiu;CERT-002",
                ),
            },
        )
        draft = ParticipantImportDraft.objects.get()
        self.client.post(
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
            mapping_payload(),
        )

        response = self.client.post(
            reverse("diplome:participant_import_confirm", kwargs={"draft_id": draft.pk})
        )

        participant_list = ParticipantList.objects.get()
        self.assertRedirects(
            response,
            reverse(
                "diplome:participant_list_detail",
                kwargs={"participant_list_id": participant_list.pk},
            ),
        )
        self.assertEqual(participant_list.owner, self.user)
        self.assertEqual(participant_list.participant_count, 2)
        self.assertEqual(participant_list.course_name, "Inspector SSM")
        self.assertEqual(Participant.objects.filter(owner=self.user).count(), 2)
        self.assertFalse(ParticipantImportDraft.objects.exists())

    def test_custom_headers_are_discovered_and_mapped_by_the_user(self):
        upload = SimpleUploadedFile(
            "custom.csv",
            (
                "Persoană;Născut la;Localitate;Serie\n"
                "Ana Popescu;12.04.1990;Brașov;CERT-001"
            ).encode("utf-8"),
            content_type="text/csv",
        )
        response = self.client.post(
            reverse("diplome:participant_import"),
            {
                "list_name": "Antet personalizat",
                "first_row_has_headers": "on",
                "source_file": upload,
            },
        )
        draft = ParticipantImportDraft.objects.get()

        self.assertRedirects(
            response,
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
        )
        self.assertEqual(
            [column["label"] for column in draft.source_columns_json],
            ["Persoană", "Născut la", "Localitate", "Serie"],
        )
        self.assertEqual(draft.column_mapping_json, {})

        mapping_response = self.client.post(
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
            mapping_payload(),
        )
        draft.refresh_from_db()

        self.assertRedirects(
            mapping_response,
            reverse("diplome:participant_import_preview", kwargs={"draft_id": draft.pk}),
        )
        self.assertTrue(draft.mapping_confirmed)
        self.assertEqual(draft.valid_rows_json[0]["full_name"], "Ana Popescu")

    def test_headerless_file_generates_columns_without_losing_first_participant(self):
        upload = SimpleUploadedFile(
            "fara-antet.csv",
            (
                "Ana Popescu;12.04.1990;Brașov;CERT-001\n"
                "Ion Ionescu;13.05.1991;Sibiu;CERT-002"
            ).encode("utf-8"),
            content_type="text/csv",
        )
        self.client.post(
            reverse("diplome:participant_import"),
            {"list_name": "Fără antet", "source_file": upload},
        )
        draft = ParticipantImportDraft.objects.get()

        self.assertEqual(
            [column["label"] for column in draft.source_columns_json],
            ["Coloana 1", "Coloana 2", "Coloana 3", "Coloana 4"],
        )
        self.assertEqual(len(draft.source_rows_json), 2)
        self.assertEqual(draft.source_rows_json[0]["source_row"], 1)

        self.client.post(
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
            mapping_payload(),
        )
        draft.refresh_from_db()
        self.assertEqual(len(draft.valid_rows_json), 2)
        self.assertEqual(draft.valid_rows_json[0]["full_name"], "Ana Popescu")

    def test_confirm_refuses_draft_without_valid_rows(self):
        draft = ParticipantImportDraft.objects.create(
            owner=self.user,
            list_name="Import invalid",
            source_file_name="participanti.csv",
            mapping_confirmed=True,
            valid_rows_json=[],
            invalid_rows_json=[],
            warnings_json=[],
            expires_at=timezone.now() + timedelta(hours=1),
        )

        response = self.client.post(
            reverse("diplome:participant_import_confirm", kwargs={"draft_id": draft.pk})
        )

        self.assertRedirects(
            response,
            reverse("diplome:participant_import_preview", kwargs={"draft_id": draft.pk}),
        )
        self.assertFalse(ParticipantList.objects.exists())

    def test_list_and_detail_are_owner_scoped(self):
        own = ParticipantList.objects.create(
            owner=self.user,
            name="Lista proprie",
            source_file_name="own.csv",
        )
        foreign = ParticipantList.objects.create(
            owner=self.other_user,
            name="Lista străină",
            source_file_name="foreign.csv",
        )

        response = self.client.get(reverse("diplome:list_index"))

        self.assertContains(response, own.name)
        self.assertNotContains(response, foreign.name)
        self.assertEqual(
            self.client.get(
                reverse(
                    "diplome:participant_list_detail",
                    kwargs={"participant_list_id": foreign.pk},
                )
            ).status_code,
            404,
        )

    def test_confirmed_list_does_not_expire(self):
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="Lista veche",
            source_file_name="veche.csv",
        )
        ParticipantList.objects.filter(pk=participant_list.pk).update(
            created_at=timezone.now() - timedelta(days=3650),
            updated_at=timezone.now() - timedelta(days=3650),
        )

        list_response = self.client.get(reverse("diplome:list_index"))
        detail_response = self.client.get(
            reverse(
                "diplome:participant_list_detail",
                kwargs={"participant_list_id": participant_list.pk},
            )
        )

        self.assertContains(list_response, "Lista veche")
        self.assertEqual(detail_response.status_code, 200)

    def test_delete_is_post_only_owner_scoped_and_cascades(self):
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="De șters",
            source_file_name="delete.csv",
            participant_count=1,
        )
        Participant.objects.create(
            owner=self.user,
            participant_list=participant_list,
            full_name="Ana Popescu",
            date_of_birth=datetime(1990, 4, 12).date(),
            place_of_birth="Brașov",
            certificate_number="CERT-001",
            source_row=2,
        )
        url = reverse(
            "diplome:participant_list_delete",
            kwargs={"participant_list_id": participant_list.pk},
        )

        self.assertEqual(self.client.get(url).status_code, 405)
        response = self.client.post(url)

        self.assertRedirects(response, reverse("diplome:list_index"))
        self.assertFalse(ParticipantList.objects.exists())
        self.assertFalse(Participant.objects.exists())

    def test_used_list_delete_preserves_batch_history_snapshot(self):
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="Lista folosită",
            source_file_name="istoric.csv",
        )
        template = create_diploma_template(
            owner=self.user,
            data={
                "name": "Template istoric",
                "category": "General",
                "description": "",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        DiplomaGenerationBatch.objects.create(
            owner=self.user,
            participant_list=participant_list,
            template=template,
            participant_list_name=participant_list.name,
            template_name=template.name,
            output_folder=f"diplomas/{self.user.pk}/batch-list-test",
        )

        response = self.client.post(
            reverse(
                "diplome:participant_list_delete",
                kwargs={"participant_list_id": participant_list.pk},
            ),
            follow=True,
        )

        self.assertRedirects(response, reverse("diplome:list_index"))
        self.assertContains(response, "Lista de participanți a fost ștearsă.")
        self.assertFalse(ParticipantList.objects.filter(pk=participant_list.pk).exists())
        batch = DiplomaGenerationBatch.objects.get()
        self.assertIsNone(batch.participant_list_id)
        self.assertEqual(batch.participant_list_display_name, "Lista folosită")

    def test_expired_and_foreign_drafts_are_not_viewable(self):
        for owner, expires_at in (
            (self.other_user, timezone.now() + timedelta(hours=1)),
            (self.user, timezone.now() - timedelta(seconds=1)),
        ):
            draft = ParticipantImportDraft.objects.create(
                owner=owner,
                list_name="Draft privat",
                source_file_name="draft.csv",
                valid_rows_json=[],
                invalid_rows_json=[],
                warnings_json=[],
                expires_at=expires_at,
            )
            with self.subTest(owner=owner, expires_at=expires_at):
                response = self.client.get(
                    reverse(
                        "diplome:participant_import_preview",
                        kwargs={"draft_id": draft.pk},
                    )
                )
                self.assertEqual(response.status_code, 404)
```
