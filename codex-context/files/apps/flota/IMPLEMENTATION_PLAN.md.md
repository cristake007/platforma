# apps/flota/IMPLEMENTATION_PLAN.md

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/flota/IMPLEMENTATION_PLAN.md`
- App: `flota`
- App guide: `codex-context/apps/flota.md`
- Role: `backend`
- Size: 2074 bytes
- Source SHA-256: `ce29053f74a0ef1e517ee4777b0816681c7754004956376c33df27738b7e08e9`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```markdown
# Flota - Phased Implementation Plan

## Phase 1 - Scaffold and Instructions

- Create the Django app package, namespaced URLs, templates, static files, migrations, tests, admin registration, and app instructions.
- Register the app at `/flota/`, add it to Operations navigation, and register its templates and scripts as Tailwind sources.
- Require authentication throughout.

## Phase 2 - Persistence

- Add persistent vehicles, assignment intervals, maintenance types, and maintenance records.
- Seed protected system types for ITP, insurance, oil changes, and service while permitting staff-managed custom types.
- Normalize vehicle identifiers, validate dates and uploads, and preserve all records through archival.

## Phase 3 - Services, Selectors, and Permissions

- Keep transactional writes in services and visibility-filtered reads in selectors.
- Allow staff to manage all records and assigned users to view only their current vehicles.
- Derive deadline states from the latest record for every maintenance type using a 30-day warning window.

## Phase 4 - Routes and Forms

- Add fleet list, vehicle create/detail/edit/archive/restore, nested maintenance create/edit, and maintenance-type management routes.
- Use server-validated multipart forms and POST/CSRF for all state changes.

## Phase 5 - User Interface

- Implement the approved compact fleet table and vehicle detail concept in the shared TUVTK shell.
- Include summary counts, filters, pagination, core deadline columns, complete service history, and assignment history.
- Use minimal progressive enhancement only for deadline label refresh.

## Phase 6 - Tests and Verification

- Test persistence, validation, assignment history, permissions, filtering, due-state boundaries, archival, forms, and responsive rendering.
- Run the focused Django checks, Tailwind build, browser QA against the approved concept, and context regeneration.

## Deferred Scope

- Notifications, email, scheduled jobs, recurring intervals, document attachments, fuel tracking, expense reporting, and permanent deletion.
```
