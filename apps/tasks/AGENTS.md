# Tasks App Instructions

## Scope

This app owns collaborative boards, memberships, stages, task persistence, task-list and Kanban views, deadline timers, and the reusable cross-app task-creation contract.

## Architecture

- Keep request validation in `forms.py`, reusable invariants in `validators.py`, writes in `services.py`, and permission-filtered reads in `selectors.py`.
- All pages and endpoints require authentication.
- Ordinary members see tasks they created or received. Board owners and staff see all tasks on the relevant board.
- Creators and staff edit/archive tasks; creators, assignees, and staff may move tasks.
- Treat PostgreSQL as authoritative. JavaScript only enhances timers, polling, dialogs, and drag-and-drop.
- Use POST with CSRF for every state change. Return 404 for inaccessible boards and tasks.

## Frontend

- Extend `layouts/base.html` and use the shared semantic theme tokens.
- Keep the list horizontally scrollable and the Kanban board horizontally usable on narrow screens.
- Preserve the native form fallback for task stage changes.

## Focused Checks

```powershell
python manage.py test apps.tasks
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py tailwind build
```

