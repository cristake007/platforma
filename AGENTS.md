# Platforma TUVTK — Agent Router

## Scope and workflow

These instructions apply to the whole repository. A deeper `AGENTS.md` adds app-specific rules for files below its directory.

The repository has a unified cross-platform command surface. Use `./install.sh` on Debian/Linux or `./install.ps1` on native Windows for setup, lifecycle, Django, frontend, test, data, and context commands. Linux production uses Docker Compose; Windows development uses user-space Python, Node, and PostgreSQL runtimes. `bin/tuvtk` is the Linux Compose implementation and is not the normal user entry point. Do not reconstruct long raw Compose commands unless validating Compose configuration itself.

Primary agent commands:

```bash
./install.sh context --max-file-kb 80
./install.sh check
./install.sh test apps.dashboard
```

On Windows use the equivalent `./install.ps1` commands. `scripts/tuvtk_cli.py` is the shared router and `scripts/generate_codex_context.py` is the context implementation. Shell, batch, and PowerShell compatibility launchers delegate to these tracked entry points.

## Smallest sufficient context

Before editing:

1. Read the applicable `AGENTS.md` files from the repository root to the target directory.
2. If exact source paths are known, open those real files directly. Do not also read their generated snapshots.
3. If paths or dependencies are unclear, read only `codex-context/apps/<app>.md` for app work or `codex-context/project-core.md` for project/core/theme work.
4. Use `codex-file-map.txt` only to locate an unknown file. Use `codex-context-index.md` only for high-level orientation.
5. Open `codex-context/files/<real-path>.md` only for targeted orientation. Before editing, open the real source file, which is authoritative.
6. Expand into another app only when an import, URL, model relation, template include, navigation entry, or shared contract proves that dependency.

Do not preload the file map, context index, project core, every app guide, migration history, or unrelated tests for a local task. Broad reading is appropriate only for an explicit audit, cross-app change, or new application.

Generated context is navigation support, not a second source of truth. If stale, inspect real source and regenerate with:

```bash
./install.sh context
```

## Repository boundaries

* `platforma_tuvtk/`: settings, root URL inclusion, ASGI, and WSGI only.
* `core/`: global shell, navigation, middleware, context processors, shared templates, and shared user profile behavior.
* `theme/`: Tailwind/daisyUI source theme and global shell JavaScript.
* `apps/`: business/domain Django apps. Each app owns its routes, views, forms, workflows, queries, validation, templates, static files, and focused tests.

Do not duplicate a model, route, service, selector, template, or workflow before searching the owning app. Keep cross-app dependencies explicit and narrow.

## Django contracts

* Keep views thin. Put writes and multi-step workflows in `services.py`, ownership-filtered reads in `selectors.py`, request/form validation in `forms.py`, and reusable domain validation in `validators.py`.
* Keep PostgreSQL as the source of truth. JavaScript may improve interaction but must not own validation or persistence.
* Require authentication where the surrounding app does. Scope user-owned objects by owner and return 404 for cross-owner access.
* Use CSRF protection and non-GET methods for state changes.
* Use namespaced app URLs. Include them from `platforma_tuvtk/urls.py` and update `core/navigation.py` only for global navigation.
* Create and review a Django migration for every schema change. Do not inspect all old migrations unless schema history is relevant.
* Normal execution goes through `install.sh`/`install.ps1`. Debian uses Docker; Windows development uses `.venv` and the repository-local PostgreSQL runtime. Do not invoke implementation scripts directly unless diagnosing the wrapper.

## Shared frontend contract

* Server-rendered application pages extend `core/templates/layouts/base.html`. A deliberately standalone page such as login must still use `data-theme="tuvtk"` and the shared compiled stylesheet.
* Use semantic daisyUI/Tailwind tokens defined in `theme/static_src/src/styles.css`: `base-*`, `base-content`, `primary`, `secondary`, `accent`, `info`, `success`, `warning`, `error`, and `text-muted`.
* Do not add literal palette utilities, hex/RGB colors, or app-local chrome tokens. Add or adjust a global semantic token only when the design system lacks one. User-authored document/canvas colors are domain data.
* Use daisyUI components and existing shared templates/includes before custom markup. Keep interfaces compact, flat, responsive, keyboard accessible, and visibly focusable.
* Use `/diplome/istoric/` (`apps/diplome/templates/diplome/history_index.html`) as the canonical list-table model: compact `table-xs` density, bordered `base-*` surface, horizontal overflow, aligned columns, semantic status badges, right-aligned actions, and consistent empty state.
* Row actions in list tables are compact icon-only square buttons with `aria-label`, `title`, decorative SVGs marked `aria-hidden="true"`, and visible keyboard focus.
* Color table actions by intent with semantic tokens: `primary` for view/edit/navigation, `success` for download/confirm, `warning` for caution, and `error` for destructive actions.
* Use vanilla JavaScript with progressive enhancement. Preserve server-side validation and native navigation/scrolling.
* Every app whose templates/scripts use Tailwind classes needs an `@source` entry in `theme/static_src/src/styles.css`.
* Read `frontend.md` and the exact template/static files for frontend changes. Read shared base/theme files only when changing global layout or tokens.
* Run Tailwind/npm through `./install.sh tailwind` and `./install.sh npm ...`, or the equivalent `install.ps1` commands on Windows.

## Safety and preservation

* Preserve all unrelated tracked and untracked user changes. Never reset, discard, or overwrite them to simplify a task.
* Inspect `.env.example`; never inspect or expose `.env` or `/etc/tuvtk/tuvtk.env` contents unless explicitly required and authorized.
* Do not delete database volumes, persistent PostgreSQL storage, uploads, private media, secrets, or environment files.
* Do not run `install.sh clean`, restore, SQL import, or other destructive database/filesystem commands unless explicitly requested.
* Do not run full Docker rebuilds, production starts/restarts, migrations, collectstatic, npm installation, or service-changing commands merely for validation.
* Do not claim SSL works. Current Compose/Nginx is HTTP-only and installer SSL modes intentionally refuse.
* Preserve the unified router. Do not add standalone Windows lifecycle scripts or duplicate setup logic outside `scripts/tuvtk_cli.py`.
* Preserve the Linux production lifecycle: build, start/wait for `db`, run `init`, then start `web` and `nginx`.

Avoid generated, runtime, dependency, binary, and local-tool paths unless directly required: `.tuvtk/`, `.venv/`, `.git/`, `.postgresql/`, `node_modules/`, `staticfiles/`, `media/`, `private_media/`, `.playwright-mcp/`, `test-results/`, `playwright-report/`, `apps/planificator-main/`, `theme/static/css/dist/`, `theme/static/fonts/`, and `theme/static/images/`.

## Verification policy

Choose the smallest checks that exercise the changed boundary. Do not run automated test suites by default because they are expensive and create database state. Provide focused test commands for the user unless execution is explicitly requested or necessary for a narrow diagnosis.

Primary project checks:

```bash
./install.sh check
./install.sh test <app-or-test-path>
```

The wrapper defaults tests to `-v 0`. Never run the full database-backed suite automatically.

Safe workflow checks:

```bash
bash -n install.sh
bash -n bin/tuvtk
bash -n generate_codex_context.sh
python3 -m py_compile scripts/tuvtk_cli.py
python3 -m py_compile scripts/generate_codex_context.py
./install.sh help
./install.sh context --max-file-kb 80
git diff --check
```

If `python3` is unavailable, use `python -m py_compile scripts/generate_codex_context.py`.

Optional read-only Compose rendering, only when Docker CLI and the deployment env file are available:

```bash
docker compose \
  --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk \
  -f /opt/tuvtk/compose.yaml \
  -p tuvtk config --quiet

docker compose \
  --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk \
  -f /opt/tuvtk/compose.yaml \
  -f /opt/tuvtk/compose.dev.yaml \
  -p tuvtk-dev config --quiet
```

For QA plans, cover invalid input, authorization and cross-owner access, destructive actions on referenced records, refresh/back navigation, and narrow-screen behavior where relevant.

## File hygiene and completion reports

Use small, reviewable changes. Keep established workflows unless the user explicitly requests replacement. Review model migrations for schema changes, but do not load migration history without a reason.

Completion reports must state:

* files changed or removed;
* behavior/instruction changes;
* migrations created, if any;
* checks actually run and checks skipped;
* whether context generation ran;
* remaining assumptions and manual checks.

After source or instruction changes, regenerate context from the repository root when the active task permits it:

```bash
./install.sh context
```
