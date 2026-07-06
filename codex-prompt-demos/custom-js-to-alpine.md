# Custom JavaScript to Alpine.js Prompt Guide

Use this when you want Codex to check whether an existing custom JavaScript behavior can be replaced by Alpine.js.

The goal is not to delete all JavaScript. The goal is to move simple local UI state into templates with Alpine and keep custom JavaScript for workflows that truly need it.

## Decision rule

Alpine.js is a good replacement when the behavior is local to the page and does not own business state.

Good Alpine candidates:

- dropdown open/close state;
- modal/dialog visibility;
- tabs and disclosure panels;
- selected row/card visual state;
- upload filename labels;
- local loading indicators;
- simple counters;
- mobile filter/sidebar toggles;
- show/hide advanced filters.

Keep custom JavaScript for:

- drag and drop;
- canvas/template editors;
- direct download flows;
- file parsing;
- JSON-heavy workflows;
- row-by-row remote updates;
- complex preview/rendering logic;
- browser APIs that are clearer in a dedicated file.

Never move these to Alpine:

- validation authority;
- permissions;
- ownership checks;
- persistence;
- business workflow state;
- anything that must survive refresh unless the server also stores it.

## Investigation prompt

```text
Investigate whether this app/page can replace scoped custom JavaScript with Alpine.js.
Do not edit files.

Target app:
- apps/<app>

Target page or workflow:
- <describe page/workflow>

Read only:
- AGENTS.md
- frontend.md
- apps/<app>/AGENTS.md
- the target template
- the related view only if needed
- the existing app-specific JS file

Output:
1. Custom JS behaviors found
2. Which behaviors can move to Alpine.js
3. Which behaviors should stay as custom JS
4. Risks
5. Exact implementation prompt for the first small change

Rules:
- Do not inspect unrelated apps.
- Do not implement.
- Do not propose a SPA pattern.
- Keep Django as source of truth.
```

## First implementation prompt

```text
Replace only one simple custom JavaScript behavior with Alpine.js.

Target app:
- apps/<app>

Behavior:
- <example: upload filename display>

Allowed files:
- <template path>
- <existing JS path only if removing now-unused code is necessary>

Rules:
- Alpine may handle local UI state only.
- Do not change backend behavior.
- Do not change validation, permissions, or persistence.
- Do not remove custom JS that still handles complex workflows.
- Keep the visual behavior the same or simpler.
- Return a minimal diff.

Checks:
- ./install.sh check
- git diff --check

Manual browser checks:
- open the target page;
- trigger the changed UI behavior;
- confirm there are no console errors;
- confirm the form/action still works after refresh.
```

## Example: upload filename display

Before asking for a full conversion, ask only for this:

```text
Replace only the upload filename preview custom JS with Alpine.js.
Do not touch upload processing.
Do not touch HTMX endpoints.
Do not touch unrelated JS behavior.
```

Expected Alpine shape:

```html
<div x-data="{ fileName: '' }">
  <input
    type="file"
    name="file"
    @change="fileName = $event.target.files[0]?.name || ''"
  >
  <p x-show="fileName" x-text="fileName"></p>
</div>
```

## Example: modal visibility

```html
<div x-data="{ open: false }">
  <button type="button" @click="open = true">Open</button>

  <div x-show="open" x-cloak>
    <button type="button" @click="open = false">Close</button>
    <!-- modal content -->
  </div>
</div>
```

## Example: advanced filters toggle

```html
<section x-data="{ filtersOpen: false }">
  <button type="button" @click="filtersOpen = !filtersOpen">
    Filters
  </button>

  <div x-show="filtersOpen" x-cloak>
    <!-- filter form fields -->
  </div>
</section>
```

## Anti-patterns

Do not ask Codex:

```text
Replace all custom JS with Alpine.
```

Ask instead:

```text
Investigate this one JS file and classify each behavior as Alpine, HTMX, keep custom JS, or remove.
```

Then implement one behavior at a time.
