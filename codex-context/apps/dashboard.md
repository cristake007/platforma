# Django app: dashboard

Migrations are excluded by default. Tests are included unless `--no-tests` is used.

## `apps/dashboard/__init__.py`

Size: 0 B

```python
```

## `apps/dashboard/AGENTS.md`

Size: 1.7 KB

````markdown
# Dashboard App Instructions

## Scope and ownership

This app owns the authenticated root dashboard at `/`.

It is a lightweight overview and navigation entry point, not a home for domain workflows or duplicate business data.

## Read before editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md` for UI/template work.
- This file.
- The exact dashboard files needed for the task.

Use `codex-context/apps/dashboard.md` only when an additional source path is unknown.

## Minimal routing

- Route or authentication: `urls.py`, `views.py`, then the matching tests.
- Page content or layout: `templates/dashboard/index.html`, then `tests.py` if the rendered contract changes.
- Shared shell, sidebar, or navigation: inspect `core/templates/layouts/base.html`, `core/templates/includes/sidebar.html`, `core/navigation.py`, and relevant `theme/` files.

## Contracts

- Keep `DashboardView` authenticated.
- Keep the route named `dashboard:index` unless a coordinated root routing change is requested.
- Keep the template app-owned and extending `layouts/base.html`.
- Use shared semantic theme tokens.
- Do not add dashboard-specific colors, cards, shell styles, or duplicate navigation logic.
- Link to planificator, diplome, media_library, tasks, or flota workflows instead of implementing their behavior here.

## UI standards

- Dashboard sections should be compact and operational.
- Avoid oversized decorative cards.
- Prefer sharp bordered sections, structured rows, and clear navigation groups.
- Use the same action button and message patterns as the rest of the project.

## Focused check

```powershell
python manage.py test apps.dashboard
```
````

## `apps/dashboard/apps.py`

Size: 98 B

```python
from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'apps.dashboard'
```

## `apps/dashboard/templates/dashboard/index.html`

Size: 520 B

```html
{% extends "layouts/base.html" %}

{% block title %}Operations Dashboard | Platforma TUVTK{% endblock %}

{% block content %}
    <section class="space-y-4">
        <div>
            <h1 class="ops-title text-2xl font-bold sm:text-[2rem]">Internal operations command center</h1>
            <p class="mt-1 max-w-3xl text-sm leading-6 text-muted">
                Monitor work intake, field activity, asset health, and alerts from a single shared workspace.
            </p>
        </div>
    </section>
{% endblock %}
```

## `apps/dashboard/tests.py`

Size: 3.7 KB

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
        self.assertContains(response, 'class="ops-submenu-label"', count=4)
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

    def test_shared_htmx_and_alpine_scripts_load_once_from_shell(self):
        response = self.client.get(reverse('dashboard:index'))

        self.assertContains(response, 'js/vendor/htmx.min.js', count=1)
        self.assertContains(response, 'htmx:configRequest', count=1)
        self.assertContains(response, 'X-CSRFToken', count=1)
        self.assertContains(response, 'js/vendor/alpine.min.js', count=1)
        content = response.content.decode()
        htmx_position = content.index('js/vendor/htmx.min.js')
        csrf_hook_position = content.index('htmx:configRequest')
        alpine_position = content.index('js/vendor/alpine.min.js')
        sidebar_position = content.index('js/sidebar.js')
        self.assertLess(htmx_position, csrf_hook_position)
        self.assertLess(csrf_hook_position, alpine_position)
        self.assertLess(alpine_position, sidebar_position)

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
        self.assertContains(response, '<span aria-hidden="true">TO</span>')
```

## `apps/dashboard/urls.py`

Size: 159 B

```python
from django.urls import path

from .views import DashboardView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
]
```

## `apps/dashboard/views.py`

Size: 204 B

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
```
