# Tasks App Instructions

## Scope

- Owns collaborative boards, memberships, stages, records, list views, Kanban views, timers, and reusable cross-app creation.

## Read Before Editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md` for UI/template work.
- This file.
- Only files for the selected workflow.

Use `codex-context/apps/tasks.md` only when a path is unknown.

## Minimal Routing

- Board list/settings: `urls.py`, `views.py`, exact board templates/includes, focused tests.
- Create/edit/archive/restore: `forms.py`, `services.py`, `views.py`, exact form/dialog partials, focused tests.
- Kanban move/order: `selectors.py`, `services.py`, `views.py`, `static/tasks/tasks.js`, exact Kanban partials, focused tests.
- Membership/ownership: `forms.py`, `validators.py`, `services.py`, `selectors.py`, settings partials, focused tests.
- Stage management: `forms.py`, `validators.py`, `services.py`, `views.py`, settings/Kanban partials, focused tests.
- Timer/polling: `selectors.py`, `views.py`, `static/tasks/tasks.js`, timer/card partials, focused tests.
- Model change: `models.py`, affected validators/services/selectors/tests, relevant migration only.

## Architecture

- Keep request validation in `forms.py`.
- Keep reusable invariants in `validators.py`.
- Keep writes in `services.py`.
- Keep permission-filtered reads in `selectors.py`.
- Require authentication on pages and endpoints.
- Keep PostgreSQL authoritative.
- Keep JavaScript limited to timers, polling, dialogs, and drag/drop enhancement.
- Use POST with CSRF for state changes.

## Reuse and UI Standards

- Reuse existing board, record, stage, member, message, and action patterns.
- Extend `layouts/base.html` and use shared semantic theme tokens.
- Keep lists horizontally usable on narrow screens.
- Preserve native form fallbacks for stage changes.
- Board settings must use compact structured rows, not decorative rounded cards.
- Kanban dragging and ordering must show obvious active, drop, moved, disabled, and destructive states.
- Destructive actions should use consistent bin/trash icon treatment with accessible labels.

## Focused Checks

```powershell
python manage.py test apps.tasks
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py tailwind build
```
