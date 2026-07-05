# frontend.md

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `frontend.md`
- App: none
- Role: `docs`
- Size: 921 bytes
- Source SHA-256: `d85cad3cd943dd05a226e42ce994ced798b9f0201cfc2b04bb3f8469e5a9c9d7`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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
