# Core Instructions

## Scope

`core/` owns shared shell files:

- base layouts;
- shared includes;
- sidebar and navigation;
- context helpers;
- global messages.

Do not put domain workflow logic in `core/`.

## Read before editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md` for UI/template work.
- This file.
- Only the shared files needed for the requested change.

## Boundaries

- `core/` may provide shared shell, navigation, layout, messages, and reusable includes.
- Domain apps own their views, forms, selectors, services, tests, and domain templates.
- Do not move app-specific business behavior into `core/`.
- Do not add cross-app abstractions until at least two apps need the same stable pattern.

## UI standards

- Shared layouts must preserve the professional enterprise look defined in `frontend.md`.
- Keep navigation compact, sharp, and operational.
- Use shared semantic tokens only.
- Do not add app-local colors to shared shell files.
- Preserve visible focus states and keyboard access.
- Keep messages/toasts consistent and reusable.
- Do not make shared layout changes to fix one app unless the pattern is truly global.

## Coding standards

- Keep context helpers small and predictable.
- Avoid heavy database work in shared template context.
- Keep navigation definitions explicit and permission-aware.
- Preserve existing route names and active-state contracts unless a coordinated navigation change is requested.

## Focused checks

```powershell
python manage.py test core
python manage.py check
```

Run broader app tests only when a shared shell change affects rendered contracts in those apps.
