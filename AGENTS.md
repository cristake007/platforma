# Platforma TUVTK — Agent Router

Operating rules for coding agents working in this repository.

Working code only. Minimal context. Verified changes.

## Project

- Server-rendered Django application.
- Stack: Django, PostgreSQL, Tailwind CSS, daisyUI, HTMX, Alpine.js.
- Django templates and PostgreSQL are the source of truth.
- HTMX returns server-rendered partial HTML.
- Alpine.js owns local browser state only.
- Existing scoped custom JavaScript may remain when it is safer or clearer.
- Do not convert the project into a SPA.
- Do not add another frontend framework unless explicitly requested.

## Required reading order

Read only what the task needs:

1. `AGENTS.md`.
2. `coding-standards.md`.
3. `frontend.md` when templates, CSS, JavaScript, HTMX, Alpine, UX, or UI are involved.
4. The deeper `apps/<app>/AGENTS.md` for the target app.
5. The exact source files needed for the requested workflow.
6. Directly referenced imports, includes, templates, forms, services, selectors, or tests only when required.

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

## App boundaries

- `platforma_tuvtk/`: settings, root URLs, ASGI, WSGI.
- `core/`: shared shell, navigation, middleware, context processors, shared templates.
- `theme/`: Tailwind/daisyUI theme, global frontend assets.
- `apps/`: domain apps. Each app owns its routes, views, forms, services, selectors, templates, static files, and tests.

Do not duplicate an existing model, service, selector, route, template, include, component pattern, or workflow.

## Coding standards

Detailed coding standards live in `coding-standards.md`.

Default split:

- Views orchestrate HTTP only.
- `forms.py` validates request/form input.
- `services.py` performs writes, transactions, and multi-step workflows.
- `selectors.py` performs permission-filtered reads.
- `validators.py` contains reusable validation rules.
- Templates render state and submit forms; they do not own business rules.
- JavaScript improves interaction only.

Before adding new code, search the target app for an existing form, include, table, action-button, message, service, selector, or validator pattern.

If the same pattern appears twice and is stable, reuse or extract it. If it appears once, keep it explicit.

## Frontend standards

Detailed frontend rules live in `frontend.md`.

Default frontend split:

- Tailwind/daisyUI: layout and components.
- HTMX: server-rendered partial updates, forms, filters, pagination, table/list refreshes.
- Alpine.js: local toggles, dialogs, selected state, loading flags, upload labels.
- Custom JavaScript: complex JSON, downloads, drag/drop, file parsing, canvas/editor workflows.

Use shared semantic theme tokens. Do not introduce app-local color systems.

New business screens should use sharp, professional, enterprise-grade layouts. Avoid childish, oversized, rounded card-heavy screens.

## Commands

Use the repository wrapper. `install.sh` routes ordinary commands through the Python command router.

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
- Do not claim tests passed unless you ran them and read the output.
- If verification cannot be run, say why.
- For UI changes, report the manual browser checks still needed.
- For visual work, inspect before/after behavior when tooling allows it.
- Do not weaken tests to make a failure disappear.

## Safety

- Preserve unrelated tracked and untracked changes.
- Never inspect or expose `.env` or `/etc/tuvtk/tuvtk.env` unless explicitly authorized.
- Do not delete database volumes, PostgreSQL data, media, private media, secrets, or environment files.
- Do not run clean, restore, SQL import, database reset, production restart, or destructive commands unless explicitly requested.
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
- validation would require destructive commands or full test suites;
- two attempted fixes fail for the same issue.

## Completion report

Always report:

- files changed;
- behavior changed;
- migrations created, if any;
- checks run;
- checks skipped and why;
- context regeneration status;
- manual checks still needed.
