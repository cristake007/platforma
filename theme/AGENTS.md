# Theme Instructions

## Scope

`theme/` owns global frontend assets:

- Tailwind source configuration;
- daisyUI `tuvtk` theme tokens;
- global CSS layers;
- shared JavaScript only when truly global;
- compiled asset inputs.

Do not put app-specific business behavior in `theme/`.

## Read before editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md`.
- This file.
- Only the exact theme files needed for the requested change.

## Theme contracts

- Keep the `tuvtk` daisyUI theme as the only application theme unless explicitly requested.
- Use brand tokens from `theme/static_src/src/styles.css`.
- Do not introduce app-local color systems.
- Prefer sharp operational UI.
- New business panels, settings rows, menus, and tables should use `rounded-none` unless an existing component contract requires otherwise.
- Use borders over shadows.
- Keep global CSS minimal.
- Add Tailwind `@source` entries only for real template/static paths.

## JavaScript contracts

- HTMX and Alpine are loaded globally from the base layout.
- Do not duplicate global library loading in apps.
- Shared JavaScript belongs here only when more than one app uses the same stable behavior.
- App-specific JavaScript stays in the owning app.

## Focused checks

```powershell
python manage.py tailwind build
python manage.py check
```
