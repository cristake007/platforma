# Platforma TUVTK

Server-rendered Django operations platform for TUVTK internal workflows.

Stack:

- Django
- PostgreSQL
- Tailwind CSS
- daisyUI
- HTMX
- Alpine.js
- Gunicorn
- Nginx

The application is not a SPA. Django templates and PostgreSQL remain the source of truth.

## Start From a Clone

Debian/Linux:

```bash
git clone https://github.com/OWNER/REPOSITORY.git tuvtk
cd tuvtk
./install.sh dev
```

Windows Command Prompt:

```bat
git clone https://github.com/OWNER/REPOSITORY.git tuvtk
cd tuvtk
install.cmd dev
```

PowerShell:

```powershell
.\install.ps1 dev
```

Development starts at:

```text
http://127.0.0.1:8000
```

Use another port:

```bash
./install.sh dev --port=8001
```

## Main Commands

Linux/Debian:

```bash
./install.sh help
./install.sh doctor
./install.sh status
./install.sh logs web
./install.sh restart
./install.sh stop

./install.sh django createsuperuser
./install.sh check
./install.sh test apps.dashboard
./install.sh migrate
./install.sh makemigrations APP
./install.sh collectstatic
./install.sh shell

./install.sh tailwind
./install.sh npm run build
./install.sh context --max-file-kb 80
```

Windows equivalents:

```powershell
.\install.ps1 help
.\install.ps1 check
.\install.ps1 test apps.dashboard
.\install.ps1 tailwind
.\install.ps1 npm run build
.\install.ps1 context --max-file-kb 80
```

`test` defaults to low verbosity.

## Coding and Agent Rules

Read these first for coding-agent work:

```text
AGENTS.md
coding-standards.md
frontend.md
apps/<app>/AGENTS.md
```

Guidance split:

- `AGENTS.md`: context budget, routing, safety, verification, and completion report.
- `coding-standards.md`: Django structure, reuse rules, forms, services, selectors, templates, buttons, tables, and messages.
- `frontend.md`: Tailwind/daisyUI, brand tokens, sharp enterprise UI, HTMX, Alpine, custom JavaScript, and visual checks.
- `apps/<app>/AGENTS.md`: app-specific ownership, contracts, focused files, and tests.

Prompt examples live in:

```text
codex-prompt-demos/README.md
```

Use generated context only for discovery:

```text
codex-context/apps/<app>.md
codex-file-map.txt
```

Do not load the whole generated context for normal work.

## Frontend Rules

See:

```text
frontend.md
docs/frontend/table-patterns.md
```

Short version:

- Tailwind/daisyUI: layout, components, and shared theme tokens.
- Brand colors come from the `tuvtk` theme.
- New business screens should be sharp, compact, and professional.
- Use `rounded-none` for new business panels, settings rows, menus, and tables unless an existing component contract requires otherwise.
- Avoid childish, decorative, rounded card-heavy layouts.
- HTMX: server-rendered partial updates.
- Alpine.js: local UI state only.
- Custom JavaScript: complex workflows where safer.
- Django/PostgreSQL: real business state.

## Debian Production

Deploy:

```bash
sudo ./install.sh deploy --domain=example.com
sudo ./install.sh status
sudo ./install.sh logs web
```

Production configuration:

```text
/etc/tuvtk/tuvtk.env
```

Default persistent data:

```text
/var/lib/tuvtk
```

Current production Compose/Nginx is HTTP-only. SSL flags are refused until HTTPS is implemented.

## Backup, Restore, and SQL

```bash
./install.sh backup BACKUP_DIRECTORY
./install.sh restore BACKUP_ARCHIVE
./install.sh export-sql OUTPUT_PATH
./install.sh import-sql DATABASE.sql
```

Restore and SQL import require confirmation unless `--yes` is supplied.

Use destructive database commands only in the intended environment.

## Local State

Generated and ignored paths:

- `.tuvtk/`
- `.venv/`
- `.postgresql/`
- `.env`
- `.env.dev`
- `media/`
- `private_media/`
- `staticfiles/`

Do not delete local state, media, environment files, Docker volumes, or production bind mounts unless the data is no longer needed.

## Safe Validation

```bash
python3 -m py_compile scripts/tuvtk_cli.py
python3 -m py_compile scripts/generate_codex_context.py
bash -n install.sh
bash -n bin/tuvtk
./install.sh help
git diff --check
```

On Windows:

```bat
install.cmd help
```

Do not use production lifecycle commands, builds, migrations, restore, SQL import, clean, or database reset merely as validation.
