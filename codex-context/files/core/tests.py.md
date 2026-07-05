# core/tests.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `core/tests.py`
- App: none
- Role: `test`
- Size: 2974 bytes
- Source SHA-256: `726a2dcb41ec4bf0001f87afe219e3228bd561217aa472a84394dd5259bc5a92`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from django.urls import resolve, reverse

from .context_processors import application_shell


class ApplicationShellTests(TestCase):
    def test_login_uses_large_logo_and_daisyui_card(self):
        response = self.client.get(reverse("login"))

        self.assertContains(response, 'data-theme="tuvtk"')
        self.assertContains(response, "card card-border w-full bg-base-100 shadow-xl")
        self.assertContains(response, "h-24 w-24 object-contain sm:h-28 sm:w-28")
        self.assertNotContains(response, "ops-btn")

    def test_navigation_marks_current_route(self):
        request = RequestFactory().get('/')
        request.resolver_match = resolve('/')
        request.user = AnonymousUser()

        context = application_shell(request)
        dashboard_item = context['app_navigation'][0]['items'][0]

        self.assertTrue(dashboard_item['is_active'])
        self.assertEqual(dashboard_item['url_name'], 'dashboard:index')

    def test_context_processor_does_not_query_the_database(self):
        user = get_user_model().objects.create_user(username="shell-user")
        request = RequestFactory().get('/')
        request.resolver_match = resolve('/')
        request.user = user
        with self.assertNumQueries(0):
            context = application_shell(request)
        self.assertEqual(context["user_display_name"], "shell-user")

    def test_avatar_initials_use_name_for_unseparated_username(self):
        user = get_user_model().objects.create_user(
            username="cristipopa",
            first_name="Cristi",
            last_name="Popa",
        )
        request = RequestFactory().get('/')
        request.resolver_match = resolve('/')
        request.user = user

        context = application_shell(request)

        self.assertEqual(context["user_display_name"], "Cristi Popa")
        self.assertEqual(context["user_initials"], "CP")

    def test_avatar_initials_fall_back_to_segmented_username(self):
        user = get_user_model().objects.create_user(username="platform-admin")
        request = RequestFactory().get('/')
        request.resolver_match = resolve('/')
        request.user = user

        context = application_shell(request)

        self.assertEqual(context["user_initials"], "PA")

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
    def test_404_page_uses_project_branding(self):
        response = self.client.get("/ruta-inexistenta/")

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(response, "Pagina nu a fost gasita", status_code=404)
        self.assertContains(response, "badge badge-outline badge-primary", status_code=404)
        self.assertContains(response, "btn btn-outline btn-primary btn-sm", status_code=404)
```
