# Source snapshot

## `README.md`

Size: 6.3 KB

````markdown
# Platforma TUVTK

Platforma TUVTK is a server-rendered Django application using PostgreSQL, Tailwind CSS, daisyUI, Gunicorn, and Nginx. It has one command vocabulary across Windows development and Debian 12 development/production.

## Start From a Clone

Debian/Linux:

```bash
git clone https://github.com/OWNER/REPOSITORY.git tuvtk
cd tuvtk
./install.sh dev
```

Windows Command Prompt, without administrator rights:

```bat
git clone https://github.com/OWNER/REPOSITORY.git tuvtk
cd tuvtk
install.cmd dev
```

PowerShell may use `.\install.ps1 dev`. Git Bash may use `./install.sh dev`; it delegates to PowerShell. The first `dev` run prepares dependencies, initializes PostgreSQL, installs Python and frontend packages, applies migrations, builds CSS, and starts development at `http://127.0.0.1:8000`.

Choose another development port with `dev --port=8001`.

## Platform Backends

On Windows, the wrapper uses user-space resources and does not register services or require administrator access:

- Python 3.12+ is installed privately when no compatible interpreter exists;
- `.venv` contains project Python packages;
- pinned Node 22 binaries are checksum-verified and downloaded under `.tuvtk/runtime` when unavailable;
- pinned PostgreSQL 17 binaries are checksum-verified and downloaded under `.postgresql`, with data kept in `.postgresql/data`;
- Django and Tailwind run as background processes with PID and log files under `.tuvtk`.

PostgreSQL listens only on `127.0.0.1` and uses password authentication. Windows supports development, tests, SQL, backup, and restore operations. Production deployment is intentionally refused on Windows.

On Debian 12, the shell launcher bootstraps Python 3 when necessary, then installs/verifies Docker Engine and the Compose plugin through the existing installer. Development uses isolated Compose volumes. Production keeps configuration in `/etc/tuvtk/tuvtk.env` and persistent data under `/var/lib/tuvtk` by default.

## Commands

Use `./install.sh` below on Linux. Replace it with `install.cmd` on Windows.

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

./install.sh fresh-db --yes --start
./install.sh tailwind
./install.sh npm run build
./install.sh context --max-file-kb 80
```

`test` defaults to verbosity 0 unless a verbosity option is supplied. `setup dev` prepares dependencies without starting Django or Tailwind. On Windows, `dev` runs Django and Tailwind in the current terminal and `Ctrl+C` stops both without opening additional console windows. Use `start` for hidden background processes; their output is written under `.tuvtk/logs`.

## Debian Production

Deploy and start production from a clone:

```bash
sudo ./install.sh deploy --domain=example.com
sudo ./install.sh status
sudo ./install.sh logs web
```

`deploy` prepares the environment, builds the image, starts and waits for
PostgreSQL, runs the `init` migration/static step, then starts `web` and
`nginx`. Optional installer settings pass through the wrapper:

```bash
sudo ./install.sh deploy --domain=example.com --http-port=8080 --data-dir=/var/lib/tuvtk
```

Production remains HTTP-only. The wrapper refuses the previous SSL compatibility flags because Compose/Nginx does not currently configure TLS.

Explicit production and development commands remain available on Debian:

```bash
sudo ./install.sh prod-status
sudo ./install.sh prod-start
sudo ./install.sh prod-stop
sudo ./install.sh dev-status
sudo ./install.sh dev-stop
```

Legacy installer invocations such as `sudo bash install.sh --dev --yes` and `sudo bash install.sh --production --yes --domain=example.com` remain temporarily supported. They may still generate the deprecated `command.sh`; the new command workflow does not generate or use it.

## Backup, Restore, and SQL

Unprefixed commands target the configured default mode. On Windows that mode is always development.

```bash
./install.sh backup BACKUP_DIRECTORY
./install.sh restore BACKUP_ARCHIVE
./install.sh export-sql OUTPUT_PATH
./install.sh import-sql DATABASE.sql
```

Restore and SQL import require confirmation unless `--yes` is supplied. Imports replace the selected database and leave application services stopped. Mode-marked production data is refused by Windows development.

`fresh-db` and `dev-db-reset` reset only the development database. On Windows this recreates `.postgresql/data`; on Debian development it removes the isolated `dev-postgres` Compose volume. Media, private media, static output, and Node modules are preserved.

Debian also supports explicit `prod-*` and `dev-*` variants. Production reset remains deliberately difficult to invoke:

```bash
sudo ./install.sh prod-db-reset --yes-i-understand-this-deletes-production-data
```

It creates a backup first unless `--no-backup` is explicitly supplied. Development reset can also be written as:

```bash
./install.sh fresh-db --yes --start
```

Test backups and restores in a disposable environment before relying on them for disaster recovery.

## Local State

These paths are generated and ignored by Git:

- `.tuvtk/`: downloaded runtime state, configuration, logs, and PIDs;
- `.venv/`: Windows Python virtual environment;
- `.postgresql/`: Windows PostgreSQL binaries and database cluster;
- `.env`: Windows-native development environment;
- `.env.dev`: Docker development environment;
- `media/`, `private_media/`, and `staticfiles/`: local generated or uploaded data.

Do not delete `.postgresql`, media, private media, production bind mounts, environment files, or Docker volumes unless the associated data is no longer required.

## Safe Validation

```bash
python3 -m py_compile scripts/tuvtk_cli.py
python3 -m py_compile scripts/generate_codex_context.py
bash -n install.sh
bash -n bin/tuvtk
./install.sh help
./install.sh context --max-file-kb 80
git diff --check
```

On Windows, validate the launcher with `install.cmd help`. Do not use production lifecycle commands, builds, migrations, restore, SQL import, clean, or database reset merely as validation.
````
