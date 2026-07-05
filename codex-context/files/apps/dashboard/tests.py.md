# apps/dashboard/tests.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/dashboard/tests.py`
- App: `dashboard`
- App guide: `codex-context/apps/dashboard.md`
- Role: `test`
- Size: 2872 bytes
- Source SHA-256: `76af3eb6bacd6aa3dc997cbed075ff503c175687e14c9052706c80743ebc89aa`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='operator',
            password='test-password',
            first_name='Test',
            last_name='Operator',
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_dashboard_uses_app_owned_template(self):
        response = self.client.get(reverse('dashboard:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertContains(response, 'Internal operations command center')

    def test_dashboard_navigation_is_active(self):
        response = self.client.get(reverse('dashboard:index'))

        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, 'Dashboard')

    def test_nested_navigation_has_collapsed_sidebar_flyout_hooks(self):
        response = self.client.get(reverse('dashboard:index'))

        self.assertContains(response, '<details class="ops-nav-group" data-sidebar-flyout', count=1)
        self.assertContains(response, 'data-sidebar-flyout-trigger', count=1)
        self.assertContains(response, 'data-sidebar-flyout-panel', count=1)
        self.assertContains(response, 'aria-haspopup="true"', count=1)
        self.assertContains(response, 'class="ops-submenu-label"', count=2)
        self.assertNotContains(response, 'ops-flyout-heading')
        self.assertNotContains(response, 'ops-submenu is-drawer-close:hidden')

    def test_sidebar_state_is_restored_before_drawer_markup_renders(self):
        response = self.client.get(reverse('dashboard:index'))

        self.assertContains(response, 'data-sidebar-start-collapsed="false"')
        self.assertContains(response, 'js/sidebar_state.js')
        content = response.content.decode()
        toggle_position = content.index('id="ops-sidebar"')
        initializer_position = content.index('js/sidebar_state.js')
        drawer_content_position = content.index('class="drawer-content')
        self.assertLess(toggle_position, initializer_position)
        self.assertLess(initializer_position, drawer_content_position)

    def test_anonymous_user_is_redirected_to_login(self):
        self.client.logout()

        response = self.client.get(reverse('dashboard:index'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard:index')}",
        )

    def test_user_menu_posts_to_django_logout(self):
        response = self.client.get(reverse('dashboard:index'))

        self.assertContains(response, f'action="{reverse("logout")}"')
        self.assertContains(response, 'Test Operator')
```
