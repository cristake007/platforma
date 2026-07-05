# apps/tasks/IMPLEMENTATION_PLAN.md

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/tasks/IMPLEMENTATION_PLAN.md`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `backend`
- Size: 6724 bytes
- Source SHA-256: `a290b9f0bc8b7378d4f080edba0b0a663cf3f2b48c978877d58739e250e29a4f`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

````markdown
# Collaborative Tasks App — Phased Implementation Plan

## Plan Storage

This plan is stored at `apps/tasks/IMPLEMENTATION_PLAN.md` alongside the application it governs.

Approved design references:

- Kanban: `C:/Users/Cristi Popa/.codex/generated_images/019f320b-e61f-7ca0-b13b-43e7bc570701/exec-c2a81d2e-9a74-4d00-b232-9b38035a456c.png`
- List: `C:/Users/Cristi Popa/.codex/generated_images/019f320b-e61f-7ca0-b13b-43e7bc570701/exec-ee827e62-a37a-4c4e-b0ad-ed1ccd53d9eb.png`

## Phase 1 — Application Scaffold

- Create the Django `apps.tasks` package, app configuration, namespaced URLs, templates, static directories, tests, and app-specific `AGENTS.md`.
- Register the app in settings and mount it at `/tasks/`.
- Activate the existing sidebar “Task-uri” item.
- Add the app templates and scripts to Tailwind `@source`.
- Require authentication on every task-app page.

Verification gate:

- `python manage.py check`
- Sidebar link resolves and anonymous access redirects to login.

## Phase 2 — Persistence and Domain Rules

Add an initial migration containing:

- `TaskBoard`: UUID, name, owner, archive state, timestamps.
- `BoardMembership`: unique board/user membership.
- `TaskStage`: board, name, ordered position, semantic tone, terminal flag.
- `Task`: UUID, board, creator, assignee, stage, title, description, low/medium/high priority, optional start time, required due time, manual rank, completion/archive timestamps, origin metadata, timestamps.

Enforce:

- Board names unique per owner and stage names unique per board.
- Board creator automatically becomes owner and member.
- Assignments limited to active board members.
- Due time must follow `start_at`, or creation time when no start is supplied.
- Every board retains at least one terminal and one non-terminal stage.
- New boards receive `De făcut`, `În lucru`, `Blocat`, and terminal `Finalizat`.
- Entering a terminal stage records `completed_at`; leaving it reopens the task.
- Archive tasks and boards instead of deleting them.

Verification gate:

- Model and validation tests.
- `python manage.py makemigrations --check --dry-run`

## Phase 3 — Services, Selectors, and Authorization

- Put all writes and transactional workflows in `services.py`.
- Put visibility-filtered reads in `selectors.py`.
- Put request validation in `forms.py` and reusable invariants in `validators.py`.
- Ordinary members see tasks they created or received.
- Board owners and staff see every task in the relevant board.
- Creators and staff edit, reassign, archive, or restore tasks.
- Assignees may move visible tasks between stages.
- Board owners and staff manage membership and stages.
- Block member removal while active tasks remain assigned to that member.
- Require ownership transfer before removing the board owner.
- Stage deletion requires a replacement stage and transactionally moves existing tasks.

Expose the reusable integration interface:

```python
create_task(
    *,
    actor,
    board,
    assignee,
    title,
    due_at,
    description="",
    priority="medium",
    start_at=None,
    stage=None,
    origin=None,
)
```

Use a nullable `TaskOrigin(app, type, object_id, label, url)` structure. Validate origin URLs as safe application links. Emit assignment and reassignment events after commit for future notification listeners, without adding notification UI or delivery.

Verification gate:

- Authorization, cross-user 404, membership, stage-transition, archive, and integration-service tests.

## Phase 4 — Board Management

- Add board creation and settings pages.
- Support member addition/removal, ownership transfer, archive/restore, and active-user assignment choices.
- Support custom stage creation, renaming, semantic tone, terminal status, reordering, and deletion with a required replacement.
- Restrict settings controls to the board owner and staff.
- Keep PostgreSQL and server validation authoritative.

Verification gate:

- Board lifecycle, membership, ownership, stage invariants, and automatic task-move tests.

## Phase 5 — Personal Hub and List View

Implement “Task-urile mele” using the approved list concept:

- Aggregate tasks created by or assigned to the user.
- Allow staff to switch to all visible tasks.
- Add board, relationship, stage, priority, search, and deadline-order filters.
- Add pagination and responsive horizontal table scrolling.
- Provide board selection and direct Kanban navigation.
- Add server-validated task create/edit forms, progressively enhanced with daisyUI dialogs.
- Show origin links when source metadata exists.

Verification gate:

- Filter, pagination, visibility, invalid-form, archive, back-navigation, and narrow-screen tests.

## Phase 6 — Kanban, Ordering, and Live Behaviour

Implement the approved Kanban concept:

- Board-specific Kanban and list tabs.
- Persist same-stage ordering and cross-stage movement.
- Provide accessible drag-and-drop plus a keyboard/non-JavaScript stage-change fallback.
- POST moves with target stage, target index, and expected task version.
- Lock affected rows, reindex both stages, and return `409` for stale changes.
- Add a permission-filtered board-state JSON endpoint.
- Poll approximately every 30 seconds and reconcile the complete visible board snapshot.

Live timer behaviour:

- Use `start_at` or `created_at` as the baseline.
- Success through 50% elapsed, warning from 50–80%, and error after 80% or overdue.
- Update displayed countdowns every second from server-provided ISO timestamps.
- Terminal tasks display `Finalizat` and stop urgency updates.
- JavaScript never owns validation or persistence.

Verification gate:

- Movement, ordering, concurrency, polling visibility, reopening, timer thresholds, keyboard operation, and CSRF tests.

## Phase 7 — Final QA and Context Generation

Run:

- `python manage.py test apps.tasks`
- `python manage.py check`
- `python manage.py makemigrations --check --dry-run`
- `python manage.py tailwind build`

Use the Browser plugin to verify desktop and narrow-screen behaviour, falling back to Playwright only if unavailable. Compare the rendered Kanban and list views against the approved concepts, including layout, typography, semantic colors, timer states, filtering, dialogs, drag behaviour, and scrolling.

Finally run:

```powershell
.\generate_codex_context.bat
```

Review the generated task context and report files changed, migration details, checks run, visual QA, and remaining manual checks.

## Deferred Scope

- Comments, attachments, labels, recurring tasks, and activity history.
- In-app or email notification delivery.
- WebSockets.
- Concrete “Adaugă ca task” buttons in existing applications.
- Permanent deletion.
````
