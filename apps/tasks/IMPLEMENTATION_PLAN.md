# Collaborative Tasks App — Phased Implementation Plan

## Low-Priority Planning Artifact

- Read this file only for roadmap work, phased migration, or historical implementation status.
- Do not read it for normal bug fixes, UI cleanups, tests, or app-local implementation changes.
- For implementation work, start with `apps/tasks/AGENTS.md` and the exact workflow files.

## Status

- Plan location: `apps/tasks/IMPLEMENTATION_PLAN.md`.
- Approved visual concepts were local design references and are not required for ordinary coding-agent context.

## Phase 1 — Application Scaffold

- Create the Django `apps.tasks` package, app config, URLs, templates, static files, tests, admin registration, and app-specific `AGENTS.md`.
- Register the app in settings and mount it at `/tasks/`.
- Add the sidebar item and Tailwind sources.
- Require authentication on every page.

Verification gate:

- `python manage.py check`
- Sidebar link resolves.
- Anonymous access redirects to login.

## Phase 2 — Persistence and Domain Rules

- Add boards, memberships, stages, and task records with UUIDs and timestamps.
- Enforce per-owner board names and per-board stage names.
- Add default stages: `De făcut`, `În lucru`, `Blocat`, and terminal `Finalizat`.
- Keep at least one terminal and one non-terminal stage per board.
- Archive tasks and boards instead of deleting them.
- Record completion when entering terminal stages and reopen when leaving them.

Verification gate:

- Model and validation tests.
- `python manage.py makemigrations --check --dry-run`

## Phase 3 — Services, Selectors, and Authorization

- Keep writes in `services.py`.
- Keep permission-filtered reads in `selectors.py`.
- Keep request validation in `forms.py`.
- Keep reusable invariants in `validators.py`.
- Preserve board ownership, membership, stage, archive, and integration-service tests.
- Keep cross-app creation available through a service-level interface.

Verification gate:

- Authorization, cross-user 404, membership, transition, archive, and integration tests.

## Phase 4 — Board Management

- Add board creation and settings pages.
- Support member addition/removal, ownership transfer, archive/restore, and assignment choices.
- Support stage creation, rename, semantic tone, terminal status, reorder, and deletion with replacement.
- Restrict settings controls to board owners and staff.

Verification gate:

- Board lifecycle, membership, ownership, stage invariant, and automatic move tests.

## Phase 5 — Personal Hub and List View

- Implement “Task-urile mele”.
- Aggregate tasks created by or assigned to the user.
- Allow staff to switch to all visible tasks.
- Add board, relationship, stage, priority, search, and deadline filters.
- Add pagination and responsive horizontal table scrolling.
- Add server-validated create/edit forms with progressive dialog enhancement.
- Show origin links when metadata exists.

Verification gate:

- Filter, pagination, visibility, invalid-form, archive, back-navigation, and narrow-screen tests.

## Phase 6 — Kanban, Ordering, and Live Behaviour

- Implement board-specific Kanban and list tabs.
- Persist same-stage ordering and cross-stage movement.
- Keep accessible drag/drop and non-JavaScript fallback movement.
- Use POST moves with target stage, target index, and expected version.
- Lock affected rows and return stale-change conflicts.
- Keep polling permission-filtered and server authoritative.
- Keep timer behavior derived from server-provided timestamps.

Verification gate:

- Movement, ordering, concurrency, polling visibility, reopening, timer threshold, keyboard, and CSRF tests.

## Phase 7 — Final QA and Context Generation

Run focused checks:

- `python manage.py test apps.tasks`
- `python manage.py check`
- `python manage.py makemigrations --check --dry-run`
- `python manage.py tailwind build`

Manual QA:

- Desktop and narrow-screen Kanban.
- List view filtering and scrolling.
- Dialog behavior.
- Drag/drop and fallback movement.
- Timer states.

Context refresh:

- Regenerate context only after implementation work is finished.
- Review generated context before committing it.

## Deferred Scope

- Comments.
- Attachments.
- Labels.
- Recurring tasks.
- Activity history.
- Notification delivery.
- WebSockets.
- Cross-app “Adaugă ca task” buttons.
- Permanent deletion.
