# Codex Prompt Demos

Copy one prompt, replace the placeholders, and use it in Codex.

Use short prompts. Keep each Codex session limited to one app, one workflow, and one safe change.

## Daily Safe Task

```text
Work only on this task:

[describe the task]

Target app:
- apps/<app>

Read only:
- AGENTS.md
- frontend.md if frontend is involved
- apps/<app>/AGENTS.md
- exact files needed for this workflow

Do not read:
- the whole repository
- all codex-context files
- unrelated apps
- unrelated tests
- migration history
- Docker/deployment files

Before editing, report:
- files you need to inspect
- why each file is needed
- whether this is app-local or cross-app

Implement the smallest safe change and stop.

Stop if another app, schema migration, or broad rewrite becomes necessary.
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
- frontend.md if frontend is involved
- apps/<app>/AGENTS.md
- exact files directly related to this workflow

Output:
- recommended approach
- files that would need editing
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
- frontend.md
- apps/<app>/AGENTS.md
- <template path>
- related view only if needed
- related tests only if rendered behavior changes

Rules:
- Use Django templates, Tailwind, and daisyUI.
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

## Media Library Demo

```text
Work only on Media Library upload/list/delete UX.

Target app:
- apps/media_library

Read only:
- AGENTS.md
- frontend.md
- apps/media_library/AGENTS.md
- apps/media_library/views.py
- apps/media_library/urls.py
- apps/media_library/forms.py
- apps/media_library/templates/media_library/library.html
- apps/media_library/tests.py

Goal:
Add HTMX partial refresh for upload and delete so the form, messages, and asset grid update without a full page reload.

Use Alpine only for:
- selected upload filename
- local loading state

Preserve:
- normal full-page fallback
- JSON API endpoints
- private asset serving
- ownership checks
- POST + CSRF

Do not touch:
- apps/diplome
- apps/tasks
- apps/planificator
- apps/flota
- Docker/deployment files
- generated context

Checks:
- ./install.sh test apps.media_library
- ./install.sh check
- git diff --check

Stop after this workflow.
```

## Tasks List Demo

```text
Work only on Tasks list pages, not Kanban drag-and-drop.

Target app:
- apps/tasks

Read only:
- AGENTS.md
- frontend.md
- apps/tasks/AGENTS.md
- apps/tasks/views.py
- apps/tasks/urls.py
- apps/tasks/forms.py
- apps/tasks/templates/tasks/hub.html
- apps/tasks/templates/tasks/board_list.html
- apps/tasks/templates/tasks/board_settings.html
- apps/tasks/templates/tasks/includes/messages.html
- apps/tasks/templates/tasks/includes/form_fields.html
- apps/tasks/tests.py

Goal:
Identify and implement small HTMX improvements for non-Kanban task list/settings workflows.

Use HTMX for:
- filters
- local list refreshes
- form sections that can return server-rendered partials

Use Alpine for:
- confirmation state
- local dialog/disclosure state
- loading indicators

Do not touch:
- board_kanban.html
- drag-and-drop logic
- BoardStateView JSON polling unless strictly required
- unrelated apps

Preserve:
- native form fallback
- permissions
- POST + CSRF
- existing task movement behavior

Checks:
- ./install.sh test apps.tasks
- ./install.sh check
- git diff --check

Stop before Kanban work.
```

## Planificator Investigation Demo

```text
Investigate Planificator generator/history only. Do not edit files.

Target app:
- apps/planificator

Read only:
- AGENTS.md
- frontend.md
- apps/planificator/AGENTS.md
- apps/planificator/views.py
- apps/planificator/forms.py
- apps/planificator/templates/planificator/generator_perioade.html
- apps/planificator/templates/planificator/includes/upload.html
- apps/planificator/templates/planificator/includes/settings.html
- apps/planificator/templates/planificator/includes/result_table.html
- apps/planificator/templates/planificator/includes/actions.html
- apps/planificator/templates/planificator/includes/messages.html
- apps/planificator/templates/planificator/istoric.html
- apps/planificator/static/planificator/generator.js
- apps/planificator/tests.py
- apps/planificator/tests_scheduler.py

Output only:
- HTMX targets
- Alpine targets
- custom JavaScript to preserve
- risks around exports/downloads
- exact implementation plan
- focused tests

Do not inspect:
- XML converter
- Word converter
- course updater
- diplome
- tasks
- flota
- media_library

Do not implement.
```

## Planificator Implementation Demo

```text
Implement only the Planificator generator/history improvements approved in the previous investigation.

Target app:
- apps/planificator

Read only the files listed in the approved investigation.

Use HTMX for:
- server-rendered form/message/result sections where safe
- history list/detail partial refreshes only if native fallback remains clean

Use Alpine for:
- month selection UI
- holiday row UI
- upload filename state
- local step/disclosure state

Preserve:
- schedule export behavior
- file download behavior
- server-side validation
- horizontal scrolling result tables
- existing permissions

Do not touch:
- XML converter
- Word converter
- course updater
- unrelated apps

Checks:
- ./install.sh test apps.planificator.tests
- ./install.sh test apps.planificator.tests_scheduler
- ./install.sh check
- git diff --check

Stop after this workflow.
```

## Diplome Investigation Demo

```text
Investigate ordinary Diplome pages only. Do not edit files.

Target app:
- apps/diplome

Read only:
- AGENTS.md
- frontend.md
- apps/diplome/AGENTS.md
- apps/diplome/views.py
- apps/diplome/urls.py
- apps/diplome/forms.py
- apps/diplome/templates/diplome/template_list.html
- apps/diplome/templates/diplome/template_form.html
- apps/diplome/templates/diplome/history_index.html
- apps/diplome/templates/diplome/batch_detail.html
- apps/diplome/templates/diplome/participant_list.html
- apps/diplome/templates/diplome/participant_list_detail.html
- relevant diplome tests only

Output:
- which pages can safely use HTMX
- which UI state can use Alpine
- what must remain custom JavaScript
- what must not be touched
- risks around downloads/PDF/history snapshots
- exact next implementation prompt

Do not inspect:
- template_editor.js
- template_renderer.js
- template_editor.html
unless you find a direct dependency and explain why.

Do not implement.
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
- apps/<app>/AGENTS.md
- exact files needed to reproduce or fix the bug

Do not read:
- unrelated apps
- generated context unless file paths are unknown
- migration history unless schema is involved

Before editing:
- identify likely cause
- list files to inspect
- say whether this is frontend, backend, or template-only

Implement the smallest safe fix.

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
