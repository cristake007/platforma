# Frontend Rules

## Stack

- Django templates
- Tailwind CSS
- daisyUI
- HTMX
- Alpine.js
- scoped custom JavaScript when needed

The application stays server-rendered.

Do not turn it into a SPA.

Do not add React, Vue, Svelte, Angular, Inertia, Next.js, Nuxt, or another frontend framework unless explicitly requested.

## Source of truth

- Django views choose responses.
- Django forms validate requests.
- Django services perform writes.
- PostgreSQL stores business state.
- JavaScript may improve interaction only.

Do not move validation, authorization, routing, ownership checks, or persistence into JavaScript.

## Tailwind and daisyUI

- Use Tailwind for layout.
- Use daisyUI for components.
- Use the `tuvtk` daisyUI theme.
- Use semantic utilities: `base-*`, `base-content`, `primary`, `secondary`, `accent`, `info`, `success`, `warning`, `error`, `text-muted`.
- Do not add literal colors or app-local color systems.
- Literal colors belong only in global token definitions, brand assets, or user-authored document/canvas data.
- Add Tailwind `@source` entries only when a new app template/static path needs class scanning.

## HTMX

Use HTMX when the server returns HTML.

Good HTMX uses:

- form submissions with partial refresh;
- validation-error partials;
- filters;
- search;
- pagination;
- table/list refreshes;
- archive/restore actions;
- delete actions;
- message areas;
- targeted swaps;
- small server-rendered polling.

Do not use HTMX for:

- direct downloads unless intentionally designed and tested;
- canvas/editor state;
- drag-and-drop state ownership;
- large JSON workflows where JSON is clearer;
- replacing Django validation or permissions.

State-changing HTMX requests must remain POST with CSRF.

## Alpine.js

Use Alpine.js only for local browser state.

Good Alpine uses:

- dropdowns;
- dialogs;
- disclosure panels;
- tabs without server state;
- selected rows/cards;
- loading flags;
- upload filename labels;
- small counters;
- narrow-screen filter toggles.

Do not use Alpine.js for:

- database state;
- validation;
- authorization;
- ownership checks;
- business workflows;
- state that must survive refresh.

## Custom JavaScript

Keep or add scoped custom JavaScript when it is safer than forcing HTMX/Alpine.

Good custom JavaScript cases:

- drag and drop;
- canvas/template editors;
- file parsing;
- JSON-heavy workflows;
- direct download flows;
- remote row-by-row updates;
- complex preview/rendering logic.

Application-specific JavaScript belongs to the owning Django app.

Shared JavaScript belongs in `theme/` or `core/` only when it is truly global.

## Templates

- Standard pages extend `core/templates/layouts/base.html`.
- Standalone pages must still use the shared theme and compiled stylesheet.
- Prefer existing includes before new markup.
- Keep tables horizontally scrollable on narrow screens.
- Preserve native links/forms where practical.
- Preserve keyboard access, visible focus, and native scrolling.

## Global assets

HTMX and Alpine are loaded once from the base layout.

Apps may add scoped behavior, but must not duplicate global library loading.
