# Source snapshot

## `apps/dashboard/AGENTS.md`

Size: 1.2 KB

````markdown
# Dashboard App Instructions

## Scope and Ownership

This app owns the authenticated root dashboard at `/`. It is a lightweight overview and navigation entry point, not a home for domain workflows or duplicate business data.

## Minimal Routing

- Route or authentication: `urls.py`, `views.py`, then the matching tests.
- Page content or layout: `templates/dashboard/index.html`, then `tests.py` if the rendered contract changes.
- Shared shell, sidebar, or navigation: leave this app and inspect `core/templates/layouts/base.html`, `core/templates/includes/sidebar.html`, `core/navigation.py`, and the relevant theme file.
- Use `codex-context/apps/dashboard.md` only when an additional path is unknown.

## Contracts

- Keep `DashboardView` authenticated and the route named `dashboard:index` unless a coordinated root routing change is requested.
- Keep the template app-owned and extending `layouts/base.html`.
- Use the shared semantic theme tokens; do not add dashboard-specific colors or shell styles.
- Put real planificator, diploma, or media behavior in its owning app and link to it rather than implementing it here.

## Focused Check

```powershell
python manage.py test apps.dashboard
```
````
