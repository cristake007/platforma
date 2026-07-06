# Frontend Rules

- Use the `tuvtk` daisyUI theme and its semantic color utilities; literal colors belong only in `theme/static_src/src/styles.css` token definitions and brand assets.
- Use `--sidebar-*` only for sidebar-specific states that do not map cleanly to daisyUI semantics. The shared `ops-*` class names are styling and JavaScript hooks, not color tokens.
- Use Tailwind for layout and daisyUI for accessible primitives. Do not add a second framework or SPA.
- HTMX and Alpine.js are allowed only as progressive enhancement: HTMX for server-rendered partial updates, Alpine for local UI state.
- Keep Django templates, views, forms, and PostgreSQL as the source of truth; do not move validation, authorization, persistence, or routing into JavaScript.
- Load shared HTMX and Alpine assets once from the base layout. Apps may add scoped behavior, but must not duplicate global library loading.
- Keep pages compact, flat, responsive, and keyboard accessible.
- Application-specific JavaScript and template includes belong to their Django app.
- Build feature interfaces directly from daisyUI components. Custom `ops-*` classes are reserved for the shared application shell and sidebar.
- Preserve native scrolling behavior and visible focus indicators.
- Generator results must remain usable on narrow screens through horizontal table scrolling.
