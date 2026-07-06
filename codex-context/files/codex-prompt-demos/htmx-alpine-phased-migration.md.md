# Source snapshot

## `codex-prompt-demos/htmx-alpine-phased-migration.md`

Size: 4.4 KB

````markdown
# HTMX + Alpine Phased Migration Prompts

Use these prompts when converting ordinary Django HTML pages into a more dynamic server-rendered interface.

Do not migrate a whole app in one prompt. Migrate one behavior at a time.

## Phase 0 — investigation only

```text
Investigate only. Do not edit files.

Target app:
- apps/<app>

Goal:
I want this app/page to feel more dynamic with HTMX and Alpine.js, but I do not want a SPA.

Read only:
- AGENTS.md
- frontend.md
- apps/<app>/AGENTS.md
- the templates/views directly related to this page
- existing app-specific JS only if the page uses it

Output:
1. Existing page flow
2. Candidate HTMX partials
3. Candidate Alpine local state
4. Custom JS that should remain
5. Risks
6. Recommended first implementation phase
7. Exact next prompt

Do not inspect unrelated apps.
Do not load the whole generated context unless file paths are unknown.
```

## Phase 1 — list/table refresh only

```text
Convert only this list/table area to HTMX.

Target app:
- apps/<app>

Target page:
- <template path>

Goal:
The table/list should refresh without a full page reload when filters/search/pagination change.

Allowed files:
- the target view
- the target template
- new partial template(s) only if needed
- the app tests file only if behavior changes

Rules:
- Keep full-page fallback working.
- Use server-rendered HTML partials.
- Preserve existing permissions and query filtering.
- Do not change create/edit/delete flows.
- Do not redesign the page.
- Do not touch unrelated apps.

Output:
- minimal diff
- files changed
- focused tests/checks
- manual browser checks
```

## Phase 2 — form validation partial only

```text
Convert only this form to HTMX partial submission.

Target app:
- apps/<app>

Target form/page:
- <template path>

Goal:
Submit the form with HTMX and show validation errors without a full page reload.

Rules:
- POST must keep CSRF.
- Django form validation remains authoritative.
- On validation error, return the form partial.
- On success, return the smallest useful updated partial or preserve existing redirect fallback.
- Do not change models or migrations.
- Do not change unrelated forms.

Output:
- minimal diff
- files changed
- tests/checks
- manual browser checks
```

## Phase 3 — Alpine local UI state only

```text
Add Alpine.js only for local UI state on this page.

Target app:
- apps/<app>

Target behavior:
- <dropdown/modal/tabs/selected rows/upload filename/filter drawer>

Rules:
- Alpine may not own server state.
- Do not move validation, permissions, or persistence into Alpine.
- Do not add global JS.
- Do not duplicate Alpine loading.
- Keep keyboard and refresh behavior acceptable.

Output:
- minimal diff
- files changed
- manual browser checks
```

## Phase 4 — extract shared table partials only after repetition exists

```text
Extract reusable table/list partials only where duplication already exists.

Target app:
- apps/<app>

Candidate templates:
- <list templates>

Rules:
- Do not create an over-generic table framework.
- Keep different column sets explicit and readable.
- Extract only shared shell pieces: empty state, loading area, pagination, table wrapper, action button patterns.
- Do not hide business-specific columns in complex template magic.
- Preserve existing visual output.

Output:
- minimal diff
- files changed
- before/after template structure
- manual browser checks
```

## Phase 5 — infinite scroll / lazy rows

Use only when pagination is not desired and the data set is not too large for the browser over time.

```text
Implement lazy row loading for this list/table.

Target app:
- apps/<app>

Target page:
- <template path>

Goal:
The table area stays inside a fixed-height scroll container. Rows load in chunks as the user scrolls near the bottom.

Rules:
- Keep a normal fallback if practical.
- Use server-rendered row partials.
- Do not load all rows at once.
- Use stable ordering.
- Preserve filters/search.
- Do not use frontend-owned data state.
- Add clear empty/end-of-list behavior.

Output:
- minimal diff
- files changed
- manual browser checks with 2,000 rows or fixture data
```

Notes:
- Infinite scroll is useful for visual flow, but pagination is easier to debug and bookmark.
- For internal operations, consider a fixed-height table with HTMX-loaded pages/chunks rather than endless browser memory growth.
````
