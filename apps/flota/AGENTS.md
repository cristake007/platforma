# Flota App Instructions

## Scope

This app owns fleet vehicles, current and historical user assignments, maintenance types, maintenance records, due-state calculations, and the fleet list/detail workflows.

## Read Before Editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md` for UI/template work.
- This file.
- Only the files for the selected workflow.

Use `codex-context/apps/flota.md` only when a path is unknown.

## Minimal Routing

- Fleet list, filters, and pagination:
  `selectors.py`, `views.py`, exact fleet table/panel templates, `static/flota/flota.js` if needed, then focused tests.
- Vehicle create, edit, archive, restore, or detail:
  `forms.py`, `services.py`, `selectors.py`, `views.py`, exact vehicle templates/includes, then focused tests.
- Assignment changes:
  `forms.py`, `validators.py`, `services.py`, `selectors.py`, assignment/detail templates, then focused tests.
- Maintenance record changes:
  `forms.py`, `validators.py`, `services.py`, `selectors.py`, maintenance templates/includes, then focused tests.
- Maintenance-type management:
  `forms.py`, `validators.py`, `services.py`, `views.py`, management templates/includes, then focused tests.
- Due-state or deadline label behavior:
  `selectors.py`, `services.py`, `static/flota/flota.js`, affected templates, then focused tests.
- Model change:
  `models.py`, affected validators/services/selectors/tests, then only the relevant migration.

## Architecture

- Keep request validation in `forms.py`.
- Keep reusable invariants in `validators.py`.
- Keep transactional writes in `services.py`.
- Keep permission-filtered reads in `selectors.py`.
- PostgreSQL is authoritative.
- JavaScript may refresh displayed countdown labels but must not own validation, authorization, or persistence.
- All pages require authentication.
- Staff manage the fleet.
- Non-staff users have read-only access only to currently assigned, non-archived vehicles.
- Return 404 for vehicles outside the current user's visibility.
- Use POST with CSRF for archive, restore, and maintenance-type state changes.
- Archive vehicles and custom maintenance types instead of exposing destructive deletion.
- System maintenance types cannot be archived.

## Domain Contracts

- A vehicle has at most one open assignment.
- Assignment changes must go through transactional services so history remains complete.
- Seed and retain the system types ITP, Insurance, Oil change, and Service.
- Custom types are fleet-wide and staff-managed.
- Maintenance deadlines are manual dates.
- `next_due_on` must follow `completed_on`.
- Due states are: valid beyond 30 days, due soon within 30 days, due today, overdue, or not recorded.
- Vehicle emblems are optional JPEG, PNG, or WebP uploads of at most 2 MB.

## Reuse and UI Standards

- Reuse existing vehicle, maintenance, assignment, table, message, and action patterns.
- Extend `layouts/base.html` and use shared semantic daisyUI/Tailwind tokens.
- Keep the fleet overview table horizontally scrollable.
- Keep detail layout stacked on narrow screens.
- The four system maintenance types remain the overview columns.
- Custom types appear on vehicle details and contribute to summary deadline counts.
- Keep forms and navigation usable without JavaScript.
- Preserve visible keyboard focus.
- Use sharp bordered operational panels instead of decorative rounded cards.

## Focused Checks

```powershell
python manage.py test apps.flota
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py tailwind build
```
