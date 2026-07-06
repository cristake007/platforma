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
