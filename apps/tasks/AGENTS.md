# Tasks App Instructions

## Scope

This app owns collaborative boards, memberships, stages, task persistence, task-list and Kanban views, deadline timers, and the reusable cross-app task-creation contract.

## Read before editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md` for UI/template work.
- This file.
- Only the files for the selected workflow.

Use `codex-context/apps/tasks.md` only when a path is unknown.

## Architecture

- Keep request validation in `forms.py`.
- Keep reusable invariants in `validators.py`.
- Keep writes in `services.py`.
- Keep permission-filtered reads in `selectors.py`.
- All pages and endpoints require authentication.
- Ordinary members see tasks they created or received.
- Board owners and staff see all tasks on the relevant board.
- Creators and staff edit/archive tasks.
- Creators, assignees, and staff may move tasks.
- PostgreSQL is authoritative.
- JavaScript enhances timers, polling, dialogs, and drag-and-drop only.
- Use POST with CSRF for every state change.
- Return 404 for inaccessible boards and tasks.

## Reuse and UI standards

- Reuse existing board, task, stage, member, message, and action patterns.
- Extend `layouts/base.html` and use shared semantic theme tokens.
- Keep task lists horizontally usable on narrow screens.
- Preserve native form fallback for task stage changes.
- Board settings must use compact structured rows, not decorative rounded cards.
- Kanban stage dragging and ordering must show obvious active, drop, moved, disabled, and destructive states.
- Destructive stage/task actions should use consistent bin/trash icon treatment with accessible labels.
- Do not hide replacement or destructive behavior behind vague controls.

## Focused checks

```powershell
python manage.py test apps.tasks
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py tailwind build
```
