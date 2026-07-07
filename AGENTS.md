# Platforma TUVTK — Agent Router

Coding-agent entry point for this repository.

Working code only. Minimal context. Verified changes.

## Fast Path

- Backend bug fix:
  `AGENTS.md` -> `coding-standards.md` -> `apps/<app>/AGENTS.md` -> exact files.
- UX, template, HTMX, Alpine, CSS, or JavaScript work:
  `AGENTS.md` -> `coding-standards.md` -> `frontend.md` -> `apps/<app>/AGENTS.md` -> exact files.
- Shared shell, navigation, or layout work:
  `AGENTS.md` -> `coding-standards.md` -> `frontend.md` -> `core/AGENTS.md` -> exact files.
- Table or list screen work:
  add `docs/frontend/table-patterns.md` only after the page is confirmed to be a table/list workflow.
- Path unknown:
  `codex-context-index.md` -> `codex-file-map.txt` -> `codex-context/apps/<app>.md`.

Stop once the next required file is known.

## Project

- Server-rendered Django application.
- Stack: Django, PostgreSQL, Tailwind CSS, daisyUI, HTMX, Alpine.js.
- Django templates and PostgreSQL are the source of truth.
- HTMX returns server-rendered partial HTML.
- Alpine.js owns local browser state only.
- Scoped custom JavaScript may remain when safer or clearer.
- Do not convert the project into a SPA.
- Do not add another frontend framework unless explicitly requested.

## Required Reading Order

Read only what the task needs:

1. `AGENTS.md`.
2. `coding-standards.md`.
3. `frontend.md` for templates, CSS, JavaScript, HTMX, Alpine, UX, or UI.
4. `apps/<app>/AGENTS.md` for the target app.
5. Exact source files for the selected workflow.
6. Direct imports, includes, templates, forms, services, selectors, or tests only when required.

Do not preload:

- the whole repository;
- all generated `codex-context/` files;
- `codex-context/files/` generated wrapper files;
- `codex-prompt-demos/` unless the task is prompt design;
- implementation plans unless the task is roadmap or migration planning;
- unrelated apps;
- unrelated tests;
- migration history;
- Docker/deployment files;
- generated/runtime folders.

Use generated context only as navigation support when source paths are unknown.

Open real source files before editing.

## App Boundaries

- `platforma_tuvtk/`: settings, root URLs, ASGI, WSGI.
- `core/`: shared shell, navigation, middleware, context processors, shared templates.
- `theme/`: Tailwind/daisyUI theme and global frontend assets.
- `apps/`: domain apps with owned routes, views, forms, services, selectors, templates, static files, and tests.

Do not duplicate existing models, services, selectors, routes, templates, includes, component patterns, or workflows.

## Coding Standards

Detailed standards live in `coding-standards.md`.

Default split:

- Views orchestrate HTTP only.
- `forms.py` validates request/form input.
- `services.py` performs writes, transactions, and multi-step workflows.
- `selectors.py` performs permission-filtered reads.
- `validators.py` contains reusable validation rules.
- Templates render state and submit forms; they do not own business rules.
- JavaScript improves interaction only.

Before adding code, search the target app for reusable forms, includes, tables, action buttons, messages, services, selectors, and validators.

If the same stable pattern appears twice, reuse or extract it.

## Frontend Standards

Detailed frontend rules live in `frontend.md`.

Default split:

- Tailwind/daisyUI: layout and components.
- HTMX: server-rendered partial updates, forms, filters, pagination, table/list refreshes.
- Alpine.js: local toggles, dialogs, selected state, loading flags, upload labels.
- Custom JavaScript: complex JSON, downloads, drag/drop, file parsing, canvas/editor workflows.

Use shared semantic theme tokens. Do not introduce app-local color systems.

New business screens should be sharp, professional, and enterprise-grade.
Avoid childish, oversized, rounded card-heavy screens.

## Commands

Use the repository wrapper.

Linux/Debian:

```bash
./install.sh check
./install.sh test <app-or-test-path>
./install.sh npm run build
./install.sh context --max-file-kb 80
```

Windows:

```powershell
.\install.ps1 check
.\install.ps1 test <app-or-test-path>
.\install.ps1 npm run build
.\install.ps1 context --max-file-kb 80
```

Do not reconstruct raw Docker Compose commands unless the task is Compose-specific.

## Verification

- Prefer the smallest focused test or check.
- Do not run full test suites by default.
- Report checks only after reading the output.
- Explain why a check was skipped when it cannot be run.
- For UI changes, report manual browser checks still needed.
- For visual work, inspect before/after behavior when tooling allows it.
- Do not weaken tests to hide a failure.

## Safety

- Preserve unrelated tracked and untracked changes.
- Environment files and production env files require explicit user authorization before inspection.
- Preserve database volumes, PostgreSQL data, media, private media, secrets, and environment files.
- Destructive commands require explicit user authorization.
- Current production Compose/Nginx is HTTP-only.

Avoid generated, runtime, dependency, binary, and local-tool paths unless directly required:

- `.tuvtk/`
- `.venv/`
- `.git/`
- `.postgresql/`
- `node_modules/`
- `staticfiles/`
- `media/`
- `private_media/`
- `.playwright-mcp/`
- `test-results/`
- `playwright-report/`
- `theme/static/css/dist/`
- `theme/static/fonts/`
- `theme/static/images/`

## Stop Conditions

Stop and ask before expanding scope when:

- the named file is missing;
- another app must be changed but was not listed;
- a schema migration is needed but not requested;
- a workflow would require a broad rewrite;
- validation would require destructive commands or full test suites;
- two attempted fixes fail for the same issue.

## Completion Report

Always report:

- files changed;
- behavior changed;
- migrations created, if any;
- checks run;
- checks skipped and why;
- context regeneration status;
- manual checks still needed.
