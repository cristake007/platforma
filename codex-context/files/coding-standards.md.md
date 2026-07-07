# Source snapshot

## `coding-standards.md`

Size: 5.9 KB

```markdown
# Coding Standards

Shared coding standards for the Platforma TUVTK Django project.

Use this file together with `AGENTS.md`, `frontend.md`, and the target app `AGENTS.md`.

## Core principles

- Keep changes small, explicit, and reviewable.
- Reuse existing project patterns before creating new ones.
- Do not duplicate forms, tables, action buttons, messages, validation, selectors, services, or template fragments.
- Do not create generic frameworks too early.
- Extract reuse only when the same stable pattern appears in more than one place.
- Keep business rules server-side.
- Keep UI behavior progressive and usable after refresh.

## Django structure

Use this default split:

- `views.py`: HTTP orchestration, request method handling, response choice.
- `forms.py`: request/form validation, cleaned data, field-level errors.
- `services.py`: writes, transactions, lifecycle changes, imports, exports, side effects.
- `selectors.py`: permission-filtered reads and query construction.
- `validators.py`: reusable validation and shared invariants.
- `models.py`: data shape, constraints, simple model helpers.
- `urls.py`: namespaced routes.
- `templates/<app>/`: page and partial templates owned by the app.
- `tests*.py`: workflow-level contracts and regressions.

Views should stay thin. If a view starts coordinating persistence, permissions, and multiple model changes, move that workflow into a service.

## Reuse rules

Before adding a new pattern, inspect the target app for:

- an existing form class;
- an existing selector query;
- an existing service method;
- an existing partial template;
- an existing table wrapper;
- an existing action button cluster;
- an existing messages/toast area;
- an existing empty state;
- an existing test pattern.

Reuse locally first. Promote to `core/` or `theme/` only when at least two apps need the same stable pattern.

Do not create cross-app abstractions from a single app requirement.

## Forms

- Use Django forms for validation.
- Keep labels, help text, required state, and errors consistent with existing app forms.
- Prefer shared form partials when a field layout repeats.
- Do not validate ownership or permissions only in the browser.
- Use POST with CSRF for every state change.
- Preserve full-page fallback when HTMX is added.

Recommended form layout:

- short section title;
- one-line explanation when needed;
- compact fields;
- inline field errors;
- one primary action;
- secondary/cancel action visually quieter;
- non-field errors above the action row.

## Tables and lists

Use `docs/frontend/table-patterns.md` for detailed table guidance.

Default table/list rules:

- Keep columns explicit in the app template.
- Extract only repeated wrappers, rows, empty states, pagination, filters, or action clusters.
- Keep tables horizontally usable on narrow screens.
- Keep headers readable and sticky only when the table is tall or horizontally complex.
- Keep row actions visually consistent across apps.
- Do not hide permission-sensitive actions only with CSS or JavaScript.

## Action buttons

Use consistent action hierarchy:

- Primary create/save/confirm action: `btn btn-primary`.
- Secondary navigation/cancel action: `btn btn-outline` or a low-emphasis link button.
- Destructive action: `btn btn-error` or a clearly marked destructive icon button.
- Table row actions: compact buttons with consistent size, label, icon, and title.
- Disabled actions: use real disabled state where possible and explain why nearby.

Do not invent a new button style for one page.

If an icon-only button is used, it must have an accessible label or title.

## Messages and toasts

- Use one consistent page message/toast area per workflow.
- Server messages remain authoritative.
- HTMX responses that change state should refresh the relevant messages area.
- Keep success, warning, error, and info styling mapped to semantic daisyUI tokens.
- Do not create app-local color classes for messages.
- Error copy should say what failed and what the user can do next.

## Template partials

Use partials for repeated UI with stable contracts:

- form sections;
- filter bars;
- table wrappers;
- table rows;
- empty states;
- pagination;
- action button groups;
- message areas;
- modal bodies.

Keep app-specific business columns and page-specific copy inside the owning app.

Do not turn partials into a large generic UI framework.

## HTMX usage

Good HTMX targets:

- form validation results;
- filter refreshes;
- search;
- pagination;
- table/list regions;
- archive/restore/delete refreshes;
- messages/toast regions;
- small server-rendered state changes.

Avoid HTMX for:

- downloads unless intentionally designed and tested;
- drag-and-drop ownership;
- canvas/editor state;
- large JSON workflows;
- replacing permissions or validation.

## Alpine usage

Use Alpine only for local browser state:

- toggles;
- dialogs;
- disclosures;
- selected rows/cards;
- loading flags;
- upload filename labels;
- narrow-screen filter panels.

Do not use Alpine for database state, permissions, validation, or workflow decisions.

## Tests

- Add or update tests when behavior changes.
- Prefer focused app tests during iteration.
- Run the smallest relevant test first.
- Run broader checks only when the change crosses app boundaries.
- Do not weaken tests to match a bug.
- If a UI-only documentation/style instruction changes no code, `git diff --check` is enough.

## Review checklist

Before reporting completion, verify:

- no unrelated files changed;
- no duplicated existing pattern was added;
- forms still validate server-side;
- selectors still enforce visibility;
- services still own writes;
- templates reuse existing includes where useful;
- buttons, tables, forms, and messages follow shared styling;
- focused checks were run or clearly skipped with a reason.
```
