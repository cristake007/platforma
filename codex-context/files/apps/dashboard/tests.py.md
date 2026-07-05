# Source snapshot

## `apps/dashboard/tests.py`

Size: 5.4 KB

Redacted secret-like assignments: 1

```python
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='operator',
            password=<redacted>
            first_name='Test',
            last_name='Operator',
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_dashboard_uses_app_owned_template(self):
        response = self.client.get(reverse('dashboard:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertTemplateNotUsed(response, 'includes/htmx_page.html')
        self.assertContains(response, 'Internal operations command center')

    def test_dashboard_htmx_request_returns_page_content_fragment(self):
        response = self.client.get(
            reverse('dashboard:index'),
            HTTP_HX_REQUEST='true',
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'includes/htmx_page.html')
        self.assertTemplateUsed(response, 'dashboard/_content.html')
        self.assertTemplateNotUsed(response, 'dashboard/index.html')
        self.assertContains(response, 'id="page-content"', count=1)
        self.assertContains(response, 'data-active-nav-url="/"')

    def test_dashboard_history_restore_request_returns_full_page(self):
        response = self.client.get(
            reverse('dashboard:index'),
            HTTP_HX_REQUEST='true',
            HTTP_HX_HISTORY_RESTORE_REQUEST='true',
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertTemplateNotUsed(response, 'includes/htmx_page.html')

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
        self.assertContains(response, 'sessionStorage.getItem("ops-sidebar-expanded")')
        self.assertContains(response, 'drawer.dataset.sidebarReady = "true"')
        self.assertNotContains(response, 'js/sidebar_state.js')
        content = response.content.decode()
        toggle_position = content.index('id="ops-sidebar"')
        initializer_position = content.index('sessionStorage.getItem("ops-sidebar-expanded")')
        sidebar_position = content.index('class="drawer-side')
        drawer_content_position = content.index('class="drawer-content')
        self.assertLess(toggle_position, initializer_position)
        self.assertLess(initializer_position, sidebar_position)
        self.assertLess(sidebar_position, drawer_content_position)

    def test_anonymous_user_is_redirected_to_login(self):
        self.client.logout()

        response = self.client.get(reverse('dashboard:index'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard:index')}",
        )

    def test_anonymous_htmx_request_uses_full_page_login_redirect(self):
        self.client.logout()

        response = self.client.get(
            reverse('dashboard:index'),
            HTTP_HX_REQUEST='true',
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            response.headers['HX-Redirect'],
            f"{reverse('login')}?next={reverse('dashboard:index')}",
        )
        self.assertNotIn('Location', response.headers)

    def test_only_pilot_dashboard_link_has_htmx_navigation(self):
        response = self.client.get(reverse('dashboard:index'))

        self.assertContains(
            response,
            'href="/" data-shell-nav-url="/" hx-get="/" '
            'hx-target="#page-content" hx-swap="outerHTML show:#ops-main-scroll:top" '
            'hx-push-url="true" hx-sync="#page-content:replace"',
        )
        self.assertContains(
            response,
            f'href="{reverse("tasks:index")}" '
            f'data-shell-nav-url="{reverse("tasks:index")}"',
        )
        self.assertNotContains(
            response,
            f'data-shell-nav-url="{reverse("tasks:index")}" hx-get=',
        )

    def test_user_menu_posts_to_django_logout(self):
        response = self.client.get(reverse('dashboard:index'))

        self.assertContains(response, f'action="{reverse("logout")}"')
        self.assertContains(response, 'Test Operator')
```
