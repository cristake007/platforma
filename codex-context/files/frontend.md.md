# Source snapshot

## `frontend.md`

Size: 921 B

```markdown
# Frontend Rules

- Use the `tuvtk` daisyUI theme and its semantic color utilities; literal colors belong only in `theme/static_src/src/styles.css` token definitions and brand assets.
- Use `--sidebar-*` only for sidebar-specific states that do not map cleanly to daisyUI semantics. The shared `ops-*` class names are styling and JavaScript hooks, not color tokens.
- Use Tailwind for layout and daisyUI for accessible primitives. Do not add a second framework or SPA.
- Keep pages compact, flat, responsive, and keyboard accessible.
- Application-specific JavaScript and template includes belong to their Django app.
- Build feature interfaces directly from daisyUI components. Custom `ops-*` classes are reserved for the shared application shell and sidebar.
- Preserve native scrolling behavior and visible focus indicators.
- Generator results must remain usable on narrow screens through horizontal table scrolling.
```
