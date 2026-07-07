# Source snapshot

## `codex-prompt-demos/README.md`

Size: 6.9 KB

````markdown
# Codex Prompt Demos

Copy one prompt, replace the placeholders, and use it in Codex.

Keep each Codex session limited to one app, one workflow, and one safe change.

## Required reading for normal tasks

```text
Read only:
- AGENTS.md
- coding-standards.md
- frontend.md if UI/templates/CSS/JS/HTMX/Alpine are involved
- apps/<app>/AGENTS.md
- exact files needed for this workflow
```

Do not read:

```text
- the whole repository
- all codex-context files
- unrelated apps
- unrelated tests
- migration history unless schema is involved
- Docker/deployment files unless deployment is the task
```

## Daily Safe Task

```text
Work only on this task:

[describe the task]

Target app:
- apps/<app>

Read only:
- AGENTS.md
- coding-standards.md
- frontend.md if frontend is involved
- apps/<app>/AGENTS.md
- exact files needed for this workflow

Before editing, report:
- files you need to inspect
- why each file is needed
- whether this is app-local or cross-app

Rules:
- Implement the smallest safe change.
- Reuse existing forms, selectors, services, templates, partials, tables, action buttons, and message patterns.
- Do not create a new abstraction unless the pattern is already repeated and stable.
- Stop if another app, schema migration, or broad rewrite becomes necessary.

Checks:
- focused check for the changed app/workflow
- ./install.sh check if backend behavior changed
- git diff --check
```

## Investigation Only

```text
Investigate only. Do not edit files.

Task idea:
[describe what I want visually or functionally]

Target app:
- apps/<app>

Read only:
- AGENTS.md
- coding-standards.md
- frontend.md if frontend is involved
- apps/<app>/AGENTS.md
- exact files directly related to this workflow

Output:
- recommended approach
- files that would need editing
- existing patterns to reuse
- HTMX vs Alpine vs custom JS decision, if frontend is involved
- risks
- focused test commands
- exact implementation prompt I can use next

Do not inspect unrelated apps.
Do not read generated context unless source paths are unknown.
Do not implement.
```

## Frontend Page Improvement

```text
Improve only this page:

Target app:
- apps/<app>

Target page:
- <template path>

Read only:
- AGENTS.md
- coding-standards.md
- frontend.md
- apps/<app>/AGENTS.md
- <template path>
- related view only if needed
- related tests only if rendered behavior changes

Rules:
- Use Django templates, Tailwind, and daisyUI.
- Use shared `tuvtk` semantic tokens.
- Keep the page sharp, compact, professional, and enterprise-grade.
- Use `rounded-none` for new business panels, settings rows, menus, and tables.
- Avoid childish rounded card-heavy layouts.
- Reuse existing form, table, action-button, empty-state, and message/toast patterns.
- Use HTMX only if server-rendered partial updates are needed.
- Use Alpine only for local UI state.
- Do not introduce a SPA pattern.
- Do not touch unrelated pages.

Goal:
[describe visual/UX improvement]

Checks:
- ./install.sh check
- ./install.sh test apps.<app> only if behavior changed
- git diff --check

Report files changed and manual browser checks needed.
```

## HTMX Workflow Conversion

```text
Convert only this workflow to HTMX:

Target app:
- apps/<app>

Workflow:
- [example: upload form + asset grid refresh]

Read only:
- AGENTS.md
- coding-standards.md
- frontend.md
- apps/<app>/AGENTS.md
- the view file for this workflow
- the template file for this workflow
- the app tests file

Use HTMX for:
- server-rendered partial updates
- form validation errors
- refreshed messages
- refreshed list/table/grid sections

Do not use HTMX for:
- direct downloads
- JSON APIs consumed elsewhere
- replacing Django validation or permissions

Preserve:
- normal full-page fallback
- POST + CSRF for state changes
- ownership checks
- existing URLs unless a new partial endpoint is necessary

Stop if this requires touching another app.

Checks:
- ./install.sh test apps.<app>
- ./install.sh check
- git diff --check
```

## Alpine Local UI Only

```text
Add Alpine.js only for local UI state.

Target app:
- apps/<app>

Target template:
- <template path>

Read only:
- AGENTS.md
- coding-standards.md
- frontend.md
- apps/<app>/AGENTS.md
- <template path>
- related app JS file only if one already exists

Use Alpine only for:
- toggles
- dialogs
- disclosure panels
- selected row/card state
- loading indicators
- upload filename display

Do not use Alpine for:
- validation
- authorization
- persistence
- server state
- business workflow state

Do not touch Django models, services, or migrations.

Checks:
- ./install.sh check
- git diff --check

Report manual browser checks needed.
```

## UI Consistency Cleanup

```text
Clean up UI consistency only.

Target app:
- apps/<app>

Target page or workflow:
- <path/workflow>

Read only:
- AGENTS.md
- coding-standards.md
- frontend.md
- apps/<app>/AGENTS.md
- exact templates/includes/static files for this page

Goals:
- remove childish rounded card-heavy layout
- use sharp bordered sections
- unify forms, tables, action buttons, and messages
- reuse existing partials where practical
- keep behavior unchanged

Do not:
- change models
- change services/selectors unless a template contract requires it
- touch unrelated pages
- add a frontend framework
- introduce app-local colors

Checks:
- ./install.sh check
- app test only if rendered behavior changed
- git diff --check
```

## Bug Fix

```text
Fix only this bug:

Bug:
[paste exact bug/error/behavior]

Target app:
- apps/<app>

Read only:
- AGENTS.md
- coding-standards.md
- apps/<app>/AGENTS.md
- frontend.md if UI is involved
- exact files needed to reproduce or fix the bug

Before editing:
- identify likely cause
- list files to inspect
- say whether this is frontend, backend, or template-only

Rules:
- Implement the smallest safe fix.
- Reuse existing patterns.
- Do not weaken tests to make the failure disappear.

Checks:
- focused test for the changed app/file
- ./install.sh check
- git diff --check

Stop if the bug requires a broad rewrite.
```

## Documentation Only

```text
Update documentation only.

Read only:
- AGENTS.md
- coding-standards.md
- README.md
- frontend.md
- the exact docs mentioned below

Task:
[describe doc update]

Do not edit application code.
Do not inspect unrelated apps.
Do not regenerate codex context unless explicitly requested.

Checks:
- git diff --check

Report files changed.
```

## After Codex Finishes

Check status:

```bash
git status --short
git diff --check
```

Commit tracked modified files only:

```bash
git add -u
git commit -m "Your commit message"
```

Commit new files too:

```bash
git add path/to/new-file
git add -u
git commit -m "Your commit message"
```
````
