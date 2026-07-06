# Platforma TUVTK — Agent Router

## Project

- Server-rendered Django application.
- Stack: Django, PostgreSQL, Tailwind CSS, daisyUI, HTMX, Alpine.js.
- Django templates and PostgreSQL are the source of truth.
- HTMX is for server-rendered partial HTML updates.
- Alpine.js is for local UI state only.
- Existing custom JavaScript may remain when it is safer or clearer.
- Do not convert the project into a SPA.
- Do not add another frontend framework unless explicitly requested.

## Scope

These rules apply to the whole repository.

A deeper `AGENTS.md` adds app-specific rules for files below its directory.

Before editing, read only:

1. this file;
2. the deeper app `AGENTS.md` for the target app;
3. the exact files named by the user;
4. files directly imported, included, extended, or referenced by those files when required.

Do not preload:

- the whole repository;
- all generated `codex-context/` files;
- unrelated apps;
- unrelated tests;
- migration history;
- Docker/deployment files;
- generated/runtime folders.

Use `codex-context/apps/<app>.md` only when source paths are unknown.

Use `codex-file-map.txt` only to locate an unknown file.

Open real source files before editing. Generated context is navigation support, not authority.

If required context is missing, stop and ask for scope expansion.

## App boundaries

- `platforma_tuvtk/`: settings, root URLs, ASGI, WSGI.
- `core/`: shared shell, navigation, middleware, context processors, shared templates.
- `theme/`: Tailwind/daisyUI theme, global frontend assets.
- `apps/`: domain apps. Each app owns its routes, views, forms, services, selectors, templates, static files, and tests.

Do not duplicate an existing model, service, selector, route, template, or workflow.

## Django rules

- Keep views thin.
- Put writes and multi-step workflows in `services.py`.
- Put permission-filtered reads in `selectors.py`.
- Put request/form validation in `forms.py`.
- Put reusable validation in `validators.py`.
- Keep validation, authorization, ownership checks, and persistence server-side.
- Use POST with CSRF for state changes.
- Return 404 for cross-owner access where the app already follows that pattern.
- Use namespaced app URLs.
- Add migrations for schema changes, but do not inspect old migrations unless needed.

## Frontend rules

Detailed frontend rules live in `frontend.md`.

Default frontend split:

- Tailwind/daisyUI: layout and components.
- HTMX: server-rendered partial updates, forms, filters, pagination, table/list refreshes.
- Alpine.js: local toggles, dialogs, selected state, loading flags, upload labels.
- Custom JavaScript: complex JSON, downloads, drag/drop, file parsing, canvas/editor workflows.

Pages should extend `core/templates/layouts/base.html` unless intentionally standalone.

Use shared semantic theme tokens. Do not introduce app-local color systems.

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

## Safety

- Preserve unrelated tracked and untracked changes.
- Never inspect or expose `.env` or `/etc/tuvtk/tuvtk.env` unless explicitly authorized.
- Do not delete database volumes, PostgreSQL data, media, private media, secrets, or environment files.
- Do not run clean, restore, SQL import, database reset, production restart, or destructive commands unless explicitly requested.
- Do not run full test suites by default. Use the smallest focused check.
- Do not claim HTTPS works; current production Compose/Nginx is HTTP-only.

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

## Stop conditions

Stop and ask before expanding scope when:

- the named file is missing;
- another app must be changed but was not listed;
- a schema migration is needed but not requested;
- a workflow would require a broad rewrite;
- validation would require destructive commands or full test suites.

## Completion report

Always report:

- files changed;
- behavior changed;
- migrations created, if any;
- checks run;
- checks skipped;
- context regeneration status;
- manual checks still needed.
