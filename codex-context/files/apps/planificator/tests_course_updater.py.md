# apps/planificator/tests_course_updater.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/planificator/tests_course_updater.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `test`
- Size: 10084 bytes
- Source SHA-256: `3b254652f4ac5f911fd556624181ce64d46c9a1db3463c511c47e2f3f9f2c4c0`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from datetime import date
import json
import socket
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
import requests

from .models import AppSetting
from .validators import ClientInputError, validate_public_http_url
from .wp_course_updater import (
    WPCourseClient,
    WordPressRequestError,
    build_final_program,
    expand_date_token,
    extract_slug_from_permalink,
    parse_effective_end_date,
    parse_excel_dates_from_row,
    valid_existing_program,
)


def resolved(address: str, port: int = 443):
    family = socket.AF_INET6 if ":" in address else socket.AF_INET
    return [(family, socket.SOCK_STREAM, 6, "", (address, port))]


def http_response(
    status: int,
    *,
    location: str | None = None,
    body: bytes = b"{}",
    headers: dict | None = None,
):
    result = requests.Response()
    result.status_code = status
    result.headers = headers or {}
    if location:
        result.headers["Location"] = location
    result._content = body
    result._content_consumed = True
    return result


class CourseUpdaterDomainTests(SimpleTestCase):
    def test_slug_and_supported_date_formats_are_parsed(self):
        self.assertEqual(
            extract_slug_from_permalink("https://example.test/cursuri/test-course/?x=1"),
            "test-course",
        )
        self.assertEqual(parse_effective_end_date("05.01.2026"), date(2026, 1, 5))
        self.assertEqual(parse_effective_end_date("05-07.01.2026"), date(2026, 1, 7))
        self.assertIsNone(parse_effective_end_date("31.02.2026"))

    def test_date_token_expansion_preserves_the_old_supported_formats(self):
        self.assertEqual(
            expand_date_token("14-16.04.2026"),
            ["14.04.2026", "15.04.2026", "16.04.2026"],
        )
        self.assertEqual(expand_date_token("2026-04-08 00:00:00"), ["08.04.2026"])
        self.assertEqual(expand_date_token("16-14.04.2026"), [])

    def test_month_values_support_old_english_and_current_romanian_exports(self):
        self.assertEqual(
            parse_excel_dates_from_row(
                {
                    "January": "08.01.2026",
                    "Martie": "05-06.03.2026",
                    "Title": "Ignored",
                }
            ),
            ["08.01.2026", "05-06.03.2026"],
        )

    def test_program_merge_filters_expired_rows_and_deduplicates_exact_text(self):
        today = date(2026, 1, 10)
        existing = [
            {"data": "09.01.2026"},
            {"data": "10.01.2026"},
            {"data": "10.01.2026"},
            {"data": "11-12.01.2026"},
            {"data": "invalid"},
        ]
        self.assertEqual(
            valid_existing_program(existing, today),
            [{"data": "10.01.2026"}, {"data": "11-12.01.2026"}],
        )
        self.assertEqual(
            build_final_program(existing, ["10.01.2026", "13.01.2026"], today),
            [
                {"data": "10.01.2026"},
                {"data": "11-12.01.2026"},
                {"data": "13.01.2026"},
            ],
        )


class CourseUpdaterNetworkSafetyTests(SimpleTestCase):
    @patch(
        "apps.planificator.validators.socket.getaddrinfo",
        return_value=resolved("93.184.216.34"),
    )
    def test_public_url_is_allowed(self, _getaddrinfo):
        self.assertEqual(validate_public_http_url("https://example.com"), "https://example.com")

    @patch(
        "apps.planificator.validators.socket.getaddrinfo",
        return_value=resolved("127.0.0.1", 80),
    )
    def test_private_destination_is_blocked(self, _getaddrinfo):
        with self.assertRaises(ClientInputError):
            validate_public_http_url("http://example.test")

    @patch("apps.planificator.validators.socket.getaddrinfo")
    def test_redirect_to_private_destination_is_blocked(self, getaddrinfo):
        getaddrinfo.side_effect = lambda host, port, **kwargs: resolved(
            "127.0.0.1" if host == "127.0.0.1" else "93.184.216.34",
            port,
        )
        client = WPCourseClient("https://example.com", "user", "password")
        client.min_interval_seconds = 0
        client.session.request = Mock(
            return_value=http_response(302, location="http://127.0.0.1/admin")
        )
        with self.assertRaises(ClientInputError):
            client._send_with_safe_redirects("GET", "https://example.com/start")
        self.assertEqual(client.session.request.call_count, 1)

    def test_cloudflare_challenge_has_a_safe_specific_error(self):
        response = http_response(
            403,
            body=b"<title>Just a moment...</title>",
            headers={"cf-mitigated": "challenge"},
        )
        with self.assertRaisesRegex(WordPressRequestError, "browser challenge"):
            WPCourseClient._raise_for_response(response)


class CourseUpdaterWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="wp-updater",
            password="test-password",
        )
        cls.user.user_permissions.add(
            Permission.objects.get(codename="use_course_planning")
        )

    def setUp(self):
        self.client.force_login(self.user)

    def json_post(self, route_name: str, payload: dict):
        return self.client.post(
            reverse(f"planificator:{route_name}"),
            data=json.dumps(payload),
            content_type="application/json",
        )

    def credentials(self, **extra):
        return {
            "wp_base_url": "https://example.com",
            "wp_username": "user",
            "wp_app_password": "password",
            **extra,
        }

    def test_page_uses_existing_route_and_exposes_updater_endpoints(self):
        response = self.client.get(reverse("planificator:actualizeaza_cursuri"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "planificator/actualizeaza_cursuri.html")
        self.assertContains(response, reverse("planificator:actualizeaza_cursuri_preview"))
        self.assertContains(response, "Conexiune WordPress")
        self.assertNotContains(response, "<th>Post ID</th>", html=True)
        self.assertNotContains(response, "Identifică")

    def test_preview_is_local_and_accepts_the_current_romanian_export(self):
        upload = SimpleUploadedFile(
            "program.csv",
            (
                "Title,Permalink,Ianuarie,Februarie\n"
                "Course,https://example.com/course/test,09.01.2026,12-13.02.2026\n"
            ).encode("utf-8"),
            content_type="text/csv",
        )
        with patch("apps.planificator.views.WPCourseClient") as client_class:
            response = self.client.post(
                reverse("planificator:actualizeaza_cursuri_preview"),
                {"input_file": upload},
            )
        self.assertEqual(response.status_code, 200)
        row = response.json()["rows"][0]
        self.assertEqual(row["slug"], "test")
        self.assertEqual(row["excel_dates"], ["09.01.2026", "12-13.02.2026"])
        client_class.assert_not_called()

    @patch("apps.planificator.views.WPCourseClient")
    def test_connect_saves_non_secret_settings_only(self, client_class):
        client_class.return_value.test_connection.return_value = {
            "id": 7,
            "name": "Editor",
        }
        response = self.json_post(
            "actualizeaza_cursuri_connect",
            self.credentials(),
        )
        self.assertEqual(response.status_code, 200)
        setting = AppSetting.objects.get(
            scope="safe_course_date_updater",
            user=self.user,
        )
        self.assertEqual(setting.payload["wp_base_url"], "https://example.com")
        self.assertEqual(setting.payload["wp_username"], "user")
        self.assertNotIn("wp_app_password", setting.payload)

    @patch("apps.planificator.views.timezone.localdate", return_value=date(2026, 1, 10))
    @patch("apps.planificator.views.WPCourseClient")
    def test_fetch_dates_merges_without_updating(self, client_class, _localdate):
        client = client_class.return_value
        client.resolve_course_post_id.return_value = 42
        client.get_course.return_value = {
            "acf": {"program": [{"data": "09.01.2026"}, {"data": "12.01.2026"}]}
        }
        response = self.json_post(
            "actualizeaza_cursuri_fetch_dates",
            self.credentials(
                permalink="https://example.com/course/test",
                slug="test",
                excel_dates=["13.01.2026"],
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["existing_valid_dates"], ["12.01.2026"])
        self.assertEqual(response.json()["final_dates"], ["12.01.2026", "13.01.2026"])
        client.update_course_program.assert_not_called()

    @patch("apps.planificator.views.timezone.localdate", return_value=date(2026, 1, 10))
    @patch("apps.planificator.views.WPCourseClient")
    def test_update_posts_only_the_final_acf_program(self, client_class, _localdate):
        client = client_class.return_value
        client.resolve_course_post_id.return_value = 42
        client.get_course.return_value = {
            "acf": {"program": [{"data": "12.01.2026"}]}
        }
        response = self.json_post(
            "actualizeaza_cursuri_update_row",
            self.credentials(
                permalink="https://example.com/course/test",
                slug="test",
                final_dates=["13.01.2026"],
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["updated"])
        client.update_course_program.assert_called_once_with(
            42,
            [{"data": "12.01.2026"}, {"data": "13.01.2026"}],
            client.auth,
        )
```
