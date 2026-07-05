# Platforma TUVTK - Agent Router

## Scope

These instructions apply to the whole repository. A deeper `AGENTS.md` adds app-specific rules for files below its directory.

The objective is the smallest sufficient context with source-level accuracy. Treat this file as a router, not as a feature specification or roadmap.

## Smallest Sufficient Context

Before editing:

1. Read the applicable `AGENTS.md` files from the repository root to the target directory.
2. If the exact source paths are already known, open those real files directly. Do not also read their generated context copies.
3. If paths or dependencies are unclear, read only `codex-context/apps/<app>.md` for app work or `codex-context/project-core.md` for project/core/theme work.
4. Use `codex-context/codex-file-map.txt` only to locate an unknown file. Use `codex-context/codex-context-index.md` only to select an unknown guide.
5. Open generated `codex-context/files/<real-path>.md` snapshots only for targeted orientation. Before editing, open the real source file, which is authoritative.
6. Expand into another app only when an import, URL, model relation, template include, navigation entry, or shared contract proves that dependency.

Do not preload the file map, context index, project core guide, every app guide, migration history, or unrelated tests for a local task. Broad repository reading is appropriate only when the request explicitly asks for an audit, a cross-app change, or a new application.

## Generated Context

- `codex-context/apps/<app>.md` lists files for one Django app.
- `codex-context/project-core.md` lists project configuration, shared shell, theme, and tooling files.
- `codex-context/files/<real-path>.md` is a generated source snapshot with a source hash.
- `codex-context/codex-context-audit.md` reports generation and coverage checks.
- `generate_codex_context_v3_ascii.bat` is the implementation of the Markdown generator.
- `generate_codex_context.bat` is the stable command that invokes it.

Generated context is navigation support, not a second source of truth. If it is stale or missing, inspect the real source and regenerate it; never infer current behavior from a stale snapshot.

## Repository Boundaries

- `platforma_tuvtk/`: settings, root URL inclusion, ASGI/WSGI only.
- `core/`: global shell, navigation, middleware, context processors, shared templates, and shared user profile behavior.
- `theme/`: Tailwind/daisyUI source theme and global shell JavaScript.
- `apps/`: business/domain Django apps. Each app owns its routes, views, forms, workflows, queries, validation, templates, static files, and focused tests.

Do not duplicate a model, route, service, selector, template, or workflow before searching the owning app. Make cross-app dependencies explicit and keep them narrow.

## Django Contracts

- Keep views thin. Put writes and multi-step workflows in `services.py`, ownership-filtered reads in `selectors.py`, request/form validation in `forms.py`, and reusable domain validation in `validators.py`.
- Keep PostgreSQL as the source of truth. JavaScript may improve interaction but must not own validation or persistence.
- Require authentication where the surrounding app does. Scope user-owned objects by owner and return 404 for cross-owner object access.
- Use CSRF protection and non-GET methods for state changes.
- Use namespaced app URLs; include them from `platforma_tuvtk/urls.py` and update `core/navigation.py` only for global navigation.
- Create and review a Django migration for every model/schema change. Do not inspect all old migrations unless schema history is relevant.
Django project works under a virtual envirorment, python is not installed system wide.

## Shared Frontend Contract

- Server-rendered application pages extend `core/templates/layouts/base.html`. A deliberately standalone page, such as login, must still use `data-theme="tuvtk"` and the shared compiled stylesheet.
- Use the semantic daisyUI/Tailwind tokens defined in `theme/static_src/src/styles.css`: `base-*`, `base-content`, `primary`, `secondary`, `accent`, `info`, `success`, `warning`, `error`, and `text-muted`.
- Do not add literal palette utilities, hex colors, RGB colors, or new app-local color tokens for application chrome. Add or adjust a global semantic token in `styles.css` when the design system lacks one.
- Custom app CSS should cover behavior or geometry that utilities cannot express and should consume global semantic variables. User-authored document/canvas colors are domain data, not application chrome.
- Use daisyUI components and existing shared templates/includes before custom markup. Keep interfaces compact, flat, responsive, keyboard accessible, and visibly focusable.
- Use `/diplome/istoric/` (`apps/diplome/templates/diplome/history_index.html`) as the canonical visual and interaction model for list-view tables. Match its compact `table-xs` density, bordered `base-*` surface, horizontal overflow behavior, column alignment, compact semantic status badges, right-aligned action group, and empty-state treatment unless the domain requires a documented exception.
- In list-view tables, row-level actions must be compact icon-only buttons, not text buttons. Use square daisyUI button styling and an icon whose meaning matches the action. Give every icon-only action an explicit accessible name (`aria-label`) and tooltip (`title`), mark decorative SVGs `aria-hidden="true"`, and preserve a visible keyboard focus state.
- Color table actions by intent using the shared brand/semantic tokens: for example `primary` for view/edit/navigation, `success` for download/confirm, `warning` for cautionary actions, and `error` for destructive actions. Use the nearest existing semantic token when an action does not fit these examples; never introduce literal palette colors for action styling.
- Use vanilla JavaScript with progressive enhancement. Preserve server-side validation and native navigation/scrolling.
- Every app whose templates or scripts use Tailwind classes must have an `@source` entry in `theme/static_src/src/styles.css`.
- Read `frontend.md` plus the exact template/static files for frontend changes. Read the shared base/theme files only when changing global layout or tokens.
- Project has Playwright MCP plugin installed in codex configuration.

## Verification

Choose the smallest checks that exercise the changed boundary. Agents must not run automated test suites by default because they are expensive and produce excessive context. Instead, provide the exact focused test commands for the user to run. This execution rule applies repository-wide; deeper `AGENTS.md` files may narrow which test command is relevant but do not authorize automatic test execution.

- Django configuration: `python manage.py check`
- Migration consistency: `python manage.py makemigrations --check --dry-run`
- One app (provide to the user): `python manage.py test apps.<app_name> -v 0`
- Theme compilation: `python manage.py tailwind build`

If an automated test must be run to diagnose or verify a problem that cannot be resolved with lighter checks, run only the narrowest relevant test target and always pass `-v 0`. Never run the full database-backed suite automatically; provide that command to the user even for repository-wide changes unless the user explicitly instructs otherwise.

For QA plans, cover invalid input, authorization and cross-owner access, destructive actions on referenced records, refresh/back navigation, and narrow-screen behavior where relevant.

## File Hygiene

Do not inspect `.env`; use `.env.example`. Avoid generated, runtime, dependency, binary, and local-tool paths unless directly required: `.venv/`, `.git/`, `.postgresql/`, `node_modules/`, `staticfiles/`, `media/`, `private_media/`, `.playwright-mcp/`, `test-results/`, `playwright-report/`, `apps/planificator-main/`, `theme/static/css/dist/`, `theme/static/fonts/`, and `theme/static/images/`.

Preserve unrelated user changes. Do not replace established workflows or introduce a SPA/CSS framework without explicit instruction.

## Completion Report

Report files changed, behavior/instruction changes, migrations, checks actually run, whether context generation ran, and any remaining assumptions or manual checks.

After source or instruction changes, run from the repository root:

```powershell
.\generate_codex_context.bat
```
