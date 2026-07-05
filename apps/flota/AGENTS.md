# Flota App Instructions

## Scope

This app owns fleet vehicles, current and historical user assignments, maintenance types, maintenance records, due-state calculations, and the fleet list/detail workflows.

## Architecture

- Keep request validation in `forms.py`, reusable invariants in `validators.py`, transactional writes in `services.py`, and permission-filtered reads in `selectors.py`.
- PostgreSQL is authoritative. JavaScript may refresh displayed countdown labels but must not own validation, authorization, or persistence.
- All pages require authentication. Staff manage the fleet; non-staff users have read-only access only to currently assigned, non-archived vehicles.
- Return 404 for vehicles outside the current user's visibility. Use POST with CSRF for archive, restore, and maintenance-type state changes.
- Archive vehicles and custom maintenance types instead of exposing destructive deletion. System maintenance types cannot be archived.

## Domain Contracts

- A vehicle has at most one open assignment. Assignment changes must go through the transactional services so history remains complete.
- Seed and retain the system types ITP, Insurance, Oil change, and Service. Custom types are fleet-wide and staff-managed.
- Maintenance deadlines are manual dates. `next_due_on` must follow `completed_on`.
- Due states are: valid beyond 30 days, due soon within 30 days, due today, overdue, or not recorded.
- Vehicle emblems are optional JPEG, PNG, or WebP uploads of at most 2 MB.

## Frontend

- Extend `layouts/base.html` and use the shared semantic daisyUI/Tailwind tokens.
- Keep the fleet overview table horizontally scrollable and the detail layout stacked on narrow screens.
- The four system maintenance types remain the overview columns. Custom types appear on vehicle details and contribute to summary deadline counts.
- Keep forms and navigation usable without JavaScript and preserve visible keyboard focus.

## Focused Checks

```powershell
python manage.py test apps.flota
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py tailwind build
```

