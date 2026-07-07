# Source snapshot

## `apps/planificator/tests_word_converter.py`

Size: 14.4 KB

```python
import base64
import io
import json
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse
from docx import Document
from openpyxl import Workbook

from .word_matching import (
    apply_word_matches,
    build_word_course_rows,
    build_word_match_preview,
    confident_match_from_scores,
    normalize_title,
    read_schedule_rows,
    score_schedule_matches,
)


def word_document_bytes(rows=None):
    rows = rows or [("Curs exact", "2 zile", "100", "", "", "")]
    document = Document()
    table = document.add_table(rows=len(rows), cols=6)
    for table_row, values in zip(table.rows, rows):
        for cell, value in zip(table_row.cells, values):
            cell.text = value
    output = io.BytesIO()
    document.save(output)
    return output.getvalue()


def schedule_row(row_index, title, dates=None):
    return {
        "row_index": row_index,
        "title": title,
        "normalized_title": normalize_title(title),
        "dates": dates or ["", "", ""],
    }


def word_upload(content=None):
    return SimpleUploadedFile(
        "planificare.docx",
        content or word_document_bytes(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


def schedule_upload(content=None, name="program.csv"):
    return SimpleUploadedFile(
        name,
        content
        or b"Title,Ianuarie,Februarie,Martie\nCurs exact,05-06.01.2026,02-03.02.2026,02-03.03.2026\n",
        content_type="text/csv",
    )


class WordScheduleParsingTests(SimpleTestCase):
    def test_csv_accepts_english_months_and_keeps_first_three_non_empty_dates(self):
        rows = read_schedule_rows(
            b"Title,January,February,March,April\nCourse,05.01.2026,,02.03.2026,06.04.2026\n",
            ".csv",
        )

        self.assertEqual(rows[0]["title"], "Course")
        self.assertEqual(
            rows[0]["dates"],
            ["05.01.2026", "02.03.2026", "06.04.2026"],
        )

    def test_xlsx_accepts_month_headers_emitted_by_current_generator(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["Title", "Ianuarie", "Februarie", "Martie"])
        sheet.append(["Curs", "05.01.2026", "02.02.2026", None])
        output = io.BytesIO()
        workbook.save(output)

        rows = read_schedule_rows(output.getvalue(), ".xlsx")

        self.assertEqual(rows[0]["dates"], ["05.01.2026", "02.02.2026", ""])

    def test_missing_title_months_and_corrupt_xlsx_are_rejected(self):
        with self.assertRaisesRegex(Exception, "Title"):
            read_schedule_rows(b"January\n05.01.2026\n", ".csv")
        with self.assertRaisesRegex(Exception, "coloane lunare"):
            read_schedule_rows(b"Title\nCourse\n", ".csv")
        with self.assertRaisesRegex(Exception, "structur"):
            read_schedule_rows(b"not-a-workbook", ".xlsx")


class WordMatchingLogicTests(SimpleTestCase):
    def test_normalization_handles_entities_diacritics_punctuation_and_spacing(self):
        self.assertEqual(
            normalize_title("  Audit &amp; Îmbunătățire—ISO 9001 "),
            "audit imbunatatire iso 9001",
        )

    def test_unique_exact_match_wins_before_fuzzy_candidates(self):
        rows = [
            schedule_row(4, "Managementul calității"),
            schedule_row(9, "Managementul mediului"),
        ]

        scored = score_schedule_matches("Managementul calitatii", rows)

        self.assertEqual(len(scored), 1)
        self.assertTrue(scored[0]["exact"])
        self.assertEqual(confident_match_from_scores("Managementul calitatii", scored), rows[0])

    def test_ambiguous_fuzzy_match_needs_review(self):
        rows = [
            schedule_row(0, "Auditor intern ISO 9001"),
            schedule_row(1, "Auditor intern ISO 14001"),
            schedule_row(2, "Prim ajutor"),
        ]
        scored = score_schedule_matches("Auditor intern ISO", rows)

        self.assertGreater(scored[0]["score"], scored[2]["score"])
        self.assertIsNone(
            confident_match_from_scores(
                "Auditor intern ISO",
                scored,
                {"min_match_score": 70, "min_token_coverage": 60, "min_match_gap": 8},
            )
        )

    def test_standard_code_breaks_a_close_tie(self):
        rows = [
            schedule_row(0, "Auditor intern ISO 9001 sisteme"),
            schedule_row(1, "Auditor intern ISO 14001 sisteme"),
        ]
        scored = score_schedule_matches("Curs auditor intern 9001", rows)

        matched = confident_match_from_scores(
            "Curs auditor intern 9001",
            scored,
            {"min_match_score": 99, "min_token_coverage": 99, "min_match_gap": 50},
        )

        self.assertEqual(matched, rows[0])

    def test_word_row_detection_skips_merged_and_sparse_rows(self):
        document = Document()
        table = document.add_table(rows=3, cols=6)
        table.rows[0].cells[0].merge(table.rows[0].cells[5]).text = "Antet"
        table.rows[1].cells[0].text = "Rând incomplet"
        for index, value in enumerate(("Curs", "2 zile", "100", "", "", "")):
            table.rows[2].cells[index].text = value

        rows = build_word_course_rows(document)

        self.assertEqual([row["title"] for row in rows], ["Curs"])

    def test_preview_and_generation_modify_only_selected_date_cells(self):
        word_bytes = word_document_bytes(
            [
                ("Curs exact", "2 zile", "100", "vechi 1", "vechi 2", "vechi 3"),
                ("Fără potrivire", "1 zi", "50", "păstrează 1", "păstrează 2", "păstrează 3"),
            ]
        )
        schedule_rows = [
            schedule_row(7, "Curs exact", ["nou 1", "nou 2", "nou 3"]),
            schedule_row(8, "Alt curs", ["alt 1", "alt 2", "alt 3"]),
        ]
        preview = build_word_match_preview(
            word_bytes,
            schedule_rows,
            {"min_match_score": 88, "min_token_coverage": 70, "min_match_gap": 8},
        )
        output, matched, skipped = apply_word_matches(word_bytes, schedule_rows, {0: 7})
        result = Document(io.BytesIO(output))

        self.assertEqual(preview["rows"][0]["selected_row_index"], 7)
        self.assertEqual(preview["rows"][1]["status"], "needs_review")
        self.assertLessEqual(len(preview["rows"][1]["candidates"]), 5)
        self.assertEqual((matched, skipped), (1, 1))
        self.assertEqual(
            [cell.text for cell in result.tables[0].rows[0].cells],
            ["Curs exact", "2 zile", "100", "nou 1", "nou 2", "nou 3"],
        )
        self.assertEqual(
            [cell.text for cell in result.tables[0].rows[1].cells][3:],
            ["păstrează 1", "păstrează 2", "păstrează 3"],
        )


class WordConverterViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="word-user", password="test")
        cls.permission = Permission.objects.get(
            codename="use_word_matcher",
            content_type__app_label="planificator",
        )
        cls.user.user_permissions.add(cls.permission)

    def setUp(self):
        self.client.force_login(self.user)

    def test_page_uses_app_template_active_navigation_and_separate_permission(self):
        response = self.client.get(reverse("planificator:word_converter"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "planificator/word_converter.html")
        self.assertContains(response, "Convertor planificare Word")
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, "Convertor Word")
        self.assertNotContains(response, "Generator perioade")
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, 'hx-boost="false"')
        self.assertContains(response, "x-data=")

    def test_anonymous_missing_permission_and_superuser_boundaries(self):
        self.client.logout()
        url = reverse("planificator:word_converter")
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")

        other = get_user_model().objects.create_user(username="course-only")
        other.user_permissions.add(
            Permission.objects.get(
                codename="use_course_planning",
                content_type__app_label="planificator",
            )
        )
        self.client.force_login(other)
        self.assertEqual(self.client.get(url).status_code, 403)

        superuser = get_user_model().objects.create_superuser(username="word-root", password="test")
        self.client.force_login(superuser)
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_page_is_get_only_and_endpoints_are_post_only(self):
        self.assertEqual(self.client.post(reverse("planificator:word_converter")).status_code, 405)
        self.assertEqual(self.client.get(reverse("planificator:word_match_preview")).status_code, 405)
        self.assertEqual(self.client.get(reverse("planificator:word_match_generate")).status_code, 405)

    def test_preview_and_generate_contract(self):
        preview = self.client.post(
            reverse("planificator:word_match_preview"),
            {"word_file": word_upload(), "schedule_file": schedule_upload()},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(preview.status_code, 200)
        self.assertEqual(preview["Content-Type"], "application/json")
        preview_payload = preview.json()
        self.assertTrue(preview_payload["success"])
        self.assertEqual(preview_payload["matched_count"], 1)
        self.assertEqual(preview_payload["rows"][0]["selected_row_index"], 0)

        generated = self.client.post(
            reverse("planificator:word_match_generate"),
            data=json.dumps(
                {
                    "word_file_b64": preview_payload["word_file_b64"],
                    "schedule_options": preview_payload["schedule_options"],
                    "matches": [{"word_row_index": 0, "schedule_row_index": 0}],
                }
            ),
            content_type="application/json",
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(generated.status_code, 200)
        self.assertEqual(
            generated["Content-Type"],
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        self.assertIn("planificare_cursuri_actualizata.docx", generated["Content-Disposition"])
        self.assertIn("attachment;", generated["Content-Disposition"])
        self.assertEqual(generated["X-Matched-Course-Rows"], "1")
        self.assertEqual(generated["X-Skipped-Course-Rows"], "0")
        document = Document(io.BytesIO(generated.content))
        self.assertEqual(
            [cell.text for cell in document.tables[0].rows[0].cells][3:],
            ["05-06.01.2026", "02-03.02.2026", "02-03.03.2026"],
        )

    def test_invalid_files_json_base64_and_indexes_return_safe_errors(self):
        corrupt = self.client.post(
            reverse("planificator:word_match_preview"),
            {"word_file": word_upload(b"not-a-docx"), "schedule_file": schedule_upload()},
        )
        self.assertEqual(corrupt.status_code, 400)
        self.assertNotIn("zip", corrupt.content.decode().lower())

        invalid_json = self.client.post(
            reverse("planificator:word_match_generate"),
            data="{bad-json",
            content_type="application/json",
        )
        self.assertEqual(invalid_json.status_code, 400)

        invalid_base64 = self.client.post(
            reverse("planificator:word_match_generate"),
            data=json.dumps(
                {"word_file_b64": "%%%", "schedule_options": [], "matches": []}
            ),
            content_type="application/json",
        )
        self.assertEqual(invalid_base64.status_code, 400)

        word_b64 = base64.b64encode(word_document_bytes()).decode("ascii")
        unknown_index = self.client.post(
            reverse("planificator:word_match_generate"),
            data=json.dumps(
                {
                    "word_file_b64": word_b64,
                    "schedule_options": [
                        {"row_index": 0, "title": "Curs exact", "dates": ["1", "2", "3"]}
                    ],
                    "matches": [{"word_row_index": 9, "schedule_row_index": 0}],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(unknown_index.status_code, 400)
        self.assertIn("inexistent", unknown_index.json()["error"])

    @patch("apps.planificator.forms.MAX_WORD_UPLOAD_BYTES", 4)
    def test_oversized_word_upload_is_rejected_before_document_parsing(self):
        response = self.client.post(
            reverse("planificator:word_match_preview"),
            {"word_file": word_upload(b"12345"), "schedule_file": schedule_upload()},
        )

        self.assertEqual(response.status_code, 413)
        self.assertIn("0 MB", response.json()["error"])

    def test_duplicate_schedule_indexes_are_rejected(self):
        option = {"row_index": 0, "title": "Curs exact", "dates": ["1", "2", "3"]}
        response = self.client.post(
            reverse("planificator:word_match_generate"),
            data=json.dumps(
                {
                    "word_file_b64": base64.b64encode(word_document_bytes()).decode("ascii"),
                    "schedule_options": [option, option],
                    "matches": [],
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("duplicate", response.json()["error"])

    def test_preview_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        response = client.post(
            reverse("planificator:word_match_preview"),
            {"word_file": word_upload(), "schedule_file": schedule_upload()},
        )
        self.assertEqual(response.status_code, 403)

    def test_frontend_does_not_parse_html_strings(self):
        source = (
            Path(__file__).resolve().parent / "static" / "planificator" / "word_converter.js"
        ).read_text(encoding="utf-8")
        self.assertNotIn("innerHTML", source)
        self.assertNotIn("insertAdjacentHTML", source)
```
