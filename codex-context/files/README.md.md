# Source snapshot

## `README.md`

Size: 3.4 KB

````markdown
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

## Frontend Rules

See:

```text
frontend.md
```

Short version:

- Tailwind/daisyUI: layout and components.
- HTMX: server-rendered partial updates.
- Alpine.js: local UI state only.
- Custom JavaScript: complex workflows where safer.
- Django/PostgreSQL: real business state.

## Codex Rules

See:

```text
AGENTS.md
```

For app-specific work, also read the target app file:

```text
apps/<app>/AGENTS.md
```

Use generated context only for discovery:

```text
codex-context/apps/<app>.md
codex-file-map.txt
```

Do not load the whole generated context for normal work.

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
````
