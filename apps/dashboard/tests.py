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
