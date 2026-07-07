# Source snapshot

## `apps/planificator/tests_xml_export.py`

Size: 9.3 KB

Redacted secret-like assignments: 1

```python
import xml.etree.ElementTree as ET

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from .file_handlers import create_excel_export
from .models import AppSetting
from .xml_export import create_xml_export, read_xml_schedule


class XmlExportContractTests(SimpleTestCase):
    def test_xml_structure_ids_dates_constants_and_order_are_stable(self):
        xml_text = create_xml_export(
            [
                {"course_name": "Course A", "date_range": "5.01.2026", "permalink": "/a"},
                {
                    "course_name": "Course B",
                    "date_range": "30.01-2.02.2026",
                    "permalink": "/b",
                },
                {
                    "course_name": "Course A",
                    "date_range": "12-13.02.2026",
                    "permalink": "/a",
                },
            ],
            2026,
            start_post_id=31000,
        )

        root = ET.fromstring(xml_text)
        items = root.findall("item")
        self.assertEqual([item.findtext("title") for item in items], ["Course A", "Course A", "Course B"])
        self.assertEqual([item.findtext("ID") for item in items], ["31000", "31001", "31002"])
        self.assertEqual(items[0].findtext("post/post_author"), "5")
        self.assertEqual(items[0].findtext("post/post_status"), "draft")
        self.assertEqual(items[0].findtext("meta/mec_more_info_title"), "perioada 1")
        self.assertEqual(items[1].findtext("meta/mec_more_info_title"), "perioada 2")
        self.assertEqual(items[0].findtext("meta/mec_start_date"), "2026-01-05")
        self.assertEqual(items[1].findtext("meta/mec_end_date"), "2026-02-13")
        self.assertEqual(items[2].findtext("meta/mec_start_date"), "2026-01-30")
        self.assertEqual(items[2].findtext("meta/mec_end_date"), "2026-02-02")
        self.assertEqual(items[0].findtext("meta/mec_start_day_seconds"), "28800")
        self.assertEqual(items[0].findtext("meta/mec_end_day_seconds"), "64800")
        self.assertEqual(items[0].findtext("mec/post_id"), "31000")
        self.assertEqual(items[0].findtext("time/start"), "All Day")

    def test_default_id_and_unsupported_date_contract(self):
        xml_text = create_xml_export(
            [{"course_name": "Course", "date_range": "01.01.2026", "permalink": ""}],
            2026,
        )
        self.assertEqual(ET.fromstring(xml_text).findtext("item/ID"), "20000")

        with self.assertRaisesRegex(ValueError, "Unsupported date format"):
            create_xml_export(
                [{"course_name": "Course", "date_range": "January 1", "permalink": ""}],
                2026,
            )

    def test_legacy_and_current_month_headers_keep_source_order(self):
        schedule = read_xml_schedule(
            (
                "Title,Permalink,February,Luna 1,Ianuarie\n"
                "Course A,/a,12-13.02.2026,5.03.2026,5.01.2026\n"
            ).encode("utf-8"),
            ".csv",
        )

        self.assertEqual(
            [event["date_range"] for event in schedule],
            ["12-13.02.2026", "5.03.2026", "5.01.2026"],
        )


class XmlExportViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="xml-user",
            password=<redacted>
        )
        cls.permission = Permission.objects.get(codename="use_xml_export")
        cls.user.user_permissions.add(cls.permission)

    def setUp(self):
        self.client.force_login(self.user)

    def test_page_uses_app_template_navigation_and_separate_permission(self):
        response = self.client.get(reverse("planificator:xml_formatter"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "planificator/xml_formatter.html")
        self.assertContains(response, "Convertor XML")
        self.assertContains(response, reverse("planificator:xml_export"))
        self.assertContains(response, 'name="start_post_id"')
        self.assertContains(response, reverse("planificator:xml_export"))
        self.assertContains(response, reverse("planificator:xml_formatter"))
        self.assertContains(response, 'class="transition-none active font-semibold"')
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, 'hx-boost="false"')
        self.assertContains(response, "x-data=")

    def test_export_uses_submitted_start_id_and_legacy_xml_download_contract(self):
        AppSetting.objects.create(
            scope="schedule_generator",
            user=self.user,
            payload={"xml_start_post_id": 31000},
        )
        upload = SimpleUploadedFile(
            "program.csv",
            b"Title,Permalink,January\nCourse A,/course-a,5.01.2026\n",
            content_type="text/csv",
        )

        response = self.client.post(
            reverse("planificator:xml_export"),
            {"input_file": upload, "start_post_id": 32000},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertEqual(
            response["Content-Disposition"],
            f'attachment; filename="formatted_courses_{timezone.localdate().year}.xml"',
        )
        root = ET.fromstring(response.content)
        self.assertEqual(root.findtext("item/ID"), "32000")
        self.assertEqual(root.findtext("item/meta/mec_read_more"), "/course-a")

    def test_htmx_marked_export_still_returns_xml_attachment(self):
        upload = SimpleUploadedFile(
            "program.csv",
            b"Title,Permalink,January\nCourse A,/course-a,5.01.2026\n",
            content_type="text/csv",
        )

        response = self.client.post(
            reverse("planificator:xml_export"),
            {"input_file": upload, "start_post_id": 32000},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertIn("attachment;", response["Content-Disposition"])
        self.assertNotIn("text/html", response["Content-Type"])

    def test_export_accepts_current_romanian_schedule_workbook(self):
        workbook = create_excel_export(
            [
                {
                    "Title": "Curs curent",
                    "Permalink": "https://example.com/curs",
                    "Durata Curs": "2 zile",
                    "investitie": "1000",
                    "date_range": "10-11.04.2026",
                    "month": 4,
                    "source_row": 2,
                    "original_order": 0,
                }
            ],
            2026,
        )
        upload = SimpleUploadedFile(
            "program.xlsx",
            workbook,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        response = self.client.post(
            reverse("planificator:xml_export"),
            {"input_file": upload, "start_post_id": 20000},
        )

        self.assertEqual(response.status_code, 200)
        root = ET.fromstring(response.content)
        self.assertEqual(root.findtext("item/title"), "Curs curent")
        self.assertEqual(root.findtext("item/meta/mec_start_date"), "2026-04-10")
        self.assertEqual(root.findtext("item/meta/mec_end_date"), "2026-04-11")

    def test_invalid_files_return_stable_json_errors(self):
        missing_columns = SimpleUploadedFile(
            "program.csv",
            b"Title,January\nCourse A,5.01.2026\n",
            content_type="text/csv",
        )
        response = self.client.post(
            reverse("planificator:xml_export"),
            {"input_file": missing_columns, "start_post_id": 20000},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json()["error"], "Missing required columns: Permalink")

        invalid_date = SimpleUploadedFile(
            "program.csv",
            b"Title,Permalink,January\nCourse A,/a,January 1\n",
            content_type="text/csv",
        )
        response = self.client.post(
            reverse("planificator:xml_export"),
            {"input_file": invalid_date, "start_post_id": 20000},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Unable to read the uploaded schedule or create XML.",
        )

    def test_authentication_permission_and_method_boundaries(self):
        page_url = reverse("planificator:xml_formatter")
        self.client.logout()
        response = self.client.get(page_url)
        self.assertRedirects(response, f"{reverse('login')}?next={page_url}")

        other = get_user_model().objects.create_user(username="xml-other")
        self.client.force_login(other)
        self.assertEqual(self.client.get(page_url).status_code, 403)

        self.client.force_login(self.user)
        self.assertEqual(self.client.post(page_url).status_code, 405)
        self.assertEqual(self.client.get(reverse("planificator:xml_export")).status_code, 405)
```
