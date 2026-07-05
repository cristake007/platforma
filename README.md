# Platforma TUVTK

Platforma TUVTK is a server-rendered Django application for TUVTK operational tools. It uses PostgreSQL, Tailwind CSS, daisyUI, Gunicorn, and Nginx.

## Primary workflow

Linux and Docker are the primary development and deployment environment. Normal operations should use the permanent wrapper:

```bash
tuvtk status
```

From a repository checkout, use the equivalent local path:

```bash
./bin/tuvtk status
```

The wrapper supplies the environment file, project directory, Compose files, and project name. Long raw `docker compose` commands are not needed for normal operation.

## Server paths

| Purpose | Default path |
| --- | --- |
| Application checkout | `/opt/tuvtk/app` |
| Environment and secrets | `/etc/tuvtk/tuvtk.env` |
| System command | `/usr/local/bin/tuvtk` |
| Backups | `/opt/tuvtk-backups` |
| Production Compose | `/opt/tuvtk/app/compose.yaml` |
| Development override | `/opt/tuvtk/app/compose.dev.yaml` |

Paths can be overridden with `TUVTK_APP_DIR`, `TUVTK_ENV_FILE`, `TUVTK_COMPOSE_FILE`, `TUVTK_DEV_COMPOSE_FILE`, and `TUVTK_PROJECT_NAME`.

## Fresh installation

On a supported Debian or Ubuntu server, run an HTTP installation as root:

```bash
sudo bash install.sh --yes \
  --repo-url=https://github.com/OWNER/REPOSITORY.git \
  --repo-branch=main \
  --domain=example.com
```

For an existing checkout with a configured `origin`, update and deploy with:

```bash
sudo bash install.sh --yes --domain=example.com
```

`--public-host` is a backward-compatible alias for `--domain`. The installer preserves existing environment values where possible, backs up configuration before overwriting it, builds the image, starts PostgreSQL, runs migrations/static collection through `init`, and starts Gunicorn and Nginx.

Use `bash install.sh --help` for all path, repository, database, IP-detection, and clean-install options. Treat `--clean` as an exceptional operation: review its backup and safety behavior before using it.

## Environment-only setup

Prepare or verify Debian/Ubuntu prerequisites without cloning the application or starting services:

```bash
sudo bash install.sh --environment
```

This checks or installs the required system packages, Docker Engine, and the Docker Compose plugin.

## Update command wrapper only

Update `/usr/local/bin/tuvtk` for an existing installation:

```bash
sudo bash install.sh --command
```

This action only installs the permanent command launcher. It does not reinstall the application, rebuild images, migrate the database, or restart services.

## Production operations

```bash
tuvtk status
tuvtk start
tuvtk stop
tuvtk restart
tuvtk logs
tuvtk logs web
tuvtk build
tuvtk rebuild
tuvtk check
```

`start` starts the production stack detached, `stop` runs Compose down without deleting persistent data, and `logs` follows all services or one named service. `check` runs `python manage.py check` in the `web` container. `rebuild` disables the image build cache and should be used deliberately.

## Development workflow

Development combines `compose.yaml` with `compose.dev.yaml` under the `tuvtk-dev` project name:

```bash
tuvtk dev
tuvtk dev-build
tuvtk dev-logs
tuvtk dev-logs web
```

`dev` starts isolated development PostgreSQL, runs the existing `init` migration/static step, then starts Django `runserver` and the Tailwind watcher. Development database, media, private media, static, Bootstrap cache, and Node modules use development-specific volumes. Production Nginx is not started by these commands, and PostgreSQL is not exposed publicly.

The Django development server listens on port `${TUVTK_DEV_PORT:-8000}`. For example, set `TUVTK_DEV_PORT=8080` before running `tuvtk dev` to publish port 8080.

## Tailwind and npm commands

```bash
tuvtk tailwind
tuvtk npm install
tuvtk npm run build
```

Node/npm run in the dedicated Node 22 development service, not in the production Python runtime image. The first Tailwind start runs `npm ci` when the development dependency volume is empty. `tuvtk tailwind` starts and follows the watcher logs.

## Django management commands

```bash
tuvtk migrate
tuvtk collectstatic
tuvtk django createsuperuser
tuvtk django <management-command> [arguments...]
```

Automated superuser creation in the installer is intentionally deferred. Use `tuvtk django createsuperuser` as the normal administrator-creation workflow.

## Testing

Run the full suite or a focused app/test path inside Docker:

```bash
tuvtk test
tuvtk test apps.dashboard
tuvtk test apps.dashboard -v 1
```

The wrapper adds `-v 0` by default. If `-v`, `--verbosity`, or `--verbosity=...` is supplied, it does not add another verbosity option.

## Backup and restore

```bash
tuvtk backup /opt/tuvtk-backups
tuvtk restore /opt/tuvtk-backups/tuvtk-backup-<timestamp>.tar.gz
tuvtk export-sql /opt/tuvtk-backups
tuvtk import-sql /path/to/database.sql
```

The wrapper backup contains a plain PostgreSQL dump, environment/configuration files, a manifest, and basic deployment files. It intentionally excludes media, private media, static files, and Docker volumes. Installer backups made before `--clean` are narrower deployment backups and do not include the database.

Restore is currently conservative: it validates the wrapper archive format and then refuses automated mutation until the restoration model receives dedicated operational testing. `import-sql` does mutate the active database and must be used only with an independently verified backup and an explicit recovery plan.

These commands do not by themselves provide complete disaster-recovery coverage. Test backup contents and restoration procedures before relying on them.

## Context generation for Codex

The primary generator is `scripts/generate_codex_context.py`:

```bash
tuvtk context
tuvtk context --verbose
tuvtk context --max-file-kb 80
```

Thin compatibility launchers are also available:

```bash
./generate_codex_context.sh
generate_codex_context.bat
generate_codex_context.ps1
```

Generated navigation files include `codex-context/`, `codex-context-index.md`, and `codex-file-map.txt`. The generator excludes environment files, secrets, media, binaries, node modules, migrations, and other generated/runtime content, and redacts common secret assignments.

## Dependency management

Direct dependency inputs and current installation manifests are paired as follows:

* `requirements.in` → `requirements.txt`
* `requirements-dev.in` → `requirements-dev.txt`
* `requirements-deploy.in` → `requirements-deploy.txt`

The `.in` files are readable direct-dependency inputs. Pip-tools was unavailable when this structure was introduced, so the `.txt` files currently remain pinned direct manifests rather than fabricated transitive locks. When pip-tools is available in an isolated maintenance environment, compile and review real locks with:

```bash
python -m piptools compile requirements.in --output-file requirements.txt
python -m piptools compile requirements-dev.in --output-file requirements-dev.txt
python -m piptools compile requirements-deploy.in --output-file requirements-deploy.txt
```

Do not claim a transitive lock exists until those commands have been run and their output reviewed. Direct pins include `psycopg[binary]==3.3.4`, `python-docx==1.2.0`, and `rapidfuzz==3.14.5`.

Docker images use versioned but patch-floating tags, including `python:3.12-slim-bookworm`, `node:22-bookworm-slim`, `postgres:17-bookworm`, and `nginx:1.28-alpine`. This allows upstream security/base-image patch updates. Digest pinning can be adopted later if byte-for-byte image reproducibility is required.

## SSL and domain notes

The current production deployment is HTTP-only. The installer accepts SSL-related options for future compatibility, but current Compose/Nginx does not implement certificate automation or an HTTPS listener. Requests using `--ssl --letsencrypt` or `--ssl --owncertificate` are safely refused before partial changes.

Implement and validate HTTPS explicitly in Compose and Nginx before enabling SSL options. Do not expose credentials or sensitive production data over the current HTTP mode.

## Removed legacy Windows workflow

The old Windows-local virtualenv, bundled PostgreSQL, runserver, and Tailwind watcher scripts were removed. Use Docker development mode instead. Windows support is limited to thin context-generator compatibility launchers; application development and deployment remain Docker-first.

## Validation and troubleshooting basics

Safe local checks:

```bash
bash -n install.sh
bash -n bin/tuvtk
bash -n generate_codex_context.sh
python3 -m py_compile scripts/generate_codex_context.py
./bin/tuvtk help
./bin/tuvtk context --max-file-kb 80
git diff --check
```

If `tuvtk` reports that Docker access requires sudo, either run it interactively where sudo can prompt or grant the operator appropriate Docker access. If a required path differs from the defaults, set the corresponding `TUVTK_*` environment variable. Use `tuvtk status` and `tuvtk logs [SERVICE]` before attempting rebuilds or restarts.
