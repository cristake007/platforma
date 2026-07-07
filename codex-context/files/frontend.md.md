# Source snapshot

## `frontend.md`

Size: 7.0 KB

```markdown
# Frontend Rules

Frontend standards for Django templates, Tailwind CSS, daisyUI, HTMX, Alpine.js, and scoped custom JavaScript.

The application stays server-rendered. Do not turn it into a SPA.

## Stack

- Django templates.
- Tailwind CSS.
- daisyUI.
- HTMX.
- Alpine.js.
- Scoped custom JavaScript when safer than forcing HTMX/Alpine.

Do not add React, Vue, Svelte, Angular, Inertia, Next.js, Nuxt, or another frontend framework unless explicitly requested.

## Source of truth

- Django views choose responses.
- Django forms validate requests.
- Django services perform writes.
- PostgreSQL stores business state.
- JavaScript improves interaction only.

Do not move validation, authorization, routing, ownership checks, or persistence into JavaScript.

## Brand and theme

Use the `tuvtk` daisyUI theme.

Current brand tokens are defined in `theme/static_src/src/styles.css`:

- primary blue: `#164194`.
- secondary red: `#d41131`.
- accent grey-green: `#7c8f9e`.
- page/panel background: white.
- muted panel background: `#f7f9fb`.
- default border: `#cfd7df`.

Use semantic utilities and CSS variables:

- `base-*`.
- `base-content`.
- `primary`.
- `secondary`.
- `accent`.
- `info`.
- `success`.
- `warning`.
- `error`.
- `text-muted`.

Do not add literal colors or app-local color systems.

Literal colors belong only in global token definitions, brand assets, or user-authored document/canvas data.

## Visual style

Target look:

- professional;
- enterprise-grade;
- compact;
- calm;
- operational;
- clear hierarchy;
- no decorative clutter.

Avoid:

- childish card-heavy layouts;
- oversized rounded cards;
- pastel dashboard blocks;
- decorative gradients;
- random shadows;
- app-local colors;
- inconsistent button shapes;
- large empty spacing on internal tools.

Use sharp business UI by default:

- prefer `rounded-none` for new business panels, tables, settings rows, menus, and action areas;
- prefer borders over shadows;
- prefer compact sections over large cards;
- keep spacing tight but readable;
- use rounded exceptions only for avatars, status dots, badges, or legacy elements already styled that way.

## Layout principles

Standard page shape:

- page title;
- short description only if useful;
- primary action near the title;
- filters/search in a compact section;
- main table/list/form region;
- messages/toasts in one predictable place;
- empty state close to the affected region.

Settings pages should use:

- section heading;
- short explanation;
- structured rows;
- setting name on the left;
- setting purpose under the name;
- control on the right;
- obvious disabled/error/destructive states.

Do not make every setting a separate card.

## Tailwind and daisyUI

- Use Tailwind for layout and spacing.
- Use daisyUI for standard components.
- Prefer existing classes and includes before adding new CSS.
- Add Tailwind `@source` entries only when a new app template/static path needs class scanning.
- Keep component size consistent across pages.
- Do not create one-off utility piles when an include or component pattern already exists.

## Common component standards

### Forms

- Keep forms compact and readable.
- Use server-rendered errors.
- Put non-field errors above the action row.
- Use one clear primary submit button.
- Put cancel/back/secondary actions beside it with lower emphasis.
- Keep destructive actions separated or clearly marked.

### Tables and lists

- Prefer tables for operational comparison and management.
- Keep headers readable.
- Keep action columns consistent.
- Keep wide tables horizontally scrollable.
- Use `docs/frontend/table-patterns.md` for detailed table/list work.

### Action buttons

- Primary action: `btn btn-primary`.
- Secondary action: `btn btn-outline` or low-emphasis link/button.
- Destructive action: `btn btn-error` or clearly marked icon button.
- Compact row actions should use the same size across the page.
- Icon-only buttons require an accessible label or title.
- Disabled buttons must use a real disabled state where possible.

### Messages and toasts

- Use one message area per workflow.
- Map state to semantic tokens: success, info, warning, error.
- HTMX updates that change state should refresh the message region.
- Avoid app-local alert colors.
- Error messages should explain the next useful action.

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

## Kanban and drag/drop interfaces

- Dragging must have an obvious active state.
- Drop targets must be visually clear.
- Moved/reordered stages must show immediate feedback.
- Destructive actions should use a bin/trash icon only with an accessible label.
- Replacement actions must explain what will be replaced and what stays unchanged.
- Do not hide critical ordering state in subtle card movement only.

## Global assets

HTMX and Alpine are loaded once from the base layout.

Apps may add scoped behavior, but must not duplicate global library loading.

## Visual verification

For UI work, report:

- before/after browser check if available;
- disabled states checked;
- empty states checked;
- error states checked;
- narrow-screen behavior checked;
- manual checks still needed.
```
