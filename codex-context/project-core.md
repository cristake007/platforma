# Project and shared context

Project-level, configuration, deployment, shared Django, and frontend source files. Generated snapshots under `codex-context/files/` contain the same authoritative-at-generation content.

## `AGENTS.md`

Size: 8.8 KB

````markdown
# Platforma TUVTK — Agent Router

## Scope and workflow

These instructions apply to the whole repository. A deeper `AGENTS.md` adds app-specific rules for files below its directory.

The repository is Linux/Docker-first. Use `bin/tuvtk` for normal Django, Compose, development, test, and context commands. Do not reconstruct long raw Compose commands unless validating Compose configuration itself.

Primary agent commands:

```bash
bin/tuvtk context --max-file-kb 80
bin/tuvtk check
bin/tuvtk test apps.dashboard
```

The shell, batch, and PowerShell context launchers are compatibility entry points only. `scripts/generate_codex_context.py` is the implementation; `bin/tuvtk context` is the primary workflow.

## Smallest sufficient context

Before editing:

1. Read the applicable `AGENTS.md` files from the repository root to the target directory.
2. If exact source paths are known, open those real files directly. Do not also read their generated snapshots.
3. If paths or dependencies are unclear, read only `codex-context/apps/<app>.md` for app work or `codex-context/project-core.md` for project/core/theme work.
4. Use `codex-file-map.txt` only to locate an unknown file. Use `codex-context-index.md` only for high-level orientation.
5. Open `codex-context/files/<real-path>.md` only for targeted orientation. Before editing, open the real source file, which is authoritative.
6. Expand into another app only when an import, URL, model relation, template include, navigation entry, or shared contract proves that dependency.

Do not preload the file map, context index, project core, every app guide, migration history, or unrelated tests for a local task. Broad reading is appropriate only for an explicit audit, cross-app change, or new application.

Generated context is navigation support, not a second source of truth. If stale, inspect real source and regenerate with:

```bash
bin/tuvtk context
```

## Repository boundaries

* `platforma_tuvtk/`: settings, root URL inclusion, ASGI, and WSGI only.
* `core/`: global shell, navigation, middleware, context processors, shared templates, and shared user profile behavior.
* `theme/`: Tailwind/daisyUI source theme and global shell JavaScript.
* `apps/`: business/domain Django apps. Each app owns its routes, views, forms, workflows, queries, validation, templates, static files, and focused tests.

Do not duplicate a model, route, service, selector, template, or workflow before searching the owning app. Keep cross-app dependencies explicit and narrow.

## Django contracts

* Keep views thin. Put writes and multi-step workflows in `services.py`, ownership-filtered reads in `selectors.py`, request/form validation in `forms.py`, and reusable domain validation in `validators.py`.
* Keep PostgreSQL as the source of truth. JavaScript may improve interaction but must not own validation or persistence.
* Require authentication where the surrounding app does. Scope user-owned objects by owner and return 404 for cross-owner access.
* Use CSRF protection and non-GET methods for state changes.
* Use namespaced app URLs. Include them from `platforma_tuvtk/urls.py` and update `core/navigation.py` only for global navigation.
* Create and review a Django migration for every schema change. Do not inspect all old migrations unless schema history is relevant.
* Normal Django execution occurs in Docker through `bin/tuvtk`; host Python is only required for the standard-library context generator.

## Shared frontend contract

* Server-rendered application pages extend `core/templates/layouts/base.html`. A deliberately standalone page such as login must still use `data-theme="tuvtk"` and the shared compiled stylesheet.
* Use semantic daisyUI/Tailwind tokens defined in `theme/static_src/src/styles.css`: `base-*`, `base-content`, `primary`, `secondary`, `accent`, `info`, `success`, `warning`, `error`, and `text-muted`.
* Do not add literal palette utilities, hex/RGB colors, or app-local chrome tokens. Add or adjust a global semantic token only when the design system lacks one. User-authored document/canvas colors are domain data.
* Use daisyUI components and existing shared templates/includes before custom markup. Keep interfaces compact, flat, responsive, keyboard accessible, and visibly focusable.
* Use `/diplome/istoric/` (`apps/diplome/templates/diplome/history_index.html`) as the canonical list-table model: compact `table-xs` density, bordered `base-*` surface, horizontal overflow, aligned columns, semantic status badges, right-aligned actions, and consistent empty state.
* Row actions in list tables are compact icon-only square buttons with `aria-label`, `title`, decorative SVGs marked `aria-hidden="true"`, and visible keyboard focus.
* Color table actions by intent with semantic tokens: `primary` for view/edit/navigation, `success` for download/confirm, `warning` for caution, and `error` for destructive actions.
* Use vanilla JavaScript with progressive enhancement. Preserve server-side validation and native navigation/scrolling.
* Every app whose templates/scripts use Tailwind classes needs an `@source` entry in `theme/static_src/src/styles.css`.
* Read `frontend.md` and the exact template/static files for frontend changes. Read shared base/theme files only when changing global layout or tokens.
* Tailwind/npm development runs through the dedicated Node service: `bin/tuvtk tailwind` and `bin/tuvtk npm ...`.

## Safety and preservation

* Preserve all unrelated tracked and untracked user changes. Never reset, discard, or overwrite them to simplify a task.
* Inspect `.env.example`; never inspect or expose `.env` or `/etc/tuvtk/tuvtk.env` contents unless explicitly required and authorized.
* Do not delete database volumes, persistent PostgreSQL storage, uploads, private media, secrets, or environment files.
* Do not run `install.sh --clean`, `bin/tuvtk clean`, restore, SQL import, or other destructive database/filesystem commands unless explicitly requested.
* Do not run full Docker rebuilds, production starts/restarts, migrations, collectstatic, npm installation, or service-changing commands merely for validation.
* Do not claim SSL works. Current Compose/Nginx is HTTP-only and installer SSL modes intentionally refuse.
* Do not reintroduce the removed Windows-local virtualenv, PostgreSQL, runserver, or Tailwind workflows. Windows batch/PowerShell files are context-generator compatibility launchers only.
* Preserve the Linux/Docker-first workflow and existing production lifecycle: build, start/wait for `db`, run `init`, then start `web` and `nginx`.

Avoid generated, runtime, dependency, binary, and local-tool paths unless directly required: `.venv/`, `.git/`, `.postgresql/`, `node_modules/`, `staticfiles/`, `media/`, `private_media/`, `.playwright-mcp/`, `test-results/`, `playwright-report/`, `apps/planificator-main/`, `theme/static/css/dist/`, `theme/static/fonts/`, and `theme/static/images/`.

## Verification policy

Choose the smallest checks that exercise the changed boundary. Do not run automated test suites by default because they are expensive and create database state. Provide focused test commands for the user unless execution is explicitly requested or necessary for a narrow diagnosis.

Primary project checks:

```bash
bin/tuvtk check
bin/tuvtk test <app-or-test-path>
```

The wrapper defaults tests to `-v 0`. Never run the full database-backed suite automatically.

Safe workflow checks:

```bash
bash -n install.sh
bash -n bin/tuvtk
bash -n generate_codex_context.sh
python3 -m py_compile scripts/generate_codex_context.py
bin/tuvtk help
bin/tuvtk context --max-file-kb 80
git diff --check
```

If `python3` is unavailable, use `python -m py_compile scripts/generate_codex_context.py`.

Optional read-only Compose rendering, only when Docker CLI and the deployment env file are available:

```bash
docker compose \
  --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app \
  -f /opt/tuvtk/app/compose.yaml \
  -p tuvtk config --quiet

docker compose \
  --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app \
  -f /opt/tuvtk/app/compose.yaml \
  -f /opt/tuvtk/app/compose.dev.yaml \
  -p tuvtk-dev config --quiet
```

For QA plans, cover invalid input, authorization and cross-owner access, destructive actions on referenced records, refresh/back navigation, and narrow-screen behavior where relevant.

## File hygiene and completion reports

Use small, reviewable changes. Keep established workflows unless the user explicitly requests replacement. Review model migrations for schema changes, but do not load migration history without a reason.

Completion reports must state:

* files changed or removed;
* behavior/instruction changes;
* migrations created, if any;
* checks actually run and checks skipped;
* whether context generation ran;
* remaining assumptions and manual checks.

After source or instruction changes, regenerate context from the repository root when the active task permits it:

```bash
bin/tuvtk context
```
````

## `compose.dev.yaml`

Size: 1.5 KB

```yaml
x-dev-app-volumes: &dev-app-volumes
  - type: bind
    source: .
    target: /app
  - type: volume
    source: dev-media
    target: /app/media
  - type: volume
    source: dev-private-media
    target: /app/private_media
  - type: volume
    source: dev-static
    target: /app/staticfiles
  - type: volume
    source: dev-bootstrap-cache
    target: /app/.bootstrap_icons_cache

services:
  db:
    volumes:
      - type: volume
        source: dev-postgres
        target: /var/lib/postgresql/data

  init:
    environment:
      DJANGO_DEBUG: "true"
    volumes: *dev-app-volumes

  web:
    command: ["python", "manage.py", "runserver", "0.0.0.0:8000"]
    environment:
      DJANGO_DEBUG: "true"
      DJANGO_ALLOWED_HOSTS: "127.0.0.1,localhost,[::1]"
      DJANGO_CSRF_TRUSTED_ORIGINS: "http://127.0.0.1:${TUVTK_DEV_PORT:-8000},http://localhost:${TUVTK_DEV_PORT:-8000}"
      DJANGO_TRUST_PROXY_HEADERS: "false"
      DJANGO_USE_X_FORWARDED_HOST: "false"
    ports:
      - "${TUVTK_DEV_PORT:-8000}:8000"
    volumes: *dev-app-volumes

  tailwind:
    image: node:22-bookworm-slim
    working_dir: /app/theme/static_src
    command:
      - /bin/sh
      - -ec
      - if [ ! -x node_modules/.bin/postcss ]; then npm ci; fi; exec npm run dev
    volumes:
      - type: bind
        source: .
        target: /app
      - type: volume
        source: dev-node-modules
        target: /app/theme/static_src/node_modules
    restart: unless-stopped

volumes:
  dev-postgres:
  dev-media:
  dev-private-media:
  dev-static:
  dev-bootstrap-cache:
  dev-node-modules:
```

## `compose.yaml`

Size: 3.7 KB

Redacted secret-like assignments: 3

```yaml
name: tuvtk

x-app-base: &app-base
  image: tuvtk-app:${TUVTK_IMAGE_TAG:-local}
  build:
    context: .
    target: runtime
  environment: &app-environment
    DJANGO_DEPLOYMENT_MODE: container
    DJANGO_SECRET_KEY: <redacted>
    DJANGO_DEBUG: "false"
    DJANGO_ALLOWED_HOSTS: ${DJANGO_ALLOWED_HOSTS:?DJANGO_ALLOWED_HOSTS is required}
    DJANGO_CSRF_TRUSTED_ORIGINS: ${DJANGO_CSRF_TRUSTED_ORIGINS:?DJANGO_CSRF_TRUSTED_ORIGINS is required}
    DJANGO_TRUST_PROXY_HEADERS: "true"
    DJANGO_USE_X_FORWARDED_HOST: "true"
    DJANGO_SECURE_SSL_REDIRECT: "false"
    DJANGO_SESSION_COOKIE_SECURE: "false"
    DJANGO_CSRF_COOKIE_SECURE: "false"
    DJANGO_STATIC_ROOT: /app/staticfiles
    DJANGO_MEDIA_ROOT: /app/media
    DJANGO_PRIVATE_MEDIA_ROOT: /app/private_media
    POSTGRES_DB: ${POSTGRES_DB:?POSTGRES_DB is required}
    POSTGRES_USER: ${POSTGRES_USER:?POSTGRES_USER is required}
    POSTGRES_PASSWORD: <redacted>
    POSTGRES_HOST: db
    POSTGRES_PORT: "5432"
    POSTGRES_CONN_MAX_AGE: ${POSTGRES_CONN_MAX_AGE:-60}
    POSTGRES_CONN_HEALTH_CHECKS: "true"
    GUNICORN_WORKERS: ${GUNICORN_WORKERS:-2}
    GUNICORN_TIMEOUT: ${GUNICORN_TIMEOUT:-900}
  volumes: &app-volumes
    - type: bind
      source: ${TUVTK_DATA_DIR:?TUVTK_DATA_DIR is required}/media
      target: /app/media
    - type: bind
      source: ${TUVTK_DATA_DIR:?TUVTK_DATA_DIR is required}/private-media
      target: /app/private_media
    - type: bind
      source: ${TUVTK_DATA_DIR:?TUVTK_DATA_DIR is required}/static
      target: /app/staticfiles
  depends_on:
    db:
      condition: service_healthy

services:
  db:
    image: postgres:17-bookworm
    environment:
      POSTGRES_DB: ${POSTGRES_DB:?POSTGRES_DB is required}
      POSTGRES_USER: ${POSTGRES_USER:?POSTGRES_USER is required}
      POSTGRES_PASSWORD: <redacted>
    volumes:
      - type: bind
        source: ${TUVTK_DATA_DIR:?TUVTK_DATA_DIR is required}/postgres
        target: /var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 24
      start_period: 10s
    restart: unless-stopped

  init:
    <<: *app-base
    command:
      - /bin/sh
      - -ec
      - python manage.py migrate --noinput && python manage.py collectstatic --noinput
    restart: "no"

  web:
    <<: *app-base
    command: ["/app/docker/start-web.sh"]
    healthcheck:
      test:
        - CMD
        - python
        - -c
        - import socket; connection = socket.create_connection(('127.0.0.1', 8000), 3); connection.close()
      interval: 10s
      timeout: 5s
      retries: 12
      start_period: 20s
    restart: unless-stopped

  nginx:
    image: nginx:1.28-alpine
    environment:
      TUVTK_PUBLIC_HOST: ${TUVTK_PUBLIC_HOST:?TUVTK_PUBLIC_HOST is required}
      NGINX_PROXY_TIMEOUT: ${NGINX_PROXY_TIMEOUT:-900s}
      NGINX_ENVSUBST_FILTER: ^(TUVTK_PUBLIC_HOST|NGINX_PROXY_TIMEOUT)$$
    ports:
      - ${TUVTK_HTTP_PORT:-80}:80
    volumes:
      - type: bind
        source: ./docker/nginx.conf.template
        target: /etc/nginx/templates/default.conf.template
        read_only: true
      - type: bind
        source: ${TUVTK_DATA_DIR:?TUVTK_DATA_DIR is required}/static
        target: /srv/static
        read_only: true
      - type: bind
        source: ${TUVTK_DATA_DIR:?TUVTK_DATA_DIR is required}/media
        target: /srv/media
        read_only: true
    depends_on:
      web:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://127.0.0.1/nginx-health"]
      interval: 10s
      timeout: 5s
      retries: 12
      start_period: 10s
    restart: unless-stopped
```

## `Dockerfile`

Size: 1.2 KB

```dockerfile
FROM node:22-bookworm-slim AS frontend

WORKDIR /build

COPY theme/static_src/package.json theme/static_src/package-lock.json ./theme/static_src/
RUN npm --prefix theme/static_src ci

COPY . .
RUN npm --prefix theme/static_src run build


FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install --yes --no-install-recommends ca-certificates fonts-liberation2 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 10001 tuvtk \
    && useradd --uid 10001 --gid tuvtk --create-home --home-dir /home/tuvtk tuvtk

WORKDIR /app

COPY requirements.txt requirements-deploy.txt ./
RUN python -m pip install --requirement requirements-deploy.txt

COPY . .
COPY --from=frontend /build/theme/static/css/dist/styles.css ./theme/static/css/dist/styles.css

RUN mkdir -p /app/staticfiles /app/media /app/private_media /app/.bootstrap_icons_cache \
    && chmod +x /app/docker/start-web.sh \
    && chown -R tuvtk:tuvtk /app/staticfiles /app/media /app/private_media /app/.bootstrap_icons_cache

USER tuvtk

EXPOSE 8000

CMD ["/app/docker/start-web.sh"]
```

## `install.sh`

Size: 29.5 KB

Redacted secret-like assignments: 1

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

readonly DEFAULT_APP_DIR="/opt/tuvtk/app"
readonly DEFAULT_ENV_FILE="/etc/tuvtk/tuvtk.env"
readonly DEFAULT_PROJECT_NAME="tuvtk"
readonly DEFAULT_DATA_DIR="/var/lib/tuvtk"
readonly DEFAULT_BACKUP_PATH="/opt/tuvtk-backups"
readonly WRAPPER_SYSTEM_PATH="/usr/local/bin/tuvtk"
readonly POSTGRES_IMAGE="postgres:17-bookworm"

APP_DIR="${TUVTK_APP_DIR:-$DEFAULT_APP_DIR}"
ENV_FILE="${TUVTK_ENV_FILE:-$DEFAULT_ENV_FILE}"
PROJECT_NAME="${TUVTK_PROJECT_NAME:-$DEFAULT_PROJECT_NAME}"
if [[ -n "${TUVTK_COMPOSE_FILE+x}" ]]; then
    COMPOSE_FILE="$TUVTK_COMPOSE_FILE"
    COMPOSE_FILE_EXPLICIT=true
else
    COMPOSE_FILE="$APP_DIR/compose.yaml"
    COMPOSE_FILE_EXPLICIT=false
fi
DATA_DIR="$DEFAULT_DATA_DIR"
DATA_DIR_EXPLICIT=false
BACKUP_PATH="$DEFAULT_BACKUP_PATH"
REPO_URL=""
REPO_BRANCH="main"
SSH_KEY=""
DOMAIN=""
EMAIL=""
HTTP_PORT="80"
HTTPS_PORT="443"
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
SECRET_KEY=<redacted>
ADMIN_USERNAME=""
ADMIN_EMAIL=""
ADMIN_PASSWORD=""
ACTION="install"
YES=false
CLEAN=false
SSL=false
LETSENCRYPT=false
OWN_CERTIFICATE=false
PUBLIC_IP=false
PRIVATE_IP=false
NETWORK_REQUESTED=false
ACTION_EXPLICIT=false
LAST_BACKUP=""

log() {
    printf '[tuvtk] %s\n' "$*"
}

warn() {
    printf '[tuvtk] WARNING: %s\n' "$*" >&2
}

fail() {
    printf '[tuvtk] ERROR: %s\n' "$*" >&2
    exit 1
}

usage() {
    cat <<'EOF'
Usage: install.sh [ACTION] [OPTIONS]

Actions:
  --environment              Install/check server prerequisites only
  --command                  Install/update only the tuvtk command wrapper
  --network                  Check external-network requirements (currently no-op)
  --clean                    Back up, then safely refresh deployment files

General options:
  -h, --help                 Show this help
  -y, --yes                  Skip confirmation prompts
  --backup-path=PATH         Backup destination (default: /opt/tuvtk-backups)
  --app-dir=PATH             Application directory (default: /opt/tuvtk/app)
  --install-dir=PATH         Backward-compatible alias for --app-dir
  --env-file=PATH            Environment file (default: /etc/tuvtk/tuvtk.env)
  --compose-file=PATH        Compose file (default: APP_DIR/compose.yaml)
  --project-name=NAME        Compose project name (default: tuvtk)
  --data-dir=PATH            Persistent data root (default: /var/lib/tuvtk)

Repository options:
  --repo-url=URL             Git repository URL; existing origin is used if omitted
  --repo-branch=BRANCH       Branch, tag, or commit (default: main)
  --ref=REF                  Backward-compatible alias for --repo-branch
  --ssh-key=PATH             Read-only SSH deploy key for a private repository

Public endpoint options:
  --domain=HOST              Public DNS name or IPv4 address
  --public-host=HOST         Backward-compatible alias for --domain
  --public-ip                Detect and use the public IPv4 address
  --private-ip               Detect and use the private IPv4 address
  --http-port=PORT           HTTP port (default: 80)
  --https-port=PORT          HTTPS port (default: 443)
  --ssl                      Request HTTPS mode
  --letsencrypt              Request Let's Encrypt mode (requires --ssl)
  --owncertificate           Request own-certificate mode (requires --ssl)
  --email=EMAIL              Let's Encrypt contact email

Database and Django options:
  --db-name=NAME
  --db-user=USER
  --db-password=PASSWORD
  --secret-key=KEY
  --admin-username=USERNAME
  --admin-email=EMAIL
  --admin-password=PASSWORD

Examples:
  sudo bash install.sh --environment
  sudo bash install.sh --command
  sudo bash install.sh --yes --domain=example.com
  sudo bash install.sh --clean --backup-path=/opt/tuvtk-backups --domain=example.com

HTTPS certificate automation is not present in the current Compose/Nginx design.
HTTPS requests are rejected before files, packages, or services are changed.
EOF
}

require_option_value() {
    local option="$1"
    local value="${2:-}"
    [[ -n "$value" && "$value" != --* ]] || fail "$option requires a value."
}

set_action() {
    local requested="$1"
    if [[ "$ACTION_EXPLICIT" == true && "$ACTION" != "$requested" ]]; then
        fail "actions --$ACTION and --$requested cannot be combined."
    fi
    ACTION="$requested"
    ACTION_EXPLICIT=true
}

parse_arguments() {
    while (($#)); do
        case "$1" in
            -h|--help) ACTION="help"; ACTION_EXPLICIT=true; shift ;;
            -y|--yes) YES=true; shift ;;
            --environment) set_action environment; shift ;;
            --command) set_action command; shift ;;
            --network) set_action network; NETWORK_REQUESTED=true; shift ;;
            --clean) CLEAN=true; shift ;;
            --backup-path=*) BACKUP_PATH="${1#*=}"; shift ;;
            --backup-path) require_option_value "$1" "${2:-}"; BACKUP_PATH="$2"; shift 2 ;;
            --app-dir=*|--install-dir=*) APP_DIR="${1#*=}"; shift ;;
            --app-dir|--install-dir) require_option_value "$1" "${2:-}"; APP_DIR="$2"; shift 2 ;;
            --env-file=*) ENV_FILE="${1#*=}"; shift ;;
            --env-file) require_option_value "$1" "${2:-}"; ENV_FILE="$2"; shift 2 ;;
            --compose-file=*) COMPOSE_FILE="${1#*=}"; COMPOSE_FILE_EXPLICIT=true; shift ;;
            --compose-file) require_option_value "$1" "${2:-}"; COMPOSE_FILE="$2"; COMPOSE_FILE_EXPLICIT=true; shift 2 ;;
            --project-name=*) PROJECT_NAME="${1#*=}"; shift ;;
            --project-name) require_option_value "$1" "${2:-}"; PROJECT_NAME="$2"; shift 2 ;;
            --data-dir=*) DATA_DIR="${1#*=}"; DATA_DIR_EXPLICIT=true; shift ;;
            --data-dir) require_option_value "$1" "${2:-}"; DATA_DIR="$2"; DATA_DIR_EXPLICIT=true; shift 2 ;;
            --repo-url=*) REPO_URL="${1#*=}"; shift ;;
            --repo-url) require_option_value "$1" "${2:-}"; REPO_URL="$2"; shift 2 ;;
            --repo-branch=*|--ref=*) REPO_BRANCH="${1#*=}"; shift ;;
            --repo-branch|--ref) require_option_value "$1" "${2:-}"; REPO_BRANCH="$2"; shift 2 ;;
            --ssh-key=*) SSH_KEY="${1#*=}"; shift ;;
            --ssh-key) require_option_value "$1" "${2:-}"; SSH_KEY="$2"; shift 2 ;;
            --domain=*|--public-host=*) DOMAIN="${1#*=}"; shift ;;
            --domain|--public-host) require_option_value "$1" "${2:-}"; DOMAIN="$2"; shift 2 ;;
            --public-ip) PUBLIC_IP=true; shift ;;
            --private-ip) PRIVATE_IP=true; shift ;;
            --email=*) EMAIL="${1#*=}"; shift ;;
            --email) require_option_value "$1" "${2:-}"; EMAIL="$2"; shift 2 ;;
            --ssl) SSL=true; shift ;;
            --letsencrypt) LETSENCRYPT=true; shift ;;
            --owncertificate) OWN_CERTIFICATE=true; shift ;;
            --http-port=*) HTTP_PORT="${1#*=}"; shift ;;
            --http-port) require_option_value "$1" "${2:-}"; HTTP_PORT="$2"; shift 2 ;;
            --https-port=*) HTTPS_PORT="${1#*=}"; shift ;;
            --https-port) require_option_value "$1" "${2:-}"; HTTPS_PORT="$2"; shift 2 ;;
            --db-name=*) DB_NAME="${1#*=}"; shift ;;
            --db-name) require_option_value "$1" "${2:-}"; DB_NAME="$2"; shift 2 ;;
            --db-user=*) DB_USER="${1#*=}"; shift ;;
            --db-user) require_option_value "$1" "${2:-}"; DB_USER="$2"; shift 2 ;;
            --db-password=*) DB_PASSWORD="${1#*=}"; shift ;;
            --db-password) require_option_value "$1" "${2:-}"; DB_PASSWORD="$2"; shift 2 ;;
            --secret-key=*) SECRET_KEY="${1#*=}"; shift ;;
            --secret-key) require_option_value "$1" "${2:-}"; SECRET_KEY="$2"; shift 2 ;;
            --admin-username=*) ADMIN_USERNAME="${1#*=}"; shift ;;
            --admin-username) require_option_value "$1" "${2:-}"; ADMIN_USERNAME="$2"; shift 2 ;;
            --admin-email=*) ADMIN_EMAIL="${1#*=}"; shift ;;
            --admin-email) require_option_value "$1" "${2:-}"; ADMIN_EMAIL="$2"; shift 2 ;;
            --admin-password=*) ADMIN_PASSWORD="${1#*=}"; shift ;;
            --admin-password) require_option_value "$1" "${2:-}"; ADMIN_PASSWORD="$2"; shift 2 ;;
            *) fail "unknown argument: $1" ;;
        esac
    done

    if [[ "$ACTION" == help ]]; then
        return 0
    fi
    if [[ "$COMPOSE_FILE_EXPLICIT" == false ]]; then
        COMPOSE_FILE="$APP_DIR/compose.yaml"
    fi
    if [[ "$ACTION" == install && "$DATA_DIR_EXPLICIT" == false && -f "$ENV_FILE" ]]; then
        local existing_data_dir
        existing_data_dir="$(read_env_value_from "$ENV_FILE" TUVTK_DATA_DIR)"
        if [[ -n "$existing_data_dir" ]]; then
            DATA_DIR="$existing_data_dir"
        fi
    fi
}

validate_absolute_path() {
    local label="$1" path="$2"
    [[ "$path" == /* && "$path" != "/" ]] || fail "$label must be an absolute path other than /."
    [[ "$path" != *$'\n'* ]] || fail "$label contains a newline."
}

validate_common_options() {
    validate_absolute_path "application directory" "$APP_DIR"
    validate_absolute_path "environment file" "$ENV_FILE"
    validate_absolute_path "Compose file" "$COMPOSE_FILE"
    validate_absolute_path "data directory" "$DATA_DIR"
    validate_absolute_path "backup path" "$BACKUP_PATH"
    [[ "$PROJECT_NAME" =~ ^[a-zA-Z0-9][a-zA-Z0-9_.-]*$ ]] || fail "invalid project name: $PROJECT_NAME"
    [[ "$HTTP_PORT" =~ ^[0-9]+$ && "$HTTP_PORT" -ge 1 && "$HTTP_PORT" -le 65535 ]] || fail "invalid HTTP port: $HTTP_PORT"
    [[ "$HTTPS_PORT" =~ ^[0-9]+$ && "$HTTPS_PORT" -ge 1 && "$HTTPS_PORT" -le 65535 ]] || fail "invalid HTTPS port: $HTTPS_PORT"
    [[ "$REPO_BRANCH" =~ ^[A-Za-z0-9][A-Za-z0-9._/@+-]*$ ]] || fail "unsafe repository branch/ref: $REPO_BRANCH"
    [[ "$DATA_DIR" != "$APP_DIR" && "$DATA_DIR" != "$APP_DIR/"* && "$APP_DIR" != "$DATA_DIR/"* ]] \
        || fail "application and persistent data directories must not overlap."
    if [[ -n "$REPO_URL" ]]; then
        [[ "$REPO_URL" == https://* || "$REPO_URL" == git@*:* ]] \
            || fail "repository URL must use HTTPS or git@host:path SSH syntax."
    fi
    if [[ -n "$SSH_KEY" ]]; then
        validate_absolute_path "SSH key" "$SSH_KEY"
        [[ -f "$SSH_KEY" ]] || fail "SSH key not found: $SSH_KEY"
    fi
    if [[ -n "$DB_NAME" ]]; then
        [[ "$DB_NAME" =~ ^[A-Za-z_][A-Za-z0-9_.-]*$ ]] || fail "invalid database name."
    fi
    if [[ -n "$DB_USER" ]]; then
        [[ "$DB_USER" =~ ^[A-Za-z_][A-Za-z0-9_.-]*$ ]] || fail "invalid database user."
    fi
}

validate_ssl_request() {
    [[ "$LETSENCRYPT" == false || "$SSL" == true ]] || fail "--letsencrypt requires --ssl."
    [[ "$OWN_CERTIFICATE" == false || "$SSL" == true ]] || fail "--owncertificate requires --ssl."
    [[ "$LETSENCRYPT" == false || "$OWN_CERTIFICATE" == false ]] || fail "choose either --letsencrypt or --owncertificate, not both."
    if [[ "$SSL" == true ]]; then
        [[ "$LETSENCRYPT" == true || "$OWN_CERTIFICATE" == true ]] \
            || fail "--ssl requires --letsencrypt or --owncertificate."
        fail "SSL mode requested, but the current Compose/Nginx deployment has no certificate automation or HTTPS listener. No changes were made."
    fi
}

require_root() {
    [[ "$EUID" -eq 0 ]] || fail "this action requires root; run it through sudo."
}

load_supported_os() {
    [[ -r /etc/os-release ]] || fail "/etc/os-release is missing; Debian or Ubuntu is required."
    # shellcheck disable=SC1091
    . /etc/os-release
    case "${ID:-}" in
        debian|ubuntu) ;;
        *) fail "unsupported distribution '${ID:-unknown}'; full installation supports Debian and Ubuntu only." ;;
    esac
    command -v dpkg >/dev/null 2>&1 || fail "dpkg is required on Debian/Ubuntu."
    case "$(dpkg --print-architecture)" in
        amd64|arm64) ;;
        *) fail "unsupported architecture; only amd64 and arm64 are supported." ;;
    esac
}

configure_docker_repository() {
    local docker_distribution="$ID"
    local docker_codename="${VERSION_CODENAME:-}"
    if [[ "$ID" == ubuntu && -n "${UBUNTU_CODENAME:-}" ]]; then
        docker_codename="$UBUNTU_CODENAME"
    fi
    [[ -n "$docker_codename" ]] || fail "could not determine the distribution codename."

    install -d -m 0755 /etc/apt/keyrings
    curl -fsSL "https://download.docker.com/linux/${docker_distribution}/gpg" -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
    cat > /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/${docker_distribution}
Suites: ${docker_codename}
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
}

install_prerequisites() {
    load_supported_os
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get install --yes ca-certificates curl git openssh-client openssl iproute2

    if ! command -v docker >/dev/null 2>&1; then
        log "Installing Docker Engine and the Compose plugin from Docker's official repository..."
        local conflicting=() package
        for package in docker.io docker-compose docker-compose-v2 podman-docker containerd runc; do
            if dpkg-query --show --showformat='${Status}' "$package" 2>/dev/null | grep -q 'install ok installed'; then
                conflicting+=("$package")
            fi
        done
        if ((${#conflicting[@]})); then
            apt-get remove --yes "${conflicting[@]}"
        fi
        configure_docker_repository
        apt-get update
        apt-get install --yes docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    elif ! docker compose version >/dev/null 2>&1; then
        log "Installing the Docker Compose plugin from Docker's official repository..."
        configure_docker_repository
        apt-get update
        apt-get install --yes docker-compose-plugin
    else
        log "Docker Engine and the Compose plugin are already installed."
    fi

    if command -v systemctl >/dev/null 2>&1; then
        systemctl enable --now docker
    fi
    docker info >/dev/null 2>&1 || fail "Docker is installed but its daemon is unavailable."
    docker compose version >/dev/null 2>&1 || fail "the Docker Compose plugin is unavailable."
}

read_env_value_from() {
    local file="$1" key="$2"
    [[ -f "$file" ]] || return 0
    awk -v key="$key" '
        $0 ~ "^[[:space:]]*" key "=" {
            sub("^[[:space:]]*" key "=", "")
            sub("\\r$", "")
            value=$0
        }
        END { print value }
    ' "$file"
}

set_env_value() {
    local key="$1" value="$2" temporary
    [[ "$value" != *$'\n'* && "$value" != *$'\r'* ]] || fail "environment value for $key contains a newline."
    temporary="$(mktemp "${ENV_FILE}.tmp.XXXXXX")"
    awk -v key="$key" '
        $0 ~ "^[[:space:]]*" key "=" { next }
        { print }
    ' "$ENV_FILE" >"$temporary"
    printf '%s=%s\n' "$key" "$value" >>"$temporary"
    chmod 0600 "$temporary"
    mv -f "$temporary" "$ENV_FILE"
}

ensure_env_value() {
    local key="$1" default_value="$2" existing
    existing="$(read_env_value_from "$ENV_FILE" "$key")"
    if [[ -z "$existing" ]]; then
        set_env_value "$key" "$default_value"
    fi
}

backup_existing_environment() {
    [[ -f "$ENV_FILE" ]] || return 0
    install -d -m 0700 "$BACKUP_PATH"
    local backup_file="$BACKUP_PATH/tuvtk.env.$(date -u +%Y%m%dT%H%M%SZ).bak"
    cp -p -- "$ENV_FILE" "$backup_file"
    chmod 0600 "$backup_file"
    log "Existing environment backed up to $backup_file"
}

write_environment() {
    local env_dir csrf_origin
    env_dir="$(dirname "$ENV_FILE")"
    install -d -m 0700 "$env_dir"
    if [[ -f "$ENV_FILE" ]]; then
        backup_existing_environment
        chmod 0600 "$ENV_FILE"
    else
        umask 077
        : >"$ENV_FILE"
    fi

    csrf_origin="http://$DOMAIN"
    if [[ "$HTTP_PORT" != 80 ]]; then
        csrf_origin="${csrf_origin}:$HTTP_PORT"
    fi
    ensure_env_value TUVTK_DATA_DIR "$DATA_DIR"
    ensure_env_value TUVTK_IMAGE_TAG local
    set_env_value TUVTK_PUBLIC_HOST "$DOMAIN"
    set_env_value TUVTK_HTTP_PORT "$HTTP_PORT"
    ensure_env_value NGINX_PROXY_TIMEOUT 900s
    ensure_env_value DJANGO_DEPLOYMENT_MODE container
    if [[ -n "$SECRET_KEY" ]]; then
        set_env_value DJANGO_SECRET_KEY "$SECRET_KEY"
    else
        ensure_env_value DJANGO_SECRET_KEY "$(openssl rand -hex 48)"
    fi
    set_env_value DJANGO_DEBUG false
    set_env_value DJANGO_ALLOWED_HOSTS "$DOMAIN"
    set_env_value DJANGO_CSRF_TRUSTED_ORIGINS "$csrf_origin"
    set_env_value DJANGO_TRUST_PROXY_HEADERS true
    set_env_value DJANGO_USE_X_FORWARDED_HOST true
    set_env_value DJANGO_SECURE_SSL_REDIRECT false
    set_env_value DJANGO_SESSION_COOKIE_SECURE false
    set_env_value DJANGO_CSRF_COOKIE_SECURE false
    if [[ -n "$DB_NAME" ]]; then set_env_value POSTGRES_DB "$DB_NAME"; else ensure_env_value POSTGRES_DB platforma_tuvtk; fi
    if [[ -n "$DB_USER" ]]; then set_env_value POSTGRES_USER "$DB_USER"; else ensure_env_value POSTGRES_USER tuvtk; fi
    if [[ -n "$DB_PASSWORD" ]]; then set_env_value POSTGRES_PASSWORD "$DB_PASSWORD"; else ensure_env_value POSTGRES_PASSWORD "$(openssl rand -hex 32)"; fi
    set_env_value POSTGRES_HOST db
    set_env_value POSTGRES_PORT 5432
    ensure_env_value POSTGRES_CONN_MAX_AGE 60
    ensure_env_value POSTGRES_CONN_HEALTH_CHECKS true
    ensure_env_value GUNICORN_WORKERS 2
    ensure_env_value GUNICORN_TIMEOUT 900
    chmod 0600 "$ENV_FILE"
}

validate_domain() {
    [[ -n "$DOMAIN" ]] || fail "a domain or IPv4 address is required."
    [[ ${#DOMAIN} -le 253 ]] || fail "domain/public host is too long."
    [[ "$DOMAIN" =~ ^[A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?$ ]] || fail "invalid domain or IPv4 address: $DOMAIN"
    [[ "$DOMAIN" != *".."* ]] || fail "invalid domain or IPv4 address: $DOMAIN"
}

detect_public_ip() {
    local detected
    detected="$(curl -4fsS --max-time 10 https://api.ipify.org || true)"
    [[ "$detected" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || fail "unable to detect a public IPv4 address."
    printf '%s' "$detected"
}

detect_private_ip() {
    local detected
    detected="$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{for (i=1; i<=NF; i++) if ($i == "src") {print $(i+1); exit}}')"
    [[ "$detected" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || fail "unable to detect a private IPv4 address."
    printf '%s' "$detected"
}

resolve_domain() {
    [[ "$PUBLIC_IP" == false || "$PRIVATE_IP" == false ]] || fail "--public-ip and --private-ip cannot be combined."
    if [[ -z "$DOMAIN" && "$PUBLIC_IP" == true ]]; then
        DOMAIN="$(detect_public_ip)"
    elif [[ -z "$DOMAIN" && "$PRIVATE_IP" == true ]]; then
        DOMAIN="$(detect_private_ip)"
    elif [[ -z "$DOMAIN" && -f "$ENV_FILE" ]]; then
        DOMAIN="$(read_env_value_from "$ENV_FILE" TUVTK_PUBLIC_HOST)"
    fi

    if [[ -z "$DOMAIN" && "$YES" == false ]]; then
        [[ -t 0 ]] || fail "no domain/public host was supplied and input is not interactive."
        read -r -p "Public domain or IPv4 address: " DOMAIN
    fi
    [[ -n "$DOMAIN" ]] || fail "--yes requires --domain, --public-ip, --private-ip, or an existing TUVTK_PUBLIC_HOST."
    validate_domain
}

confirm_full_install() {
    [[ "$YES" == true ]] && return 0
    [[ -t 0 ]] || fail "confirmation is required; rerun interactively or pass --yes."
    local answer
    printf 'Install/update TUVTK in %s for http://%s:%s? [y/N] ' "$APP_DIR" "$DOMAIN" "$HTTP_PORT"
    read -r answer
    [[ "$answer" == y || "$answer" == Y || "$answer" == yes || "$answer" == YES ]] || fail "installation cancelled."
}

configure_ssh() {
    [[ -n "$SSH_KEY" ]] || return 0
    [[ -s /etc/ssh/ssh_known_hosts ]] || fail "/etc/ssh/ssh_known_hosts must contain the repository host key."
    local escaped
    printf -v escaped '%q' "$SSH_KEY"
    export GIT_SSH_COMMAND="ssh -i ${escaped} -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile=/etc/ssh/ssh_known_hosts"
}

resolve_repository_url() {
    if [[ -z "$REPO_URL" && -d "$APP_DIR/.git" ]]; then
        REPO_URL="$(git -C "$APP_DIR" remote get-url origin 2>/dev/null || true)"
    fi
    [[ -n "$REPO_URL" ]] || fail "--repo-url is required when the application directory is not an existing Git checkout with an origin remote."
}

create_deployment_backup() {
    [[ -e "$APP_DIR" || -f "$ENV_FILE" ]] || return 0
    install -d -m 0700 "$BACKUP_PATH"
    local timestamp work archive relative
    timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
    work="$(mktemp -d "${TMPDIR:-/tmp}/tuvtk-installer-backup.XXXXXX")"
    archive="$BACKUP_PATH/tuvtk-deployment-${timestamp}.tar.gz"
    mkdir -p "$work/env" "$work/app"
    if [[ -f "$ENV_FILE" ]]; then
        cp -p -- "$ENV_FILE" "$work/env/tuvtk.env"
    fi
    for relative in compose.yaml Dockerfile bin/tuvtk docker/nginx.conf.template docker/start-web.sh; do
        if [[ -f "$APP_DIR/$relative" ]]; then
            mkdir -p "$work/app/$(dirname "$relative")"
            cp -p -- "$APP_DIR/$relative" "$work/app/$relative"
        fi
    done
    if [[ -f "$COMPOSE_FILE" && "$COMPOSE_FILE" != "$APP_DIR/compose.yaml" ]]; then
        cp -p -- "$COMPOSE_FILE" "$work/app/compose.yaml"
    fi
    printf 'format=tuvtk-installer-deployment-v1\ncreated_utc=%s\napp_dir=%s\nenv_file=%s\n' \
        "$timestamp" "$APP_DIR" "$ENV_FILE" >"$work/manifest"
    tar -C "$work" -czf "$archive" .
    rm -rf -- "$work"
    chmod 0600 "$archive"
    LAST_BACKUP="$archive"
    log "Deployment backup created: $archive"
    log "Database and media are excluded. For a full operational backup use: tuvtk backup $BACKUP_PATH"
}

ensure_clean_is_safe() {
    [[ -d "$APP_DIR/.git" ]] || fail "--clean requires an existing Git checkout; refusing ambiguous deletion."
    local changed path
    changed="$(git -C "$APP_DIR" status --porcelain --untracked-files=no)"
    while IFS= read -r path; do
        [[ -n "$path" ]] || continue
        path="${path:3}"
        case "$path" in
            compose.yaml|Dockerfile|bin/tuvtk|docker/*) ;;
            *) fail "--clean found tracked changes outside deployment files ($path); backup was created, but cleanup was refused." ;;
        esac
    done <<<"$changed"
}

checkout_source() {
    resolve_repository_url
    configure_ssh
    install -d -m 0755 "$(dirname "$APP_DIR")"

    if [[ ! -d "$APP_DIR/.git" ]]; then
        if [[ -e "$APP_DIR" && -n "$(find "$APP_DIR" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]]; then
            fail "application directory exists and is not an empty Git checkout: $APP_DIR"
        fi
        if [[ -d "$APP_DIR" ]]; then rmdir "$APP_DIR"; fi
        log "Cloning $REPO_URL..."
        git clone --no-checkout -- "$REPO_URL" "$APP_DIR"
    else
        local existing_remote
        existing_remote="$(git -C "$APP_DIR" remote get-url origin)"
        [[ "$existing_remote" == "$REPO_URL" ]] || fail "existing origin '$existing_remote' does not match '$REPO_URL'."
        if [[ "$CLEAN" == false && -n "$(git -C "$APP_DIR" status --porcelain --untracked-files=normal)" ]]; then
            fail "existing checkout has local changes; refusing to overwrite them."
        fi
    fi

    log "Fetching $REPO_BRANCH..."
    git -C "$APP_DIR" fetch --force --prune --tags origin "$REPO_BRANCH"
    if [[ "$CLEAN" == true ]]; then
        ensure_clean_is_safe
        rm -rf -- "$APP_DIR/Dockerfile" "$APP_DIR/compose.yaml" "$APP_DIR/docker" "$APP_DIR/bin/tuvtk"
    fi
    git -C "$APP_DIR" checkout --detach --force FETCH_HEAD
    [[ -f "$COMPOSE_FILE" && -f "$APP_DIR/Dockerfile" && -f "$APP_DIR/bin/tuvtk" ]] \
        || fail "selected revision is missing compose.yaml, Dockerfile, or bin/tuvtk."
}

prepare_data_directories() {
    log "Preparing persistent directories under $DATA_DIR..."
    docker pull "$POSTGRES_IMAGE" >/dev/null
    local postgres_uid postgres_gid
    postgres_uid="$(docker run --rm --entrypoint sh "$POSTGRES_IMAGE" -c 'id -u postgres')"
    postgres_gid="$(docker run --rm --entrypoint sh "$POSTGRES_IMAGE" -c 'id -g postgres')"
    install -d -m 0750 -o "$postgres_uid" -g "$postgres_gid" "$DATA_DIR/postgres"
    install -d -m 0755 -o 10001 -g 10001 "$DATA_DIR/media" "$DATA_DIR/static"
    install -d -m 0750 -o 10001 -g 10001 "$DATA_DIR/private-media"
}

install_wrapper() {
    local source="$APP_DIR/bin/tuvtk"
    [[ -f "$source" ]] || fail "wrapper source not found: $source"
    chmod 0755 "$source" || fail "unable to make wrapper executable: $source"
    if [[ ! -w "$(dirname "$WRAPPER_SYSTEM_PATH")" && "$EUID" -ne 0 ]]; then
        fail "writing $WRAPPER_SYSTEM_PATH requires root; rerun through sudo."
    fi
    local launcher
    launcher="$(mktemp "${TMPDIR:-/tmp}/tuvtk-launcher.XXXXXX")"
    {
        printf '#!/usr/bin/env bash\n'
        printf 'export TUVTK_APP_DIR=%q\n' "$APP_DIR"
        printf 'export TUVTK_ENV_FILE=%q\n' "$ENV_FILE"
        printf 'export TUVTK_COMPOSE_FILE=%q\n' "$COMPOSE_FILE"
        printf 'export TUVTK_PROJECT_NAME=%q\n' "$PROJECT_NAME"
        printf 'exec %q "$@"\n' "$source"
    } >"$launcher"
    local staged_system_path="${WRAPPER_SYSTEM_PATH}.tmp.$$"
    install -m 0755 "$launcher" "$staged_system_path" || {
        rm -f -- "$launcher"
        fail "unable to install wrapper launcher: $WRAPPER_SYSTEM_PATH"
    }
    mv -f -- "$staged_system_path" "$WRAPPER_SYSTEM_PATH" || {
        rm -f -- "$launcher" "$staged_system_path"
        fail "unable to activate wrapper launcher: $WRAPPER_SYSTEM_PATH"
    }
    rm -f -- "$launcher"
    [[ -x "$WRAPPER_SYSTEM_PATH" ]] || fail "installed wrapper is not executable: $WRAPPER_SYSTEM_PATH"
}

compose() {
    docker compose --env-file "$ENV_FILE" --project-directory "$APP_DIR" \
        -f "$COMPOSE_FILE" -p "$PROJECT_NAME" "$@"
}

port_is_listening() {
    local port="$1"
    ss -H -ltn "sport = :$port" 2>/dev/null | grep -q .
}

current_nginx_is_running() {
    [[ -f "$ENV_FILE" && -f "$COMPOSE_FILE" ]] || return 1
    compose ps --status running --services 2>/dev/null | grep -qx nginx
}

check_public_port() {
    local port="$1"
    if port_is_listening "$port"; then
        if current_nginx_is_running; then
            log "Port $port is currently used by this TUVTK deployment; continuing with update."
        else
            fail "public port $port is already in use. Stop the conflicting service before installation."
        fi
    fi
}

deploy_application() {
    log "Validating Compose configuration..."
    compose config --quiet
    log "Building application images..."
    compose build --pull
    log "Starting PostgreSQL and waiting for readiness..."
    compose up -d --wait --wait-timeout 180 db
    log "Applying migrations and collecting static files..."
    compose run --rm init
    log "Starting Gunicorn and Nginx..."
    compose up -d --wait --wait-timeout 180 --remove-orphans web nginx
    log "Running Django system checks..."
    compose exec -T web python manage.py check
}

admin_follow_up() {
    local supplied=0
    [[ -n "$ADMIN_USERNAME" ]] && ((supplied+=1))
    [[ -n "$ADMIN_EMAIL" ]] && ((supplied+=1))
    [[ -n "$ADMIN_PASSWORD" ]] && ((supplied+=1))
    if ((supplied > 0 && supplied < 3)); then
        fail "admin creation requires --admin-username, --admin-email, and --admin-password together."
    fi
    if ((supplied == 3)); then
        warn "Non-interactive superuser creation is intentionally deferred; the supplied admin credentials were not used."
        warn "Create the administrator with: tuvtk django createsuperuser"
    fi
}

print_command_summary() {
    cat <<EOF

TUVTK command wrapper installed.

Wrapper source: $APP_DIR/bin/tuvtk
System command: $WRAPPER_SYSTEM_PATH

Examples:
  tuvtk status
  tuvtk logs
  tuvtk check
  tuvtk test apps.dashboard
EOF
}

print_environment_summary() {
    cat <<'EOF'

TUVTK server prerequisites are ready.

Docker Engine and the Docker Compose plugin are available.
No application files were cloned or updated, and no services were started.
EOF
}

print_install_summary() {
    local public_url="http://$DOMAIN"
    if [[ "$HTTP_PORT" != 80 ]]; then
        public_url="${public_url}:$HTTP_PORT"
    fi
    cat <<EOF

TUVTK installation completed.

URL:             $public_url
Mode:            HTTP
Application:     $APP_DIR
Environment:     $ENV_FILE
Compose file:    $COMPOSE_FILE
Project name:    $PROJECT_NAME
Command wrapper: $WRAPPER_SYSTEM_PATH
Backup path:     $BACKUP_PATH
${LAST_BACKUP:+Deployment backup: $LAST_BACKUP}

Useful commands:
  tuvtk status
  tuvtk logs
  tuvtk check
  tuvtk test apps.dashboard
  tuvtk restart
  tuvtk backup $BACKUP_PATH

WARNING: HTTP does not encrypt credentials, cookies, or application data.
Do not use this mode for sensitive production traffic until HTTPS support is added.
EOF
}

run_environment_action() {
    require_root
    install -d -m 0755 "$APP_DIR"
    install -d -m 0700 "$(dirname "$ENV_FILE")"
    install_prerequisites
    print_environment_summary
}

run_command_action() {
    install_wrapper
    print_command_summary
}

run_network_action() {
    require_root
    log "compose.yaml does not declare an external Docker network; no network creation is required."
}

run_full_install() {
    validate_ssl_request
    resolve_domain
    confirm_full_install
    require_root
    admin_follow_up
    install_prerequisites
    check_public_port "$HTTP_PORT"
    create_deployment_backup
    checkout_source
    write_environment
    prepare_data_directories
    install_wrapper
    deploy_application
    print_install_summary
}

main() {
    parse_arguments "$@"
    if [[ "$ACTION" == help ]]; then
        usage
        return 0
    fi
    validate_common_options
    case "$ACTION" in
        environment)
            [[ "$CLEAN" == false ]] || fail "--clean cannot be combined with --environment."
            run_environment_action
            ;;
        command)
            [[ "$CLEAN" == false ]] || fail "--clean cannot be combined with --command."
            run_command_action
            ;;
        network)
            [[ "$CLEAN" == false ]] || fail "--clean cannot be combined with --network."
            run_network_action
            ;;
        install) run_full_install ;;
        *) fail "internal error: unsupported action $ACTION" ;;
    esac
}

main "$@"
```

## `manage.py`

Size: 671 B

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma_tuvtk.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```

## `package-lock.json`

Size: 75.0 KB

```json
{
  "name": "platforma-tuvtk-tools",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "platforma-tuvtk-tools",
      "devDependencies": {
        "repomix": "^1.16.0"
      }
    },
    "node_modules/@clack/core": {
      "version": "0.5.0",
      "resolved": "https://registry.npmjs.org/@clack/core/-/core-0.5.0.tgz",
      "integrity": "sha512-p3y0FIOwaYRUPRcMO7+dlmLh8PSRcrjuTndsiA0WAFbWES0mLZlrjVoBRZ9DzkPFJZG6KGkJmoEAY0ZcVWTkow==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "picocolors": "^1.0.0",
        "sisteransi": "^1.0.5"
      }
    },
    "node_modules/@clack/prompts": {
      "version": "0.11.0",
      "resolved": "https://registry.npmjs.org/@clack/prompts/-/prompts-0.11.0.tgz",
      "integrity": "sha512-pMN5FcrEw9hUkZA4f+zLlzivQSeQf5dRGJjSUbvVYDLvpKCdQx5OaknvKzgbtXOizhP+SJJJjqEbOe55uKKfAw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@clack/core": "0.5.0",
        "picocolors": "^1.0.0",
        "sisteransi": "^1.0.5"
      }
    },
    "node_modules/@hono/node-server": {
      "version": "1.19.14",
      "resolved": "https://registry.npmjs.org/@hono/node-server/-/node-server-1.19.14.tgz",
      "integrity": "sha512-GwtvgtXxnWsucXvbQXkRgqksiH2Qed37H9xHZocE5sA3N8O8O8/8FA3uclQXxXVzc9XBZuEOMK7+r02FmSpHtw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18.14.1"
      },
      "peerDependencies": {
        "hono": "^4"
      }
    },
    "node_modules/@isaacs/fs-minipass": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/@isaacs/fs-minipass/-/fs-minipass-4.0.1.tgz",
      "integrity": "sha512-wgm9Ehl2jpeqP3zw/7mo3kRHFp5MEDhqAdwy1fTGkHAwnkGOVsgpvQhL8B5n1qlb01jV3n/bI0ZfZp5lWA1k4w==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "minipass": "^7.0.4"
      },
      "engines": {
        "node": ">=18.0.0"
      }
    },
    "node_modules/@modelcontextprotocol/sdk": {
      "version": "1.29.0",
      "resolved": "https://registry.npmjs.org/@modelcontextprotocol/sdk/-/sdk-1.29.0.tgz",
      "integrity": "sha512-zo37mZA9hJWpULgkRpowewez1y6ML5GsXJPY8FI0tBBCd77HEvza4jDqRKOXgHNn867PVGCyTdzqpz0izu5ZjQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@hono/node-server": "^1.19.9",
        "ajv": "^8.17.1",
        "ajv-formats": "^3.0.1",
        "content-type": "^1.0.5",
        "cors": "^2.8.5",
        "cross-spawn": "^7.0.5",
        "eventsource": "^3.0.2",
        "eventsource-parser": "^3.0.0",
        "express": "^5.2.1",
        "express-rate-limit": "^8.2.1",
        "hono": "^4.11.4",
        "jose": "^6.1.3",
        "json-schema-typed": "^8.0.2",
        "pkce-challenge": "^5.0.0",
        "raw-body": "^3.0.0",
        "zod": "^3.25 || ^4.0",
        "zod-to-json-schema": "^3.25.1"
      },
      "engines": {
        "node": ">=18"
      },
      "peerDependencies": {
        "@cfworker/json-schema": "^4.1.1",
        "zod": "^3.25 || ^4.0"
      },
      "peerDependenciesMeta": {
        "@cfworker/json-schema": {
          "optional": true
        },
        "zod": {
          "optional": false
        }
      }
    },
    "node_modules/@nodelib/fs.scandir": {
      "version": "2.1.5",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.scandir/-/fs.scandir-2.1.5.tgz",
      "integrity": "sha512-vq24Bq3ym5HEQm2NKCr3yXDwjc7vTsEThRDnkp2DK9p1uqLR+DHurm/NOTo0KG7HYHU7eppKZj3MyqYuMBf62g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.stat": "2.0.5",
        "run-parallel": "^1.1.9"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nodelib/fs.stat": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.stat/-/fs.stat-2.0.5.tgz",
      "integrity": "sha512-RkhPPp2zrqDAQA/2jNhnztcPAlv64XdhIp7a7454A5ovI7Bukxgt7MX7udwAu3zg1DcpPU0rz3VV1SeaqvY4+A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nodelib/fs.walk": {
      "version": "1.2.8",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.walk/-/fs.walk-1.2.8.tgz",
      "integrity": "sha512-oGB+UxlgWcgQkgwo8GcEGwemoTFt3FIO9ababBmaGwXIoBKZ+GTy0pP185beGg7Llih/NSHSV2XAs1lnznocSg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.scandir": "2.1.5",
        "fastq": "^1.6.0"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@repomix/strip-comments": {
      "version": "2.4.2",
      "resolved": "https://registry.npmjs.org/@repomix/strip-comments/-/strip-comments-2.4.2.tgz",
      "integrity": "sha512-7a18ODb043eszMBr6mpVWz802xIRMzdmptarVxTtnMIW7ZQzba/v8jLp3kcHUHb76uRkyJRPpGSwdm7+8GmsEA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/@repomix/tree-sitter-wasms": {
      "version": "0.1.17",
      "resolved": "https://registry.npmjs.org/@repomix/tree-sitter-wasms/-/tree-sitter-wasms-0.1.17.tgz",
      "integrity": "sha512-tc3HnFqdMF1pXhIMzG3aTaBDpIiHK2tPfn3fwqA6P3WTbHa+1EuuTubbKshvmN7xCHP5Ojz0/VW4R+XvR88KOw==",
      "dev": true,
      "license": "Unlicense"
    },
    "node_modules/@secretlint/core": {
      "version": "13.0.2",
      "resolved": "https://registry.npmjs.org/@secretlint/core/-/core-13.0.2.tgz",
      "integrity": "sha512-15vg+zCmjQuDFVoOPNt0TyEu0Z95eir2MO19++wG82yM/vbPtFu/m9qd6oh54ZOBXgMcchdGDTxMwJNDnCLxcA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@secretlint/profiler": "13.0.2",
        "@secretlint/types": "13.0.2",
        "debug": "^4.4.3",
        "structured-source": "^4.0.0"
      },
      "engines": {
        "node": ">=22.0.0"
      }
    },
    "node_modules/@secretlint/profiler": {
      "version": "13.0.2",
      "resolved": "https://registry.npmjs.org/@secretlint/profiler/-/profiler-13.0.2.tgz",
      "integrity": "sha512-vGaLZCoi9KewOF+sM0iIEBviWaH9mls1HmQFBgEPq4fnvmVO4PfKIkVr4CcAFm3Msg4NjzFE2RBAGwRR+5HEmQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@secretlint/secretlint-rule-preset-recommend": {
      "version": "13.0.2",
      "resolved": "https://registry.npmjs.org/@secretlint/secretlint-rule-preset-recommend/-/secretlint-rule-preset-recommend-13.0.2.tgz",
      "integrity": "sha512-D03Kw51qOgffj9zNlJFZUarVmP8zGcCZNi7A14+vZtHskbbBPEsS/f09idb48rrlMSaRMBN29IkqfbmPyL9xtw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=22.0.0"
      }
    },
    "node_modules/@secretlint/types": {
      "version": "13.0.2",
      "resolved": "https://registry.npmjs.org/@secretlint/types/-/types-13.0.2.tgz",
      "integrity": "sha512-cAZjr6ZTKgSuJMLyTGDrUEtK3XEZa+JStIkD+DmdkT32VGAN+dQJiYr1So3XJopsKSrqhP5kjZKT8WWtftZIpQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=22.0.0"
      }
    },
    "node_modules/@sindresorhus/merge-streams": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/@sindresorhus/merge-streams/-/merge-streams-4.0.0.tgz",
      "integrity": "sha512-tlqY9xq5ukxTUZBmoOp+m61cqwQD5pHJtFY3Mn8CA8ps6yghLH/Hw8UPdqg4OLmFW3IFlcXnQNmo/dh8HzXYIQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/@types/parse-path": {
      "version": "7.0.3",
      "resolved": "https://registry.npmjs.org/@types/parse-path/-/parse-path-7.0.3.tgz",
      "integrity": "sha512-LriObC2+KYZD3FzCrgWGv/qufdUy4eXrxcLgQMfYXgPbLIecKIsVBaQgUPmxSSLcjmYbDTQbMgr6qr6l/eb7Bg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/accepts": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/accepts/-/accepts-2.0.0.tgz",
      "integrity": "sha512-5cvg6CtKwfgdmVqY1WIiXKc3Q1bkRqGLi+2W/6ao+6Y7gu/RCwRuAhGEzh5B4KlszSuTLgZYuqFqo5bImjNKng==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "mime-types": "^3.0.0",
        "negotiator": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/ajv": {
      "version": "8.20.0",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-8.20.0.tgz",
      "integrity": "sha512-Thbli+OlOj+iMPYFBVBfJ3OmCAnaSyNn4M1vz9T6Gka5Jt9ba/HIR56joy65tY6kx/FCF5VXNB819Y7/GUrBGA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.3",
        "fast-uri": "^3.0.1",
        "json-schema-traverse": "^1.0.0",
        "require-from-string": "^2.0.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/ajv-formats": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/ajv-formats/-/ajv-formats-3.0.1.tgz",
      "integrity": "sha512-8iUql50EUR+uUcdRQ3HDqa6EVyo3docL8g5WJ3FNcWmu62IbkGUue/pEyLBW8VGKKucTPgqeks4fIU1DA4yowQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ajv": "^8.0.0"
      },
      "peerDependencies": {
        "ajv": "^8.0.0"
      },
      "peerDependenciesMeta": {
        "ajv": {
          "optional": true
        }
      }
    },
    "node_modules/balanced-match": {
      "version": "4.0.4",
      "resolved": "https://registry.npmjs.org/balanced-match/-/balanced-match-4.0.4.tgz",
      "integrity": "sha512-BLrgEcRTwX2o6gGxGOCNyMvGSp35YofuYzw9h1IMTRmKqttAZZVU67bdb9Pr2vUHA8+j3i2tJfjO6C6+4myGTA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "18 || 20 || >=22"
      }
    },
    "node_modules/binary-extensions": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/binary-extensions/-/binary-extensions-3.1.0.tgz",
      "integrity": "sha512-Jvvd9hy1w+xUad8+ckQsWA/V1AoyubOvqn0aygjMOVM4BfIaRav1NFS3LsTSDaV4n4FtcCtQXvzep1E6MboqwQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18.20"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/body-parser": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/body-parser/-/body-parser-2.3.0.tgz",
      "integrity": "sha512-2cGmJupaNgg+QUwVLAucDuWuoMZ6EX9iHDRswZ5lsNYEmwPaRknMPCLZz07yTzVq/83p4o/wzbDZbBrTvGGTIw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "bytes": "^3.1.2",
        "content-type": "^2.0.0",
        "debug": "^4.4.3",
        "http-errors": "^2.0.1",
        "iconv-lite": "^0.7.2",
        "on-finished": "^2.4.1",
        "qs": "^6.15.2",
        "raw-body": "^3.0.2",
        "type-is": "^2.1.0"
      },
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/body-parser/node_modules/content-type": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/content-type/-/content-type-2.0.0.tgz",
      "integrity": "sha512-j/O/d7GcZCyNl7/hwZAb606rzqkyvaDctLmckbxLzHvFBzTJHuGEdodATcP3yIRoDrLHkIATJuvzbFlp/ki2cQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/boundary": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/boundary/-/boundary-2.0.0.tgz",
      "integrity": "sha512-rJKn5ooC9u8q13IMCrW0RSp31pxBCHE3y9V/tp3TdWSLf8Em3p6Di4NBpfzbJge9YjjFEsD0RtFEjtvHL5VyEA==",
      "dev": true,
      "license": "BSD-2-Clause"
    },
    "node_modules/brace-expansion": {
      "version": "5.0.7",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-5.0.7.tgz",
      "integrity": "sha512-7oFy703dxfY3/NLxC1fh2SUCQ0H9rmAY+5EpDVfXjUTTs+HEwR2nYaqLv+GWcTsumwxPfiz6CzCNkwXwBUwqCA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "balanced-match": "^4.0.2"
      },
      "engines": {
        "node": "18 || 20 || >=22"
      }
    },
    "node_modules/braces": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/braces/-/braces-3.0.3.tgz",
      "integrity": "sha512-yQbXgO/OSZVD2IsiLlro+7Hf6Q18EJrKSEsdoMzKePKXct3gvD8oLcOQdIzGupr5Fj+EDe8gO/lxc1BzfMpxvA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "fill-range": "^7.1.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/bytes": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/bytes/-/bytes-3.1.2.tgz",
      "integrity": "sha512-/Nf7TyzTx6S3yRJObOAV7956r8cr2+Oj8AC5dt8wSP3BQAoeX58NoHyCU8P8zGkNXStjTSi6fzO6F0pBdcYbEg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/call-bind-apply-helpers": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/call-bind-apply-helpers/-/call-bind-apply-helpers-1.0.2.tgz",
      "integrity": "sha512-Sp1ablJ0ivDkSzjcaJdxEunN5/XvksFJ2sMBFfq6x0ryhQV/2b/KwFe21cMpmHtPOSij8K99/wSfoEuTObmuMQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/call-bound": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/call-bound/-/call-bound-1.0.4.tgz",
      "integrity": "sha512-+ys997U96po4Kx/ABpBCqhA9EuxJaQWDQg7295H4hBphv3IZg0boBKuwYpt4YXp6MZ5AmZQnU/tyMTlRpaSejg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "get-intrinsic": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/chokidar": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/chokidar/-/chokidar-5.0.0.tgz",
      "integrity": "sha512-TQMmc3w+5AxjpL8iIiwebF73dRDF4fBIieAqGn9RGCWaEVwQ6Fb2cGe31Yns0RRIzii5goJ1Y7xbMwo1TxMplw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "readdirp": "^5.0.0"
      },
      "engines": {
        "node": ">= 20.19.0"
      },
      "funding": {
        "url": "https://paulmillr.com/funding/"
      }
    },
    "node_modules/chownr": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/chownr/-/chownr-3.0.0.tgz",
      "integrity": "sha512-+IxzY9BZOQd/XuYPRmrvEVjF/nqj5kgT4kEq7VofrDoM1MxoRjEWkrCC3EtLi59TVawxTAn+orJwFQcrqEN1+g==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/commander": {
      "version": "15.0.0",
      "resolved": "https://registry.npmjs.org/commander/-/commander-15.0.0.tgz",
      "integrity": "sha512-z67u4ZhzCL/Tydu1lJARtEZYWbWaN7oYLHbsuzocr6y4N6WZAagG3RQ4FW61V1/0+jImpj293XfrcYnd1qxtPg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=22.12.0"
      }
    },
    "node_modules/content-disposition": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/content-disposition/-/content-disposition-1.1.0.tgz",
      "integrity": "sha512-5jRCH9Z/+DRP7rkvY83B+yGIGX96OYdJmzngqnw2SBSxqCFPd0w2km3s5iawpGX8krnwSGmF0FW5Nhr0Hfai3g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/content-type": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/content-type/-/content-type-1.0.5.tgz",
      "integrity": "sha512-nTjqfcBFEipKdXCv4YDQWCfmcLZKm81ldF0pAopTvyrFGVbcR6P/VAAd5G7N+0tTr8QqiU0tFadD6FK4NtJwOA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/cookie": {
      "version": "0.7.2",
      "resolved": "https://registry.npmjs.org/cookie/-/cookie-0.7.2.tgz",
      "integrity": "sha512-yki5XnKuf750l50uGTllt6kKILY4nQ1eNIQatoXEByZ5dWgnKqbnqmTrBE5B4N7lrMJKQ2ytWMiTO2o0v6Ew/w==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/cookie-signature": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/cookie-signature/-/cookie-signature-1.2.2.tgz",
      "integrity": "sha512-D76uU73ulSXrD1UXF4KE2TMxVVwhsnCgfAyTg9k8P6KGZjlXKrOLe4dJQKI3Bxi5wjesZoFXJWElNWBjPZMbhg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.6.0"
      }
    },
    "node_modules/cors": {
      "version": "2.8.6",
      "resolved": "https://registry.npmjs.org/cors/-/cors-2.8.6.tgz",
      "integrity": "sha512-tJtZBBHA6vjIAaF6EnIaq6laBBP9aq/Y3ouVJjEfoHbRBcHBAHYcMh/w8LDrk2PvIMMq8gmopa5D4V8RmbrxGw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "object-assign": "^4",
        "vary": "^1"
      },
      "engines": {
        "node": ">= 0.10"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/cross-spawn": {
      "version": "7.0.6",
      "resolved": "https://registry.npmjs.org/cross-spawn/-/cross-spawn-7.0.6.tgz",
      "integrity": "sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "path-key": "^3.1.0",
        "shebang-command": "^2.0.0",
        "which": "^2.0.1"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/debug": {
      "version": "4.4.3",
      "resolved": "https://registry.npmjs.org/debug/-/debug-4.4.3.tgz",
      "integrity": "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.3"
      },
      "engines": {
        "node": ">=6.0"
      },
      "peerDependenciesMeta": {
        "supports-color": {
          "optional": true
        }
      }
    },
    "node_modules/depd": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/depd/-/depd-2.0.0.tgz",
      "integrity": "sha512-g7nH6P6dyDioJogAAGprGpCtVImJhpPk/roCzdb3fIh61/s/nPsfR6onyMwkCAR/OlC3yBC0lESvUoQEAssIrw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/dunder-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/dunder-proto/-/dunder-proto-1.0.1.tgz",
      "integrity": "sha512-KIN/nDJBQRcXw0MLVhZE9iQHmG68qAVIBg9CqmUYjmQIhgij9U5MFvrqkUL5FbtyyzZuOeOt0zdeRe4UY7ct+A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.1",
        "es-errors": "^1.3.0",
        "gopd": "^1.2.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/ee-first": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/ee-first/-/ee-first-1.1.1.tgz",
      "integrity": "sha512-WMwm9LhRUo+WUaRN+vRuETqG89IgZphVSNkdFgeb6sS/E4OrDIN7t48CAewSHXc6C8lefD8KKfr5vY61brQlow==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/encodeurl": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/encodeurl/-/encodeurl-2.0.0.tgz",
      "integrity": "sha512-Q0n9HRi4m6JuGIV1eFlmvJB7ZEVxu93IrMyiMsGC0lrMJMWzRgx6WGquyfQgZVb31vhGgXnfmPNNXmxnOkRBrg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/es-define-property": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/es-define-property/-/es-define-property-1.0.1.tgz",
      "integrity": "sha512-e3nRfgfUZ4rNGL232gUgX06QNyyez04KdjFrF+LTRoOXmrOgFKDg4BCdsjW8EnT69eqdYGmRpJwiPVYNrCaW3g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-errors": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-errors/-/es-errors-1.3.0.tgz",
      "integrity": "sha512-Zf5H2Kxt2xjTvbJvP2ZWLEICxA6j+hAmMzIlypy4xcBg1vKVnx89Wy0GbS+kf5cwCVFFzdCFh2XSCFNULS6csw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-object-atoms": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/es-object-atoms/-/es-object-atoms-1.1.2.tgz",
      "integrity": "sha512-HWcBoN6NileqtSydK2FqHbS/LoDd2pqrnQHLyJzBj4kOp/ky2MWMN694xOfkK8/SnUsW2DH7EfyVlydKCsm1Zw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/escape-html": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/escape-html/-/escape-html-1.0.3.tgz",
      "integrity": "sha512-NiSupZ4OeuGwr68lGIeym/ksIZMJodUGOSCZ/FSnTxcrekbvqrgdUxlJOMpijaKZVjAJrWrGs/6Jy8OMuyj9ow==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/etag": {
      "version": "1.8.1",
      "resolved": "https://registry.npmjs.org/etag/-/etag-1.8.1.tgz",
      "integrity": "sha512-aIL5Fx7mawVa300al2BnEE4iNvo1qETxLrPI/o05L7z6go7fCw1J6EQmbK4FmJ2AS7kgVF/KEZWufBfdClMcPg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/eventsource": {
      "version": "3.0.7",
      "resolved": "https://registry.npmjs.org/eventsource/-/eventsource-3.0.7.tgz",
      "integrity": "sha512-CRT1WTyuQoD771GW56XEZFQ/ZoSfWid1alKGDYMmkt2yl8UXrVR4pspqWNEcqKvVIzg6PAltWjxcSSPrboA4iA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "eventsource-parser": "^3.0.1"
      },
      "engines": {
        "node": ">=18.0.0"
      }
    },
    "node_modules/eventsource-parser": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/eventsource-parser/-/eventsource-parser-3.1.0.tgz",
      "integrity": "sha512-kJezFj9YFAMLeORyi7aCLxLbD5/qWMQnoMVlVPyHIll7lgRJCc3JVln9Vgl9nwQi0YkMnhdGTMNn7CkRRAptMg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18.0.0"
      }
    },
    "node_modules/express": {
      "version": "5.2.1",
      "resolved": "https://registry.npmjs.org/express/-/express-5.2.1.tgz",
      "integrity": "sha512-hIS4idWWai69NezIdRt2xFVofaF4j+6INOpJlVOLDO8zXGpUVEVzIYk12UUi2JzjEzWL3IOAxcTubgz9Po0yXw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "accepts": "^2.0.0",
        "body-parser": "^2.2.1",
        "content-disposition": "^1.0.0",
        "content-type": "^1.0.5",
        "cookie": "^0.7.1",
        "cookie-signature": "^1.2.1",
        "debug": "^4.4.0",
        "depd": "^2.0.0",
        "encodeurl": "^2.0.0",
        "escape-html": "^1.0.3",
        "etag": "^1.8.1",
        "finalhandler": "^2.1.0",
        "fresh": "^2.0.0",
        "http-errors": "^2.0.0",
        "merge-descriptors": "^2.0.0",
        "mime-types": "^3.0.0",
        "on-finished": "^2.4.1",
        "once": "^1.4.0",
        "parseurl": "^1.3.3",
        "proxy-addr": "^2.0.7",
        "qs": "^6.14.0",
        "range-parser": "^1.2.1",
        "router": "^2.2.0",
        "send": "^1.1.0",
        "serve-static": "^2.2.0",
        "statuses": "^2.0.1",
        "type-is": "^2.0.1",
        "vary": "^1.1.2"
      },
      "engines": {
        "node": ">= 18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/express-rate-limit": {
      "version": "8.5.2",
      "resolved": "https://registry.npmjs.org/express-rate-limit/-/express-rate-limit-8.5.2.tgz",
      "integrity": "sha512-5Kb34ipNX694DH48vN9irak1Qx30nb0PLYHXfJgw4YEjiC3ZEmZJhwOp+VfiCYwFzvFTdB9QkArYS5kXa2cx2A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ip-address": "^10.2.0"
      },
      "engines": {
        "node": ">= 16"
      },
      "funding": {
        "url": "https://github.com/sponsors/express-rate-limit"
      },
      "peerDependencies": {
        "express": ">= 4.11"
      }
    },
    "node_modules/fast-deep-equal": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/fast-deep-equal/-/fast-deep-equal-3.1.3.tgz",
      "integrity": "sha512-f3qQ9oQy9j2AhBe/H9VC91wLmKBCCU/gDOnKNAYG5hswO7BLKj09Hc5HYNz9cGI++xlpDCIgDaitVs03ATR84Q==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/fast-glob": {
      "version": "3.3.3",
      "resolved": "https://registry.npmjs.org/fast-glob/-/fast-glob-3.3.3.tgz",
      "integrity": "sha512-7MptL8U0cqcFdzIzwOTHoilX9x5BrNqye7Z/LuC7kCMRio1EMSyqRK3BEAUD7sXRq4iT4AzTVuZdhgQ2TCvYLg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.stat": "^2.0.2",
        "@nodelib/fs.walk": "^1.2.3",
        "glob-parent": "^5.1.2",
        "merge2": "^1.3.0",
        "micromatch": "^4.0.8"
      },
      "engines": {
        "node": ">=8.6.0"
      }
    },
    "node_modules/fast-uri": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/fast-uri/-/fast-uri-3.1.3.tgz",
      "integrity": "sha512-i70LwGWUduXqzicKXWshooq+sWL1K3WUU5rKZNG/0i3a1OSoX3HqhH5WbWwTmqWfor4urUakGPiRQcleRZTwOg==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/fastify"
        },
        {
          "type": "opencollective",
          "url": "https://opencollective.com/fastify"
        }
      ],
      "license": "BSD-3-Clause"
    },
    "node_modules/fast-xml-builder": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/fast-xml-builder/-/fast-xml-builder-1.2.1.tgz",
      "integrity": "sha512-tPb5TTWfgfVx5BNSi2xV0eLr89POeXXn0dXIsCJ9m1narrWxeIyx6je9d7Rce/3NyXLbvuQmLkxq+RuxMWejvw==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/NaturalIntelligence"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "path-expression-matcher": "^1.5.0",
        "xml-naming": "^0.1.0"
      }
    },
    "node_modules/fastq": {
      "version": "1.20.1",
      "resolved": "https://registry.npmjs.org/fastq/-/fastq-1.20.1.tgz",
      "integrity": "sha512-GGToxJ/w1x32s/D2EKND7kTil4n8OVk/9mycTc4VDza13lOvpUZTGX3mFSCtV9ksdGBVzvsyAVLM6mHFThxXxw==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "reusify": "^1.0.4"
      }
    },
    "node_modules/fill-range": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/fill-range/-/fill-range-7.1.1.tgz",
      "integrity": "sha512-YsGpe3WHLK8ZYi4tWDg2Jy3ebRz2rXowDxnld4bkQB00cc/1Zw9AWnC0i9ztDJitivtQvaI9KaLyKrc+hBW0yg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "to-regex-range": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/finalhandler": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/finalhandler/-/finalhandler-2.1.1.tgz",
      "integrity": "sha512-S8KoZgRZN+a5rNwqTxlZZePjT/4cnm0ROV70LedRHZ0p8u9fRID0hJUZQpkKLzro8LfmC8sx23bY6tVNxv8pQA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "debug": "^4.4.0",
        "encodeurl": "^2.0.0",
        "escape-html": "^1.0.3",
        "on-finished": "^2.4.1",
        "parseurl": "^1.3.3",
        "statuses": "^2.0.1"
      },
      "engines": {
        "node": ">= 18.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/forwarded": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/forwarded/-/forwarded-0.2.0.tgz",
      "integrity": "sha512-buRG0fpBtRHSTCOASe6hD258tEubFoRLb4ZNA6NxMVHNw2gOcwHo9wyablzMzOA5z9xA9L1KNjk/Nt6MT9aYow==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/fresh": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/fresh/-/fresh-2.0.0.tgz",
      "integrity": "sha512-Rx/WycZ60HOaqLKAi6cHRKKI7zxWbJ31MhntmtwMoaTeF7XFH9hhBp8vITaMidfljRQ6eYWCKkaTK+ykVJHP2A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/function-bind": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/function-bind/-/function-bind-1.1.2.tgz",
      "integrity": "sha512-7XHNxH7qX9xG5mIwxkhumTox/MIRNcOgDrxWsMt2pAr23WHp6MrRlN7FBSFpCpr+oVO0F744iUgR82nJMfG2SA==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/get-intrinsic": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/get-intrinsic/-/get-intrinsic-1.3.0.tgz",
      "integrity": "sha512-9fSjSaos/fRIVIp+xSJlE6lfwhES7LNtKaCBIamHsjr2na1BiABJPo0mOjjz8GJDURarmCPGqaiVg5mfjb98CQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "es-define-property": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "function-bind": "^1.1.2",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "has-symbols": "^1.1.0",
        "hasown": "^2.0.2",
        "math-intrinsics": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/get-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/get-proto/-/get-proto-1.0.1.tgz",
      "integrity": "sha512-sTSfBjoXBp89JvIKIefqw7U2CCebsc74kiY6awiGogKtoSGbgjYE/G/+l9sF3MWFPNc9IcoOC4ODfKHfxFmp0g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/git-up": {
      "version": "8.1.1",
      "resolved": "https://registry.npmjs.org/git-up/-/git-up-8.1.1.tgz",
      "integrity": "sha512-FDenSF3fVqBYSaJoYy1KSc2wosx0gCvKP+c+PRBht7cAaiCeQlBtfBDX9vgnNOHmdePlSFITVcn4pFfcgNvx3g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-ssh": "^1.4.0",
        "parse-url": "^9.2.0"
      }
    },
    "node_modules/git-url-parse": {
      "version": "16.1.0",
      "resolved": "https://registry.npmjs.org/git-url-parse/-/git-url-parse-16.1.0.tgz",
      "integrity": "sha512-cPLz4HuK86wClEW7iDdeAKcCVlWXmrLpb2L+G9goW0Z1dtpNS6BXXSOckUTlJT/LDQViE1QZKstNORzHsLnobw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "git-up": "^8.1.0"
      }
    },
    "node_modules/glob-parent": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-5.1.2.tgz",
      "integrity": "sha512-AOIgSQCepiJYwP3ARnGx+5VnTu2HBYdzbGP45eLw1vr3zB3vZLeyed1sC9hnbcOc9/SrMyM5RPQrkGz4aS9Zow==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "is-glob": "^4.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/globby": {
      "version": "16.2.0",
      "resolved": "https://registry.npmjs.org/globby/-/globby-16.2.0.tgz",
      "integrity": "sha512-QrJia2qDf5BB/V6HYlDTs0I0lBahyjLzpGQg3KT7FnCdTonAyPy2RtY802m2k4ALx6Dp752f82WsOczEVr3l6Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@sindresorhus/merge-streams": "^4.0.0",
        "fast-glob": "^3.3.3",
        "ignore": "^7.0.5",
        "is-path-inside": "^4.0.0",
        "slash": "^5.1.0",
        "unicorn-magic": "^0.4.0"
      },
      "engines": {
        "node": ">=20"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/gopd": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/gopd/-/gopd-1.2.0.tgz",
      "integrity": "sha512-ZUKRh6/kUFoAiTAtTYPZJ3hw9wNxx+BIBOijnlG9PnrJsCcSjs1wyyD6vJpaYtgnzDrKYRSqf3OO6Rfa93xsRg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/gpt-tokenizer": {
      "version": "3.4.0",
      "resolved": "https://registry.npmjs.org/gpt-tokenizer/-/gpt-tokenizer-3.4.0.tgz",
      "integrity": "sha512-wxFLnhIXTDjYebd9A9pGl3e31ZpSypbpIJSOswbgop5jLte/AsZVDvjlbEuVFlsqZixVKqbcoNmRlFDf6pz/UQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/handlebars": {
      "version": "4.7.9",
      "resolved": "https://registry.npmjs.org/handlebars/-/handlebars-4.7.9.tgz",
      "integrity": "sha512-4E71E0rpOaQuJR2A3xDZ+GM1HyWYv1clR58tC8emQNeQe3RH7MAzSbat+V0wG78LQBo6m6bzSG/L4pBuCsgnUQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "minimist": "^1.2.5",
        "neo-async": "^2.6.2",
        "source-map": "^0.6.1",
        "wordwrap": "^1.0.0"
      },
      "bin": {
        "handlebars": "bin/handlebars"
      },
      "engines": {
        "node": ">=0.4.7"
      },
      "optionalDependencies": {
        "uglify-js": "^3.1.4"
      }
    },
    "node_modules/has-symbols": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/has-symbols/-/has-symbols-1.1.0.tgz",
      "integrity": "sha512-1cDNdwJ2Jaohmb3sg4OmKaMBwuC48sYni5HUw2DvsC8LjGTLK9h+eb1X6RyuOHe4hT0ULCW68iomhjUoKUqlPQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/hasown": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/hasown/-/hasown-2.0.4.tgz",
      "integrity": "sha512-T2UbfbBEF32wiepXIsMlTW9+dDYC6wMh/t/vYA4tuOMKqWz/n3vr1NFSxQiyP+zk2mXsoMA/i/7qV6LKut1t1A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/hono": {
      "version": "4.12.27",
      "resolved": "https://registry.npmjs.org/hono/-/hono-4.12.27.tgz",
      "integrity": "sha512-1yrb/+w6HWQJrUCLkJ2IF5jNIPvvFkblV5RNOYl6bV+OA6p9GLcMpHFFGTosSvHvcAUibuUukRqhlYI4z32C7Q==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=16.9.0"
      }
    },
    "node_modules/http-errors": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/http-errors/-/http-errors-2.0.1.tgz",
      "integrity": "sha512-4FbRdAX+bSdmo4AUFuS0WNiPz8NgFt+r8ThgNWmlrjQjt1Q7ZR9+zTlce2859x4KSXrwIsaeTqDoKQmtP8pLmQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "depd": "~2.0.0",
        "inherits": "~2.0.4",
        "setprototypeof": "~1.2.0",
        "statuses": "~2.0.2",
        "toidentifier": "~1.0.1"
      },
      "engines": {
        "node": ">= 0.8"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/iconv-lite": {
      "version": "0.7.2",
      "resolved": "https://registry.npmjs.org/iconv-lite/-/iconv-lite-0.7.2.tgz",
      "integrity": "sha512-im9DjEDQ55s9fL4EYzOAv0yMqmMBSZp6G0VvFyTMPKWxiSBHUj9NW/qqLmXUwXrrM7AvqSlTCfvqRb0cM8yYqw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "safer-buffer": ">= 2.1.2 < 3.0.0"
      },
      "engines": {
        "node": ">=0.10.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/ignore": {
      "version": "7.0.5",
      "resolved": "https://registry.npmjs.org/ignore/-/ignore-7.0.5.tgz",
      "integrity": "sha512-Hs59xBNfUIunMFgWAbGX5cq6893IbWg4KnrjbYwX3tx0ztorVgTDA6B2sxf8ejHJ4wz8BqGUMYlnzNBer5NvGg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/inherits": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/inherits/-/inherits-2.0.4.tgz",
      "integrity": "sha512-k/vGaX4/Yla3WzyMCvTQOXYeIHvqOKtnqBduzTHpzpQZzAskKMhZ2K+EnBiSM9zGSoIFeMpXKxa4dYeZIQqewQ==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/ip-address": {
      "version": "10.2.0",
      "resolved": "https://registry.npmjs.org/ip-address/-/ip-address-10.2.0.tgz",
      "integrity": "sha512-/+S6j4E9AHvW9SWMSEY9Xfy66O5PWvVEJ08O0y5JGyEKQpojb0K0GKpz/v5HJ/G0vi3D2sjGK78119oXZeE0qA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 12"
      }
    },
    "node_modules/ipaddr.js": {
      "version": "1.9.1",
      "resolved": "https://registry.npmjs.org/ipaddr.js/-/ipaddr.js-1.9.1.tgz",
      "integrity": "sha512-0KI/607xoxSToH7GjN1FfSbLoU0+btTicjsQSWQlh/hZykN8KpmMf7uYwPW3R+akZ6R/w18ZlXSHBYXiYUPO3g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/is-binary-path": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/is-binary-path/-/is-binary-path-3.0.0.tgz",
      "integrity": "sha512-eSkpSYbqKip82Uw4z0iBK/5KmVzL2pf36kNKRtu6+mKvrow9sqF4w5hocQ9yV5v+9+wzHt620x3B7Wws/8lsGg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "binary-extensions": "^3.0.0"
      },
      "engines": {
        "node": ">=18.20"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/is-extglob": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/is-extglob/-/is-extglob-2.1.1.tgz",
      "integrity": "sha512-SbKbANkN603Vi4jEZv49LeVJMn4yGwsbzZworEoyEiutsN3nJYdbO36zfhGJ6QEDpOZIFkDtnq5JRxmvl3jsoQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-glob": {
      "version": "4.0.3",
      "resolved": "https://registry.npmjs.org/is-glob/-/is-glob-4.0.3.tgz",
      "integrity": "sha512-xelSayHH36ZgE7ZWhli7pW34hNbNl8Ojv5KVmkJD4hBdD3th8Tfk9vYasLM+mXWOZhFkgZfxhLSnrwRr4elSSg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-extglob": "^2.1.1"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-number": {
      "version": "7.0.0",
      "resolved": "https://registry.npmjs.org/is-number/-/is-number-7.0.0.tgz",
      "integrity": "sha512-41Cifkg6e8TylSpdtTpeLVMqvSBEVzTttHvERD741+pnZ8ANv0004MRL43QKPDlK9cGvNp6NZWZUBlbGXYxxng==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.12.0"
      }
    },
    "node_modules/is-path-inside": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/is-path-inside/-/is-path-inside-4.0.0.tgz",
      "integrity": "sha512-lJJV/5dYS+RcL8uQdBDW9c9uWFLLBNRyFhnAKXw5tVqLlKZ4RMGZKv+YQ/IA3OhD+RpbJa1LLFM1FQPGyIXvOA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/is-promise": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/is-promise/-/is-promise-4.0.0.tgz",
      "integrity": "sha512-hvpoI6korhJMnej285dSg6nu1+e6uxs7zG3BYAm5byqDsgJNWwxzM6z6iZiAgQR4TJ30JmBTOwqZUw3WlyH3AQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/is-ssh": {
      "version": "1.4.1",
      "resolved": "https://registry.npmjs.org/is-ssh/-/is-ssh-1.4.1.tgz",
      "integrity": "sha512-JNeu1wQsHjyHgn9NcWTaXq6zWSR6hqE0++zhfZlkFBbScNkyvxCdeV8sRkSBaeLKxmbpR21brail63ACNxJ0Tg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "protocols": "^2.0.1"
      }
    },
    "node_modules/isbinaryfile": {
      "version": "5.0.7",
      "resolved": "https://registry.npmjs.org/isbinaryfile/-/isbinaryfile-5.0.7.tgz",
      "integrity": "sha512-gnWD14Jh3FzS3CPhF0AxNOJ8CxqeblPTADzI38r0wt8ZyQl5edpy75myt08EG2oKvpyiqSqsx+Wkz9vtkbTqYQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 18.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/gjtorikian/"
      }
    },
    "node_modules/isexe": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/isexe/-/isexe-2.0.0.tgz",
      "integrity": "sha512-RHxMLp9lnKHGHRng9QFhRCMbYAcVpn69smSGcq3f36xjgVVWThj4qqLbTLlq7Ssj8B+fIQ1EuCEGI2lKsyQeIw==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/jiti": {
      "version": "2.7.0",
      "resolved": "https://registry.npmjs.org/jiti/-/jiti-2.7.0.tgz",
      "integrity": "sha512-AC/7JofJvZGrrneWNaEnJeOLUx+JlGt7tNa0wZiRPT4MY1wmfKjt2+6O2p2uz2+skll8OZZmJMNqeke7kKbNgQ==",
      "dev": true,
      "license": "MIT",
      "bin": {
        "jiti": "lib/jiti-cli.mjs"
      }
    },
    "node_modules/jose": {
      "version": "6.2.3",
      "resolved": "https://registry.npmjs.org/jose/-/jose-6.2.3.tgz",
      "integrity": "sha512-YYVDInQKFJfR/xa3ojUTl8c2KoTwiL1R5Wg9YCydwH0x0B9grbzlg5HC7mMjCtUJjbQ/YnGEZIhI5tCgfTb4Hw==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/panva"
      }
    },
    "node_modules/jschardet": {
      "version": "3.1.4",
      "resolved": "https://registry.npmjs.org/jschardet/-/jschardet-3.1.4.tgz",
      "integrity": "sha512-/kmVISmrwVwtyYU40iQUOp3SUPk2dhNCMsZBQX0R1/jZ8maaXJ/oZIzUOiyOqcgtLnETFKYChbJ5iDC/eWmFHg==",
      "dev": true,
      "license": "LGPL-2.1+",
      "engines": {
        "node": ">=0.1.90"
      }
    },
    "node_modules/json-schema-traverse": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-1.0.0.tgz",
      "integrity": "sha512-NM8/P9n3XjXhIZn1lLhkFaACTOURQXjWhV4BA/RnOv8xvgqtqpAX9IO4mRQxSx1Rlo4tqzeqb0sOlruaOy3dug==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/json-schema-typed": {
      "version": "8.0.2",
      "resolved": "https://registry.npmjs.org/json-schema-typed/-/json-schema-typed-8.0.2.tgz",
      "integrity": "sha512-fQhoXdcvc3V28x7C7BMs4P5+kNlgUURe2jmUT1T//oBRMDrqy1QPelJimwZGo7Hg9VPV3EQV5Bnq4hbFy2vetA==",
      "dev": true,
      "license": "BSD-2-Clause"
    },
    "node_modules/json5": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/json5/-/json5-2.2.3.tgz",
      "integrity": "sha512-XmOWe7eyHYH14cLdVPoyg+GOH3rYX++KpzrylJwSW98t3Nk+U8XOl8FWKOgwtzdb8lXGf6zYwDUzeHMWfxasyg==",
      "dev": true,
      "license": "MIT",
      "bin": {
        "json5": "lib/cli.js"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/math-intrinsics": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/math-intrinsics/-/math-intrinsics-1.1.0.tgz",
      "integrity": "sha512-/IXtbwEk5HTPyEwyKX6hGkYXxM9nbj64B+ilVJnC/R6B0pH5G4V3b0pVbL7DBj4tkhBAppbQUlf6F6Xl9LHu1g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/media-typer": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/media-typer/-/media-typer-1.1.0.tgz",
      "integrity": "sha512-aisnrDP4GNe06UcKFnV5bfMNPBUw4jsLGaWwWfnH3v02GnBuXX2MCVn5RbrWo0j3pczUilYblq7fQ7Nw2t5XKw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/merge-descriptors": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/merge-descriptors/-/merge-descriptors-2.0.0.tgz",
      "integrity": "sha512-Snk314V5ayFLhp3fkUREub6WtjBfPdCPY1Ln8/8munuLuiYhsABgBVWsozAG+MWMbVEvcdcpbi9R7ww22l9Q3g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/merge2": {
      "version": "1.4.1",
      "resolved": "https://registry.npmjs.org/merge2/-/merge2-1.4.1.tgz",
      "integrity": "sha512-8q7VEgMJW4J8tcfVPy8g09NcQwZdbwFEqhe/WZkoIzjn/3TGDwtOCYtXGxA3O8tPzpczCCDgv+P2P5y00ZJOOg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/micromatch": {
      "version": "4.0.8",
      "resolved": "https://registry.npmjs.org/micromatch/-/micromatch-4.0.8.tgz",
      "integrity": "sha512-PXwfBhYu0hBCPw8Dn0E+WDYb7af3dSLVWKi3HGv84IdF4TyFoC0ysxFd0Goxw7nSv4T/PzEJQxsYsEiFCKo2BA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "braces": "^3.0.3",
        "picomatch": "^2.3.1"
      },
      "engines": {
        "node": ">=8.6"
      }
    },
    "node_modules/mime-db": {
      "version": "1.54.0",
      "resolved": "https://registry.npmjs.org/mime-db/-/mime-db-1.54.0.tgz",
      "integrity": "sha512-aU5EJuIN2WDemCcAp2vFBfp/m4EAhWJnUNSSw0ixs7/kXbd6Pg64EmwJkNdFhB8aWt1sH2CTXrLxo/iAGV3oPQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/mime-types": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/mime-types/-/mime-types-3.0.2.tgz",
      "integrity": "sha512-Lbgzdk0h4juoQ9fCKXW4by0UJqj+nOOrI9MJ1sSj4nI8aI2eo1qmvQEie4VD1glsS250n15LsWsYtCugiStS5A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "mime-db": "^1.54.0"
      },
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/minimatch": {
      "version": "10.2.5",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-10.2.5.tgz",
      "integrity": "sha512-MULkVLfKGYDFYejP07QOurDLLQpcjk7Fw+7jXS2R2czRQzR56yHRveU5NDJEOviH+hETZKSkIk5c+T23GjFUMg==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "brace-expansion": "^5.0.5"
      },
      "engines": {
        "node": "18 || 20 || >=22"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/minimist": {
      "version": "1.2.8",
      "resolved": "https://registry.npmjs.org/minimist/-/minimist-1.2.8.tgz",
      "integrity": "sha512-2yyAR8qBkN3YuheJanUpWC5U3bb5osDywNB8RzDVlDwDHbocAJveqqj1u8+SVD7jkWT4yvsHCpWqqWqAxb0zCA==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/minipass": {
      "version": "7.1.3",
      "resolved": "https://registry.npmjs.org/minipass/-/minipass-7.1.3.tgz",
      "integrity": "sha512-tEBHqDnIoM/1rXME1zgka9g6Q2lcoCkxHLuc7ODJ5BxbP5d4c2Z5cGgtXAku59200Cx7diuHTOYfSBD8n6mm8A==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "engines": {
        "node": ">=16 || 14 >=14.17"
      }
    },
    "node_modules/minizlib": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/minizlib/-/minizlib-3.1.0.tgz",
      "integrity": "sha512-KZxYo1BUkWD2TVFLr0MQoM8vUUigWD3LlD83a/75BqC+4qE0Hb1Vo5v1FgcfaNXvfXzr+5EhQ6ing/CaBijTlw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "minipass": "^7.1.2"
      },
      "engines": {
        "node": ">= 18"
      }
    },
    "node_modules/ms": {
      "version": "2.1.3",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.1.3.tgz",
      "integrity": "sha512-6FlzubTLZG3J2a/NVCAleEhjzq5oxgHyaCU9yYXvcLsvoVaHJq/s5xXI6/XXP6tz7R9xAOtHnSO/tXtF3WRTlA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/negotiator": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/negotiator/-/negotiator-1.0.0.tgz",
      "integrity": "sha512-8Ofs/AUQh8MaEcrlq5xOX0CQ9ypTF5dl78mjlMNfOK08fzpgTHQRQPBxcPlEtIw0yRpws+Zo/3r+5WRby7u3Gg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/neo-async": {
      "version": "2.6.2",
      "resolved": "https://registry.npmjs.org/neo-async/-/neo-async-2.6.2.tgz",
      "integrity": "sha512-Yd3UES5mWCSqR+qNT93S3UoYUkqAZ9lLg8a7g9rimsWmYGK8cVToA4/sF3RrshdyV3sAGMXVUmpMYOw+dLpOuw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/object-assign": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/object-assign/-/object-assign-4.1.1.tgz",
      "integrity": "sha512-rJgTQnkUnH1sFw8yT6VSU3zD3sWmu6sZhIseY8VX+GRu3P6F7Fu+JNDoXfklElbLJSnc3FUQHVe4cU5hj+BcUg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/object-inspect": {
      "version": "1.13.4",
      "resolved": "https://registry.npmjs.org/object-inspect/-/object-inspect-1.13.4.tgz",
      "integrity": "sha512-W67iLl4J2EXEGTbfeHCffrjDfitvLANg0UlX3wFUUSTx92KXRFegMHUVgSqE+wvhAbi4WqjGg9czysTV2Epbew==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/on-finished": {
      "version": "2.4.1",
      "resolved": "https://registry.npmjs.org/on-finished/-/on-finished-2.4.1.tgz",
      "integrity": "sha512-oVlzkg3ENAhCk2zdv7IJwd/QUD4z2RxRwpkcGY8psCVcCYZNq4wYnVWALHM+brtuJjePWiYF/ClmuDr8Ch5+kg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ee-first": "1.1.1"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/once": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/once/-/once-1.4.0.tgz",
      "integrity": "sha512-lNaJgI+2Q5URQBkccEKHTQOPaXdUxnZZElQTZY0MFUAuaEqe1E+Nyvgdz/aIyNi6Z9MzO5dv1H8n58/GELp3+w==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "wrappy": "1"
      }
    },
    "node_modules/parse-path": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/parse-path/-/parse-path-7.1.0.tgz",
      "integrity": "sha512-EuCycjZtfPcjWk7KTksnJ5xPMvWGA/6i4zrLYhRG0hGvC3GPU/jGUj3Cy+ZR0v30duV3e23R95T1lE2+lsndSw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "protocols": "^2.0.0"
      }
    },
    "node_modules/parse-url": {
      "version": "9.2.0",
      "resolved": "https://registry.npmjs.org/parse-url/-/parse-url-9.2.0.tgz",
      "integrity": "sha512-bCgsFI+GeGWPAvAiUv63ZorMeif3/U0zaXABGJbOWt5OH2KCaPHF6S+0ok4aqM9RuIPGyZdx9tR9l13PsW4AYQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@types/parse-path": "^7.0.0",
        "parse-path": "^7.0.0"
      },
      "engines": {
        "node": ">=14.13.0"
      }
    },
    "node_modules/parseurl": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/parseurl/-/parseurl-1.3.3.tgz",
      "integrity": "sha512-CiyeOxFT/JZyN5m0z9PfXw4SCBJ6Sygz1Dpl0wqjlhDEGGBP1GnsUVEL0p63hoG1fcj3fHynXi9NYO4nWOL+qQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/path-expression-matcher": {
      "version": "1.6.1",
      "resolved": "https://registry.npmjs.org/path-expression-matcher/-/path-expression-matcher-1.6.1.tgz",
      "integrity": "sha512-h7bxdzhHk8Knyc4Tj+jMaa7fEEoUJy7p1qtbVgkYg1Uhpe5Np5VuGXCRZnkZvU+Q42M1vStt0ifa3ueykRJPmQ==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/NaturalIntelligence"
        }
      ],
      "license": "MIT",
      "engines": {
        "node": ">=14.0.0"
      }
    },
    "node_modules/path-key": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/path-key/-/path-key-3.1.1.tgz",
      "integrity": "sha512-ojmeN0qd+y0jszEtoY48r0Peq5dwMEkIlCOu6Q5f41lfkswXuKtYrhgoTpLnyIcHm24Uhqx+5Tqm2InSwLhE6Q==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-to-regexp": {
      "version": "8.4.2",
      "resolved": "https://registry.npmjs.org/path-to-regexp/-/path-to-regexp-8.4.2.tgz",
      "integrity": "sha512-qRcuIdP69NPm4qbACK+aDogI5CBDMi1jKe0ry5rSQJz8JVLsC7jV8XpiJjGRLLol3N+R5ihGYcrPLTno6pAdBA==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/picocolors": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-1.1.1.tgz",
      "integrity": "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/picomatch": {
      "version": "2.3.2",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-2.3.2.tgz",
      "integrity": "sha512-V7+vQEJ06Z+c5tSye8S+nHUfI51xoXIXjHQ99cQtKUkQqqO1kO/KCJUfZXuB47h/YBlDhah2H3hdUGXn8ie0oA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/picospinner": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/picospinner/-/picospinner-3.0.0.tgz",
      "integrity": "sha512-lGA1TNsmy2bxvRsTI2cV01kfTwKzZjnZSDmF9llYNyMHMrU4sP87lQ5taiIKm88L3cbswjl008nwyGc3WpNvzg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18.0.0"
      }
    },
    "node_modules/pkce-challenge": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/pkce-challenge/-/pkce-challenge-5.0.1.tgz",
      "integrity": "sha512-wQ0b/W4Fr01qtpHlqSqspcj3EhBvimsdh0KlHhH8HRZnMsEa0ea2fTULOXOS9ccQr3om+GcGRk4e+isrZWV8qQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=16.20.0"
      }
    },
    "node_modules/protocols": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/protocols/-/protocols-2.0.2.tgz",
      "integrity": "sha512-hHVTzba3wboROl0/aWRRG9dMytgH6ow//STBZh43l/wQgmMhYhOFi0EHWAPtoCz9IAUymsyP0TSBHkhgMEGNnQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/proxy-addr": {
      "version": "2.0.7",
      "resolved": "https://registry.npmjs.org/proxy-addr/-/proxy-addr-2.0.7.tgz",
      "integrity": "sha512-llQsMLSUDUPT44jdrU/O37qlnifitDP+ZwrmmZcoSKyLKvtZxpyV0n2/bD/N4tBAAZ/gJEdZU7KMraoK1+XYAg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "forwarded": "0.2.0",
        "ipaddr.js": "1.9.1"
      },
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/qs": {
      "version": "6.15.3",
      "resolved": "https://registry.npmjs.org/qs/-/qs-6.15.3.tgz",
      "integrity": "sha512-O9gl3zCl5h5blw1KGUzQKhA5oUXSl8rwUIM5o0S3nCXMliSvy5Dzx7/DJcI+SwgICv+IneSZwhBh1oSyEHA71A==",
      "dev": true,
      "license": "BSD-3-Clause",
      "dependencies": {
        "es-define-property": "^1.0.1",
        "side-channel": "^1.1.1"
      },
      "engines": {
        "node": ">=0.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/queue-microtask": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/queue-microtask/-/queue-microtask-1.2.3.tgz",
      "integrity": "sha512-NuaNSa6flKT5JaSYQzJok04JzTL1CA6aGhv5rfLW3PgqA+M2ChpZQnAC8h8i4ZFkBS8X5RqkDBHA7r4hej3K9A==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "license": "MIT"
    },
    "node_modules/range-parser": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/range-parser/-/range-parser-1.3.0.tgz",
      "integrity": "sha512-hek2mFQpPuI4E1BBKrSto+BU3e3x4xuarsbiwr3+lf7p44juvFMV0XFWQAP3xUyqXA4RrXLIoaSUGbSt056ZMw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/raw-body": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/raw-body/-/raw-body-3.0.2.tgz",
      "integrity": "sha512-K5zQjDllxWkf7Z5xJdV0/B0WTNqx6vxG70zJE4N0kBs4LovmEYWJzQGxC9bS9RAKu3bgM40lrd5zoLJ12MQ5BA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "bytes": "~3.1.2",
        "http-errors": "~2.0.1",
        "iconv-lite": "~0.7.0",
        "unpipe": "~1.0.0"
      },
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/readdirp": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/readdirp/-/readdirp-5.0.0.tgz",
      "integrity": "sha512-9u/XQ1pvrQtYyMpZe7DXKv2p5CNvyVwzUB6uhLAnQwHMSgKMBR62lc7AHljaeteeHXn11XTAaLLUVZYVZyuRBQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 20.19.0"
      },
      "funding": {
        "type": "individual",
        "url": "https://paulmillr.com/funding/"
      }
    },
    "node_modules/repomix": {
      "version": "1.16.0",
      "resolved": "https://registry.npmjs.org/repomix/-/repomix-1.16.0.tgz",
      "integrity": "sha512-C41hGZsuwpcOJXKtbBCQ0agbT1yTOyIPoA9LYbS5MMHvj19jLML148r98iYthqI7B3VaHvlscxv7o6U0fqI7BQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@clack/prompts": "^0.11.0",
        "@modelcontextprotocol/sdk": "^1.29.0",
        "@repomix/strip-comments": "^2.4.2",
        "@repomix/tree-sitter-wasms": "^0.1.17",
        "@secretlint/core": "^13.0.2",
        "@secretlint/secretlint-rule-preset-recommend": "^13.0.2",
        "chokidar": "^5.0.0",
        "commander": "^15.0.0",
        "fast-xml-builder": "^1.2.0",
        "git-url-parse": "^16.1.0",
        "globby": "^16.2.0",
        "gpt-tokenizer": "^3.4.0",
        "handlebars": "^4.7.9",
        "iconv-lite": "^0.7.0",
        "is-binary-path": "^3.0.0",
        "isbinaryfile": "^5.0.2",
        "jiti": "^2.7.0",
        "jschardet": "^3.1.4",
        "json5": "^2.2.3",
        "minimatch": "^10.2.5",
        "picocolors": "^1.1.1",
        "picospinner": "^3.0.0",
        "tar": "^7.5.16",
        "tinyclip": "^0.1.14",
        "tinypool": "^2.1.0",
        "valibot": "^1.4.1",
        "web-tree-sitter": "^0.26.9",
        "zod": "^4.4.3"
      },
      "bin": {
        "repomix": "bin/repomix.cjs"
      },
      "engines": {
        "node": ">=22.0.0",
        "yarn": ">=1.22.22"
      }
    },
    "node_modules/require-from-string": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/require-from-string/-/require-from-string-2.0.2.tgz",
      "integrity": "sha512-Xf0nWe6RseziFMu+Ap9biiUbmplq6S9/p+7w7YXP/JBHhrUDDUhwa+vANyubuqfZWTveU//DYVGsDG7RKL/vEw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/reusify": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/reusify/-/reusify-1.1.0.tgz",
      "integrity": "sha512-g6QUff04oZpHs0eG5p83rFLhHeV00ug/Yf9nZM6fLeUrPguBTkTQOdpAWWspMh55TZfVQDPaN3NQJfbVRAxdIw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "iojs": ">=1.0.0",
        "node": ">=0.10.0"
      }
    },
    "node_modules/router": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/router/-/router-2.2.0.tgz",
      "integrity": "sha512-nLTrUKm2UyiL7rlhapu/Zl45FwNgkZGaCpZbIHajDYgwlJCOzLSk+cIPAnsEqV955GjILJnKbdQC1nVPz+gAYQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "debug": "^4.4.0",
        "depd": "^2.0.0",
        "is-promise": "^4.0.0",
        "parseurl": "^1.3.3",
        "path-to-regexp": "^8.0.0"
      },
      "engines": {
        "node": ">= 18"
      }
    },
    "node_modules/run-parallel": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/run-parallel/-/run-parallel-1.2.0.tgz",
      "integrity": "sha512-5l4VyZR86LZ/lDxZTR6jqL8AFE2S0IFLMP26AbjsLVADxHdhB/c0GUsH+y39UfCi3dzz8OlQuPmnaJOMoDHQBA==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "queue-microtask": "^1.2.2"
      }
    },
    "node_modules/safer-buffer": {
      "version": "2.1.2",
      "resolved": "https://registry.npmjs.org/safer-buffer/-/safer-buffer-2.1.2.tgz",
      "integrity": "sha512-YZo3K82SD7Riyi0E1EQPojLz7kpepnSQI9IyPbHHg1XXXevb5dJI7tpyN2ADxGcQbHG7vcyRHk0cbwqcQriUtg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/send": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/send/-/send-1.2.1.tgz",
      "integrity": "sha512-1gnZf7DFcoIcajTjTwjwuDjzuz4PPcY2StKPlsGAQ1+YH20IRVrBaXSWmdjowTJ6u8Rc01PoYOGHXfP1mYcZNQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "debug": "^4.4.3",
        "encodeurl": "^2.0.0",
        "escape-html": "^1.0.3",
        "etag": "^1.8.1",
        "fresh": "^2.0.0",
        "http-errors": "^2.0.1",
        "mime-types": "^3.0.2",
        "ms": "^2.1.3",
        "on-finished": "^2.4.1",
        "range-parser": "^1.2.1",
        "statuses": "^2.0.2"
      },
      "engines": {
        "node": ">= 18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/serve-static": {
      "version": "2.2.1",
      "resolved": "https://registry.npmjs.org/serve-static/-/serve-static-2.2.1.tgz",
      "integrity": "sha512-xRXBn0pPqQTVQiC8wyQrKs2MOlX24zQ0POGaj0kultvoOCstBQM5yvOhAVSUwOMjQtTvsPWoNCHfPGwaaQJhTw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "encodeurl": "^2.0.0",
        "escape-html": "^1.0.3",
        "parseurl": "^1.3.3",
        "send": "^1.2.0"
      },
      "engines": {
        "node": ">= 18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/setprototypeof": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/setprototypeof/-/setprototypeof-1.2.0.tgz",
      "integrity": "sha512-E5LDX7Wrp85Kil5bhZv46j8jOeboKq5JMmYM3gVGdGH8xFpPWXUMsNrlODCrkoxMEeNi/XZIwuRvY4XNwYMJpw==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/shebang-command": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/shebang-command/-/shebang-command-2.0.0.tgz",
      "integrity": "sha512-kHxr2zZpYtdmrN1qDjrrX/Z1rR1kG8Dx+gkpK1G4eXmvXswmcE1hTWBWYUzlraYw1/yZp6YuDY77YtvbN0dmDA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "shebang-regex": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/shebang-regex": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/shebang-regex/-/shebang-regex-3.0.0.tgz",
      "integrity": "sha512-7++dFhtcx3353uBaq8DDR4NuxBetBzC7ZQOhmTQInHEd6bSrXdiEyzCvG07Z44UYdLShWUyXt5M/yhz8ekcb1A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/side-channel": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/side-channel/-/side-channel-1.1.1.tgz",
      "integrity": "sha512-6x6dK6zJdpTzF4sQeNYxwtvBzf6Eg4GtlesS94HOvTudUeyK2WXAaIfmDgsyslYrRBeFIlsi54AYsFGUuhmvrQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "object-inspect": "^1.13.4",
        "side-channel-list": "^1.0.1",
        "side-channel-map": "^1.0.1",
        "side-channel-weakmap": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-list": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/side-channel-list/-/side-channel-list-1.0.1.tgz",
      "integrity": "sha512-mjn/0bi/oUURjc5Xl7IaWi/OJJJumuoJFQJfDDyO46+hBWsfaVM65TBHq2eoZBhzl9EchxOijpkbRC8SVBQU0w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "object-inspect": "^1.13.4"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-map": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/side-channel-map/-/side-channel-map-1.0.1.tgz",
      "integrity": "sha512-VCjCNfgMsby3tTdo02nbjtM/ewra6jPHmpThenkTYh8pG9ucZ/1P8So4u4FGBek/BjpOVsDCMoLA/iuBKIFXRA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.5",
        "object-inspect": "^1.13.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-weakmap": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/side-channel-weakmap/-/side-channel-weakmap-1.0.2.tgz",
      "integrity": "sha512-WPS/HvHQTYnHisLo9McqBHOJk2FkHO/tlpvldyrnem4aeQp4hai3gythswg6p01oSoTl58rcpiFAjF2br2Ak2A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.5",
        "object-inspect": "^1.13.3",
        "side-channel-map": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/sisteransi": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/sisteransi/-/sisteransi-1.0.5.tgz",
      "integrity": "sha512-bLGGlR1QxBcynn2d5YmDX4MGjlZvy2MRBDRNHLJ8VI6l6+9FUiyTFNJ0IveOSP0bcXgVDPRcfGqA0pjaqUpfVg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/slash": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/slash/-/slash-5.1.0.tgz",
      "integrity": "sha512-ZA6oR3T/pEyuqwMgAKT0/hAv8oAXckzbkmR0UkUosQ+Mc4RxGoJkRmwHgHufaenlyAgE1Mxgpdcrf75y6XcnDg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=14.16"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "dev": true,
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/statuses": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/statuses/-/statuses-2.0.2.tgz",
      "integrity": "sha512-DvEy55V3DB7uknRo+4iOGT5fP1slR8wQohVdknigZPMpMstaKJQWhwiYBACJE3Ul2pTnATihhBYnRhZQHGBiRw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/structured-source": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/structured-source/-/structured-source-4.0.0.tgz",
      "integrity": "sha512-qGzRFNJDjFieQkl/sVOI2dUjHKRyL9dAJi2gCPGJLbJHBIkyOHxjuocpIEfbLioX+qSJpvbYdT49/YCdMznKxA==",
      "dev": true,
      "license": "BSD-2-Clause",
      "dependencies": {
        "boundary": "^2.0.0"
      }
    },
    "node_modules/tar": {
      "version": "7.5.19",
      "resolved": "https://registry.npmjs.org/tar/-/tar-7.5.19.tgz",
      "integrity": "sha512-4LeEWl96twnS2Q7Bz4MGqgazLqO+hJN63GZxXoIqh1T3VweYD997gbU1ItNsQafqqXTXd5WFyFdReLtwvRBNiw==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "@isaacs/fs-minipass": "^4.0.0",
        "chownr": "^3.0.0",
        "minipass": "^7.1.2",
        "minizlib": "^3.1.0",
        "yallist": "^5.0.0"
      },
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/tinyclip": {
      "version": "0.1.15",
      "resolved": "https://registry.npmjs.org/tinyclip/-/tinyclip-0.1.15.tgz",
      "integrity": "sha512-uo33abH+Ays0xYaDysoBt494Hb3hsEczMpcC0MwFl773pazORx4fmvKhclhR1wonUbB6vvpRsvVMwnhfqeMc+A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^16.14.0 || >= 17.3.0"
      }
    },
    "node_modules/tinypool": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/tinypool/-/tinypool-2.1.0.tgz",
      "integrity": "sha512-Pugqs6M0m7Lv1I7FtxN4aoyToKg1C4tu+/381vH35y8oENM/Ai7f7C4StcoK4/+BSw9ebcS8jRiVrORFKCALLw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^20.0.0 || >=22.0.0"
      }
    },
    "node_modules/to-regex-range": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/to-regex-range/-/to-regex-range-5.0.1.tgz",
      "integrity": "sha512-65P7iz6X5yEr1cwcgvQxbbIw7Uk3gOy5dIdtZ4rDveLqhrdJP+Li/Hx6tyK0NEb+2GCyneCMJiGqrADCSNk8sQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-number": "^7.0.0"
      },
      "engines": {
        "node": ">=8.0"
      }
    },
    "node_modules/toidentifier": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/toidentifier/-/toidentifier-1.0.1.tgz",
      "integrity": "sha512-o5sSPKEkg/DIQNmH43V0/uerLrpzVedkUh8tGNvaeXpfpuwjKenlSox/2O/BTlZUtEe+JG7s5YhEz608PlAHRA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.6"
      }
    },
    "node_modules/type-is": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/type-is/-/type-is-2.1.0.tgz",
      "integrity": "sha512-faYHw0anBbc/kWF3zFTEnxSFOAGUX9GFbOBthvDdLsIlEoWOFOtS0zgCiQYwIskL9iGXZL3kAXD8OoZ4GmMATA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "content-type": "^2.0.0",
        "media-typer": "^1.1.0",
        "mime-types": "^3.0.0"
      },
      "engines": {
        "node": ">= 18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/type-is/node_modules/content-type": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/content-type/-/content-type-2.0.0.tgz",
      "integrity": "sha512-j/O/d7GcZCyNl7/hwZAb606rzqkyvaDctLmckbxLzHvFBzTJHuGEdodATcP3yIRoDrLHkIATJuvzbFlp/ki2cQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/uglify-js": {
      "version": "3.19.3",
      "resolved": "https://registry.npmjs.org/uglify-js/-/uglify-js-3.19.3.tgz",
      "integrity": "sha512-v3Xu+yuwBXisp6QYTcH4UbH+xYJXqnq2m/LtQVWKWzYc1iehYnLixoQDN9FH6/j9/oybfd6W9Ghwkl8+UMKTKQ==",
      "dev": true,
      "license": "BSD-2-Clause",
      "optional": true,
      "bin": {
        "uglifyjs": "bin/uglifyjs"
      },
      "engines": {
        "node": ">=0.8.0"
      }
    },
    "node_modules/unicorn-magic": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/unicorn-magic/-/unicorn-magic-0.4.0.tgz",
      "integrity": "sha512-wH590V9VNgYH9g3lH9wWjTrUoKsjLF6sGLjhR4sH1LWpLmCOH0Zf7PukhDA8BiS7KHe4oPNkcTHqYkj7SOGUOw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=20"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/unpipe": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/unpipe/-/unpipe-1.0.0.tgz",
      "integrity": "sha512-pjy2bYhSsufwWlKwPc+l3cN7+wuJlK6uz0YdJEOlQDbl6jo/YlPi4mb8agUkVC8BF7V8NuzeyPNqRksA3hztKQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/valibot": {
      "version": "1.4.2",
      "resolved": "https://registry.npmjs.org/valibot/-/valibot-1.4.2.tgz",
      "integrity": "sha512-gjdCvJ6d3RyHAneqxMYMW9QMCwYMb3jpOO0IyHZV1bnRHFBHrX3VkIILt5XYR0WhwHiH7Mty8ovuPZ/O3gamrg==",
      "dev": true,
      "license": "MIT",
      "peerDependencies": {
        "typescript": ">=5"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/vary": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/vary/-/vary-1.1.2.tgz",
      "integrity": "sha512-BNGbWLfd0eUPabhkXUVm0j8uuvREyTh5ovRa/dyow/BqAbZJyC+5fU+IzQOzmAKzYqYRAISoRhdQr3eIZ/PXqg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/web-tree-sitter": {
      "version": "0.26.10",
      "resolved": "https://registry.npmjs.org/web-tree-sitter/-/web-tree-sitter-0.26.10.tgz",
      "integrity": "sha512-vengBGYS7FpAerkR3o04oBL4L8MkVmjawK50AFBu7v0HZBkmF9ZavPGKoXLSSmRhp7T/YgsJ7joAS3yAxHPEqQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/which": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/which/-/which-2.0.2.tgz",
      "integrity": "sha512-BLI3Tl1TW3Pvl70l3yq3Y64i+awpwXqsGBYWkkqMtnbXgrMD+yj7rhW0kuEDxzJaYXGjEW5ogapKNMEKNMjibA==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "isexe": "^2.0.0"
      },
      "bin": {
        "node-which": "bin/node-which"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/wordwrap": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/wordwrap/-/wordwrap-1.0.0.tgz",
      "integrity": "sha512-gvVzJFlPycKc5dZN4yPkP8w7Dc37BtP1yczEneOb4uq34pXZcvrtRTmWV8W+Ume+XCxKgbjM+nevkyFPMybd4Q==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/wrappy": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/wrappy/-/wrappy-1.0.2.tgz",
      "integrity": "sha512-l4Sp/DRseor9wL6EvV2+TuQn63dMkPjZ/sp9XkghTEbV9KlPS1xUsZ3u7/IQO4wxtcFB4bgpQPRcR3QCvezPcQ==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/xml-naming": {
      "version": "0.1.0",
      "resolved": "https://registry.npmjs.org/xml-naming/-/xml-naming-0.1.0.tgz",
      "integrity": "sha512-k8KO9hrMyNk6tUWqUfkTEZbezRRpONVOzUTnc97VnCvyj6Tf9lyUR9EDAIeiVLv56jsMcoXEwjW8Kv5yPY52lw==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/NaturalIntelligence"
        }
      ],
      "license": "MIT",
      "engines": {
        "node": ">=16.0.0"
      }
    },
    "node_modules/yallist": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/yallist/-/yallist-5.0.0.tgz",
      "integrity": "sha512-YgvUTfwqyc7UXVMrB+SImsVYSmTS8X/tSrtdNZMImM+n7+QTriRXyXim0mBrTXNeqzVF0KWGgHPeiyViFFrNDw==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/zod": {
      "version": "4.4.3",
      "resolved": "https://registry.npmjs.org/zod/-/zod-4.4.3.tgz",
      "integrity": "sha512-ytENFjIJFl2UwYglde2jchW2Hwm4GJFLDiSXWdTrJQBIN9Fcyp7n4DhxJEiWNAJMV1/BqWfW/kkg71UDcHJyTQ==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/colinhacks"
      }
    },
    "node_modules/zod-to-json-schema": {
      "version": "3.25.2",
      "resolved": "https://registry.npmjs.org/zod-to-json-schema/-/zod-to-json-schema-3.25.2.tgz",
      "integrity": "sha512-O/PgfnpT1xKSDeQYSCfRI5Gy3hPf91mKVDuYLUHZJMiDFptvP41MSnWofm8dnCm0256ZNfZIM7DSzuSMAFnjHA==",
      "dev": true,
      "license": "ISC",
      "peerDependencies": {
        "zod": "^3.25.28 || ^4"
      }
    }
  }
}
```

## `package.json`

Size: 155 B

```json
{
  "name": "platforma-tuvtk-tools",
  "private": true,
  "scripts": {
    "repomix": "repomix"
  },
  "devDependencies": {
    "repomix": "^1.16.0"
  }
}
```

## `README.md`

Size: 8.8 KB

````markdown
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
````

## `requirements-deploy.txt`

Size: 90 B

```text
# Direct deployment overlay installed by Dockerfile.
-r requirements.txt
gunicorn==23.0.0
```

## `requirements-dev.txt`

Size: 171 B

```text
# Direct development overlay. This remains compatible with existing install commands.
-r requirements.txt
django-browser-reload==1.21.0
pylint==4.0.6
pylint-django==2.7.0
```

## `requirements.txt`

Size: 392 B

```text
# Direct base/runtime requirements used by Docker. This is not yet a
# resolver-generated transitive lock; see requirements.in for the compile command.
Django==6.0.6
psycopg[binary]==3.3.4
django-tailwind==4.5.0
django-bootstrap-icons==0.9.0
openpyxl==3.1.2
Pillow==12.3.0
defusedxml==0.7.1
python-docx==1.2.0
rapidfuzz==3.14.5
requests==2.32.3
reportlab==5.0.0
svglib==2.0.2
tinycss2==1.5.1
```

## `.agents/plugins/marketplace.json`

Size: 369 B

```json
{
  "name": "personal",
  "interface": {
    "displayName": "Personal"
  },
  "plugins": [
    {
      "name": "playwright",
      "source": {
        "source": "local",
        "path": "./plugins/playwright"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Developer Tools"
    }
  ]
}
```

## `.dockerignore`

Size: 268 B

```text
.git
.gitignore
.venv
.env
.postgresql
.playwright-mcp
.bootstrap_icons_cache
__pycache__
*.py[cod]
node_modules
**/node_modules
codex-context
media
private_media
staticfiles
test-results
playwright-report
repomix-output.*
theme/static/css/dist
apps/planificator-main
```

## `.gitattributes`

Size: 122 B

```text
*.sh text eol=lf
Dockerfile text eol=lf
*.yaml text eol=lf
*.template text eol=lf
*.bat text eol=crlf
*.ps1 text eol=crlf
```

## `.gitignore`

Size: 268 B

```text
# Editor and local environment
.vscode/
.venv/

node_modules/
__pycache__/
*.py[cod]
.bootstrap_icons_cache/
.playwright-mcp/
test-results/
playwright-report/
tmp/
db.sqlite3
.env
.postgresql/
media/
private_media/
staticfiles/
theme/static/css/dist/
repomix-output.*
```

## `apps/__init__.py`

Size: 0 B

```python
```

## `bin/tuvtk`

Size: 14.6 KB

```text
#!/usr/bin/env bash
set -Eeuo pipefail

readonly APP_DIR="${TUVTK_APP_DIR:-/opt/tuvtk/app}"
readonly ENV_FILE="${TUVTK_ENV_FILE:-/etc/tuvtk/tuvtk.env}"
readonly COMPOSE_FILE="${TUVTK_COMPOSE_FILE:-/opt/tuvtk/app/compose.yaml}"
readonly DEV_COMPOSE_FILE="${TUVTK_DEV_COMPOSE_FILE:-$APP_DIR/compose.dev.yaml}"
readonly PROJECT_NAME="${TUVTK_PROJECT_NAME:-tuvtk}"
readonly DB_SERVICE="db"
readonly WEB_SERVICE="web"
readonly BACKUP_FORMAT="tuvtk-backup-v1"

DOCKER_COMMAND=()

fail() {
    printf 'tuvtk: ERROR: %s\n' "$*" >&2
    exit 1
}

usage() {
    cat <<'EOF'
Usage: tuvtk COMMAND [ARGS...]

Docker lifecycle:
  status, ps                    Show service status
  up, start                     Start services in the background
  down, stop                    Stop and remove service containers
  restart                       Restart services
  build                         Build images and start services
  rebuild                       Rebuild without cache and start services
  logs [SERVICE]                Follow all logs or one service's logs

Django:
  check                          Run Django system checks
  test [TARGET] [ARGS...]        Run tests; defaults to verbosity 0
  migrate [ARGS...]              Apply migrations
  makemigrations [APP] [ARGS...] Create migrations
  collectstatic                  Collect static files non-interactively
  shell                          Open the Django shell
  dbshell                        Open the Django database shell
  django COMMAND [ARGS...]       Run an arbitrary manage.py command
  exec SERVICE COMMAND [ARGS...] Run a command in a service

Data and maintenance:
  backup DIRECTORY               Create a database/configuration archive
  restore ARCHIVE                Validate a backup; restore is deferred
  export-sql PATH                Export PostgreSQL as plain SQL
  import-sql SQL_FILE            Import a plain SQL dump
  context                        Generate Codex context when supported
  clean                          Remove safe local generated caches

Development:
  dev                            Start db, Django, and Tailwind detached
  dev-build                      Build Django and start the development stack
  dev-logs [SERVICE]             Follow development logs
  tailwind                       Start and follow the Tailwind watcher
  npm COMMAND...                 Run npm in the dedicated Node service

Configuration environment variables:
  TUVTK_APP_DIR       (default: /opt/tuvtk/app)
  TUVTK_ENV_FILE      (default: /etc/tuvtk/tuvtk.env)
  TUVTK_COMPOSE_FILE  (default: /opt/tuvtk/app/compose.yaml)
  TUVTK_DEV_COMPOSE_FILE (default: APP_DIR/compose.dev.yaml)
  TUVTK_PROJECT_NAME  (default: tuvtk)
  TUVTK_DEV_PORT      (default: 8000)

Examples:
  tuvtk status
  tuvtk logs web
  tuvtk test apps.dashboard
  tuvtk dev
  tuvtk dev-logs web
  tuvtk npm run build
  tuvtk django createsuperuser
  tuvtk backup /var/backups/tuvtk
EOF
}

require_app_dir() {
    [[ -d "$APP_DIR" ]] || fail "application directory not found: $APP_DIR (set TUVTK_APP_DIR to override)"
}

require_deployment_paths() {
    require_app_dir
    [[ -f "$ENV_FILE" ]] || fail "environment file not found: $ENV_FILE (set TUVTK_ENV_FILE to override)"
    [[ -f "$COMPOSE_FILE" ]] || fail "Compose file not found: $COMPOSE_FILE (set TUVTK_COMPOSE_FILE to override)"
}

prepare_docker() {
    command -v docker >/dev/null 2>&1 || fail "Docker is not installed or is not in PATH."
    docker compose version >/dev/null 2>&1 || fail "the Docker Compose plugin is unavailable; install 'docker compose' (not legacy docker-compose)."

    if docker info >/dev/null 2>&1; then
        DOCKER_COMMAND=(docker)
        return
    fi

    command -v sudo >/dev/null 2>&1 || fail "Docker is unavailable to this user and sudo is not installed."
    if sudo -n docker info >/dev/null 2>&1; then
        DOCKER_COMMAND=(sudo docker)
        return
    fi

    if [[ -t 0 && -t 1 ]]; then
        printf 'tuvtk: Docker access requires sudo; sudo may prompt for your password.\n' >&2
        DOCKER_COMMAND=(sudo docker)
        return
    fi

    fail "Docker is unavailable to this user. Run through sudo or grant the user Docker access."
}

prepare_compose() {
    require_deployment_paths
    prepare_docker
}

prepare_dev_compose() {
    require_deployment_paths
    [[ -f "$DEV_COMPOSE_FILE" ]] \
        || fail "development Compose file not found: $DEV_COMPOSE_FILE (set TUVTK_DEV_COMPOSE_FILE to override)"
    prepare_docker
}

compose() {
    "${DOCKER_COMMAND[@]}" compose \
        --env-file "$ENV_FILE" \
        --project-directory "$APP_DIR" \
        -f "$COMPOSE_FILE" \
        -p "$PROJECT_NAME" \
        "$@"
}

dev_compose() {
    "${DOCKER_COMMAND[@]}" compose \
        --env-file "$ENV_FILE" \
        --project-directory "$APP_DIR" \
        -f "$COMPOSE_FILE" \
        -f "$DEV_COMPOSE_FILE" \
        -p "${PROJECT_NAME}-dev" \
        "$@"
}

django_exec() {
    compose exec "$WEB_SERVICE" python manage.py "$@"
}

env_value() {
    local key="$1"
    awk -v key="$key" '
        $0 ~ "^[[:space:]]*" key "=" {
            sub("^[[:space:]]*" key "=", "")
            sub("\\r$", "")
            value=$0
        }
        END { print value }
    ' "$ENV_FILE"
}

database_identity() {
    DB_NAME="$(env_value POSTGRES_DB)"
    DB_USER="$(env_value POSTGRES_USER)"
    [[ -n "$DB_NAME" ]] || fail "POSTGRES_DB is missing from $ENV_FILE."
    [[ -n "$DB_USER" ]] || fail "POSTGRES_USER is missing from $ENV_FILE."
}

has_verbosity() {
    local argument
    for argument in "$@"; do
        case "$argument" in
            -v|--verbosity|--verbosity=*) return 0 ;;
        esac
    done
    return 1
}

export_sql() {
    local destination="$1"
    database_identity

    if [[ -d "$destination" || "$destination" == */ ]]; then
        mkdir -p "$destination"
        destination="${destination%/}/tuvtk-$(date -u +%Y%m%dT%H%M%SZ).sql"
    else
        local parent
        parent="$(dirname "$destination")"
        [[ -d "$parent" ]] || fail "output directory does not exist: $parent"
    fi

    local temporary="${destination}.tmp.$$"
    umask 077
    if ! compose exec -T "$DB_SERVICE" pg_dump -U "$DB_USER" -d "$DB_NAME" >"$temporary"; then
        rm -f "$temporary"
        fail "PostgreSQL export failed."
    fi
    mv "$temporary" "$destination"
    printf 'Database exported to %s\n' "$destination"
}

import_sql() {
    local source="$1"
    [[ -f "$source" ]] || fail "SQL file not found: $source"
    database_identity
    printf 'Importing %s into database %s...\n' "$source" "$DB_NAME"
    compose exec -T "$DB_SERVICE" psql -v ON_ERROR_STOP=1 -U "$DB_USER" -d "$DB_NAME" <"$source"
}

create_backup() {
    local backup_directory="$1"
    mkdir -p "$backup_directory"
    chmod 0700 "$backup_directory"
    [[ -d "$backup_directory" && -w "$backup_directory" ]] || fail "backup directory is not writable: $backup_directory"
    database_identity

    local work_directory archive timestamp
    timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
    archive="${backup_directory%/}/tuvtk-backup-${timestamp}.tar.gz"
    work_directory="$(mktemp -d "${TMPDIR:-/tmp}/tuvtk-backup.XXXXXX")"

    mkdir -p "$work_directory/env" "$work_directory/deployment"
    printf '%s\n' "$BACKUP_FORMAT" >"$work_directory/BACKUP_FORMAT"
    printf 'created_utc=%s\nproject_name=%s\ndatabase_name=%s\ndatabase_user=%s\n' \
        "$timestamp" "$PROJECT_NAME" "$DB_NAME" "$DB_USER" >"$work_directory/manifest"
    cp -- "$ENV_FILE" "$work_directory/env/tuvtk.env"
    cp -- "$COMPOSE_FILE" "$work_directory/deployment/compose.yaml"
    for deployment_file in Dockerfile docker/nginx.conf.template docker/start-web.sh; do
        if [[ -f "$APP_DIR/$deployment_file" ]]; then
            mkdir -p "$work_directory/deployment/$(dirname "$deployment_file")"
            cp -- "$APP_DIR/$deployment_file" "$work_directory/deployment/$deployment_file"
        fi
    done

    if ! compose exec -T "$DB_SERVICE" pg_dump -U "$DB_USER" -d "$DB_NAME" >"$work_directory/database.sql"; then
        rm -rf -- "$work_directory"
        fail "database export failed; no backup archive was created."
    fi
    if ! tar -C "$work_directory" -czf "$archive" .; then
        rm -rf -- "$work_directory"
        fail "unable to create backup archive."
    fi
    rm -rf -- "$work_directory"
    chmod 0600 "$archive"
    printf 'Backup created: %s\n' "$archive"
    printf 'Media, private media, static files, and Docker volumes were intentionally excluded.\n'
}

restore_backup() {
    local archive="$1"
    [[ -f "$archive" ]] || fail "backup archive not found: $archive"

    local work_directory
    work_directory="$(mktemp -d "${TMPDIR:-/tmp}/tuvtk-restore.XXXXXX")"
    if tar -tzf "$archive" | awk '
        /(^|\/)\.\.($|\/)/ || /^\// { unsafe=1 }
        END { exit unsafe ? 0 : 1 }
    '; then
        rm -rf -- "$work_directory"
        fail "backup archive contains unsafe paths."
    fi
    tar -xzf "$archive" -C "$work_directory" || fail "unable to read backup archive."
    [[ -f "$work_directory/BACKUP_FORMAT" ]] || fail "archive is not a tuvtk wrapper backup."
    [[ "$(<"$work_directory/BACKUP_FORMAT")" == "$BACKUP_FORMAT" ]] || fail "unsupported backup format."
    [[ -f "$work_directory/database.sql" && -f "$work_directory/env/tuvtk.env" && -f "$work_directory/manifest" ]] \
        || fail "backup is incomplete; database.sql, env/tuvtk.env, and manifest are required."

    rm -rf -- "$work_directory"
    fail "archive format $BACKUP_FORMAT was validated, but automated restore is intentionally disabled until the Phase 2 installer and environment model are finalized. No files or database data were changed."
}

clean_generated() {
    require_app_dir
    find "$APP_DIR" \
        \( -path "$APP_DIR/.git" -o -path "$APP_DIR/.venv" -o -path "$APP_DIR/node_modules" \
           -o -path "$APP_DIR/media" -o -path "$APP_DIR/private_media" -o -path "$APP_DIR/staticfiles" \
           -o -path "$APP_DIR/.postgresql" \) -prune -o \
        -type d \( -name __pycache__ -o -name .pytest_cache -o -name .mypy_cache \) -exec rm -rf -- {} +
    find "$APP_DIR" \
        \( -path "$APP_DIR/.git" -o -path "$APP_DIR/.venv" -o -path "$APP_DIR/node_modules" \
           -o -path "$APP_DIR/media" -o -path "$APP_DIR/private_media" -o -path "$APP_DIR/staticfiles" \
           -o -path "$APP_DIR/.postgresql" \) -prune -o \
        -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*.tmp' \) -delete
    rm -rf -- "$APP_DIR/tmp" "$APP_DIR/test-results" "$APP_DIR/playwright-report"
    printf 'Removed safe local caches and temporary test artifacts.\n'
}

command_name="${1:-help}"
if (($#)); then
    shift
fi

case "$command_name" in
    help|-h|--help)
        usage
        ;;
    dev)
        (($# == 0)) || fail "usage: tuvtk dev"
        prepare_dev_compose
        dev_compose up -d db
        dev_compose run --rm init
        dev_compose up -d web tailwind
        ;;
    dev-build)
        (($# == 0)) || fail "usage: tuvtk dev-build"
        prepare_dev_compose
        dev_compose build web
        dev_compose up -d db
        dev_compose run --rm init
        dev_compose up -d web tailwind
        ;;
    dev-logs)
        (($# <= 1)) || fail "usage: tuvtk dev-logs [SERVICE]"
        prepare_dev_compose
        dev_compose logs -f "$@"
        ;;
    tailwind)
        (($# == 0)) || fail "usage: tuvtk tailwind"
        prepare_dev_compose
        dev_compose up -d tailwind
        dev_compose logs -f tailwind
        ;;
    npm)
        (($# > 0)) || fail "usage: tuvtk npm COMMAND [ARGS...]"
        prepare_dev_compose
        dev_compose run --rm --no-deps tailwind npm "$@"
        ;;
    context)
        require_app_dir
        if [[ -f "$APP_DIR/scripts/generate_codex_context.py" ]]; then
            if command -v python3 >/dev/null 2>&1; then
                (cd "$APP_DIR" && python3 scripts/generate_codex_context.py "$@")
            elif command -v python >/dev/null 2>&1; then
                (cd "$APP_DIR" && python scripts/generate_codex_context.py "$@")
            else
                fail "Python 3 is required for context generation. Install host Python 3, or run 'docker compose run --rm web python scripts/generate_codex_context.py' with an image that contains the current source."
            fi
        elif [[ -f "$APP_DIR/generate_codex_context.bat" ]]; then
            fail "the current context generator is Windows-only; Phase 4 will replace it with scripts/generate_codex_context.py."
        else
            fail "no context generator was found in $APP_DIR."
        fi
        ;;
    clean)
        (($# == 0)) || fail "usage: tuvtk clean"
        clean_generated
        ;;
    *)
        prepare_compose
        case "$command_name" in
            status|ps) (($# == 0)) || fail "usage: tuvtk $command_name"; compose ps ;;
            up|start) (($# == 0)) || fail "usage: tuvtk $command_name"; compose up -d ;;
            down|stop) (($# == 0)) || fail "usage: tuvtk $command_name"; compose down ;;
            restart) (($# == 0)) || fail "usage: tuvtk restart"; compose restart ;;
            build) (($# == 0)) || fail "usage: tuvtk build"; compose build && compose up -d ;;
            rebuild) (($# == 0)) || fail "usage: tuvtk rebuild"; compose build --no-cache && compose up -d ;;
            logs)
                (($# <= 1)) || fail "usage: tuvtk logs [SERVICE]"
                compose logs -f "$@"
                ;;
            check) (($# == 0)) || fail "usage: tuvtk check"; django_exec check ;;
            test)
                if has_verbosity "$@"; then
                    django_exec test "$@"
                else
                    django_exec test "$@" -v 0
                fi
                ;;
            migrate) django_exec migrate "$@" ;;
            makemigrations) django_exec makemigrations "$@" ;;
            collectstatic) (($# == 0)) || fail "usage: tuvtk collectstatic"; django_exec collectstatic --noinput ;;
            shell) (($# == 0)) || fail "usage: tuvtk shell"; django_exec shell ;;
            dbshell) (($# == 0)) || fail "usage: tuvtk dbshell"; django_exec dbshell ;;
            django) (($# > 0)) || fail "usage: tuvtk django COMMAND [ARGS...]"; django_exec "$@" ;;
            exec)
                (($# >= 2)) || fail "usage: tuvtk exec SERVICE COMMAND [ARGS...]"
                compose exec "$@"
                ;;
            export-sql) (($# == 1)) || fail "usage: tuvtk export-sql PATH"; export_sql "$1" ;;
            import-sql) (($# == 1)) || fail "usage: tuvtk import-sql SQL_FILE"; import_sql "$1" ;;
            backup) (($# == 1)) || fail "usage: tuvtk backup BACKUP_DIRECTORY"; create_backup "$1" ;;
            restore) (($# == 1)) || fail "usage: tuvtk restore BACKUP_ARCHIVE"; restore_backup "$1" ;;
            *) fail "unknown command: $command_name (run 'tuvtk help')" ;;
        esac
        ;;
esac
```

## `CODEX_RESUME_PHASES.md`

Size: 27.0 KB

````markdown
# TUVTK Django Linux/Docker Workflow Cleanup — Resume Plan

## 1. Objective

This Django project already has a functional Linux Docker deployment, but the repository historically presented Windows local development as the primary workflow.

The goal is to make the project Linux/Docker-first by adding:

* a permanent Docker command wrapper;
* an EspoCRM-style installer;
* a development Compose workflow;
* a cross-platform Codex context generator;
* cleanup of obsolete Windows wrappers;
* improved dependency reproducibility;
* removal of personal `.vscode/` state;
* Linux/Docker-first README and AGENTS instructions;
* final safe validation.

The EspoCRM installer is only a behavioral reference. Do not copy EspoCRM-specific PHP, MariaDB, or application logic.

Useful EspoCRM-style patterns to preserve conceptually:

* central argument parsing and action dispatch;
* `--yes`, `--environment`, `--command`, and `--clean` modes;
* backup paths and backup-before-overwrite behavior;
* domain, SSL-mode, and public/private IP arguments;
* prerequisite and Docker preparation;
* command-wrapper-only updates;
* a clear final installation summary.

The required production lifecycle must remain:

1. Build the application image.
2. Start PostgreSQL and wait for readiness.
3. Run the one-shot `init` service:
   * `python manage.py migrate --noinput`
   * `python manage.py collectstatic --noinput`
4. Start Gunicorn (`web`) and Nginx (`nginx`).
5. Run Django checks where safe.

## 2. Completed phases

### Phase 0 — Inspection

Completed without modifying files.

Important findings:

* Deployment: `compose.yaml`, `Dockerfile`, `docker/start-web.sh`, `docker/nginx.conf.template`, `.dockerignore`, and `.env.example`.
* Installer: `install.sh`.
* Behavioral reference: `references/espocrm-install.sh`.
* Documentation: `README.md` and `AGENTS.md`.
* Dependencies: `requirements.txt`, `requirements-dev.txt`, and `requirements-deploy.txt`.
* Frontend: `theme/static_src/package.json` and `theme/static_src/package-lock.json`.
* Windows context tools: `generate_codex_context.bat`, `generate_codex_context_updated.bat`, and `generate_codex_context_v3_ascii.bat`.
* Editor state: `.vscode/settings.json` and `.vscode/extensions.json`.
* Production Compose services:
  * `db`: PostgreSQL 17 with persistent storage and health check;
  * `init`: migrations and static collection;
  * `web`: Gunicorn;
  * `nginx`: reverse proxy and static/media server.

### Phase 1 — Permanent wrapper

Completed.

Added executable `bin/tuvtk`, replacing commands such as:

```bash
sudo docker compose \
  --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app \
  -f /opt/tuvtk/app/compose.yaml \
  exec web python manage.py test apps.dashboard -v 0
```

with:

```bash
./bin/tuvtk test apps.dashboard
```

Defaults:

* `APP_DIR=/opt/tuvtk/app`
* `ENV_FILE=/etc/tuvtk/tuvtk.env`
* `COMPOSE_FILE=/opt/tuvtk/app/compose.yaml`
* `PROJECT_NAME=tuvtk`

Supported overrides:

* `TUVTK_APP_DIR`
* `TUVTK_ENV_FILE`
* `TUVTK_COMPOSE_FILE`
* `TUVTK_PROJECT_NAME`

Implemented production and maintenance commands include `help`, `status`, `ps`, `up`, `start`, `down`, `stop`, `restart`, `build`, `rebuild`, `logs`, `check`, `test`, `migrate`, `makemigrations`, `collectstatic`, `shell`, `dbshell`, `exec`, `django`, `context`, `backup`, `restore`, `export-sql`, `import-sql`, and `clean`.

Backup/restore is deliberately conservative:

* backup captures plain database SQL, environment/configuration, manifest, and basic deployment files;
* media and Docker volumes are excluded;
* restore validates the wrapper archive format but intentionally refuses mutation until installer/environment semantics are finalized further.

Phase 1 validation completed:

```bash
bash -n bin/tuvtk
chmod +x bin/tuvtk
./bin/tuvtk help
```

`./bin/tuvtk status` was attempted but correctly refused because the non-interactive session lacked Docker daemon access and passwordless sudo.

### Phase 2 — EspoCRM-style installer

Completed by replacing `install.sh`. No Phase 2 compatibility change was needed in `bin/tuvtk`.

Implemented options include:

* `--help`, `--yes`, `--environment`, `--command`, `--network`, and `--clean`;
* `--backup-path`, app/env/Compose/project/data path overrides;
* repository URL, branch/ref, and SSH deploy-key support;
* `--domain` and backward-compatible `--public-host`;
* public/private IPv4 detection;
* HTTP/HTTPS port options;
* database and Django secret overrides;
* admin credential parsing;
* SSL, Let's Encrypt, and own-certificate mode parsing;
* backward-compatible `--install-dir` and `--ref`.

Important behavior:

* central action dispatch;
* Debian/Ubuntu prerequisite handling;
* Docker Engine and Compose plugin detection;
* existing Git checkout/update support;
* existing environment values preserved;
* environment backup before updates;
* missing secrets/passwords generated securely;
* deployment backup before checkout updates;
* conservative `--clean` safety checks;
* database/media persistence left untouched;
* `/usr/local/bin/tuvtk` installed as a small launcher that preserves custom installer paths;
* production `db` → `init` → `web`/`nginx` lifecycle preserved.

Conservative decisions:

* Current Compose/Nginx is HTTP-only. SSL modes fail before mutation instead of claiming HTTPS works.
* Installer deployment backups exclude the database and media. Use `tuvtk backup` for the wrapper's operational backup format.
* Automated superuser creation is deferred. Use `tuvtk django createsuperuser`.
* `--clean` refuses tracked changes outside known deployment files.
* `--network` is a harmless no-op because Compose declares no external network.

Phase 2 validation completed:

```bash
bash -n install.sh
bash install.sh --help
chmod +x install.sh
./install.sh --help
git diff --check -- install.sh
```

The HTTPS negative path was also verified to fail with “No changes were made.” No package installation, build, restart, migration, static collection, clean, backup, or certificate action was run.

### Phase 3 — Development Compose workflow

Completed.

Added `compose.dev.yaml` and updated `bin/tuvtk`. Production `compose.yaml` and `install.sh` were not changed in this phase.

Development behavior:

* `db`: isolated development PostgreSQL volume;
* `init`: migrations/static collection against development volumes;
* `web`: source-mounted Django `runserver` with `DEBUG=True`;
* `tailwind`: dedicated Node 22 watcher/npm service;
* production Nginx is not started by development commands;
* default development HTTP port is `${TUVTK_DEV_PORT:-8000}`;
* PostgreSQL and Tailwind expose no public ports;
* project name is `${TUVTK_PROJECT_NAME:-tuvtk}-dev`;
* development database, media, private media, static output, Bootstrap cache, and Node modules use development-specific volumes.

Commands added:

```bash
./bin/tuvtk dev
./bin/tuvtk dev-build
./bin/tuvtk dev-logs
./bin/tuvtk dev-logs web
./bin/tuvtk tailwind
./bin/tuvtk npm install
./bin/tuvtk npm run build
```

`dev` starts development PostgreSQL, runs `init`, then starts Django and Tailwind detached. The first Tailwind start runs `npm ci` when its dependency volume is empty.

Phase 3 validation completed:

* wrapper syntax/help;
* merged production/development Compose config;
* development service and volume listings;
* production-only Compose config;
* wrapper whitespace check.

No services, migrations, builds, npm installation, or watchers were actually started.

### Phase 4 — Cross-platform Codex context generator

Completed.

Added:

* `scripts/generate_codex_context.py`
* `generate_codex_context.sh`
* `generate_codex_context.ps1`

Converted to thin Python compatibility wrappers:

* `generate_codex_context.bat`
* `generate_codex_context_updated.bat` (deprecated)
* `generate_codex_context_v3_ascii.bat` (deprecated)

Updated `bin/tuvtk context` to use host `python3`, then `python`, and to pass through generator arguments. Docker is not required when host Python is available.

The generator:

* uses only the Python standard library and is Python 3.12 compatible;
* detects the Git/project root;
* supports `--root`, `--output`, `--max-file-kb`, `--include-tests`, `--no-tests`, and `--verbose`;
* detects Django apps;
* excludes migrations by default;
* excludes env files, secrets, media, archives, databases, certificates, private keys, generated context, node modules, caches, and binary formats;
* redacts common secret assignments and skips private-key/secret-heavy content;
* atomically regenerates the context output;
* preserves `codex-context/files/...` source snapshots because the current `AGENTS.md` still references them;
* writes both required root outputs and compatibility copies inside `codex-context/`.

Generated outputs:

* `codex-context/`
* `codex-context-index.md`
* `codex-file-map.txt`
* `codex-context/project-core.md`
* `codex-context/apps/<app>.md`
* `codex-context/files/<source-path>.md`

Final Phase 4 generation result with an 80 KB limit:

* included files: 223;
* skipped files: 10;
* pruned directories: 13;
* total included source size: approximately 1.35 MB;
* tests included;
* migrations excluded.

Phase 4 validation completed:

```bash
python3 -m py_compile scripts/generate_codex_context.py
bash -n bin/tuvtk
bash -n generate_codex_context.sh
./bin/tuvtk help
python3 scripts/generate_codex_context.py --help
./bin/tuvtk context --max-file-kb 80
cmp codex-context-index.md codex-context/codex-context-index.md
cmp codex-file-map.txt codex-context/codex-file-map.txt
```

Repeated generation produced stable counts. Path/content checks found no forbidden source paths, unredacted obvious secret assignments, or private-key markers in generated context.

### Phase 5 — Windows wrapper cleanup

Completed.

Removed the obsolete Windows virtualenv, local PostgreSQL, Django runserver, Tailwind watcher, and duplicate/deprecated context-generator wrappers. The only Windows wrappers retained are the thin Python context-generator compatibility launchers:

* `generate_codex_context.bat`;
* `generate_codex_context.ps1`.

`generate_codex_context.sh` remains the thin Linux/macOS launcher. Legacy references in `README.md` and `AGENTS.md` are intentionally deferred to the Phase 8 documentation rewrite.

### Phase 6 — Dependency reproducibility

Completed.

Added readable direct-dependency inputs while preserving the existing Docker-compatible filenames:

* `requirements.in` → `requirements.txt`;
* `requirements-dev.in` → `requirements-dev.txt`;
* `requirements-deploy.in` → `requirements-deploy.txt`.

Pip-tools was unavailable and was not installed, so the `.txt` files remain explicitly documented direct-requirement manifests rather than fabricated transitive locks. The previously loose dependencies were pinned to `psycopg[binary]==3.3.4`, `python-docx==1.2.0`, and `rapidfuzz==3.14.5`. Docker image tags remain versioned but patch-floating so upstream security/base-image patches remain available. Phase 7 must remove `.vscode/` and add it to `.gitignore`.

### Phase 7 — Remove `.vscode/`

Completed.

Removed tracked `.vscode/settings.json` and `.vscode/extensions.json`, removed the empty `.vscode/` directory, and added `.vscode/` to `.gitignore`. The directory is intentionally treated as personal editor state, not shared project configuration.

### Phase 8 — Rewrite README.md and AGENTS.md

Completed.

Rewrote repository documentation around the Linux/Docker-first installer, permanent `tuvtk` wrapper, isolated development Compose workflow, Python context generator, direct dependency inputs/manifests, HTTP-only SSL limitation, removed Windows-local workflow, and safe agent validation policy. Phase 9 final validation is next.

### Phase 9 — Final safe validation

Completed.

Shell syntax, Python compilation, wrapper help, context generation, generated-output exclusions/redaction, documentation consistency, `.vscode/` ignore behavior, global whitespace, and production/development Compose rendering all passed. Context generation included 214 files, skipped 13 files, and pruned 13 directories. No builds, service changes, migrations, static collection, npm commands, tests, imports, restores, or cleanup operations were run.

## 3. Current repository state

All planned Linux/Docker workflow cleanup phases are complete. Remaining work is limited to the manual follow-ups and operational validation recorded below.

Workflow files currently changed or untracked by completed phases include:

* modified `install.sh`;
* new `bin/tuvtk`;
* new `compose.dev.yaml`;
* new `scripts/generate_codex_context.py`;
* new `generate_codex_context.sh` and `generate_codex_context.ps1`;
* modified thin/deprecated context batch wrappers;
* regenerated `codex-context/`, `codex-context-index.md`, and `codex-file-map.txt`.

The worktree also contains unrelated pre-existing application changes. They belong to the user and must be preserved. At the time of this resume file, these included changes in dashboard, planificator, core templates/navigation/tests, theme CSS/JavaScript, and untracked HTMX/template/vendor support files. Do not reset, discard, overwrite, or fold those changes into workflow cleanup without explicit authorization.

The generated context intentionally reflects the current worktree, including uncommitted application source. Regeneration can therefore modify many tracked snapshot files and remove snapshots for excluded migrations or stale/deleted source files.

Files intentionally not yet updated:

* `README.md` remains Windows-first until Phase 8.
* `AGENTS.md` still names the old batch generator until Phase 8; compatibility wrappers remain so those references are not broken.
* Dependency files remain in their original structure until Phase 6.
* `.vscode/` was removed in Phase 7 and is ignored as personal editor state.

## 4. Important decisions already made

### Production behavior

Do not alter the existing production lifecycle or production Compose behavior without a demonstrated requirement. PostgreSQL, migrations/static collection, Gunicorn, and Nginx must remain ordered sensibly.

### Wrapper model

`bin/tuvtk` is the permanent project command. `/usr/local/bin/tuvtk` is installed by `install.sh --command` as a small launcher so custom app/env/Compose/project paths remain effective.

### Installer `--command` model

Match the useful EspoCRM behavior conceptually: update only the permanent command tool for an existing installation. Do not rebuild, restart, migrate, or reinstall the application in `--command` mode.

### Backup and restore

Keep backup/restore conservative until the environment and operational restore model receives dedicated testing. Do not present current wrapper restore as a complete disaster-recovery solution.

### SSL

Production remains HTTP-only. Installer SSL options are parsed but safely refused because current Compose/Nginx does not implement certificate automation or an HTTPS listener. Do not claim HTTPS works.

### Development isolation

Development uses a separate Compose project and separate persistent volumes. Do not point development PostgreSQL at the production bind-mounted database directory.

### Windows compatibility

The repository should become Linux/Docker-first. Keep only thin Windows compatibility wrappers that still provide clear value. Do not retain duplicate Windows implementations.

### `.vscode/` policy

The final decision supersedes the Phase 0 recommendation:

* `.vscode/` is personal/temporary editor state;
* remove tracked `.vscode/settings.json` and `.vscode/extensions.json` in Phase 7;
* add `.vscode/` to `.gitignore`;
* do not document `.vscode/` as shared project configuration.

### Generated context

The Python generator is authoritative. Shell, PowerShell, and batch files are launchers only. Keep compatibility copies of the index/map until `AGENTS.md` is rewritten and any consumers are checked.

## 5. Remaining phases with detailed instructions

### Phase 5 — Windows wrapper cleanup (completed)

Goal: remove or deprecate obsolete Windows-only local development wrappers.

Before deleting anything, search references in:

* `README.md`;
* `AGENTS.md`;
* scripts and comments;
* CI configuration, if present;
* documentation, if present;
* Compose and Docker files;
* all shell, batch, and PowerShell files.

Classify every tracked `.bat` and `.ps1` file.

Expected keep:

* `generate_codex_context.bat` as a thin compatibility launcher;
* optionally `generate_codex_context.ps1`, also thin.

Expected removal or deprecation after reference checks:

* `activate_venv.bat`;
* `runserver.bat`;
* `runserver.ps1`;
* `start_postgres.bat`;
* `stop_postgres.bat`;
* `watch_tailwind.ps1`;
* `generate_codex_context_updated.bat`;
* `generate_codex_context_v3_ascii.bat`.

Current `README.md` and `AGENTS.md` still reference several of these. Because full documentation rewrite is Phase 8, either:

1. keep short deprecation launchers/notes temporarily where deletion would create broken instructions; or
2. make only the minimum reference correction necessary and explicitly defer the full rewrite.

Do not leave the large Windows generator implementation; it has already been replaced with a thin deprecated launcher.

Phase 5 validation:

```bash
rg -n 'activate_venv|runserver\.(bat|ps1)|start_postgres|stop_postgres|watch_tailwind|generate_codex_context_(updated|v3_ascii)' README.md AGENTS.md .github docs scripts . 2>/dev/null
git status --short
git diff --check
```

Do not proceed to dependency or documentation work in this phase.

### Phase 6 — Dependency reproducibility (completed)

Goal: improve dependency reproducibility without application changes or unjustified upgrades.

Inspect:

* `requirements.txt`;
* `requirements-dev.txt`;
* `requirements-deploy.txt`;
* dependency installation in `Dockerfile`;
* Python version constraints implied by Django and the container.

Currently loose/ranged direct dependencies include:

* `psycopg[binary]>=3.1.12,<4`;
* `python-docx`;
* `rapidfuzz`.

Pinned direct dependencies already include Django, Pillow, OpenPyXL, Requests, ReportLab, svglib, django-tailwind, Gunicorn, and development tools.

Preferred structure:

```text
requirements/base.in
requirements/base.txt
requirements/dev.in
requirements/dev.txt
requirements/deploy.in
requirements/deploy.txt
```

A simpler `requirements.in`/`requirements.txt` structure is acceptable if it fits the repository better.

Rules:

* preserve readable direct requirements;
* pin currently loose direct dependencies;
* lock transitive dependencies only with a real resolver;
* use pip-tools if available and appropriate;
* do not fabricate lock output if pip-tools or dependency resolution is unavailable;
* do not install packages globally;
* do not upgrade major versions unless required and justified;
* do not modify application code.

Review but do not casually change these image tags:

* `node:22-bookworm-slim`;
* `python:3.12-slim-bookworm`;
* `postgres:17-bookworm`;
* `nginx:1.28-alpine`.

If digest pinning is not adopted, Phase 8 documentation must state that patch/security image updates are intentionally allowed.

Phase 6 validation should include the exact resolver/compile command if one is actually run and:

```bash
git diff --check
```

Do not run application tests automatically unless a narrow diagnostic genuinely requires them.

### Phase 7 — Remove `.vscode/` (completed)

Goal: remove personal editor state and make the policy explicit through ignore rules.

Actions:

* remove `.vscode/settings.json`;
* remove `.vscode/extensions.json`;
* remove the now-empty `.vscode/` directory;
* add `.vscode/` to `.gitignore`.

Do not preserve or document `.vscode/` as shared configuration.

Validation:

```bash
git status --short
git diff --check -- .gitignore
```

### Phase 8 — Rewrite README.md and AGENTS.md (completed)

Goal: make Linux/Docker the primary documented workflow.

README requirements:

* quick/fresh install;
* environment-only preparation;
* wrapper-only command update;
* production start, stop, restart, logs, and status;
* focused low-verbosity tests;
* migrations and static collection;
* conservative backup/restore status;
* development mode and development logs;
* Tailwind/npm development commands;
* HTTP-only SSL/domain warning;
* file locations;
* dependency/image reproducibility note.

Use examples such as:

```bash
tuvtk status
tuvtk start
tuvtk stop
tuvtk restart
tuvtk logs
tuvtk check
tuvtk test apps.dashboard
tuvtk migrate
tuvtk collectstatic
tuvtk backup /opt/tuvtk-backups
tuvtk dev
tuvtk dev-logs
tuvtk tailwind
tuvtk npm run build
```

Document paths:

* `/opt/tuvtk/app`;
* `/etc/tuvtk/tuvtk.env`;
* `/usr/local/bin/tuvtk`;
* `/opt/tuvtk-backups`.

Document development details:

* `compose.dev.yaml` uses isolated development database/media/static/node-module volumes;
* Nginx is not started by development commands;
* development uses `${TUVTK_DEV_PORT:-8000}`.

Document SSL accurately: current production is HTTP-only and installer SSL modes refuse safely.

AGENTS requirements:

* use `bin/tuvtk context`;
* use `bin/tuvtk check`;
* use `bin/tuvtk test <app>`;
* do not require `generate_codex_context.bat` as the primary workflow;
* a thin `.bat` launcher may be mentioned only as Windows compatibility;
* retain repository routing, ownership, security, frontend, and focused-test guidance that remains valid.

Remove Windows-first instructions involving local `.venv`, bundled `.postgresql`, PowerShell runserver, and obsolete Windows wrappers.

Validation:

```bash
git diff --check -- README.md AGENTS.md
rg -n 'start_postgres|runserver\.(bat|ps1)|watch_tailwind|generate_codex_context_v3_ascii' README.md AGENTS.md
```

After documentation/instruction changes, regenerate context with:

```bash
bin/tuvtk context --max-file-kb 80
```

### Phase 9 — Final safe validation (completed)

Run safe checks only:

```bash
bash -n install.sh
bash -n bin/tuvtk
bash -n generate_codex_context.sh
python3 -m py_compile scripts/generate_codex_context.py
./bin/tuvtk help
./bin/tuvtk context --max-file-kb 80
git diff --check
```

If `python3` is unavailable, use:

```bash
python -m py_compile scripts/generate_codex_context.py
```

If Docker is available and safe, render configurations without starting services:

```bash
docker compose \
  --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app \
  -f /opt/tuvtk/app/compose.yaml \
  -p tuvtk config --quiet

docker compose \
  --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app \
  -f /opt/tuvtk/app/compose.yaml \
  -f /opt/tuvtk/app/compose.dev.yaml \
  -p tuvtk-dev config --quiet
```

Do not run service-changing or destructive commands unless separately authorized:

* no full build/rebuild;
* no service start/restart;
* no migration or collectstatic;
* no npm installation;
* no database import/restore;
* no clean operation.

The final report must list completed phases, files added/changed/removed, the final command set, fresh install, environment-only preparation, wrapper-only update, context generation, low-verbosity testing, development startup, backup usage, `.vscode/` removal, and remaining manual risks.

## 6. Validation commands

Use the smallest checks appropriate to the active phase. The consolidated safe validation set is:

```bash
bash -n install.sh
bash -n bin/tuvtk
bash -n generate_codex_context.sh
python3 -m py_compile scripts/generate_codex_context.py
./bin/tuvtk help
./bin/tuvtk context --max-file-kb 80
git status --short
git diff --check
```

Safe Compose rendering, when Docker CLI and the env file are available:

```bash
docker compose --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app \
  -f /opt/tuvtk/app/compose.yaml \
  -p tuvtk config --quiet

docker compose --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app \
  -f /opt/tuvtk/app/compose.yaml \
  -f /opt/tuvtk/app/compose.dev.yaml \
  -p tuvtk-dev config --quiet
```

Focused tests are not run automatically under repository policy. Give the user the command unless explicitly authorized:

```bash
bin/tuvtk test apps.dashboard
```

## 7. Safety rules

* Always preserve unrelated uncommitted application changes.
* Read applicable `AGENTS.md` files before editing.
* Before removing files, search README, AGENTS, scripts, CI, Compose, Docker, documentation, and comments for references.
* Do not modify Django application logic for workflow cleanup unless compatibility strictly requires it and the user authorizes it.
* Do not delete database storage, Docker volumes, uploaded media, private media, secrets, or environment files.
* Never overwrite an existing env file without a backup.
* Do not point development PostgreSQL at production storage.
* Do not claim SSL works unless Compose/Nginx truly implements HTTPS.
* Do not fake lock files, test results, Docker results, or validation results.
* Do not run automated test suites by default. Use the narrowest explicitly authorized target with `-v 0`.
* Do not run builds, service restarts, migrations, collectstatic, npm installation, database import/restore, or clean operations merely for validation.
* If Docker, Python, pip-tools, ShellCheck, or another tool is unavailable, report that honestly and continue with safe checks.
* Keep changes phase-scoped and reviewable.
* After source or instruction changes, regenerate cross-platform context with `bin/tuvtk context`; do not return to the old batch implementation.

## 8. Exact resume prompts for future Codex sessions

### Phase 5 historical prompt

```text
Proceed with Phase 5 only from CODEX_RESUME_PHASES.md.

Clean up obsolete Windows wrappers after checking every reference required by the resume plan.

Do not proceed to Phase 6. Preserve unrelated uncommitted changes. Keep only thin context-generation compatibility wrappers where useful, and do not break README.md or AGENTS.md references without a minimal compatibility/deprecation path.
```

### Phase 6 historical prompt

```text
Proceed with Phase 6 only from CODEX_RESUME_PHASES.md.

Improve dependency reproducibility without modifying application logic or performing unjustified upgrades.

Do not proceed to Phase 7. Do not fake resolved lock files if pip-tools or dependency resolution is unavailable. Report exact resolver commands and limitations.
```

### Phase 7 historical prompt

```text
Proceed with Phase 7 only from CODEX_RESUME_PHASES.md.

Remove the tracked .vscode/ directory and add .vscode/ to .gitignore.

Do not proceed to Phase 8. Preserve all unrelated changes and validate only the editor-policy change.
```

### Phase 8 historical prompt

```text
Proceed with Phase 8 only from CODEX_RESUME_PHASES.md.

Rewrite README.md and AGENTS.md around the Linux/Docker-first installer, wrapper, development Compose, and Python context-generator workflows.

Do not proceed to Phase 9. Remove Windows-first instructions, retain valid repository safety contracts, and regenerate Codex context after the documentation changes.
```

### Phase 9 historical prompt

```text
Proceed with Phase 9 only from CODEX_RESUME_PHASES.md.

Run safe final validation and produce the final project report.

Do not run builds, starts/restarts, migrations, collectstatic, npm installation, tests, clean, database import, or restore unless explicitly authorized and demonstrably safe.
```

### Generic status audit

```text
Read CODEX_RESUME_PHASES.md and inspect the current git status. Do not implement anything yet.

Report which cleanup phases are complete, which phase is next, whether the worktree differs from the resume record, and any safety concerns before continuing.
```
````

## `core/__init__.py`

Size: 0 B

```python
```

## `core/admin.py`

Size: 386 B

```python
from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'has_avatar')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    @admin.display(boolean=True, description='Avatar')
    def has_avatar(self, profile):
        return bool(profile.avatar)
```

## `core/apps.py`

Size: 149 B

```python
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from . import signals  # noqa: F401
```

## `core/context_processors.py`

Size: 3.6 KB

```python
import re

from django.urls import reverse

from .navigation import NAVIGATION


def _is_active(item: dict, current_url_name: str) -> bool:
    active_names = item.get("active_url_names", (item.get("url_name"),))
    return bool(current_url_name and current_url_name in active_names)


def _is_allowed(item: dict, request, permissions: set[str]) -> bool:
    permission = item.get("permission")
    return not permission or request.user.is_superuser or permission in permissions


def build_navigation(request, permissions: set[str] | None = None) -> list[dict]:
    resolver_match = request.resolver_match
    current_url_name = resolver_match.view_name if resolver_match else ""
    permissions = permissions if permissions is not None else getattr(
        request, "_application_shell_permissions", set()
    )
    navigation = []
    for section in NAVIGATION:
        items = []
        for item in section["items"]:
            children = [
                {**child, "is_active": _is_active(child, current_url_name)}
                for child in item.get("children", ())
                if _is_allowed(child, request, permissions)
            ]
            if item.get("children") and not children:
                continue
            if not _is_allowed(item, request, permissions):
                continue
            items.append(
                {
                    **item,
                    "children": children,
                    "is_active": _is_active(item, current_url_name)
                    or any(child["is_active"] for child in children),
                }
            )
        navigation.append({**section, "items": items})
    return navigation


def build_application_shell(request, profile=None, permissions: set[str] | None = None) -> dict:
    user_display_name = "Vizitator"
    user_initials = "VI"
    user_avatar_url = ""
    if request.user.is_authenticated:
        username = request.user.get_username()
        full_name = request.user.get_full_name()
        user_display_name = full_name or username
        full_name_parts = full_name.split()
        username_parts = [part for part in re.split(r"[\W_]+", username) if part]
        if len(full_name_parts) > 1:
            user_initials = f"{full_name_parts[0][0]}{full_name_parts[-1][0]}".upper()
        elif len(username_parts) > 1:
            user_initials = f"{username_parts[0][0]}{username_parts[-1][0]}".upper()
        else:
            user_initials = username[:2].upper() or "U"
        if profile and profile.avatar:
            user_avatar_url = profile.avatar.url
    navigation = build_navigation(request, permissions)
    active_navigation_url = ""
    for section in navigation:
        for item in section["items"]:
            active_child = next(
                (child for child in item["children"] if child["is_active"]),
                None,
            )
            active_item = active_child or (item if item["is_active"] else None)
            if active_item and active_item.get("url_name"):
                active_navigation_url = reverse(active_item["url_name"])
                break
        if active_navigation_url:
            break

    return {
        "app_navigation": navigation,
        "active_navigation_url": active_navigation_url,
        "app_name": "Platforma TUVTK",
        "app_tagline": "Operațiuni interne",
        "user_display_name": user_display_name,
        "user_initials": user_initials,
        "user_avatar_url": user_avatar_url,
    }


def application_shell(request):
    shell = getattr(request, "application_shell", None)
    return shell if shell is not None else build_application_shell(request)
```

## `core/middleware.py`

Size: 1.1 KB

```python
from .context_processors import build_application_shell
from .models import UserProfile


class ApplicationShellMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._application_shell_profile = None
        request._application_shell_permissions = set()
        if request.user.is_authenticated:
            request._application_shell_profile = (
                UserProfile.objects.only("avatar", "user_id").filter(user_id=request.user.pk).first()
            )
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and not request.user.is_superuser:
            request._application_shell_permissions = request.user.get_all_permissions()
        request.application_shell = build_application_shell(
            request,
            getattr(request, "_application_shell_profile", None),
            getattr(request, "_application_shell_permissions", set()),
        )
        return None
```

## `core/mixins.py`

Size: 1.5 KB

```python
from django.http import HttpResponse
from django.urls import reverse


class HtmxPageMixin:
    """Return a page fragment for explicit HTMX navigation requests."""

    htmx_template_name = "includes/htmx_page.html"
    htmx_content_template = None
    shell_page_title = "Platforma TUVTK"
    shell_nav_url_name = None

    def is_htmx_fragment_request(self):
        headers = self.request.headers
        return (
            headers.get("HX-Request") == "true"
            and headers.get("HX-History-Restore-Request") != "true"
        )

    def get_template_names(self):
        if self.is_htmx_fragment_request():
            return [self.htmx_template_name]
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "htmx_content_template": self.htmx_content_template,
                "shell_page_title": self.shell_page_title,
                "shell_active_nav_url": reverse(self.shell_nav_url_name),
            }
        )
        return context

    def handle_no_permission(self):
        response = super().handle_no_permission()
        if (
            self.request.headers.get("HX-Request") == "true"
            and response.status_code in {301, 302}
            and response.get("Location")
        ):
            return HttpResponse(
                status=204,
                headers={"HX-Redirect": response["Location"]},
            )
        return response
```

## `core/models.py`

Size: 384 B

```python
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True)

    def __str__(self):
        return f'{self.user.get_username()} profile'
```

## `core/navigation.py`

Size: 5.5 KB

```python
NAVIGATION = (
    {
        "label": "Overview",
        "items": (
            {
                "label": "Dashboard",
                "icon": "grid-1x2-fill",
                "url_name": "dashboard:index",
                "htmx": True,
            },
            {
                "label": "Task-uri",
                "icon": "list-task",
                "url_name": "tasks:index",
                "active_url_names": (
                    "tasks:index",
                    "tasks:board_create",
                    "tasks:board_kanban",
                    "tasks:board_list",
                    "tasks:board_settings",
                    "tasks:task_create",
                    "tasks:task_edit",
                ),
            },
        ),
    },
    {
        "label": "Operations",
        "items": (
            {
                "label": "Planificator",
                "icon": "calendar3",
                "children": (
                    {
                        "label": "Generator perioade",
                        "url_name": "planificator:generator_perioade",
                        "permission": "planificator.use_course_planning",
                        "active_url_names": (
                            "planificator:generator_perioade",
                            "planificator:generator_perioade_result",
                        ),
                    },
                    {
                        "label": "Convertor Word",
                        "url_name": "planificator:word_converter",
                        "permission": "planificator.use_word_matcher",
                    },
                    {
                        "label": "Convertor XML",
                        "url_name": "planificator:xml_formatter",
                        "permission": "planificator.use_xml_export",
                    },
                    {
                        "label": "Actualizeaza cursuri",
                        "url_name": "planificator:actualizeaza_cursuri",
                        "permission": "planificator.use_course_planning",
                    },
                    {
                        "label": "Istoric",
                        "url_name": "planificator:istoric",
                        "htmx": True,
                        "permission": "planificator.use_course_planning",
                        "active_url_names": (
                            "planificator:istoric",
                            "planificator:istoric_detail",
                        ),
                    },
                ),
            },
            {
                "label": "Flota",
                "icon": "car-front-fill",
                "url_name": "flota:index",
                "active_url_names": (
                    "flota:index",
                    "flota:vehicle_create",
                    "flota:vehicle_detail",
                    "flota:vehicle_edit",
                    "flota:maintenance_create",
                    "flota:maintenance_edit",
                    "flota:maintenance_type_list",
                    "flota:maintenance_type_create",
                    "flota:maintenance_type_edit",
                ),
            },
            {
                "label": "Diplome",
                "icon": "certificate",
                "icon_set": "mdi",
                "children": (
                    {
                        "label": "Liste",
                        "url_name": "diplome:list_index",
                    },
                    {
                        "label": "Template-uri",
                        "url_name": "diplome:template_list",
                        "active_url_names": (
                            "diplome:template_list",
                            "diplome:template_create",
                            "diplome:template_editor",
                            "diplome:template_preview",
                        ),
                    },
                    {
                        "label": "Generator diplome",
                        "url_name": "diplome:generation_index",
                        "active_url_names": (
                            "diplome:generation_index",
                            "diplome:generation_preview",
                            "diplome:generation_create",
                            "diplome:generation_bulk_create",
                            "diplome:generation_download",
                        ),
                    },
                    {
                        "label": "Istoric",
                        "url_name": "diplome:history_index",
                        "active_url_names": (
                            "diplome:history_index",
                            "diplome:batch_detail",
                            "diplome:batch_zip_download",
                        ),
                    },
                ),
            },
            {
                "label": "Bibliotecă media",
                "icon": "images",
                "url_name": "media_library:index",
                "active_url_names": (
                    "media_library:index",
                    "media_library:content",
                    "media_library:delete",
                ),
            },
        ),
    },
    {
        "label": "Administration",
        "items": (
            {"label": "Users", "icon": "people"},
            {"label": "Roles & permissions", "icon": "shield-check"},
            {"label": "Integrations", "icon": "diagram-3"},
            {"label": "Audit log", "icon": "file-earmark-text"},
            {"label": "Settings", "icon": "gear"},
        ),
    },
)
```

## `core/signals.py`

Size: 334 B

```python
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

## `core/templates/404.html`

Size: 2.8 KB

```html
{% extends "layouts/base.html" %}

{% block title %}Pagina nu a fost gasita | Platforma TUVTK{% endblock %}

{% block content %}
    <section class="mx-auto flex min-h-[calc(100dvh-10rem)] w-full max-w-5xl items-center py-8">
        <div class="grid w-full gap-6 lg:grid-cols-[minmax(0,1fr)_18rem] lg:items-center">
            <div class="space-y-5">
                <div class="badge badge-outline badge-primary">Eroare 404</div>
                <div class="space-y-3">
                    <h1 class="text-2xl font-bold text-primary sm:text-[2rem]">Pagina nu a fost gasita</h1>
                    <p class="max-w-2xl text-sm leading-6 text-muted">
                        Adresa accesata nu exista sau a fost mutata. Verifica linkul ori revino in zona principala a platformei.
                    </p>
                </div>
                <div class="flex flex-wrap gap-2">
                    <a href="{% url 'dashboard:index' %}" class="btn btn-outline btn-primary btn-sm">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3 10.5 12 3l9 7.5M5.5 9v10.5h13V9" />
                        </svg>
                        Dashboard
                    </a>
                    <a href="{% url 'planificator:generator_perioade' %}" class="btn btn-outline btn-secondary btn-sm">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8 7h8M8 11h8M8 15h5M6 3.5h12A1.5 1.5 0 0 1 19.5 5v14A1.5 1.5 0 0 1 18 20.5H6A1.5 1.5 0 0 1 4.5 19V5A1.5 1.5 0 0 1 6 3.5Z" />
                        </svg>
                        Generator perioade
                    </a>
                </div>
            </div>

            <aside class="card card-border border-base-300 bg-base-100 shadow-none" aria-label="Detalii eroare">
                <div class="card-body gap-3 p-5">
                    <div class="flex items-center justify-between gap-3">
                        <span class="text-sm font-semibold text-primary">Status</span>
                        <span class="badge badge-secondary badge-outline">404</span>
                    </div>
                    <div class="divider my-0"></div>
                    <p class="text-sm text-base-content">Ruta solicitata nu este disponibila in Platforma TUVTK.</p>
                    <p class="text-xs text-muted">Daca ai ajuns aici dintr-un link intern, acesta trebuie actualizat.</p>
                </div>
            </aside>
        </div>
    </section>
{% endblock %}
```

## `core/templates/includes/htmx_page.html`

Size: 293 B

```html
<title>{{ shell_page_title }}</title>
<div
    id="page-content"
    class="mx-auto w-full max-w-[1600px] px-4 py-4 sm:px-5 sm:py-5 lg:px-6 lg:py-5"
    data-active-nav-url="{{ shell_active_nav_url }}"
    hx-history-elt
    hx-history="false"
>
    {% include htmx_content_template %}
</div>
```

## `core/templates/includes/sidebar.html`

Size: 6.0 KB

```html
{% load bootstrap_icons %}
<div class="drawer-side z-40 h-full min-h-0 is-drawer-close:overflow-visible">
    <label for="ops-sidebar" aria-label="Închide bara laterală" class="drawer-overlay"></label>
    <aside class="ops-sidebar flex h-full flex-col overflow-visible transition-[width] duration-200 is-drawer-close:w-14 is-drawer-open:w-72">
        <nav class="ops-sidebar-nav min-h-0 flex-1 overflow-y-auto py-4 is-drawer-close:overflow-visible" aria-label="Navigare principală" tabindex="0">
            <div class="space-y-4">
                {% for section in app_navigation %}
                    <section>
                        <h2 class="ops-sidebar-heading mb-2 px-3 text-[11px] font-semibold uppercase tracking-[0.2em] is-drawer-close:hidden">{{ section.label }}</h2>
                        <ul class="menu p-0">
                            {% for item in section.items %}
                                <li>
                                    {% if item.children %}
                                        <details class="ops-nav-group" data-sidebar-flyout {% if item.is_active %}open{% endif %}>
                                            <summary class="is-drawer-close:tooltip is-drawer-close:tooltip-right is-drawer-close:justify-center transition-none" data-sidebar-flyout-trigger data-tip="{{ item.label }}" aria-haspopup="true" aria-controls="ops-submenu-{{ forloop.parentloop.counter }}-{{ forloop.counter }}" aria-expanded="{% if item.is_active %}true{% else %}false{% endif %}">
                                                <span class="ops-nav-icon">
                                                    {% if item.icon_set == "mdi" %}{% md_icon item.icon extra_classes="ops-nav-glyph" %}{% else %}{% bs_icon item.icon extra_classes="ops-nav-glyph bi-valign-default" %}{% endif %}
                                                </span>
                                                <span class="is-drawer-close:hidden">{{ item.label }}</span>
                                                <svg class="ops-nav-chevron is-drawer-close:hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="m9 6 6 6-6 6" /></svg>
                                            </summary>
                                            <ul id="ops-submenu-{{ forloop.parentloop.counter }}-{{ forloop.counter }}" class="ops-submenu" data-sidebar-flyout-panel>
                                                {% for child in item.children %}
                                                    <li>
                                                        {% if child.url_name %}
                                                            <a href="{% url child.url_name %}" data-shell-nav-url="{% url child.url_name %}"{% if child.htmx %} hx-get="{% url child.url_name %}" hx-target="#page-content" hx-swap="outerHTML show:#ops-main-scroll:top" hx-push-url="true" hx-sync="#page-content:replace"{% endif %} class="transition-none{% if child.is_active %} active font-semibold{% endif %}" {% if child.is_active %}aria-current="page"{% endif %}><span class="ops-submenu-label">{{ child.label }}</span></a>
                                                        {% else %}
                                                            <a href="#" class="transition-none"><span class="ops-submenu-label">{{ child.label }}</span></a>
                                                        {% endif %}
                                                    </li>
                                                {% endfor %}
                                            </ul>
                                        </details>
                                    {% else %}
                                        {% if item.url_name %}
                                            <a href="{% url item.url_name %}" data-shell-nav-url="{% url item.url_name %}"{% if item.htmx %} hx-get="{% url item.url_name %}" hx-target="#page-content" hx-swap="outerHTML show:#ops-main-scroll:top" hx-push-url="true" hx-sync="#page-content:replace"{% endif %} class="is-drawer-close:tooltip is-drawer-close:tooltip-right is-drawer-close:justify-center transition-none{% if item.is_active %} active font-semibold{% endif %}" data-tip="{{ item.label }}" {% if item.is_active %}aria-current="page"{% endif %}>
                                        {% else %}
                                            <a href="#" class="is-drawer-close:tooltip is-drawer-close:tooltip-right is-drawer-close:justify-center transition-none" data-tip="{{ item.label }}">
                                        {% endif %}
                                            <span class="ops-nav-icon">{% bs_icon item.icon extra_classes="ops-nav-glyph bi-valign-default" %}</span>
                                            <span class="is-drawer-close:hidden">{{ item.label }}</span>
                                        </a>
                                    {% endif %}
                                </li>
                            {% endfor %}
                        </ul>
                    </section>
                {% endfor %}
            </div>
        </nav>
        <div class="border-t border-[var(--sidebar-footer-divider)] p-3 is-drawer-close:hidden">
            <div class="ops-sidebar-note p-3">
                <div class="flex items-center justify-between gap-3">
                    <div>
                        <p class="text-sm font-semibold text-[var(--sidebar-footer-heading-text)]">Platformă în dezvoltare</p>
                        <p class="text-xs text-[var(--sidebar-footer-text)]">Modulele vor fi activate treptat</p>
                    </div>
                    <span class="badge border border-[var(--sidebar-footer-border)] bg-[var(--sidebar-footer-bg)] text-[var(--sidebar-item-text)]">Local</span>
                </div>
                <div class="mt-3 flex items-center justify-between text-xs text-[var(--sidebar-footer-text)]">
                    <span>Mediu</span>
                    <span>Dezvoltare</span>
                </div>
            </div>
        </div>
    </aside>
</div>
```

## `core/templates/layouts/base.html`

Size: 8.1 KB

```html
{% load static tailwind_tags optional_browser_reload %}
<!DOCTYPE html>
<html lang="ro" data-theme="tuvtk">
<head>
    <title>{% block title %}Platforma TUVTK{% endblock %}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="htmx-config" content='{"historyRestoreAsHxRequest": false}'>
    <link rel="preload" href="{% static 'fonts/inter/InterVariable.woff2' %}" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="{% static 'bootstrap_icons/css/bootstrap_icons.css' %}">
    {% tailwind_css %}
    <script src="{% static 'js/vendor/htmx.min.js' %}" defer></script>
    {% block page_styles %}{% endblock %}
</head>
<body class="h-dvh overflow-hidden">
    <div class="ops-shell flex h-full min-h-0 flex-col">
        <header class="ops-topbar shrink-0">
            <div class="flex h-full items-center gap-3 px-4 sm:px-5 lg:pl-2 lg:pr-6">
                <div class="flex min-w-0 items-center gap-3">
                    <label for="ops-sidebar" class="drawer-button ops-sidebar-toggle" aria-label="Comută bara laterală" title="Comută bara laterală">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 7h16M4 12h16M4 17h16" />
                        </svg>
                    </label>
                    <a href="{% url 'dashboard:index' %}" class="flex min-w-0 items-center gap-3">
                        <img src="{% static 'images/logo.svg' %}" class="ops-logo" alt="Sigla Platforma TUVTK">
                        <div class="min-w-0 leading-tight">
                            <p class="truncate text-sm font-semibold text-base-content">{{ app_name }}</p>
                            <p class="truncate text-[11px] uppercase tracking-[0.18em] text-muted">{{ app_tagline }}</p>
                        </div>
                    </a>
                </div>

                <div class="ml-auto flex items-center gap-2">
                    <div class="ops-header-chip hidden sm:inline-flex">
                        <span class="inline-block h-2 w-2 rounded-full bg-primary"></span>
                        Mediu local
                    </div>
                    <details class="dropdown dropdown-end ops-user-flyout">
                        <summary class="ops-user-trigger transition-none" aria-label="Deschide meniul utilizatorului" title="Meniu utilizator">
                            <span class="ops-avatar-frame relative shrink-0">
                                <span class="avatar{% if not user_avatar_url %} avatar-placeholder{% endif %}">
                                    <span class="ops-avatar">
                                    {% if user_avatar_url %}
                                        <img src="{{ user_avatar_url }}" class="object-cover" alt="{{ user_display_name }}">
                                    {% else %}
                                        <span aria-hidden="true">{{ user_initials }}</span>
                                    {% endif %}
                                    </span>
                                </span>
                                <span class="ops-avatar-status" aria-hidden="true"></span>
                            </span>
                        </summary>
                        <ul class="menu dropdown-content ops-user-menu z-[60] mt-2 w-64 border p-0 transition-none animate-none">
                            {% if request.user.is_staff %}
                                <li>
                                    <a href="{% url 'admin:index' %}" class="transition-none">
                                        <span class="ops-user-menu-icon" aria-hidden="true">
                                            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.7" d="M12 3.75a2.25 2.25 0 0 1 2.122 1.5h2.628A2.25 2.25 0 0 1 19 7.5v9a2.25 2.25 0 0 1-2.25 2.25h-9A2.25 2.25 0 0 1 5.5 16.5v-9a2.25 2.25 0 0 1 2.25-2.25h2.128A2.25 2.25 0 0 1 12 3.75Z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.7" d="M9.75 5.25h4.5v2.5h-4.5v-2.5ZM9 12h6M9 15.5h4" />
                                            </svg>
                                        </span>
                                        <span class="ops-user-menu-label">Administrare Django</span>
                                    </a>
                                </li>
                            {% endif %}
                            <li class="ops-user-logout">
                                <form method="post" action="{% url 'logout' %}">
                                    {% csrf_token %}
                                    <button type="submit" class="w-full cursor-pointer text-left transition-none">
                                        <span class="ops-user-menu-icon" aria-hidden="true">
                                            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.7" d="M14.25 8.25V6A2.25 2.25 0 0 0 12 3.75H6.75A2.25 2.25 0 0 0 4.5 6v12a2.25 2.25 0 0 0 2.25 2.25H12A2.25 2.25 0 0 0 14.25 18v-2.25M10.5 12h9m0 0-3-3m3 3-3 3" />
                                            </svg>
                                        </span>
                                        <span class="ops-user-menu-label">Deconectare</span>
                                    </button>
                                </form>
                            </li>
                        </ul>
                    </details>
                </div>
            </div>
        </header>

        <div class="drawer h-full min-h-0 flex-1 lg:drawer-open">
            <input
                id="ops-sidebar"
                type="checkbox"
                class="drawer-toggle"
                data-sidebar-start-collapsed="{% block sidebar_start_collapsed %}false{% endblock %}"
            >
            <script>
                (() => {
                    const toggle = document.getElementById("ops-sidebar");
                    const drawer = toggle?.closest(".drawer");
                    if (!toggle || !drawer) return;

                    const desktop = window.matchMedia("(min-width: 1024px)");
                    const startsCollapsed = toggle.dataset.sidebarStartCollapsed === "true";
                    let savedState = null;

                    try {
                        savedState = sessionStorage.getItem("ops-sidebar-expanded");
                    } catch {
                        // Storage can be unavailable in restricted browser contexts.
                    }

                    toggle.checked = desktop.matches
                        && !startsCollapsed
                        && (savedState === null || savedState === "true");

                    requestAnimationFrame(() => {
                        requestAnimationFrame(() => drawer.dataset.sidebarReady = "true");
                    });
                })();
            </script>
            {% include "includes/sidebar.html" %}
            <div class="drawer-content h-full min-h-0 overflow-hidden">
                <main id="ops-main-scroll" class="ops-scrollbar h-full overflow-y-auto">
                    <div
                        id="page-content"
                        class="mx-auto w-full max-w-[1600px] px-4 py-4 sm:px-5 sm:py-5 lg:px-6 lg:py-5"
                        data-active-nav-url="{{ active_navigation_url }}"
                        hx-history-elt
                        hx-history="false"
                    >
                        {% block content %}{% endblock %}
                    </div>
                </main>
            </div>
        </div>
    </div>
    <script src="{% static 'js/sidebar.js' %}" defer></script>
    <script src="{% static 'js/shell_htmx.js' %}" defer></script>
    {% block page_scripts %}{% endblock %}
    {% optional_browser_reload_script %}
</body>
</html>
```

## `core/templates/registration/login.html`

Size: 2.5 KB

```html
{% load static tailwind_tags %}
<!DOCTYPE html>
<html lang="ro" data-theme="tuvtk">
<head>
    <title>Loghează-te | Platforma TUVTK</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preload" href="{% static 'fonts/inter/InterVariable.woff2' %}" as="font" type="font/woff2" crossorigin>
    {% tailwind_css %}
</head>
<body class="min-h-dvh bg-base-200 text-base-content">
    <main class="hero min-h-dvh px-4 py-10">
        <section class="hero-content w-full max-w-md p-0">
            <div class="card card-border w-full bg-base-100 shadow-xl">
                <div class="card-body gap-5 p-8 sm:p-10">
                    <div class="flex flex-col items-center text-center">
                        <img src="{% static 'images/logo.svg' %}" class="h-24 w-24 object-contain sm:h-28 sm:w-28" alt="Platforma TUVTK logo">
                        <h1 class="mt-3 text-xl font-bold">Platforma TUVTK</h1>
                        <p class="text-xs uppercase tracking-[0.16em] text-muted">Internal operations</p>
                    </div>

                    <div class="divider my-0"></div>
                    <div>
                        <h2 class="text-2xl font-bold">Loghează-te</h2>
                        <p class="mt-1 text-sm text-muted">Folosește contul tău pentru a continua.</p>
                    </div>

            {% if form.errors %}
                <div class="alert alert-error text-sm" role="alert">
                    Numele de utilizator sau parola nu au fost acceptate.
                </div>
            {% endif %}

            <form method="post" class="space-y-4">
                {% csrf_token %}
                <input type="hidden" name="next" value="{{ next }}">
                <fieldset class="fieldset">
                    <legend class="fieldset-legend">Utilizator</legend>
                    <input type="text" name="username" value="{{ form.username.value|default:'' }}" autocomplete="username" autofocus required class="input input-primary w-full">
                </fieldset>
                <fieldset class="fieldset">
                    <legend class="fieldset-legend">Parolă</legend>
                    <input type="password" name="password" autocomplete="current-password" required class="input input-primary w-full">
                </fieldset>
                <button type="submit" class="btn btn-primary w-full">Loghează-te</button>
            </form>
                </div>
            </div>
        </section>
    </main>
</body>
</html>
```

## `core/templatetags/__init__.py`

Size: 1 B

```python

```

## `core/templatetags/optional_browser_reload.py`

Size: 410 B

```python
from django.conf import settings
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def optional_browser_reload_script(context):
    if not getattr(settings, "HAS_DJANGO_BROWSER_RELOAD", False):
        return ""
    from django_browser_reload.jinja import django_browser_reload_script

    return django_browser_reload_script(nonce=context.get("csp_nonce"))
```

## `core/tests.py`

Size: 3.0 KB

```python
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from django.urls import resolve, reverse

from .context_processors import application_shell


class ApplicationShellTests(TestCase):
    def test_login_uses_large_logo_and_daisyui_card(self):
        response = self.client.get(reverse("login"))

        self.assertContains(response, 'data-theme="tuvtk"')
        self.assertContains(response, "card card-border w-full bg-base-100 shadow-xl")
        self.assertContains(response, "h-24 w-24 object-contain sm:h-28 sm:w-28")
        self.assertNotContains(response, "ops-btn")

    def test_navigation_marks_current_route(self):
        request = RequestFactory().get('/')
        request.resolver_match = resolve('/')
        request.user = AnonymousUser()

        context = application_shell(request)
        dashboard_item = context['app_navigation'][0]['items'][0]

        self.assertTrue(dashboard_item['is_active'])
        self.assertEqual(dashboard_item['url_name'], 'dashboard:index')
        self.assertEqual(context['active_navigation_url'], '/')

    def test_context_processor_does_not_query_the_database(self):
        user = get_user_model().objects.create_user(username="shell-user")
        request = RequestFactory().get('/')
        request.resolver_match = resolve('/')
        request.user = user
        with self.assertNumQueries(0):
            context = application_shell(request)
        self.assertEqual(context["user_display_name"], "shell-user")

    def test_avatar_initials_use_name_for_unseparated_username(self):
        user = get_user_model().objects.create_user(
            username="cristipopa",
            first_name="Cristi",
            last_name="Popa",
        )
        request = RequestFactory().get('/')
        request.resolver_match = resolve('/')
        request.user = user

        context = application_shell(request)

        self.assertEqual(context["user_display_name"], "Cristi Popa")
        self.assertEqual(context["user_initials"], "CP")

    def test_avatar_initials_fall_back_to_segmented_username(self):
        user = get_user_model().objects.create_user(username="platform-admin")
        request = RequestFactory().get('/')
        request.resolver_match = resolve('/')
        request.user = user

        context = application_shell(request)

        self.assertEqual(context["user_initials"], "PA")

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
    def test_404_page_uses_project_branding(self):
        response = self.client.get("/ruta-inexistenta/")

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(response, "Pagina nu a fost gasita", status_code=404)
        self.assertContains(response, "badge badge-outline badge-primary", status_code=404)
        self.assertContains(response, "btn btn-outline btn-primary btn-sm", status_code=404)
```

## `docker/nginx.conf.template`

Size: 1.4 KB

```text
server {
    listen 80 default_server;
    server_name _;

    location = /nginx-health {
        access_log off;
        default_type text/plain;
        return 200 "ok\n";
    }

    location / {
        return 444;
    }
}

server {
    listen 80;
    server_name ${TUVTK_PUBLIC_HOST};

    client_max_body_size 40m;

    location = /nginx-health {
        access_log off;
        default_type text/plain;
        return 200 "ok\n";
    }

    location ^~ /static/ {
        root /srv;
        try_files $uri =404;
        access_log off;
        expires 1h;
        add_header Cache-Control "public, max-age=3600";
    }

    location ^~ /media/avatars/ {
        root /srv;
        try_files $uri =404;
        add_header X-Content-Type-Options nosniff always;
    }

    location ^~ /media/flota/ {
        root /srv;
        try_files $uri =404;
        add_header X-Content-Type-Options nosniff always;
    }

    location ^~ /media/ {
        return 404;
    }

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout ${NGINX_PROXY_TIMEOUT};
        proxy_read_timeout ${NGINX_PROXY_TIMEOUT};
    }
}
```

## `docker/start-web.sh`

Size: 225 B

```bash
#!/bin/sh
set -eu

exec gunicorn platforma_tuvtk.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-2}" \
    --timeout "${GUNICORN_TIMEOUT:-900}" \
    --access-logfile - \
    --error-logfile -
```

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

## `generate_codex_context.bat`

Size: 82 B

```batch
@echo off
python "%~dp0scripts\generate_codex_context.py" %*
exit /b %ERRORLEVEL%
```

## `generate_codex_context.ps1`

Size: 84 B

```powershell
& python "$PSScriptRoot\scripts\generate_codex_context.py" @args
exit $LASTEXITCODE
```

## `generate_codex_context.sh`

Size: 170 B

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/scripts/generate_codex_context.py" "$@"
```

## `platforma_tuvtk/__init__.py`

Size: 0 B

```python
```

## `platforma_tuvtk/asgi.py`

Size: 407 B

```python
"""
ASGI config for platforma_tuvtk project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma_tuvtk.settings')

application = get_asgi_application()
```

## `platforma_tuvtk/settings.py`

Size: 8.4 KB

Redacted secret-like assignments: 1

```python
"""
Django settings for platforma_tuvtk project.

Generated by 'django-admin startproject' using Django 6.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/6.0/ref/settings/
"""

from importlib.util import find_spec
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file(BASE_DIR / '.env')


def env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def env_list(name: str, default: str = '') -> list[str]:
    raw_value = os.environ.get(name, default)
    return [value.strip() for value in raw_value.split(',') if value.strip()]


def detect_npm_bin_path() -> str:
    configured_path = os.environ.get('NPM_BIN_PATH')
    if configured_path:
        return configured_path

    local_appdata = os.environ.get('LOCALAPPDATA')
    if local_appdata:
        local_appdata_path = Path(local_appdata)

        local_node_install = local_appdata_path / 'Programs' / 'nodejs' / 'npm.cmd'
        if local_node_install.exists():
            return str(local_node_install)

        winget_packages = local_appdata_path / 'Microsoft' / 'WinGet' / 'Packages'
        for pattern in (
            'OpenJS.NodeJS.22_*',
            'OpenJS.NodeJS.LTS_*',
            'OpenJS.NodeJS_*',
        ):
            for package_dir in sorted(winget_packages.glob(pattern), reverse=True):
                npm_paths = sorted(package_dir.glob('node-v*-win-x64/npm.cmd'), reverse=True)
                if npm_paths:
                    return str(npm_paths[0])

    return 'npm'


def prepend_node_bin_to_path(npm_bin_path: str) -> None:
    npm_path = Path(npm_bin_path)
    if not npm_path.is_absolute():
        return

    node_bin_dir = str(npm_path.parent)
    current_path = os.environ.get('Path', '')
    path_entries = current_path.split(os.pathsep) if current_path else []
    if node_bin_dir not in path_entries:
        os.environ['Path'] = os.pathsep.join([node_bin_dir, *path_entries]) if path_entries else node_bin_dir


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_bool('DJANGO_DEBUG', True)
DEPLOYMENT_MODE = os.environ.get('DJANGO_DEPLOYMENT_MODE', 'development').strip().lower()

# SECURITY WARNING: keep the secret key used in production secret!
configured_secret_key = os.environ.get('DJANGO_SECRET_KEY', '').strip()
if DEPLOYMENT_MODE == 'container' and not configured_secret_key:
    raise ImproperlyConfigured('DJANGO_SECRET_KEY is required in container deployment mode.')
SECRET_KEY = <redacted>

HAS_DJANGO_BROWSER_RELOAD = DEBUG and find_spec("django_browser_reload") is not None

ALLOWED_HOSTS = env_list('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost,testserver')
CSRF_TRUSTED_ORIGINS = env_list('DJANGO_CSRF_TRUSTED_ORIGINS')
USE_X_FORWARDED_HOST = env_bool('DJANGO_USE_X_FORWARDED_HOST', False)
SECURE_PROXY_SSL_HEADER = (
    ('HTTP_X_FORWARDED_PROTO', 'https')
    if env_bool('DJANGO_TRUST_PROXY_HEADERS', False)
    else None
)
SECURE_SSL_REDIRECT = env_bool('DJANGO_SECURE_SSL_REDIRECT', False)
SESSION_COOKIE_SECURE = env_bool('DJANGO_SESSION_COOKIE_SECURE', False)
CSRF_COOKIE_SECURE = env_bool('DJANGO_CSRF_COOKIE_SECURE', False)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap_icons',
    # Project apps
    'core',
    'apps.dashboard',
    'apps.planificator',
    'apps.diplome',
    'apps.media_library',
    'apps.tasks',
    'apps.flota',
    # Frontend tooling
    'tailwind',
    'theme',
]

if HAS_DJANGO_BROWSER_RELOAD:
    # Add django_browser_reload only in DEBUG mode
    INSTALLED_APPS += ["django_browser_reload"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.ApplicationShellMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if HAS_DJANGO_BROWSER_RELOAD:
    # Add django_browser_reload middleware only in DEBUG mode
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]

ROOT_URLCONF = 'platforma_tuvtk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.application_shell',
            ],
        },
    },
]

WSGI_APPLICATION = 'platforma_tuvtk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'platforma_tuvtk'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', '127.0.0.1'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        # Keep connection reuse disabled on the Django dev server.
        'CONN_MAX_AGE': int(os.environ.get('POSTGRES_CONN_MAX_AGE', '0')),
        'CONN_HEALTH_CHECKS': os.environ.get(
            'POSTGRES_CONN_HEALTH_CHECKS',
            'true',
        ).lower() in {'1', 'true', 'yes', 'on'},
        # The bundled Windows cluster may have WIN1252 template databases.
        # Build Django test databases explicitly from template0 as UTF8 so
        # Romanian application content is preserved.
        'TEST': {
            'CHARSET': 'UTF8',
            'TEMPLATE': 'template0',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Bucharest'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = Path(os.environ.get('DJANGO_STATIC_ROOT', BASE_DIR / 'staticfiles'))
MEDIA_URL = '/media/'
MEDIA_ROOT = Path(os.environ.get('DJANGO_MEDIA_ROOT', BASE_DIR / 'media'))
PRIVATE_MEDIA_ROOT = Path(
    os.environ.get('DJANGO_PRIVATE_MEDIA_ROOT', BASE_DIR / 'private_media')
)
# The stateless Word converter returns a base64-encoded document for the
# generation request. The application-level validator keeps JSON at 32 MB.
DATA_UPLOAD_MAX_MEMORY_SIZE = 40 * 1024 * 1024

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard:index'
LOGOUT_REDIRECT_URL = 'login'

TAILWIND_APP_NAME = "theme"
NPM_BIN_PATH = detect_npm_bin_path()
prepend_node_bin_to_path(NPM_BIN_PATH)
BS_ICONS_CACHE = BASE_DIR / '.bootstrap_icons_cache'
```

## `platforma_tuvtk/urls.py`

Size: 1.5 KB

```python
"""
URL configuration for platforma_tuvtk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('apps.dashboard.urls')),
    path('planificator/', include('apps.planificator.urls')),
    path('diplome/', include('apps.diplome.urls')),
    path('biblioteca-media/', include('apps.media_library.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('flota/', include('apps.flota.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if getattr(settings, "HAS_DJANGO_BROWSER_RELOAD", False):
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
```

## `platforma_tuvtk/wsgi.py`

Size: 407 B

```python
"""
WSGI config for platforma_tuvtk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma_tuvtk.settings')

application = get_wsgi_application()
```

## `plugins/playwright/.codex-plugin/plugin.json`

Size: 1.2 KB

```json
{
  "name": "playwright",
  "version": "0.1.0",
  "description": "Browser automation for testing the TUVTK Django application with Playwright MCP.",
  "author": {
    "name": "TUVTK project"
  },
  "homepage": "https://github.com/microsoft/playwright-mcp",
  "repository": "https://github.com/microsoft/playwright-mcp",
  "license": "Apache-2.0",
  "keywords": [
    "playwright",
    "browser",
    "django",
    "testing"
  ],
  "interface": {
    "displayName": "Playwright",
    "shortDescription": "Test the TUVTK Django app in a real browser.",
    "longDescription": "Adds Microsoft's Playwright MCP browser automation to Codex for exploratory testing, responsive checks, accessibility inspection, and frontend debugging in the TUVTK Django project.",
    "developerName": "Microsoft / TUVTK project",
    "category": "Developer Tools",
    "capabilities": [
      "Interactive",
      "Read",
      "Write"
    ],
    "defaultPrompt": [
      "Start the Django app and test its main user flows.",
      "Check the current page for accessibility and responsive issues.",
      "Reproduce this frontend bug in the browser and report the cause."
    ]
  },
  "mcpServers": "./.mcp.json"
}
```

## `plugins/playwright/.mcp.json`

Size: 323 B

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "-y",
        "@playwright/mcp@0.0.77",
        "--headless",
        "--isolated",
        "--browser",
        "chrome",
        "--console-level",
        "warning",
        "--viewport-size",
        "1440x900"
      ]
    }
  }
}
```

## `references/espocrm-install.sh`

Size: 26.6 KB

Redacted secret-like assignments: 1

```bash
#!/bin/bash

# EspoCRM installer v2.8.0
#
# EspoCRM - Open Source CRM application.
# Copyright (C) 2014-2026 EspoCRM, Inc.
# Website: https://www.espocrm.com

set -e

function printExitError() {
    local message="$1"

    restoreBackup

    printf "\n"
    printRedMessage "ERROR"
    printf ": ${message}\n"

    exit 1
}

printRedMessage() {
    local message="$1"

    local red='\033[0;31m'
    local default='\033[0m'

    printf "${red}${message}${default}"
}

function restoreBackup() {
    if [ -n "$backupDirectory" ] && [ -d "$backupDirectory" ]; then
        cp -rp "${backupDirectory}"/* "${data[homeDirectory]}"
    fi
}

if ! [ $(id -u) = 0 ]; then
    printExitError "This script should be run as root or with sudo."
fi

# Pre installation modes:
# 1. HTTP. Without parameters.
# 2. Ask3. Without parameters, when already installed. It will ask about:
#    1. HTTP
#    2. letsencrypt
#    3. SSL
# 3. Ask2. Parameter --ssl. It will ask about letsencrypt + email.
# 4. SSL. Parameter --ssl --owncertificate. Installation with a set self-signed certificate.
# 5. Letsencrypt. Parameter --ssl --letsencrypt. It will ask for an email address.

preInstallationMode=1

declare -A data=(
    [server]="nginx"
    [ssl]=false
    [owncertificate]=false
    [letsencrypt]=false
    [dbRootPassword]=$(openssl rand -hex 10)
    [dbPassword]=$(openssl rand -hex 10)
    [adminUsername]="admin"
    [adminPassword]=$(openssl rand -hex 6)
    [homeDirectory]="/var/www/espocrm"
    [action]="main"
    [backupPath]="SCRIPT_DIRECTORY/espocrm-backup"
)

declare -A modes=(
    [1]="letsencrypt"
    [2]="ssl"
    [3]="http"
)

declare -A modesLabels=(
    [letsencrypt]="Let's Encrypt certificate"
    [ssl]="Own SSL/TLS certificate"
    [http]="HTTP only"
)

function handleArguments() {
    for ARGUMENT in "$@"
    do
        local key=$(echo "$ARGUMENT" | cut -f1 -d=)
        local value=$(echo "$ARGUMENT" | cut -f2 -d=)

        case "$key" in
            -y | --yes)
                noConfirmation=true
                ;;

            --ssl)
                data[ssl]=true
                ;;

            --owncertificate)
                data[owncertificate]=true
                ;;

            --letsencrypt)
                data[letsencrypt]=true
                ;;

            --clean)
                needClean=true
                ;;

            --domain)
                data[domain]="${value}"
                ;;

            --email)
                data[email]="${value}"
                ;;

            --db-root-password | --dbRootPassword)
                data[dbRootPassword]="${value}"
                ;;

            --db-password | --dbPassword)
                data[dbPassword]="${value}"
                ;;

            --admin-username | --adminUsername)
                data[adminUsername]="${value}"
                ;;

            --admin-password | --adminPassword)
                data[adminPassword]="${value}"
                ;;

            --command)
                data[action]="command"
                ;;

            --backup-path | --backupPath)
                data[backupPath]="${value}"
                ;;

            --environment)
                data[action]="environment"
                ;;

            --network)
                data[action]="network"
                ;;

            --public-ip)
                data[ipAddressType]="1"
                ;;

            --private-ip)
                data[ipAddressType]="2"
                ;;
        esac
    done
}

function promptConfirmation() {
    local text=$1

    read -p "${text}" choice

    case "$choice" in
        y|Y|yes|YES )
            echo true
            return
            ;;
    esac

    echo false
}

function stopProcess() {
    restoreBackup

    echo "Aborted."
    exit 0
}

function getOs() {
    local osType="unknown"

    case $(uname | tr '[:upper:]' '[:lower:]') in
        linux*)
            local linuxOs=$(getLinuxOs)

            if [ -n "$linuxOs" ]; then
                osType="$linuxOs"
            fi
            ;;
        darwin*)
            osType="osx"
            ;;
        msys*)
            osType="windows"
            ;;
    esac

    echo "$osType"
}

function getLinuxOs() {
    declare -a linuxOsList=(centos redhat fedora ubuntu debian mint)

    find -L /etc/ -maxdepth 1 -type f -name "*release" -print | while read file; do
        local osString=$(cat "$file" | grep "^NAME=" | sed 's/NAME=//' | tr -d '"' | tr '[:upper:]' '[:lower:]')

        for linuxOs in "${linuxOsList[@]}"
        do
            if [[ "$osString" == *"$linuxOs"* ]]; then
                echo "$linuxOs"
                return
            fi
        done
    done
}

function getHostname() {
    local hostname=$(hostname -f)

    if [ $hostname != "localhost" ]; then
        isFqdn=$(isFqdn "$hostname")

        if [ "$isFqdn" != true ]; then
            hostname=$(getServerIp)
        fi
    fi

    echo "$hostname"
}

function getServerIp() {
    local serverIP=$(hostname -I | awk '{print $1}')

    if [ -z "$serverIP" ] || [ "$(isIpValid $serverIP)" != true ]; then
        serverIP=$(ip route get 1 | awk '{print $NF;exit}')
    fi

    if [ "$(isIpValid $serverIP)" = true ]; then
        echo "$serverIP"
    fi
}

function getPublicIp() {
    local publicIP=$(curl -4 -s ifconfig.me)

    if [ "$(isIpValid $publicIP)" = true ]; then
        echo "$publicIP"
    fi
}

function getActualInstalledMode() {
    if [ -f "${data[homeDirectory]}/docker-compose.yml" ]; then
        head -n 1 "${data[homeDirectory]}/docker-compose.yml" | grep -oP "(?<=MODE: ).*"
    fi
}

function getInstallationMode() {
    if [ -z "$installationMode" ] || [ -z "${modes[$installationMode]}" ]; then
        printExitError "Unknown installation mode. Please try again."
    fi

    echo "${modes[$installationMode]}"
}

function getYamlValue {
    local keyName="$1"
    local category="$2"

    if [ -f "${data[homeDirectory]}/docker-compose.yml" ]; then
        sed -n "/${category}:/,/networks:/p" "${data[homeDirectory]}/docker-compose.yml" | grep -oP "(?<=${keyName}: ).*" | head -1
    fi
}

function isFqdn() {
    local hostname=$1

    if [ -z "$hostname" ]; then
        echo false
        return
    fi

    local isIpValid=$(isIpValid "$hostname")
    if [ "$isIpValid" = true ]; then
        echo false
        return
    fi

    if [[ $hostname == *"."* ]]; then
        echo true
        return
    fi

    echo false
}

function isHostAvailable() {
    local hostname=$1

    host $hostname 2>&1 > /dev/null
    if [ $? -eq 0 ]; then
        echo true
        return
    fi

    echo false
}

function isIpValid() {
    local ipAddress="$1"

    if [[ $ipAddress =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo true
        return
    fi

    echo false
}

function isPortInUse() {
    local port="$1"

    if [ -z "$port" ]; then
        echo false
        return
    fi

    if (echo >"/dev/tcp/localhost/$port") &>/dev/null ; then
        echo true
        return
    fi

    echo false
}

function isEmailValidated() {
    local emailAddress="$1"

    local regex="^(([A-Za-z0-9]+((\.|\-|\_|\+)?[A-Za-z0-9]?)*[A-Za-z0-9]+)|[A-Za-z0-9]+)@(([A-Za-z0-9]+)+((\.|\-|\_)?([A-Za-z0-9]+)+)*)+\.([A-Za-z]{2,})+$"

    if [[ "$emailAddress" =~ ${regex} ]]; then
        echo true
        return
    fi

    echo false
}

function isInstalled() {
    if [ -d "${data[homeDirectory]}" ]; then
        echo true
        return
    fi

    local isRunning=$(isServiceRunning)

    echo "$isRunning"
}

function isServiceRunning() {
    if [ -x "$(command -v docker)" ] && [ "$(docker ps -aqf name=espocrm)" ]; then
        echo true
        return
    fi

    echo false
}

function forceServiceStop() {
    docker stop $(docker ps -aqf "name=espocrm")
    docker rm $(docker ps -aqf "name=espocrm")
}

function checkFixSystemRequirements() {
    local os="$1"

    # Check port
    local isPortInUse=$(isPortInUse "${data[httpPort]}")

    if [ "$isPortInUse" = true ]; then
        printExitError "The required port \"${data[httpPort]}\" is already in use. Free up the port and try again."
    fi

    declare -a missingLibs=()

    if ! [ -x "$(command -v wget)" ] && ! [ -x "$(command -v curl)" ]; then
        missingLibs+=("curl")
    fi

    if ! [ -x "$(command -v unzip)" ]; then
        missingLibs+=("unzip")
    fi

    if [ -z "$missingLibs" ]; then
        return
    fi

    case "$os" in
        ubuntu | debian | mint )
            apt-get update; \
                apt-get install -y --no-install-recommends \
                curl \
                unzip
            ;;

        * )
            printExitError "Missing libraries: ${missingLibs[@]}. Please install them and try again."
            ;;
    esac
}

function getBackupDirectory() {
    local backupPath="${data[backupPath]}"

    backupPath=${backupPath//SCRIPT_DIRECTORY/$scriptDirectory}
    backupPath=${backupPath%/}

    echo "${backupPath}/$(date +'%Y-%m-%d_%H%M%S')"
}

function backupActualInstallation {
    if [ ! -d "${data[homeDirectory]}" ]; then
        return
    fi

    echo "Creating a backup..."

    backupDirectory=$(getBackupDirectory)

    mkdir -p "${backupDirectory}"

    cp -rp "${data[homeDirectory]}"/* "${backupDirectory}"

    echo "Backup is created: $backupDirectory"
}

function cleanInstallation() {
    printf "Cleaning the previous installation...\n"

    if [ -f "${data[homeDirectory]}/docker-compose.yml" ]; then
        docker compose -f "${data[homeDirectory]}/docker-compose.yml" down
    fi

    if [ $(isServiceRunning) = true ]; then
        forceServiceStop
    fi

    backupActualInstallation

    rm -rf "${data[homeDirectory]}"
}

function rebaseInstallation() {
    local isRebase=${rebaseInstallation:-false}

    if [ "$isRebase" != true ]; then
        return
    fi

    printf "\n"
    printf "Starting the reinstallation process...\n"

    normalizeActualInstalledData

    backupActualInstallation

    printf "\n"

    docker compose -f "${data[homeDirectory]}/docker-compose.yml" down

    rm -rf "${data[homeDirectory]}/data/${data[server]}"
    rm "${data[homeDirectory]}/docker-compose.yml"
}

function cleanTemporaryFiles() {
    if [ -f "${scriptDirectory}/espocrm-installer-2.8.0.zip" ]; then
        rm "${scriptDirectory}/espocrm-installer-2.8.0.zip"
    fi

    if [ -d "${scriptDirectory}/espocrm-installer-2.8.0" ]; then
        rm -rf "${scriptDirectory}/espocrm-installer-2.8.0"
    fi
}

function normalizeActualInstalledData() {
    declare -A currentData

    currentData[dbRootPassword]=$(getYamlValue "MARIADB_ROOT_PASSWORD" "espocrm-db")
    currentData[dbPassword]=$(getYamlValue "MARIADB_PASSWORD" "espocrm-db")
    currentData[adminUsername]=$(getYamlValue "ESPOCRM_ADMIN_USERNAME" "espocrm")
    currentData[adminPassword]=$(getYamlValue "ESPOCRM_ADMIN_PASSWORD" "espocrm")

    for key in "${!currentData[@]}"
    do
        local value="${currentData[$key]}"

        if [ -z "$value" ]; then
            printExitError "Unable to start the reinstallation process. If you want to start a clean installation with losing your data, use \"--clean\" option."
        fi

        data[$key]="$value"
    done
}

function normalizePreInstallationMode() {
    if [ "${data[ssl]}" = true ] && [ "${data[owncertificate]}" = true ]; then
        preInstallationMode=4
        return
    fi

    if [ "${data[ssl]}" = true ] && [ "${data[letsencrypt]}" = true ]; then
        preInstallationMode=5
        return
    fi

    if [ "${data[ssl]}" = true ]; then
        preInstallationMode=3
        return
    fi
}

function normalizeData() {
    declare -a requiredFields=(
        domain
    )

    for requiredField in "${requiredFields[@]}"
    do
        if [ -z "${data[$requiredField]}" ]; then
            printExitError "The field \"$requiredField\" is required."
        fi
    done

    if [ "$mode" == "letsencrypt" ]; then
        local isEmailValidated=$(isEmailValidated "${data[email]}")

        if [ -z "${data[email]}" ] || [ "$isEmailValidated" != true ]; then
            printExitError "Empty or incorrect \"email\" field."
        fi
    fi

    data[url]="http://${data[domain]}"
    data[httpPort]="80"

    if [ "$mode" != "http" ]; then
        data[url]="https://${data[domain]}"
        data[httpPort]="443"
    fi

    # Validate domain
    validateIpOrDomain

    isFqdn=$(isFqdn "${data[domain]}")

    if [ "$isFqdn" != true ] && [ "$mode" != "http" ]; then
        printExitError "Your domain name: \"${data[domain]}\" is incorrect. SSL/TLS certificate can only be used for a valid domain name."
    fi
}

function createParamsFromData() {
    for field in "${!data[@]}"
    do
        if [ -n "${data[$field]}" ]; then
            params+=("--$field=${data[$field]}")
        fi
    done
}

function download() {
    local url=$1
    local name=$2

    if [ -x "$(which wget)" ] ; then
        local downloadMode="wget"
    elif [ -x "$(which curl)" ]; then
        local downloadMode="curl"
    fi

    if [ -z "$downloadMode" ]; then
        printExitError "The \"wget\" or \"curl\" is not found on your system. Please install one of them and try again."
    fi

    if [ -n "$name" ]; then
        case $downloadMode in
            wget )
                wget -q $url -O $name
                return
                ;;

            curl )
                curl -o $name -sfL $url
                return
                ;;
        esac
    fi

    case $downloadMode in
        wget )
            wget -q $url
            ;;

        curl )
            curl -sfL $url
            ;;
    esac
}

function runShellScript() {
    local script="$1"
    shift
    local scriptParams=("$@")

    if [ ! -f "./$script" ]; then
        printExitError "Unable to find the \"$script\" script. Try to run the installer again."
    fi

    chmod +x "./$script"

    if [ -n "$scriptParams" ]; then
        "./$script" "${scriptParams[@]}" || {
            restoreBackup
            exit 1
        }
        return
    fi

    "./$script" || {
        restoreBackup
        exit 1
    }
}

function handleExistingInstallation {
    if [ -n "$needClean" ] && [ $needClean = true ]; then
        cleanInstallation || {
            printExitError "Unable to clean existing installation."
        }
    fi

    if [ $(isInstalled) != true ]; then
        return
    fi

    printf "\n"
    printf "The installed EspoCRM instance is found.\n"

    case "$(getActualInstalledMode)" in
        http | letsencrypt | ssl )
            preInstallationMode=2
            rebaseInstallation=true
            ;;

        * )
            printExitError "Unable to determine the current installation mode. If you want to start a clean installation with losing your data, use \"--clean\" option."
            ;;
    esac
}

function handlePreInstallationMode() {
    local mode="$1"

    case "$mode" in
        1 | 2 )
            installationMode=3
            ;;

        3 )
            read -p "
Please choose the installation mode you prefer [1-2]:
  * 1. Free SSL/TLS certificate provided by the Let's Encrypt (recommended)? [1]
  * 2. Own SSL/TLS certificate (for advanced users only)? [2]
" installationMode
            ;;

        4 )
            installationMode=2
            ;;

        5 )
            installationMode=1
            ;;

        * )
            printExitError "Unknown installation mode. Please try to run the script again."
            ;;
    esac
}

function defineIpAddress() {
    if [ -n "${data[domain]}" ] || [ -n "$noConfirmation" ]; then
        defineDomainNameAutomatically
        return
    fi

    local publicIp=$(getPublicIp)
    local privateIp=$(getServerIp)

    if [ -z "${data[ipAddressType]}" ]; then
        read -p "
Please choose your IP for the future EspoCRM instance [1-3]:
  * 1. Public IP (recommended): $publicIp [1]
  * 2. Private IP (for local installation only): $privateIp [2]
  * 3. Enter another IP or a domain [3]
" data[ipAddressType]
    fi

    case "${data[ipAddressType]}" in
        1 )
            data[domain]="$publicIp"
            ;;

        2 )
            data[domain]="$privateIp"
            ;;

        3 )
            printf "\nEnter an IPv4 (e.g. 234.32.0.32):\n"
            read data[domain]
            ;;

        * )
            printRedMessage "Incorrect selection. Please try again."
            unset data[ipAddressType]

            defineIpAddress
            return
            ;;
    esac

    validateIpOrDomain
}

function defineDomainNameAutomatically() {
    if [ -n "${data[domain]}" ]; then
        validateIpOrDomain
        return
    fi

    local publicIp=$(getPublicIp)
    local privateIp=$(getServerIp)

    case "${data[ipAddressType]}" in
        private )
            data[domain]="$privateIp"
            ;;

        * )
            data[domain]="$publicIp"
            ;;
    esac
}

function validateIpOrDomain() {
    isFqdn=$(isFqdn "${data[domain]}")
    isIpValid=$(isIpValid "${data[domain]}")

    if [ -z "$noConfirmation" ]; then
        if [ "$isFqdn" != true ] && [ "$isIpValid" != true ]; then
            printf "\nYour domain name or IP: \"${data[domain]}\" is incorrect. Please enter a valid one and try again\n"
            read data[domain]

            isFqdn=$(isFqdn "${data[domain]}")
            isIpValid=$(isIpValid "${data[domain]}")
        fi
    fi

    if [ "$isFqdn" != true ] && [ "$isIpValid" != true ]; then
        printExitError "Your domain name or IP: \"${data[domain]}\" is incorrect."
    fi
}

function handleInstallationMode() {
    local mode="$1"

    case "$mode" in
        1 )
            if [ -z "${data[email]}" ]; then
                printf "\nEnter your email address to generate the Let's Encrypt certificate:\n"
                read data[email]
            fi
            ;;

        2 )
            printf "NOTICE: For using your own SSL/TLS certificates you have to setup them manually after the installation.\n"
            sleep 1
            ;;

        3 )
            defineIpAddress
            ;;

        * )
            printExitError "Incorrect installation mode. Please try again."
            ;;
    esac

    if [ -z "${data[domain]}" ]; then
        printf "\nEnter a domain name for the future EspoCRM instance (e.g. espoexample.com):\n"
        read data[domain]
    fi
}

function downloadSourceFiles() {
    rm -rf ./espocrm-installer-2.8.0.zip ./espocrm-installer-2.8.0/

    download https://github.com/espocrm/espocrm-installer/releases/download/2.8.0/espocrm-installer-2.8.0.zip "espocrm-installer-2.8.0.zip"
    unzip -q "espocrm-installer-2.8.0.zip"

    if [ ! -d "./espocrm-installer-2.8.0" ]; then
        printExitError "Unable to load source files."
    fi
}

function prepareDocker() {
    mkdir -p "${data[homeDirectory]}"
    mkdir -p "${data[homeDirectory]}/data"
    mkdir -p "${data[homeDirectory]}/data/${data[server]}"

    if [ ! -d "./installation-modes/$mode/${data[server]}" ]; then
        printExitError "Unable to find configuration for the \"${data[server]}\" server. Try to run the installation again."
    fi

    if [ ! -f "./installation-modes/$mode/${data[server]}/docker-compose.yml" ]; then
        printExitError "Error: Unable to find \"docker-compose.yml\" file. Try to run the installation again."
    fi

    mv "./installation-modes/$mode/${data[server]}/docker-compose.yml" "${data[homeDirectory]}/docker-compose.yml"
    mv "./installation-modes/$mode/${data[server]}"/* "${data[homeDirectory]}/data/${data[server]}"

    # Copy helper commands
    find "./commands" -type f  | while read file; do
        fileName=$(basename "$file")
        cp "$file" "${data[homeDirectory]}/$fileName"
        chmod +x "${data[homeDirectory]}/$fileName"
    done

    # Correct existing params
    local configFile="${data[homeDirectory]}/data/espocrm/data/config.php"

    if [ -f "$configFile" ]; then
        sed -i "s#'siteUrl' => '.*'#'siteUrl' => '${data[url]}'#g" "$configFile"
    fi
}

runDockerDatabase() {
    docker compose -f "${data[homeDirectory]}/docker-compose.yml" up -d espocrm-db || {
        restoreBackup
        exit 1
    }

    printf "\nWaiting for the database ready.\n"

    local dbUser=$(getYamlValue "MARIADB_USER" espocrm-db)
    local dbPass=$(getYamlValue "MARIADB_PASSWORD" espocrm-db)

    for i in {1..36}
    do
        docker exec -i espocrm-db mariadb --user="$dbUser" --password="$dbPass" -e "SHOW DATABASES;" > /dev/null 2>&1 && break

        printf "."

        sleep 5
    done

    printf "\n"
}

function runDocker() {
    runDockerDatabase

    docker compose -f "${data[homeDirectory]}/docker-compose.yml" up -d || {
        restoreBackup
        exit 1
    }

    printf "\nWaiting for the first-time EspoCRM configuration.\n"
    printf "This may take up to 5 minutes.\n"

    runDockerResult=false

    for i in {1..120}
    do
        if [ $(curl -sfkLI "${data[url]}" --resolve "${data[domain]}:${data[httpPort]}:127.0.0.1" -o /dev/null -w '%{http_code}\n') == "200" ]; then
            runDockerResult=true
            break
        fi

        printf "."

        if [ $i -eq 61 ]; then
            printf "\n\nYour server is running slow. In 90%% the process is faster.\n"
            printf "You have to wait 5 more minutes.\n"
        fi

        sleep 5
    done

    for i in {1..20}
    do
        if [ "$(docker container inspect -f '{{.State.Running}}' espocrm-websocket)" == "true" ]; then
            sleep 3
            docker compose -f "${data[homeDirectory]}/docker-compose.yml" restart espocrm-nginx > /dev/null 2>&1
            break
        fi

        printf "."

        sleep 5
    done
}

function displaySummaryInformation() {
    printf "\n"
    printf "Summary information:\n"
    printf "  Domain: ${data[domain]}\n"
    printf "  Mode: ${modesLabels[$mode]}\n"

    if [ "$mode" == "letsencrypt" ]; then
        printf "  Email for the Let's Encrypt certificate: ${data[email]}\n"
    fi

    printf "\n"

    isConfirmed=$(promptConfirmation "Do you want to continue? [y/n] ")

    if [ "$isConfirmed" != true ]; then
        stopProcess
    fi
}

#---------- ACTIONS --------------------

function actionMain() {
    if [ -z "$noConfirmation" ]; then
        printf "This script will install EspoCRM with all the needed prerequisites (including Docker, Nginx, PHP, MariaDB).\n"

        isConfirmed=$(promptConfirmation "Do you want to continue the installation? [y/n] ")
        if [ "$isConfirmed" != true ]; then
            stopProcess
        fi
    fi

    handleExistingInstallation

    normalizePreInstallationMode

    handlePreInstallationMode "$preInstallationMode"
    handleInstallationMode "$installationMode"

    mode=$(getInstallationMode)

    normalizeData

    if [ -z "$noConfirmation" ]; then
        displaySummaryInformation
    fi

    rebaseInstallation

    checkFixSystemRequirements "$operatingSystem"

    cleanTemporaryFiles

    downloadSourceFiles

    cd "espocrm-installer-2.8.0"

    # Check and configure a system
    case $(getOs) in
        ubuntu | debian | mint )
            runShellScript "system-configuration/debian.sh"
            ;;

        * )
            printExitError "Your OS is not supported by the script. We recommend to use Ubuntu server."
            ;;
    esac

    case $mode in
        http | ssl | letsencrypt )
            declare -a params
            createParamsFromData
            runShellScript "installation-modes/$mode/init.sh" "${params[@]}"
            ;;

        * )
            printExitError "Unknown installation mode \"$mode\"."
            ;;
    esac

    # Prepare docker
    prepareDocker

    # Run Docker
    runDocker

    printf "\n\n"

    if [ "$runDockerResult" = true ]; then
        printf "The installation has been successfully completed.\n"
    else
        printRedMessage "The installation process is still in progress due to low server performance.\n"
        printf " - In order to check the process, run:\n"
        printf "   ${data[homeDirectory]}/command.sh logs\n"
        printf " - In order to cancel the process, run:\n"
        printf "   ${data[homeDirectory]}/command.sh stop\n"
    fi

    # Post installation message
    case $mode in
        http )
            printf "
IMPORTANT: Your EspoCRM instance is working in HTTP mode.
If you want to install with SSL/TLS certificate, use \"--ssl\" option. For more details, please visit https://docs.espocrm.com/administration/installation-by-script#installation-with-ssltls-certificate.
"
            ;;

        ssl )
            printf "
IMPORTANT: Your EspoCRM instance is working in insecure mode with a self-signed certificate.
You have to setup your own SSL/TLS certificates. For more details, please visit https://docs.espocrm.com/administration/installation-by-script#2-own-ssltls-certificate.
"
            ;;
    esac

    printf "
Login data/information to your EspoCRM instance:
URL: ${data[url]}
Username: ${data[adminUsername]}
Password: <redacted>
"

    printf "\nYour instance files are located at: \"${data[homeDirectory]}\".\n"
}

actionCommand() {
    cleanTemporaryFiles

    downloadSourceFiles

    if [ ! -f "${data[homeDirectory]}/command.sh" ]; then
        printExitError "EspoCRM directory is not found."
    fi

    cp ./espocrm-installer-2.8.0/commands/command.sh "${data[homeDirectory]}/command.sh" || {
        printExitError "Unable to update the ${data[homeDirectory]}/command.sh"
    }

    chmod +x "${data[homeDirectory]}/command.sh"

    echo "Done"
}

actionEnvironment() {
    if [ -z "$noConfirmation" ]; then
        printf "This script will set up the environment required for EspoCRM (including Docker, Nginx, PHP, MariaDB).\n"

        isConfirmed=$(promptConfirmation "Do you want to continue? [y/n] ")
        if [ "$isConfirmed" != true ]; then
            stopProcess
        fi
    fi

    checkFixSystemRequirements "$operatingSystem"

    cleanTemporaryFiles

    downloadSourceFiles

    cd "espocrm-installer-2.8.0"

    # Check and configure a system
    case $(getOs) in
        ubuntu | debian | mint )
            runShellScript "system-configuration/debian.sh"
            ;;

        * )
            printExitError "Your OS is not supported by the script. We recommend to use Ubuntu server."
            ;;
    esac

    mkdir -p "${data[homeDirectory]}"

    cp ./commands/command.sh "${data[homeDirectory]}/command.sh" || {
        printExitError "Unable to copy the ${data[homeDirectory]}/command.sh"
    }

    chmod +x "${data[homeDirectory]}/command.sh"

    echo "Done"
}

# DEPRECATED
# todo: remove in 2027
actionNetwork() {
    docker network inspect "external" >/dev/null 2>&1 || docker network create "external"

    echo "Done"
}

#---------------------------------------

scriptDirectory="$(dirname "$(readlink -f "$BASH_SOURCE")")"
operatingSystem=$(getOs)

handleArguments "$@"

# run an action

case "${data[action]}" in
    main )
        actionMain
        ;;

    command )
        actionCommand
        ;;

    environment )
        actionEnvironment
        ;;

    network )
        actionNetwork
        ;;

    * )
        printExitError "Unknown action \"{data[action]}\"."
        ;;
esac

cleanTemporaryFiles
```

## `repomix.config.json`

Size: 1.3 KB

```json
{
  "$schema": "https://repomix.com/schemas/latest/schema.json",
  "output": {
    "filePath": "repomix-codex.xml",
    "style": "xml",
    "parsableStyle": true,
    "truncateBase64": true
  },
  "ignore": {
    "useGitignore": true,
    "useDotIgnore": true,
    "useDefaultPatterns": true,
    "customPatterns": [
      ".agents/**",
      ".bootstrap_icons_cache/**",
      ".vscode/**",
      ".git/**",
      ".venv/**",
      ".postgresql/**",

      "plugins/playwright/**",
      "**/.playwright-mcp/**",
      "**/playwright-report/**",
      "**/test-results/**",
      "**/.codex-plugin/**",

      "**/__pycache__/**",
      "**/*.pyc",
      "**/*.pyo",

      "**/node_modules/**",
      "**/staticfiles/**",
      "**/media/**",
      "**/private_media/**",
      "apps/planificator-main/**",

      "theme/static/css/dist/**",
      "theme/static/fonts/**",
      "theme/static/images/**",

      "**/*.woff",
      "**/*.woff2",
      "**/*.ttf",
      "**/*.otf",
      "**/*.eot",

      "**/*.svg",
      "**/*.png",
      "**/*.jpg",
      "**/*.jpeg",
      "**/*.gif",
      "**/*.webp",
      "**/*.ico",

      "**/*.map",

      "repomix-output.*",
      "repomix-codex.*",
      "codex-file-map.txt"
    ]
  },
  "security": {
    "enableSecurityCheck": true
  }
}
```

## `scripts/generate_codex_context.py`

Size: 23.5 KB

```python
#!/usr/bin/env python3
"""Generate secret-aware, cross-platform Codex repository context."""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass


DEFAULT_MAX_FILE_KB = 160
MARKER_FILE = ".generated-by-tuvtk-context"

EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    "node_modules",
    "staticfiles",
    "media",
    "private_media",
    "private-media",
    "dist",
    "build",
    ".postgresql",
    ".playwright-mcp",
    "test-results",
    "playwright-report",
}

EXCLUDED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".svg",
    ".bmp",
    ".tiff",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".zip",
    ".tar",
    ".gz",
    ".tgz",
    ".bz2",
    ".xz",
    ".7z",
    ".rar",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".dump",
    ".pem",
    ".key",
    ".crt",
    ".cer",
    ".pfx",
    ".p12",
    ".pyc",
    ".pyo",
    ".so",
    ".dll",
    ".dylib",
    ".exe",
    ".bin",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
}

TEXT_EXTENSIONS = {
    ".py",
    ".html",
    ".htm",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".css",
    ".scss",
    ".less",
    ".md",
    ".rst",
    ".txt",
    ".yaml",
    ".yml",
    ".toml",
    ".json",
    ".jsonc",
    ".xml",
    ".csv",
    ".sh",
    ".bash",
    ".bat",
    ".cmd",
    ".ps1",
    ".ini",
    ".cfg",
    ".conf",
    ".config",
    ".template",
    ".jinja",
    ".j2",
    ".sql",
}

TEXT_FILENAMES = {
    "Dockerfile",
    "Makefile",
    "Procfile",
    ".dockerignore",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    "tuvtk",
}

SECRET_NAME_TOKENS = {
    "secret",
    "secrets",
    "private",
    "credential",
    "credentials",
    "token",
    "tokens",
    "certificate",
    "certificates",
    "cert",
    "certs",
    "key",
    "keys",
}

SECRET_ASSIGNMENT = re.compile(
    r"^(?P<prefix>\s*(?:export\s+)?(?:DJANGO_)?(?:SECRET_KEY|PASSWORD|TOKEN|API_KEY|"
    r"PRIVATE_KEY|POSTGRES_PASSWORD)\s*[:=]\s*)(?P<value>.*)$",
    re.IGNORECASE,
)
PRIVATE_KEY_MARKER = re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")
TEST_FILE_PATTERN = re.compile(r"(^|/)(?:tests?(?:/|\.|$)|test_[^/]+\.py$)")
TOKEN_SPLIT = re.compile(r"[^a-z0-9]+")

LANGUAGES = {
    ".py": "python",
    ".html": "html",
    ".htm": "html",
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".css": "css",
    ".scss": "scss",
    ".md": "markdown",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".json": "json",
    ".xml": "xml",
    ".sh": "bash",
    ".bash": "bash",
    ".bat": "batch",
    ".cmd": "batch",
    ".ps1": "powershell",
    ".sql": "sql",
}

CORE_PRIORITY_NAMES = {
    "README.md",
    "AGENTS.md",
    "compose.yaml",
    "compose.dev.yaml",
    "Dockerfile",
    "install.sh",
    "manage.py",
    "package.json",
    "package-lock.json",
    "requirements.txt",
    "requirements-dev.txt",
    "requirements-deploy.txt",
}


@dataclass(frozen=True)
class IncludedFile:
    relative_path: str
    absolute_path: Path
    size: int
    content: str
    redactions: int
    section: str


@dataclass(frozen=True)
class SkippedEntry:
    relative_path: str
    reason: str


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate cross-platform, secret-aware Codex context.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Project root. Git root is auto-detected when omitted.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("codex-context"),
        help="Context output directory, relative to the project root by default.",
    )
    parser.add_argument(
        "--max-file-kb",
        type=int,
        default=DEFAULT_MAX_FILE_KB,
        help="Maximum size of an individual included text file.",
    )
    tests = parser.add_mutually_exclusive_group()
    tests.add_argument(
        "--include-tests",
        dest="include_tests",
        action="store_true",
        help="Include test modules and test directories (the default).",
    )
    tests.add_argument(
        "--no-tests",
        dest="include_tests",
        action="store_false",
        help="Exclude test modules and test directories.",
    )
    parser.set_defaults(include_tests=True)
    parser.add_argument("--verbose", action="store_true", help="Print included and skipped paths.")
    args = parser.parse_args(argv)
    if args.max_file_kb <= 0:
        parser.error("--max-file-kb must be greater than zero")
    return args


def git_root(start: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    value = result.stdout.strip()
    return Path(value).resolve() if value else None


def detect_root(explicit_root: Path | None) -> Path:
    if explicit_root is not None:
        root = explicit_root.expanduser().resolve()
    else:
        root = git_root(Path.cwd().resolve()) or git_root(Path(__file__).resolve().parent)
        if root is None:
            script_candidate = Path(__file__).resolve().parent.parent
            root = script_candidate if (script_candidate / "manage.py").is_file() else Path.cwd().resolve()
    if not root.is_dir():
        raise ValueError(f"project root is not a directory: {root}")
    return root


def resolve_output(root: Path, requested: Path) -> tuple[Path, Path, Path]:
    output = requested.expanduser()
    if not output.is_absolute():
        output = root / output
    output = output.resolve()
    home = Path.home().resolve()
    forbidden = {Path(output.anchor).resolve(), home, root}
    if output in forbidden:
        raise ValueError(f"unsafe output directory: {output}")
    if root in output.parents and output.name != "codex-context":
        raise ValueError("an output inside the project must be named 'codex-context'")
    if output.exists() and output != root / "codex-context" and not (output / MARKER_FILE).is_file():
        raise ValueError(f"existing custom output is not marked as generator-owned: {output}")
    return output, output.parent / "codex-context-index.md", output.parent / "codex-file-map.txt"


def path_tokens(name: str) -> set[str]:
    return {token for token in TOKEN_SPLIT.split(name.lower()) if token}


def looks_secret_by_path(relative: Path) -> bool:
    name = relative.name.lower()
    if name == ".env" or name.endswith(".env"):
        return True
    if name.startswith(".env.") and name not in {".env.example", ".env.sample", ".env.template"}:
        return True
    for part in relative.parts:
        if path_tokens(part) & SECRET_NAME_TOKENS:
            return True
    return False


def is_test_path(relative_path: str) -> bool:
    return TEST_FILE_PATTERN.search(relative_path.lower()) is not None


def language_for(path: Path) -> str:
    if path.name == "Dockerfile":
        return "dockerfile"
    return LANGUAGES.get(path.suffix.lower(), "text")


def redact_content(content: str) -> tuple[str | None, int]:
    if PRIVATE_KEY_MARKER.search(content):
        return None, 0
    redacted_lines: list[str] = []
    redactions = 0
    for line in content.splitlines(keepends=True):
        line_without_newline = line.rstrip("\r\n")
        newline = line[len(line_without_newline) :]
        match = SECRET_ASSIGNMENT.match(line_without_newline)
        if match:
            redacted_lines.append(f"{match.group('prefix')}<redacted>{newline}")
            redactions += 1
        else:
            redacted_lines.append(line)
    if redactions >= 8:
        return None, redactions
    return "".join(redacted_lines), redactions


def detect_apps(root: Path) -> dict[str, Path]:
    apps_root = root / "apps"
    if not apps_root.is_dir():
        return {}
    markers = {"apps.py", "models.py", "views.py", "urls.py", "admin.py"}
    detected: dict[str, Path] = {}
    for candidate in sorted(apps_root.iterdir(), key=lambda item: item.name.lower()):
        if not candidate.is_dir() or candidate.name.startswith("."):
            continue
        names = {child.name for child in candidate.iterdir()}
        if names & markers or (candidate / "migrations").is_dir():
            detected[candidate.name] = candidate
    return detected


def section_for(relative: Path, app_names: set[str]) -> str:
    if len(relative.parts) >= 2 and relative.parts[0] == "apps" and relative.parts[1] in app_names:
        return f"app:{relative.parts[1]}"
    return "project-core"


def discover_files(
    root: Path,
    output: Path,
    max_bytes: int,
    include_tests: bool,
    app_names: set[str],
    verbose: bool,
) -> tuple[list[IncludedFile], list[SkippedEntry], list[SkippedEntry]]:
    included: list[IncludedFile] = []
    skipped: list[SkippedEntry] = []
    skipped_directories: list[SkippedEntry] = []
    output_resolved = output.resolve()

    for current, directory_names, file_names in os.walk(root, topdown=True):
        current_path = Path(current)
        kept_directories: list[str] = []
        for directory_name in sorted(directory_names, key=str.lower):
            candidate = (current_path / directory_name).resolve()
            relative = candidate.relative_to(root).as_posix()
            reason = ""
            if candidate == output_resolved:
                reason = "generated context output"
            elif directory_name.startswith(f".{output.name}.staging-") or directory_name.startswith(
                f".{output.name}.previous-"
            ):
                reason = "generated context staging output"
            elif directory_name in EXCLUDED_DIRECTORY_NAMES:
                reason = "excluded directory"
            elif directory_name == "migrations":
                reason = "Django migrations excluded by default"
            elif looks_secret_by_path(Path(relative)):
                reason = "secret-like path"
            if reason:
                skipped_directories.append(SkippedEntry(relative, reason))
                if verbose:
                    print(f"SKIP DIR  {relative}: {reason}")
            else:
                kept_directories.append(directory_name)
        directory_names[:] = kept_directories

        for file_name in sorted(file_names, key=str.lower):
            absolute = current_path / file_name
            relative_path = absolute.relative_to(root)
            relative = relative_path.as_posix()
            reason = ""
            try:
                size = absolute.stat().st_size
            except OSError as exc:
                skipped.append(SkippedEntry(relative, f"stat failed: {exc}"))
                continue

            suffix = absolute.suffix.lower()
            if relative in {"codex-context-index.md", "codex-file-map.txt"}:
                reason = "generated context root output"
            elif looks_secret_by_path(relative_path):
                reason = "secret-like filename/path"
            elif suffix in EXCLUDED_EXTENSIONS:
                reason = "binary, archive, database, certificate, or media extension"
            elif not include_tests and is_test_path(relative):
                reason = "tests excluded by --no-tests"
            elif size > max_bytes:
                reason = f"larger than {max_bytes // 1024} KB"
            elif suffix not in TEXT_EXTENSIONS and file_name not in TEXT_FILENAMES:
                reason = "unrecognized text file type"

            if reason:
                skipped.append(SkippedEntry(relative, reason))
                if verbose:
                    print(f"SKIP FILE {relative}: {reason}")
                continue

            try:
                raw = absolute.read_bytes()
            except OSError as exc:
                skipped.append(SkippedEntry(relative, f"read failed: {exc}"))
                continue
            if b"\x00" in raw:
                skipped.append(SkippedEntry(relative, "binary content"))
                continue
            try:
                content = raw.decode("utf-8-sig")
            except UnicodeDecodeError:
                skipped.append(SkippedEntry(relative, "not UTF-8 text"))
                continue

            safe_content, redactions = redact_content(content)
            if safe_content is None:
                reason = "private key or secret-heavy content"
                skipped.append(SkippedEntry(relative, reason))
                if verbose:
                    print(f"SKIP FILE {relative}: {reason}")
                continue

            included.append(
                IncludedFile(
                    relative_path=relative,
                    absolute_path=absolute,
                    size=size,
                    content=safe_content,
                    redactions=redactions,
                    section=section_for(relative_path, app_names),
                )
            )
            if verbose:
                suffix_message = f" ({redactions} redaction(s))" if redactions else ""
                print(f"INCLUDE   {relative}: {size} bytes{suffix_message}")

    included.sort(key=lambda item: item.relative_path.lower())
    skipped.sort(key=lambda item: item.relative_path.lower())
    skipped_directories.sort(key=lambda item: item.relative_path.lower())
    return included, skipped, skipped_directories


def format_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    return f"{size / 1024:.1f} KB"


def markdown_file(file: IncludedFile, heading_level: int = 2) -> str:
    fence_length = max(3, max((len(match) for match in re.findall(r"`+", file.content)), default=0) + 1)
    fence = "`" * fence_length
    redaction_note = f"\n\nRedacted secret-like assignments: {file.redactions}" if file.redactions else ""
    content_newline = "\n" if file.content and not file.content.endswith("\n") else ""
    return (
        f"{'#' * heading_level} `{file.relative_path}`\n\n"
        f"Size: {format_size(file.size)}{redaction_note}\n\n"
        f"{fence}{language_for(file.absolute_path)}\n{file.content}"
        f"{content_newline}{fence}\n"
    )


def snapshot_relative_path(relative_path: str) -> Path:
    return Path("files") / f"{relative_path}.md"


def write_snapshot(staging: Path, file: IncludedFile) -> None:
    destination = staging / snapshot_relative_path(file.relative_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        f"# Source snapshot\n\n{markdown_file(file)}",
        encoding="utf-8",
        newline="\n",
    )


def core_sort_key(file: IncludedFile) -> tuple[int, str]:
    priority = 0 if file.relative_path in CORE_PRIORITY_NAMES else 1
    return priority, file.relative_path.lower()


def write_project_core(staging: Path, files: list[IncludedFile]) -> None:
    destination = staging / "project-core.md"
    parts = [
        "# Project and shared context\n",
        "Project-level, configuration, deployment, shared Django, and frontend source files. "
        "Generated snapshots under `codex-context/files/` contain the same authoritative-at-generation content.\n",
    ]
    for file in sorted(files, key=core_sort_key):
        parts.append(markdown_file(file))
    destination.write_text("\n".join(parts), encoding="utf-8", newline="\n")


def write_app_guides(staging: Path, apps: dict[str, Path], files: list[IncludedFile]) -> None:
    apps_output = staging / "apps"
    apps_output.mkdir(parents=True, exist_ok=True)
    by_app: dict[str, list[IncludedFile]] = {name: [] for name in apps}
    for file in files:
        if file.section.startswith("app:"):
            by_app[file.section.split(":", 1)[1]].append(file)
    for app_name in sorted(apps):
        parts = [
            f"# Django app: {app_name}\n",
            "Migrations are excluded by default. Tests are included unless `--no-tests` is used.\n",
        ]
        for file in by_app[app_name]:
            parts.append(markdown_file(file))
        (apps_output / f"{app_name}.md").write_text(
            "\n".join(parts), encoding="utf-8", newline="\n"
        )


def grouped_tree(files: list[IncludedFile]) -> list[str]:
    groups: dict[str, int] = {}
    for file in files:
        top = file.relative_path.split("/", 1)[0]
        groups[top] = groups.get(top, 0) + 1
    return [f"- `{name}/`: {groups[name]} file(s)" for name in sorted(groups, key=str.lower)]


def project_name(root: Path) -> str:
    readme = root / "README.md"
    if readme.is_file():
        try:
            for line in readme.read_text(encoding="utf-8-sig").splitlines():
                if line.startswith("# ") and line[2:].strip():
                    return line[2:].strip()
        except OSError:
            pass
    return root.name


def write_index(
    path: Path,
    root: Path,
    output: Path,
    files: list[IncludedFile],
    skipped: list[SkippedEntry],
    skipped_directories: list[SkippedEntry],
    apps: dict[str, Path],
    include_tests: bool,
    generated_at: str,
) -> None:
    total_bytes = sum(file.size for file in files)
    redacted_files = sum(1 for file in files if file.redactions)
    large_files = [entry for entry in skipped if entry.reason.startswith("larger than")]
    lines = [
        f"# {project_name(root)} Codex context",
        "",
        f"Generated: {generated_at}",
        f"Project root: `{root}`",
        f"Context directory: `{output}`",
        f"Included files: {len(files)}",
        f"Skipped files: {len(skipped)}",
        f"Pruned directories: {len(skipped_directories)}",
        f"Total included bytes: {total_bytes} ({format_size(total_bytes)})",
        f"Files with redacted assignments: {redacted_files}",
        f"Tests included: {'yes' if include_tests else 'no'}",
        "Django migrations: excluded by default",
        "",
        "## Quick instructions for Codex",
        "",
        "Use `codex-file-map.txt` to locate a file, then open the real repository source before editing. "
        "Generated context is navigation support and may become stale.",
        "",
        "## File groups",
        "",
        *grouped_tree(files),
        "",
        "## Django apps",
        "",
    ]
    if apps:
        lines.extend(f"- [{name}]({output.name}/apps/{name}.md)" for name in sorted(apps))
    else:
        lines.append("No Django apps were detected under `apps/`.")
    lines.extend(["", "## Large files skipped", ""])
    if large_files:
        lines.extend(f"- `{entry.relative_path}`: {entry.reason}" for entry in large_files)
    else:
        lines.append("None.")
    lines.extend(["", "## Other skipped files", ""])
    other_skipped = [entry for entry in skipped if entry not in large_files]
    if other_skipped:
        lines.extend(f"- `{entry.relative_path}`: {entry.reason}" for entry in other_skipped)
    else:
        lines.append("None.")
    lines.extend(["", "## Pruned directories", ""])
    if skipped_directories:
        lines.extend(f"- `{entry.relative_path}/`: {entry.reason}" for entry in skipped_directories)
    else:
        lines.append("None.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_file_map(path: Path, output: Path, files: list[IncludedFile]) -> None:
    lines = ["relative_path\tbytes\tcontext_output"]
    for file in files:
        snapshot = output / snapshot_relative_path(file.relative_path)
        lines.append(f"{file.relative_path}\t{file.size}\t{snapshot.as_posix()}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def replace_output(staging: Path, output: Path) -> None:
    backup: Path | None = None
    if output.exists():
        backup = output.with_name(f".{output.name}.previous-{os.getpid()}")
        if backup.exists():
            shutil.rmtree(backup)
        output.rename(backup)
    try:
        staging.rename(output)
    except Exception:
        if backup is not None and backup.exists() and not output.exists():
            backup.rename(output)
        raise
    if backup is not None:
        shutil.rmtree(backup)


def generate(args: argparse.Namespace) -> tuple[int, int, int, Path, Path, Path]:
    root = detect_root(args.root)
    output, index_path, file_map_path = resolve_output(root, args.output)
    apps = detect_apps(root)
    included, skipped, skipped_directories = discover_files(
        root=root,
        output=output,
        max_bytes=args.max_file_kb * 1024,
        include_tests=args.include_tests,
        app_names=set(apps),
        verbose=args.verbose,
    )
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=output.parent))
    try:
        (staging / MARKER_FILE).write_text(
            "Generated by scripts/generate_codex_context.py.\n", encoding="utf-8"
        )
        for file in included:
            write_snapshot(staging, file)
        write_project_core(staging, [file for file in included if file.section == "project-core"])
        write_app_guides(staging, apps, included)
        (staging / "codex-context-audit.md").write_text(
            f"# Context generation audit\n\nGenerated: {generated_at}\n\n"
            f"Included files: {len(included)}\n\nSkipped files: {len(skipped)}\n\n"
            f"Pruned directories: {len(skipped_directories)}\n",
            encoding="utf-8",
            newline="\n",
        )
        index_temp = index_path.with_name(f".{index_path.name}.tmp-{os.getpid()}")
        map_temp = file_map_path.with_name(f".{file_map_path.name}.tmp-{os.getpid()}")
        write_index(
            index_temp,
            root,
            output,
            included,
            skipped,
            skipped_directories,
            apps,
            args.include_tests,
            generated_at,
        )
        write_file_map(map_temp, output, included)
        shutil.copyfile(index_temp, staging / "codex-context-index.md")
        shutil.copyfile(map_temp, staging / "codex-file-map.txt")
        generated_files = sorted(
            path.relative_to(staging).as_posix() for path in staging.rglob("*") if path.is_file()
        )
        generated_files.append("codex-generated-files.txt")
        (staging / "codex-generated-files.txt").write_text(
            "\n".join(generated_files) + "\n", encoding="utf-8", newline="\n"
        )
        replace_output(staging, output)
        os.replace(index_temp, index_path)
        os.replace(map_temp, file_map_path)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise

    return len(included), len(skipped), len(skipped_directories), output, index_path, file_map_path


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_arguments(argv)
        included, skipped, pruned, output, index_path, file_map_path = generate(args)
    except (OSError, ValueError) as exc:
        print(f"context generator: ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Generated Codex context: {output}")
    print(f"Index: {index_path}")
    print(f"File map: {file_map_path}")
    print(f"Included files: {included}; skipped files: {skipped}; pruned directories: {pruned}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `theme/__init__.py`

Size: 0 B

```python
```

## `theme/apps.py`

Size: 85 B

```python
from django.apps import AppConfig


class ThemeConfig(AppConfig):
    name = 'theme'
```

## `theme/static/fonts/inter/LICENSE.txt`

Size: 4.3 KB

```text
Copyright (c) 2016 The Inter Project Authors (https://github.com/rsms/inter)

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at:
http://scripts.sil.org/OFL

-----------------------------------------------------------
SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007
-----------------------------------------------------------

PREAMBLE
The goals of the Open Font License (OFL) are to stimulate worldwide
development of collaborative font projects, to support the font creation
efforts of academic and linguistic communities, and to provide a free and
open framework in which fonts may be shared and improved in partnership
with others.

The OFL allows the licensed fonts to be used, studied, modified and
redistributed freely as long as they are not sold by themselves. The
fonts, including any derivative works, can be bundled, embedded,
redistributed and/or sold with any software provided that any reserved
names are not used by derivative works. The fonts and derivatives,
however, cannot be released under any other type of license. The
requirement for fonts to remain under this license does not apply
to any document created using the fonts or their derivatives.

DEFINITIONS
"Font Software" refers to the set of files released by the Copyright
Holder(s) under this license and clearly marked as such. This may
include source files, build scripts and documentation.

"Reserved Font Name" refers to any names specified as such after the
copyright statement(s).

"Original Version" refers to the collection of Font Software components as
distributed by the Copyright Holder(s).

"Modified Version" refers to any derivative made by adding to, deleting,
or substituting -- in part or in whole -- any of the components of the
Original Version, by changing formats or by porting the Font Software to a
new environment.

"Author" refers to any designer, engineer, programmer, technical
writer or other person who contributed to the Font Software.

PERMISSION AND CONDITIONS
Permission is hereby granted, free of charge, to any person obtaining
a copy of the Font Software, to use, study, copy, merge, embed, modify,
redistribute, and sell modified and unmodified copies of the Font
Software, subject to the following conditions:

1) Neither the Font Software nor any of its individual components,
in Original or Modified Versions, may be sold by itself.

2) Original or Modified Versions of the Font Software may be bundled,
redistributed and/or sold with any software, provided that each copy
contains the above copyright notice and this license. These can be
included either as stand-alone text files, human-readable headers or
in the appropriate machine-readable metadata fields within text or
binary files as long as those fields can be easily viewed by the user.

3) No Modified Version of the Font Software may use the Reserved Font
Name(s) unless explicit written permission is granted by the corresponding
Copyright Holder. This restriction only applies to the primary font name as
presented to the users.

4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
Software shall not be used to promote, endorse or advertise any
Modified Version, except to acknowledge the contribution(s) of the
Copyright Holder(s) and the Author(s) or with their explicit written
permission.

5) The Font Software, modified or unmodified, in part or in whole,
must be distributed entirely under this license, and must not be
distributed under any other license. The requirement for fonts to
remain under this license does not apply to any document created
using the Font Software.

TERMINATION
This license becomes null and void if any of the above conditions are
not met.

DISCLAIMER
THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
OTHER DEALINGS IN THE FONT SOFTWARE.
```

## `theme/static/js/shell_htmx.js`

Size: 1.5 KB

```javascript
(() => {
    if (window.__opsShellHtmxInitialized) return;
    window.__opsShellHtmxInitialized = true;

    const syncShellNavigation = () => {
        const pageContent = document.getElementById("page-content");
        const activeUrl = pageContent?.dataset.activeNavUrl;
        if (!activeUrl) return;

        document.querySelectorAll("[data-shell-nav-url]").forEach((link) => {
            const isActive = link.dataset.shellNavUrl === activeUrl;
            link.classList.toggle("active", isActive);
            link.classList.toggle("font-semibold", isActive);
            if (isActive) {
                link.setAttribute("aria-current", "page");
            } else {
                link.removeAttribute("aria-current");
            }
        });

        document.querySelectorAll("[data-sidebar-flyout]").forEach((flyout) => {
            const hasActiveChild = Boolean(flyout.querySelector("[data-shell-nav-url].active"));
            flyout.open = hasActiveChild;
            flyout.querySelector("[data-sidebar-flyout-trigger]")
                ?.setAttribute("aria-expanded", String(hasActiveChild));
        });
    };

    document.addEventListener("htmx:afterSettle", syncShellNavigation);
    document.addEventListener("htmx:historyRestore", syncShellNavigation);
    document.addEventListener("htmx:responseError", (event) => {
        const responseUrl = event.detail.xhr.responseURL;
        if (responseUrl) window.location.assign(responseUrl);
    });

    syncShellNavigation();
})();
```

## `theme/static/js/sidebar.js`

Size: 5.5 KB

```javascript
(() => {
    const toggle = document.getElementById("ops-sidebar");
    if (!toggle) return;

    const desktop = window.matchMedia("(min-width: 1024px)");
    const startsCollapsed = Boolean(document.querySelector('[data-sidebar-start-collapsed="true"]'));
    const flyouts = Array.from(document.querySelectorAll("[data-sidebar-flyout]"));
    const closeTimers = new WeakMap();
    const exitTimers = new WeakMap();
    const CLOSE_DELAY = 220;
    const EXIT_DURATION = 160;
    const isCollapsed = () => desktop.matches && !toggle.checked;

    const clearCloseTimer = (flyout) => {
        const timer = closeTimers.get(flyout);
        if (timer) window.clearTimeout(timer);
        closeTimers.delete(flyout);
    };

    const cancelClose = (flyout) => {
        clearCloseTimer(flyout);
        const timer = exitTimers.get(flyout);
        if (timer) window.clearTimeout(timer);
        exitTimers.delete(flyout);
        if (flyout.open) {
            flyout.classList.remove("is-flyout-closing");
            flyout.querySelector("[data-sidebar-flyout-trigger]")?.setAttribute("aria-expanded", "true");
        }
    };

    const finishClose = (flyout) => {
        clearCloseTimer(flyout);
        const timer = exitTimers.get(flyout);
        if (timer) window.clearTimeout(timer);
        exitTimers.delete(flyout);
        flyout.classList.remove("is-flyout-active", "is-flyout-closing", "is-flyout-preparing");
        flyout.open = false;
        flyout.querySelector("[data-sidebar-flyout-trigger]")?.setAttribute("aria-expanded", "false");
    };

    const closeFlyout = (flyout, { immediate = false, restoreFocus = false } = {}) => {
        clearCloseTimer(flyout);
        if (!flyout.open) return;

        const trigger = flyout.querySelector("[data-sidebar-flyout-trigger]");
        if (restoreFocus) trigger?.focus();
        trigger?.setAttribute("aria-expanded", "false");

        if (immediate || !isCollapsed() || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
            finishClose(flyout);
            return;
        }

        flyout.classList.add("is-flyout-closing");
        exitTimers.set(flyout, window.setTimeout(() => finishClose(flyout), EXIT_DURATION));
    };

    const scheduleClose = (flyout) => {
        if (!isCollapsed() || !flyout.open) return;
        const panel = flyout.querySelector("[data-sidebar-flyout-panel]");
        if (panel?.contains(document.activeElement)) return;
        clearCloseTimer(flyout);
        closeTimers.set(flyout, window.setTimeout(() => closeFlyout(flyout), CLOSE_DELAY));
    };

    const prepareOpenAnimation = (flyout) => {
        if (!isCollapsed()) return;
        flyout.classList.remove("is-flyout-closing");
        flyout.classList.add("is-flyout-preparing");
        window.requestAnimationFrame(() => {
            window.requestAnimationFrame(() => flyout.classList.remove("is-flyout-preparing"));
        });
    };

    flyouts.forEach((flyout) => {
        const trigger = flyout.querySelector("[data-sidebar-flyout-trigger]");
        trigger?.setAttribute("aria-expanded", String(flyout.open));

        flyout.addEventListener("toggle", () => {
            if (flyout.open) {
                trigger?.setAttribute("aria-expanded", "true");
                if (isCollapsed()) {
                    flyouts.forEach((other) => {
                        if (other !== flyout) closeFlyout(other, { immediate: true });
                    });
                    flyout.classList.add("is-flyout-active");
                    prepareOpenAnimation(flyout);
                }
            } else {
                flyout.classList.remove("is-flyout-active", "is-flyout-closing", "is-flyout-preparing");
                trigger?.setAttribute("aria-expanded", "false");
            }
        });
        flyout.addEventListener("pointerenter", () => cancelClose(flyout));
        flyout.addEventListener("pointerleave", () => scheduleClose(flyout));
        flyout.addEventListener("focusin", () => clearCloseTimer(flyout));
        flyout.addEventListener("focusout", (event) => {
            if (!flyout.contains(event.relatedTarget)) scheduleClose(flyout);
        });
        flyout.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && isCollapsed() && flyout.open) {
                event.preventDefault();
                closeFlyout(flyout, { restoreFocus: true });
            }
        });
    });

    const applyState = () => {
        if (desktop.matches) {
            if (startsCollapsed) {
                toggle.checked = false;
            } else {
                const saved = sessionStorage.getItem("ops-sidebar-expanded");
                toggle.checked = saved === null ? true : saved === "true";
            }
        } else {
            toggle.checked = false;
        }
        if (isCollapsed()) flyouts.forEach((flyout) => closeFlyout(flyout, { immediate: true }));
    };

    toggle.addEventListener("change", () => {
        if (desktop.matches) {
            sessionStorage.setItem("ops-sidebar-expanded", String(toggle.checked));
        }
        flyouts.forEach((flyout) => {
            cancelClose(flyout);
            if (isCollapsed()) closeFlyout(flyout, { immediate: true });
        });
    });
    document.addEventListener("pointerdown", (event) => {
        if (!isCollapsed()) return;
        flyouts.forEach((flyout) => {
            if (flyout.open && !flyout.contains(event.target)) closeFlyout(flyout);
        });
    });
    desktop.addEventListener("change", applyState);
    applyState();
})();
```

## `theme/static/js/vendor/htmx.min.js`

Size: 50.0 KB

```javascript
var htmx=function(){"use strict";const Q={onLoad:null,process:null,on:null,off:null,trigger:null,ajax:null,find:null,findAll:null,closest:null,values:function(e,t){const n=dn(e,t||"post");return n.values},remove:null,addClass:null,removeClass:null,toggleClass:null,takeClass:null,swap:null,defineExtension:null,removeExtension:null,logAll:null,logNone:null,logger:null,config:{historyEnabled:true,historyCacheSize:10,refreshOnHistoryMiss:false,defaultSwapStyle:"innerHTML",defaultSwapDelay:0,defaultSettleDelay:20,includeIndicatorStyles:true,indicatorClass:"htmx-indicator",requestClass:"htmx-request",addedClass:"htmx-added",settlingClass:"htmx-settling",swappingClass:"htmx-swapping",allowEval:true,allowScriptTags:true,inlineScriptNonce:"",inlineStyleNonce:"",attributesToSettle:["class","style","width","height"],withCredentials:false,timeout:0,wsReconnectDelay:"full-jitter",wsBinaryType:"blob",disableSelector:"[hx-disable], [data-hx-disable]",scrollBehavior:"instant",defaultFocusScroll:false,getCacheBusterParam:false,globalViewTransitions:false,methodsThatUseUrlParams:["get","delete"],selfRequestsOnly:true,ignoreTitle:false,scrollIntoViewOnBoost:true,triggerSpecsCache:null,disableInheritance:false,responseHandling:[{code:"204",swap:false},{code:"[23]..",swap:true},{code:"[45]..",swap:false,error:true}],allowNestedOobSwaps:true,historyRestoreAsHxRequest:true,reportValidityOfForms:false},parseInterval:null,location:location,_:null,version:"2.0.10"};Q.onLoad=j;Q.process=Ft;Q.on=ye;Q.off=xe;Q.trigger=ae;Q.ajax=Nn;Q.find=f;Q.findAll=y;Q.closest=g;Q.remove=z;Q.addClass=w;Q.removeClass=b;Q.toggleClass=G;Q.takeClass=W;Q.swap=_e;Q.defineExtension=_n;Q.removeExtension=zn;Q.logAll=$;Q.logNone=_;Q.parseInterval=d;Q._=e;const n={addTriggerHandler:St,bodyContains:se,canAccessLocalStorage:U,findThisElement:we,filterValues:yn,swap:_e,hasAttribute:s,getAttributeValue:a,getClosestAttributeValue:ne,getClosestMatch:A,getExpressionVars:Rn,getHeaders:mn,getInputValues:dn,getInternalData:oe,getSwapSpecification:bn,getTriggerSpecs:st,getTarget:Se,makeFragment:P,mergeObjects:le,makeSettleInfo:Sn,oobSwap:He,querySelectorExt:ce,settleImmediately:Yt,shouldCancel:ht,triggerEvent:ae,triggerErrorEvent:fe,withExtensions:Vt};const de=["get","post","put","delete","patch"];const R=de.map(function(e){return"[hx-"+e+"], [data-hx-"+e+"]"}).join(", ");function d(e){if(e==undefined){return undefined}let t=NaN;if(e.slice(-2)=="ms"){t=parseFloat(e.slice(0,-2))}else if(e.slice(-1)=="s"){t=parseFloat(e.slice(0,-1))*1e3}else if(e.slice(-1)=="m"){t=parseFloat(e.slice(0,-1))*1e3*60}else{t=parseFloat(e)}return isNaN(t)?undefined:t}function ee(e,t){return e instanceof Element&&e.getAttribute(t)}function s(e,t){return!!e.hasAttribute&&(e.hasAttribute(t)||e.hasAttribute("data-"+t))}function a(e,t){return ee(e,t)||ee(e,"data-"+t)}function c(e){const t=e.parentElement;if(!t&&e.parentNode instanceof ShadowRoot)return e.parentNode;return t}function te(){return document}function q(e,t){return e.getRootNode?e.getRootNode({composed:t}):te()}function A(e,t){while(e&&!t(e)){e=c(e)}return e||null}function o(e,t,n){const r=a(t,n);const o=a(t,"hx-disinherit");var i=a(t,"hx-inherit");if(e!==t){if(Q.config.disableInheritance){if(i&&(i==="*"||i.split(" ").indexOf(n)>=0)){return r}else{return null}}if(o&&(o==="*"||o.split(" ").indexOf(n)>=0)){return"unset"}}return r}function ne(t,n){let r=null;A(t,function(e){return!!(r=o(t,ue(e),n))});if(r!=="unset"){return r}}function h(e,t){return e instanceof Element&&e.matches(t)}function N(e){const t=/<([a-z][^\/\0>\x20\t\r\n\f]*)/i;const n=t.exec(e);if(n){return n[1].toLowerCase()}else{return""}}function I(e){if("parseHTMLUnsafe"in Document){return Document.parseHTMLUnsafe(e)}const t=new DOMParser;return t.parseFromString(e,"text/html")}function L(e,t){while(t.childNodes.length>0){e.append(t.childNodes[0])}}function r(e){const t=te().createElement("script");ie(e.attributes,function(e){t.setAttribute(e.name,e.value)});t.textContent=e.textContent;t.async=false;if(Q.config.inlineScriptNonce){t.nonce=Q.config.inlineScriptNonce}return t}function i(e){return e.matches("script")&&(e.type==="text/javascript"||e.type==="module"||e.type==="")}function D(e){Array.from(e.querySelectorAll("script")).forEach(e=>{if(i(e)){const t=r(e);const n=e.parentNode;try{n.insertBefore(t,e)}catch(e){H(e)}finally{e.remove()}}})}function P(e){const t=e.replace(/<head(\s[^>]*)?>[\s\S]*?<\/head>/i,"");const n=N(t);let r;if(n==="html"){r=new DocumentFragment;const i=I(e);L(r,i.body);r.title=i.title}else if(n==="body"){r=new DocumentFragment;const i=I(t);L(r,i.body);r.title=i.title}else{const i=I('<body><template class="internal-htmx-wrapper">'+t+"</template></body>");r=i.querySelector("template").content;r.title=i.title;var o=r.querySelector("title");if(o&&o.parentNode===r){o.remove();r.title=o.innerText}}if(r){if(Q.config.allowScriptTags){D(r)}else{r.querySelectorAll("script").forEach(e=>e.remove())}}return r}function re(e){if(e){e()}}function t(e,t){return Object.prototype.toString.call(e)==="[object "+t+"]"}function k(e){return typeof e==="function"}function M(e){return t(e,"Object")}function oe(e){const t="htmx-internal-data";let n=e[t];if(!n){n=e[t]={}}return n}function F(t){const n=[];if(t){for(let e=0;e<t.length;e++){n.push(t[e])}}return n}function ie(t,n){if(t){for(let e=0;e<t.length;e++){n(t[e])}}}function B(e){const t=e.getBoundingClientRect();const n=t.top;const r=t.bottom;return n<window.innerHeight&&r>=0}function se(e){return e.getRootNode({composed:true})===document}function X(e){return e.trim().split(/\s+/)}function le(e,t){for(const n in t){if(t.hasOwnProperty(n)){e[n]=t[n]}}return e}function v(e){try{return JSON.parse(e)}catch(e){H(e);return null}}function U(){const e="htmx:sessionStorageTest";try{sessionStorage.setItem(e,e);sessionStorage.removeItem(e);return true}catch(e){return false}}function V(e){try{const t=new URL(e,window.location.href);e=t.pathname+t.search}catch(e){}if(e!="/"){e=e.replace(/\/+$/,"")}return e}function e(e){return On(te().body,function(){return eval(e)})}function j(t){const e=Q.on("htmx:load",function(e){t(e.detail.elt)});return e}function $(){Q.logger=function(e,t,n){if(console){console.log(t,e,n)}}}function _(){Q.logger=null}function f(e,t){if(typeof e!=="string"){return e.querySelector(t)}else{return f(te(),e)}}function y(e,t){if(typeof e!=="string"){return e.querySelectorAll(t)}else{return y(te(),e)}}function x(){return window}function z(e,t){e=S(e);if(t){x().setTimeout(function(){z(e);e=null},t)}else{c(e).removeChild(e)}}function ue(e){return e instanceof Element?e:null}function J(e){return e instanceof HTMLElement?e:null}function K(e){return typeof e==="string"?e:null}function p(e){return e instanceof Element||e instanceof Document||e instanceof DocumentFragment?e:null}function w(e,t,n){e=ue(S(e));if(!e){return}if(n){x().setTimeout(function(){w(e,t);e=null},n)}else{e.classList&&e.classList.add(t)}}function b(e,t,n){let r=ue(S(e));if(!r){return}if(n){x().setTimeout(function(){b(r,t);r=null},n)}else{if(r.classList){r.classList.remove(t);if(r.classList.length===0){r.removeAttribute("class")}}}}function G(e,t){e=S(e);e.classList.toggle(t)}function W(e,t){e=S(e);ie(e.parentElement.children,function(e){b(e,t)});w(ue(e),t)}function g(e,t){e=ue(S(e));if(e){return e.closest(t)}return null}function l(e,t){return e.substring(0,t.length)===t}function Z(e,t){return e.substring(e.length-t.length)===t}function Y(e){const t=e.trim();if(l(t,"<")&&Z(t,"/>")){return t.substring(1,t.length-2)}else{return t}}function m(t,r,n){if(r.indexOf("global ")===0){return m(t,r.slice(7),true)}t=S(t);const o=[];{let t=0;let n=0;for(let e=0;e<r.length;e++){const l=r[e];if(l===","&&t===0){o.push(r.substring(n,e));n=e+1;continue}if(l==="<"){t++}else if(l==="/"&&e<r.length-1&&r[e+1]===">"){t--}}if(n<r.length){o.push(r.substring(n))}}const i=[];const s=[];while(o.length>0){const r=Y(o.shift());let e;if(r.indexOf("closest ")===0){e=g(ue(t),Y(r.slice(8)))}else if(r.indexOf("find ")===0){e=f(p(t),Y(r.slice(5)))}else if(r==="next"||r==="nextElementSibling"){e=ue(t).nextElementSibling}else if(r.indexOf("next ")===0){e=pe(t,Y(r.slice(5)),!!n)}else if(r==="previous"||r==="previousElementSibling"){e=ue(t).previousElementSibling}else if(r.indexOf("previous ")===0){e=ge(t,Y(r.slice(9)),!!n)}else if(r==="document"){e=document}else if(r==="window"){e=window}else if(r==="body"){e=document.body}else if(r==="root"){e=q(t,!!n)}else if(r==="host"){e=t.getRootNode().host}else{s.push(r)}if(e){i.push(e)}}if(s.length>0){const e=s.join(",");const u=p(q(t,!!n));i.push(...F(u.querySelectorAll(e)))}return i}var pe=function(t,e,n){const r=p(q(t,n)).querySelectorAll(e);for(let e=0;e<r.length;e++){const o=r[e];if(o.compareDocumentPosition(t)===Node.DOCUMENT_POSITION_PRECEDING){return o}}};var ge=function(t,e,n){const r=p(q(t,n)).querySelectorAll(e);for(let e=r.length-1;e>=0;e--){const o=r[e];if(o.compareDocumentPosition(t)===Node.DOCUMENT_POSITION_FOLLOWING){return o}}};function ce(e,t){if(typeof e!=="string"){return m(e,t)[0]}else{return m(te().body,e)[0]}}function S(e,t){if(typeof e==="string"){return f(p(t)||document,e)}else{return e}}function me(e,t,n,r){if(k(t)){return{target:te().body,event:K(e),listener:t,options:n}}else{return{target:S(e),event:K(t),listener:n,options:r}}}function ye(t,n,r,o){Gn(function(){const e=me(t,n,r,o);e.target.addEventListener(e.event,e.listener,e.options)});const e=k(n);return e?n:r}function xe(t,n,r){Gn(function(){const e=me(t,n,r);e.target.removeEventListener(e.event,e.listener)});return k(n)?n:r}const be=te().createElement("output");function ve(t,n){const e=ne(t,n);if(e){if(e==="this"){return[we(t,n)]}else{const r=m(t,e);const o=/(^|,)(\s*)inherit(\s*)($|,)/.test(e);if(o){const i=ue(A(t,function(e){return e!==t&&s(ue(e),n)}));if(i){r.push(...ve(i,n))}}if(r.length===0){H('The selector "'+e+'" on '+n+" returned no matches!");return[be]}else{return r}}}}function we(e,t){return ue(A(e,function(e){return a(ue(e),t)!=null}))}function Se(e){const t=ne(e,"hx-target");if(t){if(t==="this"){return we(e,"hx-target")}else{return ce(e,t)}}else{const n=oe(e);if(n.boosted){return te().body}else{return e}}}function Ee(e){return Q.config.attributesToSettle.includes(e)}function Ce(t,n){ie(Array.from(t.attributes),function(e){if(!n.hasAttribute(e.name)&&Ee(e.name)){t.removeAttribute(e.name)}});ie(n.attributes,function(e){if(Ee(e.name)){t.setAttribute(e.name,e.value)}})}function Oe(t,e){const n=Jn(e);for(let e=0;e<n.length;e++){const r=n[e];try{if(r.isInlineSwap(t)){return true}}catch(e){H(e)}}return t==="outerHTML"}function He(e,o,i,t){t=t||te();let n="#"+CSS.escape(ee(o,"id"));let s="outerHTML";if(e==="true"){}else if(e.indexOf(":")>0){s=e.substring(0,e.indexOf(":"));n=e.substring(e.indexOf(":")+1)}else{s=e}o.removeAttribute("hx-swap-oob");o.removeAttribute("data-hx-swap-oob");const r=m(t,n,false);if(r.length){ie(r,function(e){let t;const n=o.cloneNode(true);t=te().createDocumentFragment();t.appendChild(n);if(!Oe(s,e)){t=p(n)}const r={shouldSwap:true,target:e,fragment:t};if(!ae(e,"htmx:oobBeforeSwap",r))return;e=r.target;if(r.shouldSwap){Re(t);je(s,e,e,t,i);Te()}ie(i.elts,function(e){ae(e,"htmx:oobAfterSwap",r)})});o.parentNode.removeChild(o)}else{o.parentNode.removeChild(o);fe(te().body,"htmx:oobErrorNoTarget",{content:o,target:n})}return e}function Te(){const e=f("#--htmx-preserve-pantry--");if(e){for(const t of[...e.children]){const n=f("#"+t.id);n.parentNode.moveBefore(t,n);n.remove()}e.remove()}}function Re(e){ie(y(e,"[hx-preserve], [data-hx-preserve]"),function(e){const t=a(e,"id");const n=te().getElementById(t);if(n!=null){if(e.moveBefore){let e=f("#--htmx-preserve-pantry--");if(e==null){te().body.insertAdjacentHTML("afterend","<div id='--htmx-preserve-pantry--'></div>");e=f("#--htmx-preserve-pantry--")}e.moveBefore(n,null)}else{e.parentNode.replaceChild(n,e)}}})}function qe(i,e,s){ie(e.querySelectorAll("[id]"),function(t){const n=ee(t,"id");if(n&&n.length>0){const e=p(i);const r=e&&e.querySelector(CSS.escape(t.tagName)+"#"+CSS.escape(n));if(r&&r!==e){const o=t.cloneNode();Ce(t,r);s.tasks.push(function(){Ce(t,o)})}}})}function Ae(e){return function(){b(e,Q.config.addedClass);Ft(ue(e));Ne(p(e));ae(e,"htmx:load")}}function Ne(e){const t="[autofocus]";const n=J(h(e,t)?e:e.querySelector(t));if(n!=null){n.focus()}}function u(e,t,n,r){qe(e,n,r);while(n.childNodes.length>0){const o=n.firstChild;w(ue(o),Q.config.addedClass);e.insertBefore(o,t);if(o.nodeType!==Node.TEXT_NODE&&o.nodeType!==Node.COMMENT_NODE){r.tasks.push(Ae(o))}}}function Ie(e,t){let n=0;while(n<e.length){t=(t<<5)-t+e.charCodeAt(n++)|0}return t}function Le(t){let n=0;for(let e=0;e<t.attributes.length;e++){const r=t.attributes[e];if(r.value){n=Ie(r.name,n);n=Ie(r.value,n)}}return n}function De(t){const n=oe(t);if(n.onHandlers){for(let e=0;e<n.onHandlers.length;e++){const r=n.onHandlers[e];xe(t,r.event,r.listener)}delete n.onHandlers}}function Pe(e){const t=oe(e);if(t.timeout){clearTimeout(t.timeout)}if(t.listenerInfos){ie(t.listenerInfos,function(e){if(e.on){xe(e.on,e.trigger,e.listener)}})}De(e);ie(Object.keys(t),function(e){if(e!=="firstInitCompleted")delete t[e]})}function E(e){ae(e,"htmx:beforeCleanupElement");Pe(e);ie(e.children,function(e){E(e)})}function ke(t,e,n){if(t.tagName==="BODY"){return Ve(t,e,n)}let r;const o=t.previousSibling;const i=c(t);if(!i){return}u(i,t,e,n);if(o==null){r=i.firstChild}else{r=o.nextSibling}n.elts=n.elts.filter(function(e){return e!==t});while(r&&r!==t){if(r instanceof Element){n.elts.push(r)}r=r.nextSibling}E(t);t.remove()}function Me(e,t,n){return u(e,e.firstChild,t,n)}function Fe(e,t,n){return u(c(e),e,t,n)}function Be(e,t,n){return u(e,null,t,n)}function Xe(e,t,n){return u(c(e),e.nextSibling,t,n)}function Ue(e){E(e);const t=c(e);if(t){return t.removeChild(e)}}function Ve(e,t,n){const r=e.firstChild;u(e,r,t,n);if(r){while(r.nextSibling){E(r.nextSibling);e.removeChild(r.nextSibling)}E(r);e.removeChild(r)}}function je(t,e,n,r,o){switch(t){case"none":return;case"outerHTML":ke(n,r,o);return;case"afterbegin":Me(n,r,o);return;case"beforebegin":Fe(n,r,o);return;case"beforeend":Be(n,r,o);return;case"afterend":Xe(n,r,o);return;case"delete":Ue(n);return;default:var i=Jn(e);for(let e=0;e<i.length;e++){const s=i[e];try{const l=s.handleSwap(t,n,r,o);if(l){if(Array.isArray(l)){for(let e=0;e<l.length;e++){const u=l[e];if(u.nodeType!==Node.TEXT_NODE&&u.nodeType!==Node.COMMENT_NODE){o.tasks.push(Ae(u))}}}return}}catch(e){H(e)}}if(t==="innerHTML"){Ve(n,r,o)}else{je(Q.config.defaultSwapStyle,e,n,r,o)}}}function $e(e,n,r){var t=y(e,"[hx-swap-oob], [data-hx-swap-oob]");ie(t,function(e){if(Q.config.allowNestedOobSwaps||e.parentElement===null){const t=a(e,"hx-swap-oob");if(t!=null){He(t,e,n,r)}}else{e.removeAttribute("hx-swap-oob");e.removeAttribute("data-hx-swap-oob")}});return t.length>0}function _e(h,d,p,g){if(!g){g={}}let m=null;let n=null;let e=function(){re(g.beforeSwapCallback);h=S(h);const r=g.contextElement?q(g.contextElement,false):te();const e=document.activeElement;let t={};t={elt:e,start:e?e.selectionStart:null,end:e?e.selectionEnd:null};const o=Sn(h);if(p.swapStyle==="textContent"){h.textContent=d}else{let n=P(d);o.title=g.title||n.title;if(g.historyRequest){n=n.querySelector("[hx-history-elt],[data-hx-history-elt]")||n}if(g.selectOOB){const i=g.selectOOB.split(",");for(let t=0;t<i.length;t++){const s=i[t].split(":",2);let e=s[0].trim();if(e.indexOf("#")===0){e=e.substring(1)}const l=s[1]||"true";const u=n.querySelector("#"+e);if(u){He(l,u,o,r)}}}$e(n,o,r);ie(y(n,"template"),function(e){if(e.content&&$e(e.content,o,r)){e.remove()}});if(g.select){const c=te().createDocumentFragment();ie(n.querySelectorAll(g.select),function(e){c.appendChild(e)});n=c}Re(n);je(p.swapStyle,g.contextElement,h,n,o);Te()}if(t.elt&&!se(t.elt)&&ee(t.elt,"id")){const f=document.getElementById(ee(t.elt,"id"));const a={preventScroll:p.focusScroll!==undefined?!p.focusScroll:!Q.config.defaultFocusScroll};if(f){if(t.start&&f.setSelectionRange){try{f.setSelectionRange(t.start,t.end)}catch(e){}}f.focus(a)}}b(h,Q.config.swappingClass);ie(o.elts,function(e){if(e.classList){w(e,Q.config.settlingClass)}ae(e,"htmx:afterSwap",g.eventInfo)});re(g.afterSwapCallback);if(!p.ignoreTitle){Xn(o.title)}const n=function(){ie(o.tasks,function(e){e.call()});ie(o.elts,function(e){if(e.classList){b(e,Q.config.settlingClass)}ae(e,"htmx:afterSettle",g.eventInfo)});if(g.anchor){const e=ue(S("#"+g.anchor));if(e){e.scrollIntoView({block:"start",behavior:"auto"})}}En(o.elts,p);re(g.afterSettleCallback);re(m)};if(p.settleDelay>0){x().setTimeout(n,p.settleDelay)}else{n()}};let t=Q.config.globalViewTransitions;if(p.hasOwnProperty("transition")){t=p.transition}const r=g.contextElement||te();if(t&&ae(r,"htmx:beforeTransition",g.eventInfo)&&typeof Promise!=="undefined"&&document.startViewTransition){const o=new Promise(function(e,t){m=e;n=t});const i=e;e=function(){document.startViewTransition(function(){i();return o})}}try{if(p?.swapDelay&&p.swapDelay>0){x().setTimeout(e,p.swapDelay)}else{e()}}catch(e){fe(r,"htmx:swapError",g.eventInfo);re(n);throw e}}function ze(e,t,n){const r=e.getResponseHeader(t);if(r.indexOf("{")===0){const o=v(r);for(const i in o){if(o.hasOwnProperty(i)){let e=o[i];if(M(e)){n=e.target!==undefined?e.target:n}else{e={value:e}}ae(n,i,e)}}}else{const s=r.split(",");for(let e=0;e<s.length;e++){ae(n,s[e].trim(),[])}}}const Je=/\s/;const C=/[\s,]/;const Ke=/[_$a-zA-Z]/;const Ge=/[_$a-zA-Z0-9]/;const We=['"',"'","/"];const Ze=/[^\s]/;const Ye=/[{(]/;const Qe=/[})]/;function et(e){const t=[];let n=0;while(n<e.length){if(Ke.exec(e.charAt(n))){var r=n;while(Ge.exec(e.charAt(n+1))){n++}t.push(e.substring(r,n+1))}else if(We.indexOf(e.charAt(n))!==-1){const o=e.charAt(n);var r=n;n++;while(n<e.length&&e.charAt(n)!==o){if(e.charAt(n)==="\\"){n++}n++}t.push(e.substring(r,n+1))}else{const i=e.charAt(n);t.push(i)}n++}return t}function tt(e,t,n){return Ke.exec(e.charAt(0))&&e!=="true"&&e!=="false"&&e!=="this"&&e!==n&&t!=="."}function nt(r,o,i){if(o[0]==="["){o.shift();let e=1;let t=" return (function("+i+"){ return (";let n=null;while(o.length>0){const s=o[0];if(s==="]"){e--;if(e===0){if(n===null){t=t+"true"}o.shift();t+=")})";try{const l=On(r,function(){return Function(t)()},function(){return true});l.source=t;return l}catch(e){fe(te().body,"htmx:syntax:error",{error:e,source:t});return null}}}else if(s==="["){e++}if(tt(s,n,i)){t+="(("+i+"."+s+") ? ("+i+"."+s+") : (window."+s+"))"}else{t=t+s}n=o.shift()}}}function O(e,t){let n="";while(e.length>0&&!t.test(e[0])){n+=e.shift()}return n}function rt(e){let t;if(e.length>0&&Ye.test(e[0])){e.shift();t=O(e,Qe).trim();e.shift()}else{t=O(e,C)}return t}const ot="input, textarea, select";function it(e,t,n){const r=[];const o=et(t);do{O(o,Ze);const l=o.length;const u=O(o,/[,\[\s]/);if(u!==""){if(u==="every"){const c={trigger:"every"};O(o,Ze);c.pollInterval=d(O(o,/[,\[\s]/));O(o,Ze);var i=nt(e,o,"event");if(i){c.eventFilter=i}r.push(c)}else{const f={trigger:u};var i=nt(e,o,"event");if(i){f.eventFilter=i}O(o,Ze);while(o.length>0&&o[0]!==","){const a=o.shift();if(a==="changed"){f.changed=true}else if(a==="once"){f.once=true}else if(a==="consume"){f.consume=true}else if(a==="delay"&&o[0]===":"){o.shift();f.delay=d(O(o,C))}else if(a==="from"&&o[0]===":"){o.shift();if(Ye.test(o[0])){var s=rt(o)}else{var s=O(o,C);if(s==="closest"||s==="find"||s==="next"||s==="previous"){o.shift();const h=rt(o);if(h.length>0){s+=" "+h}}}f.from=s}else if(a==="target"&&o[0]===":"){o.shift();f.target=rt(o)}else if(a==="throttle"&&o[0]===":"){o.shift();f.throttle=d(O(o,C))}else if(a==="queue"&&o[0]===":"){o.shift();f.queue=O(o,C)}else if(a==="root"&&o[0]===":"){o.shift();f[a]=rt(o)}else if(a==="threshold"&&o[0]===":"){o.shift();f[a]=O(o,C)}else{fe(e,"htmx:syntax:error",{token:o.shift()})}O(o,Ze)}r.push(f)}}if(o.length===l){fe(e,"htmx:syntax:error",{token:o.shift()})}O(o,Ze)}while(o[0]===","&&o.shift());if(n){n[t]=r}return r}function st(e){const t=a(e,"hx-trigger");let n=[];if(t){const r=Q.config.triggerSpecsCache;n=r&&r[t]||it(e,t,r)}if(n.length>0){return n}else if(h(e,"form")){return[{trigger:"submit"}]}else if(h(e,'input[type="button"], input[type="submit"]')){return[{trigger:"click"}]}else if(h(e,ot)){return[{trigger:"change"}]}else{return[{trigger:"click"}]}}function lt(e){oe(e).cancelled=true}function ut(e,t,n){const r=oe(e);r.timeout=x().setTimeout(function(){if(se(e)&&r.cancelled!==true){if(!pt(n,e,Xt("hx:poll:trigger",{triggerSpec:n,target:e}))){t(e)}ut(e,t,n)}},n.pollInterval)}function ct(e){return location.hostname===e.hostname&&ee(e,"href")&&ee(e,"href").indexOf("#")!==0}function ft(e){return g(e,Q.config.disableSelector)}function at(t,n,e){if(t instanceof HTMLAnchorElement&&ct(t)&&(t.target===""||t.target==="_self")||t.tagName==="FORM"&&String(ee(t,"method")).toLowerCase()!=="dialog"){n.boosted=true;let r,o;if(t.tagName==="A"){r="get";o=ee(t,"href")}else{const i=ee(t,"method");r=i?i.toLowerCase():"get";o=ee(t,"action");if(o==null||o===""){o=location.href}if(r==="get"&&o.includes("?")){o=o.replace(/\?[^#]+/,"")}}e.forEach(function(e){gt(t,function(e,t){const n=ue(e);if(ft(n)){E(n);return}he(r,o,n,t)},n,e,true)})}}function ht(e,t){if(e.type==="submit"&&t.tagName==="FORM"){return true}else if(e.type==="click"){const n=t.closest('input[type="submit"], button');if(n&&n.form&&n.type==="submit"){return true}const r=t.closest("a");const o=/^#.+/;if(r&&r.href&&!o.test(r.getAttribute("href"))){return true}}return false}function dt(e,t){return oe(e).boosted&&e instanceof HTMLAnchorElement&&t.type==="click"&&(t.ctrlKey||t.metaKey)}function pt(e,t,n){const r=e.eventFilter;if(r){try{return r.call(t,n)!==true}catch(e){const o=r.source;fe(te().body,"htmx:eventFilter:error",{error:e,source:o});return true}}return false}function gt(l,u,e,c,f){const a=oe(l);let t;if(c.from){t=m(l,c.from)}else{t=[l]}if(c.changed){if(!("lastValue"in a)){a.lastValue=new WeakMap}t.forEach(function(e){if(!a.lastValue.has(c)){a.lastValue.set(c,new WeakMap)}a.lastValue.get(c).set(e,e.value)})}ie(t,function(i){const s=function(e){if(!se(l)){i.removeEventListener(c.trigger,s);return}if(dt(l,e)){return}if(f||ht(e,i)){e.preventDefault()}if(pt(c,l,e)){return}const t=oe(e);t.triggerSpec=c;if(t.handledFor==null){t.handledFor=[]}if(t.handledFor.indexOf(l)<0){t.handledFor.push(l);if(c.consume){e.stopPropagation()}if(c.target&&e.target){if(!h(ue(e.target),c.target)){return}}if(c.once){if(a.triggeredOnce){return}else{a.triggeredOnce=true}}if(c.changed){const n=e.target;const r=n.value;const o=a.lastValue.get(c);if(o.has(n)&&o.get(n)===r){return}o.set(n,r)}if(a.delayed){clearTimeout(a.delayed)}if(a.throttle){return}if(c.throttle>0){if(!a.throttle){ae(l,"htmx:trigger");u(l,e);a.throttle=x().setTimeout(function(){a.throttle=null},c.throttle)}}else if(c.delay>0){a.delayed=x().setTimeout(function(){ae(l,"htmx:trigger");u(l,e)},c.delay)}else{ae(l,"htmx:trigger");u(l,e)}}};if(e.listenerInfos==null){e.listenerInfos=[]}e.listenerInfos.push({trigger:c.trigger,listener:s,on:i});i.addEventListener(c.trigger,s)})}let mt=false;let yt=null;function xt(){if(!yt){yt=function(){mt=true};window.addEventListener("scroll",yt);window.addEventListener("resize",yt);setInterval(function(){if(mt){mt=false;ie(te().querySelectorAll("[hx-trigger*='revealed'],[data-hx-trigger*='revealed']"),function(e){bt(e)})}},200)}}function bt(e){if(!s(e,"data-hx-revealed")&&B(e)){e.setAttribute("data-hx-revealed","true");const t=oe(e);if(t.initHash){ae(e,"revealed")}else{e.addEventListener("htmx:afterProcessNode",function(){ae(e,"revealed")},{once:true})}}}function vt(e,t,n,r){const o=function(){if(!n.loaded){n.loaded=true;ae(e,"htmx:trigger");t(e)}};if(r>0){x().setTimeout(o,r)}else{o()}}function wt(t,n,e){let i=false;ie(de,function(r){if(s(t,"hx-"+r)){const o=a(t,"hx-"+r);i=true;n.path=o;n.verb=r;e.forEach(function(e){St(t,e,n,function(e,t){const n=ue(e);if(ft(n)){E(n);return}he(r,o,n,t)})})}});return i}function St(r,e,t,n){if(e.trigger==="revealed"){xt();gt(r,n,t,e);bt(ue(r))}else if(e.trigger==="intersect"){const o={};if(e.root){o.root=ce(r,e.root)}if(e.threshold){o.threshold=parseFloat(e.threshold)}const i=new IntersectionObserver(function(t){for(let e=0;e<t.length;e++){const n=t[e];if(n.isIntersecting){ae(r,"intersect");break}}},o);i.observe(ue(r));gt(ue(r),n,t,e)}else if(!t.firstInitCompleted&&e.trigger==="load"){if(!pt(e,r,Xt("load",{elt:r}))){vt(ue(r),n,t,e.delay)}}else if(e.pollInterval>0){t.polling=true;ut(ue(r),n,e)}else{gt(r,n,t,e)}}function Et(e){const t=ue(e);if(!t){return false}const n=t.attributes;for(let e=0;e<n.length;e++){const r=n[e].name;if(l(r,"hx-on:")||l(r,"data-hx-on:")||l(r,"hx-on-")||l(r,"data-hx-on-")){return true}}return false}const Ct=(new XPathEvaluator).createExpression('.//*[@*[ starts-with(name(), "hx-on:") or starts-with(name(), "data-hx-on:") or'+' starts-with(name(), "hx-on-") or starts-with(name(), "data-hx-on-") ]]');function Ot(e,t){if(Et(e)){t.push(ue(e))}const n=Ct.evaluate(e);let r=null;while(r=n.iterateNext())t.push(ue(r))}function Ht(e){const t=[];if(e instanceof DocumentFragment){for(const n of e.childNodes){Ot(n,t)}}else{Ot(e,t)}return t}function Tt(e){if(e.querySelectorAll){const n=", [hx-boost] a, [data-hx-boost] a, a[hx-boost], a[data-hx-boost]";const r=[];for(const i in jn){const s=jn[i];if(s.getSelectors){var t=s.getSelectors();if(t){r.push(t)}}}const o=e.querySelectorAll(R+n+", form, [type='submit'],"+" [hx-ext], [data-hx-ext], [hx-trigger], [data-hx-trigger]"+r.flat().map(e=>", "+e).join(""));return o}else{return[]}}function Rt(e){const t=At(e.target);const n=It(e);if(n){n.lastButtonClicked=t}}function qt(e){const t=It(e);if(t){t.lastButtonClicked=null}}function At(e){return g(ue(e),"button, input[type='submit']")}function Nt(e){return e.form||g(e,"form")}function It(e){const t=At(e.target);if(!t){return}const n=Nt(t);if(!n){return}return oe(n)}function Lt(e){e.addEventListener("click",Rt);e.addEventListener("focusin",Rt);e.addEventListener("focusout",qt)}function Dt(t,e,n){const r=oe(t);if(!Array.isArray(r.onHandlers)){r.onHandlers=[]}let o;const i=function(e){On(t,function(){if(ft(t)){return}if(!o){o=new Function("event",n)}o.call(t,e)})};t.addEventListener(e,i);r.onHandlers.push({event:e,listener:i})}function Pt(t){De(t);for(let e=0;e<t.attributes.length;e++){const n=t.attributes[e].name;const r=t.attributes[e].value;if(l(n,"hx-on")||l(n,"data-hx-on")){const o=n.indexOf("-on")+3;const i=n.slice(o,o+1);if(i==="-"||i===":"){let e=n.slice(o+1);if(l(e,":")){e="htmx"+e}else if(l(e,"-")){e="htmx:"+e.slice(1)}else if(l(e,"htmx-")){e="htmx:"+e.slice(5)}Dt(t,e,r)}}}}function kt(t){ae(t,"htmx:beforeProcessNode");const n=oe(t);const e=st(t);const r=wt(t,n,e);if(!r){if(ne(t,"hx-boost")==="true"){at(t,n,e)}else if(s(t,"hx-trigger")){e.forEach(function(e){St(t,e,n,function(){})})}}if(t.tagName==="FORM"||ee(t,"type")==="submit"&&s(t,"form")){Lt(t)}n.firstInitCompleted=true;ae(t,"htmx:afterProcessNode")}function Mt(e){if(!(e instanceof Element)){return false}const t=oe(e);const n=Le(e);if(t.initHash!==n){Pe(e);t.initHash=n;return true}return false}function Ft(e){e=S(e);if(ft(e)){E(e);return}const t=[];if(Mt(e)){t.push(e)}ie(Tt(e),function(e){if(ft(e)){E(e);return}if(Mt(e)){t.push(e)}});ie(Ht(e),Pt);ie(t,kt)}function Bt(e){return e.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase()}function Xt(e,t){return new CustomEvent(e,{bubbles:true,cancelable:true,composed:true,detail:t})}function fe(e,t,n){ae(e,t,le({error:t},n))}function Ut(e){return e==="htmx:afterProcessNode"}function Vt(e,t,n){ie(Jn(e,[],n),function(e){try{t(e)}catch(e){H(e)}})}function H(e){console.error(e)}function ae(e,t,n){e=S(e);if(n==null){n={}}n.elt=e;const r=Xt(t,n);if(Q.logger&&!Ut(t)){Q.logger(e,t,n)}if(n.error){H(n.error+(n.target?", "+n.target:""));ae(e,"htmx:error",{errorInfo:n})}let o=e.dispatchEvent(r);const i=Bt(t);if(o&&i!==t){const s=Xt(i,r.detail);o=o&&e.dispatchEvent(s)}Vt(ue(e),function(e){o=o&&(e.onEvent(t,r)!==false&&!r.defaultPrevented)});return o}let jt;function $t(e){jt=e;if(U()){sessionStorage.setItem("htmx-current-path-for-history",e)}}$t(location.pathname+location.search);function _t(){const e=te().querySelector("[hx-history-elt],[data-hx-history-elt]");return e||te().body}function zt(t,e){if(!U()){return}const n=Kt(e);const r=te().title;const o=window.scrollY;if(Q.config.historyCacheSize<=0){sessionStorage.removeItem("htmx-history-cache");return}t=V(t);const i=v(sessionStorage.getItem("htmx-history-cache"))||[];for(let e=0;e<i.length;e++){if(i[e].url===t){i.splice(e,1);break}}const s={url:t,content:n,title:r,scroll:o};ae(te().body,"htmx:historyItemCreated",{item:s,cache:i});i.push(s);while(i.length>Q.config.historyCacheSize){i.shift()}while(i.length>0){try{sessionStorage.setItem("htmx-history-cache",JSON.stringify(i));break}catch(e){fe(te().body,"htmx:historyCacheError",{cause:e,cache:i});i.shift()}}}function Jt(t){if(!U()){return null}t=V(t);const n=v(sessionStorage.getItem("htmx-history-cache"))||[];for(let e=0;e<n.length;e++){if(n[e].url===t){return n[e]}}return null}function Kt(e){const t=Q.config.requestClass;const n=e.cloneNode(true);ie(y(n,"."+t),function(e){b(e,t)});ie(y(n,"[data-disabled-by-htmx]"),function(e){e.removeAttribute("disabled")});return n.innerHTML}function Gt(){const e=_t();let t=jt;if(U()){t=sessionStorage.getItem("htmx-current-path-for-history")}t=t||location.pathname+location.search;const n=te().querySelector('[hx-history="false" i],[data-hx-history="false" i]');if(!n){ae(te().body,"htmx:beforeHistorySave",{path:t,historyElt:e});zt(t,e)}if(Q.config.historyEnabled)history.replaceState({htmx:true},te().title,location.href)}function Wt(e){if(Q.config.getCacheBusterParam){e=e.replace(/org\.htmx\.cache-buster=[^&]*&?/,"");if(Z(e,"&")||Z(e,"?")){e=e.slice(0,-1)}}if(Q.config.historyEnabled){history.pushState({htmx:true},"",e)}$t(e)}function Zt(e){if(Q.config.historyEnabled)history.replaceState({htmx:true},"",e);$t(e)}function Yt(e){ie(e,function(e){e.call(undefined)})}function Qt(e){const t=new XMLHttpRequest;const n={swapStyle:"innerHTML",swapDelay:0,settleDelay:0};const r={path:e,xhr:t,historyElt:_t(),swapSpec:n};t.open("GET",e,true);if(Q.config.historyRestoreAsHxRequest){t.setRequestHeader("HX-Request","true")}t.setRequestHeader("HX-History-Restore-Request","true");t.setRequestHeader("HX-Current-URL",location.href);t.onload=function(){if(this.status>=200&&this.status<400){r.response=this.response;ae(te().body,"htmx:historyCacheMissLoad",r);_e(r.historyElt,r.response,n,{contextElement:r.historyElt,historyRequest:true});$t(r.path);ae(te().body,"htmx:historyRestore",{path:e,cacheMiss:true,serverResponse:r.response})}else{fe(te().body,"htmx:historyCacheMissLoadError",r)}};if(ae(te().body,"htmx:historyCacheMiss",r)){t.send()}}function en(e){Gt();e=e||location.pathname+location.search;const t=Jt(e);if(t){const n={swapStyle:"innerHTML",swapDelay:0,settleDelay:0,scroll:t.scroll};const r={path:e,item:t,historyElt:_t(),swapSpec:n};if(ae(te().body,"htmx:historyCacheHit",r)){_e(r.historyElt,t.content,n,{contextElement:r.historyElt,title:t.title});$t(r.path);ae(te().body,"htmx:historyRestore",r)}}else{if(Q.config.refreshOnHistoryMiss){Q.location.reload(true)}else{Qt(e)}}}function tn(e){let t=ve(e,"hx-indicator");if(t==null){t=[e]}ie(t,function(e){const t=oe(e);t.requestCount=(t.requestCount||0)+1;w(e,Q.config.requestClass)});return t}function nn(e){let t=ve(e,"hx-disabled-elt");if(t==null){t=[]}ie(t,function(e){const t=oe(e);t.requestCount=(t.requestCount||0)+1;if(!e.hasAttribute("disabled")){e.setAttribute("disabled","");e.setAttribute("data-disabled-by-htmx","")}});return t}function rn(e,t){ie(e.concat(t),function(e){const t=oe(e);t.requestCount=(t.requestCount||1)-1});ie(e,function(e){const t=oe(e);if(t.requestCount===0){b(e,Q.config.requestClass)}});ie(t,function(e){const t=oe(e);if(t.requestCount===0&&e.hasAttribute("data-disabled-by-htmx")){e.removeAttribute("disabled");e.removeAttribute("data-disabled-by-htmx")}})}function on(t,n){for(let e=0;e<t.length;e++){const r=t[e];if(r.isSameNode(n)){return true}}return false}function sn(e){const t=e;if(t.name===""||t.name==null||t.disabled||g(t,"fieldset[disabled]")){return false}if(t.type==="button"||t.type==="submit"||t.tagName==="image"||t.tagName==="reset"||t.tagName==="file"){return false}if(t.type==="checkbox"||t.type==="radio"){return t.checked}return true}function ln(t,e,n){if(t!=null&&e!=null){if(Array.isArray(e)){e.forEach(function(e){n.append(t,e)})}else{n.append(t,e)}}}function un(t,n,r){if(t!=null&&n!=null){let e=r.getAll(t);if(Array.isArray(n)){e=e.filter(e=>n.indexOf(e)<0)}else{e=e.filter(e=>e!==n)}r.delete(t);ie(e,e=>r.append(t,e))}}function cn(e){if(e instanceof HTMLSelectElement&&e.multiple){return F(e.querySelectorAll("option:checked")).map(function(e){return e.value})}if(e instanceof HTMLInputElement&&e.files){return F(e.files)}return e.value}function fn(t,n,r,e,o){if(e==null||on(t,e)){return}else{t.push(e)}if(sn(e)){const i=ee(e,"name");ln(i,cn(e),n);if(o){an(e,r)}}if(e instanceof HTMLFormElement){ie(e.elements,function(e){if(t.indexOf(e)>=0){un(e.name,cn(e),n)}else{t.push(e)}if(o){an(e,r)}});new FormData(e).forEach(function(e,t){if(e instanceof File&&e.name===""){return}ln(t,e,n)})}}function an(e,t){const n=e;if(n.willValidate){ae(n,"htmx:validation:validate");if(!n.checkValidity()){if(ae(n,"htmx:validation:failed",{message:n.validationMessage,validity:n.validity})&&!t.length&&Q.config.reportValidityOfForms){n.reportValidity()}t.push({elt:n,message:n.validationMessage,validity:n.validity})}}}function hn(n,e){for(const t of e.keys()){n.delete(t)}e.forEach(function(e,t){n.append(t,e)});return n}function dn(e,t){const n=[];const r=new FormData;const o=new FormData;const i=[];const s=oe(e);if(s.lastButtonClicked&&!se(s.lastButtonClicked)){s.lastButtonClicked=null}let l=e instanceof HTMLFormElement&&e.noValidate!==true||a(e,"hx-validate")==="true";if(s.lastButtonClicked){l=l&&s.lastButtonClicked.formNoValidate!==true}if(t!=="get"){fn(n,o,i,Nt(e),l)}fn(n,r,i,e,l);if(s.lastButtonClicked||e.tagName==="BUTTON"||e.tagName==="INPUT"&&ee(e,"type")==="submit"){const c=s.lastButtonClicked||e;const f=ee(c,"name");ln(f,c.value,o)}const u=ve(e,"hx-include");ie(u,function(e){fn(n,r,i,ue(e),l);if(!h(e,"form")){ie(p(e).querySelectorAll(ot),function(e){fn(n,r,i,e,l)})}});hn(r,o);return{errors:i,formData:r,values:kn(r)}}function pn(e,t,n){if(e!==""){e+="&"}if(String(n)==="[object Object]"){n=JSON.stringify(n)}const r=encodeURIComponent(n);e+=encodeURIComponent(t)+"="+r;return e}function gn(e){e=Dn(e);let n="";e.forEach(function(e,t){n=pn(n,t,e)});return n}function mn(e,t,n){const r={"HX-Request":"true","HX-Trigger":ee(e,"id"),"HX-Trigger-Name":ee(e,"name"),"HX-Target":a(t,"id"),"HX-Current-URL":location.href};Cn(e,"hx-headers",false,r);if(n!==undefined){r["HX-Prompt"]=n}if(oe(e).boosted){r["HX-Boosted"]="true"}return r}function yn(n,e){const t=ne(e,"hx-params");if(t){if(t==="none"){return new FormData}else if(t==="*"){return n}else if(t.indexOf("not ")===0){ie(t.slice(4).split(","),function(e){e=e.trim();n.delete(e)});return n}else{const r=new FormData;ie(t.split(","),function(t){t=t.trim();if(n.has(t)){n.getAll(t).forEach(function(e){r.append(t,e)})}});return r}}else{return n}}function xn(e){return!!ee(e,"href")&&ee(e,"href").indexOf("#")>=0}function bn(e,t){const n=t||ne(e,"hx-swap");const r={swapStyle:oe(e).boosted?"innerHTML":Q.config.defaultSwapStyle,swapDelay:Q.config.defaultSwapDelay,settleDelay:Q.config.defaultSettleDelay};if(Q.config.scrollIntoViewOnBoost&&oe(e).boosted&&!xn(e)){r.show="top"}if(n){const s=X(n);if(s.length>0){for(let e=0;e<s.length;e++){const l=s[e];if(l.indexOf("swap:")===0){r.swapDelay=d(l.slice(5))}else if(l.indexOf("settle:")===0){r.settleDelay=d(l.slice(7))}else if(l.indexOf("transition:")===0){r.transition=l.slice(11)==="true"}else if(l.indexOf("ignoreTitle:")===0){r.ignoreTitle=l.slice(12)==="true"}else if(l.indexOf("scroll:")===0){const u=l.slice(7);var o=u.split(":");const c=o.pop();var i=o.length>0?o.join(":"):null;r.scroll=c;r.scrollTarget=i}else if(l.indexOf("show:")===0){const f=l.slice(5);var o=f.split(":");const a=o.pop();var i=o.length>0?o.join(":"):null;r.show=a;r.showTarget=i}else if(l.indexOf("focus-scroll:")===0){const h=l.slice("focus-scroll:".length);r.focusScroll=h=="true"}else if(e==0){r.swapStyle=l}else{H("Unknown modifier in hx-swap: "+l)}}}}return r}function vn(e){return ne(e,"hx-encoding")==="multipart/form-data"||h(e,"form")&&ee(e,"enctype")==="multipart/form-data"}function wn(t,n,r){let o=null;Vt(n,function(e){if(o==null){o=e.encodeParameters(t,r,n)}});if(o!=null){return o}else{if(vn(n)){return hn(new FormData,Dn(r))}else{return gn(r)}}}function Sn(e){return{tasks:[],elts:[e]}}function En(e,t){const n=e[0];const r=e[e.length-1];if(t.scroll){var o=null;if(t.scrollTarget){o=ue(ce(n,t.scrollTarget))}if(t.scroll==="top"&&(n||o)){o=o||n;o.scrollTop=0}if(t.scroll==="bottom"&&(r||o)){o=o||r;o.scrollTop=o.scrollHeight}if(typeof t.scroll==="number"){x().setTimeout(function(){window.scrollTo(0,t.scroll)},0)}}if(t.show){var o=null;if(t.showTarget){let e=t.showTarget;if(t.showTarget==="window"){e="body"}o=ue(ce(n,e))}if(t.show==="top"&&(n||o)){o=o||n;o.scrollIntoView({block:"start",behavior:Q.config.scrollBehavior})}if(t.show==="bottom"&&(r||o)){o=o||r;o.scrollIntoView({block:"end",behavior:Q.config.scrollBehavior})}}}function Cn(r,e,o,i,s){if(i==null){i={}}if(r==null){return i}const l=a(r,e);if(l){let e=l.trim();let t=o;if(e==="unset"){return null}if(e.indexOf("javascript:")===0){e=e.slice(11);t=true}else if(e.indexOf("js:")===0){e=e.slice(3);t=true}if(e.indexOf("{")!==0){e="{"+e+"}"}let n;if(t){n=On(r,function(){if(s){return Function("event","return ("+e+")").call(r,s)}else{return Function("return ("+e+")").call(r)}},{})}else{n=v(e)}for(const u in n){if(n.hasOwnProperty(u)){if(i[u]==null){i[u]=n[u]}}}}return Cn(ue(c(r)),e,o,i,s)}function On(e,t,n){if(Q.config.allowEval){return t()}else{fe(e,"htmx:evalDisallowedError");return n}}function Hn(e,t,n){return Cn(e,"hx-vars",true,n,t)}function Tn(e,t,n){return Cn(e,"hx-vals",false,n,t)}function Rn(e,t){return le(Hn(e,t),Tn(e,t))}function qn(t,n,r){if(r!==null){try{t.setRequestHeader(n,r)}catch(e){t.setRequestHeader(n,encodeURIComponent(r));t.setRequestHeader(n+"-URI-AutoEncoded","true")}}}function An(t){if(t.responseURL){try{const e=new URL(t.responseURL);return e.pathname+e.search}catch(e){fe(te().body,"htmx:badResponseUrl",{url:t.responseURL})}}}function T(e,t){return t.test(e.getAllResponseHeaders())}function Nn(t,n,r){t=t.toLowerCase();if(r){if(r instanceof Element||typeof r==="string"){return he(t,n,null,null,{targetOverride:S(r)||be,returnPromise:true})}else{let e=S(r.target);if(r.target&&!e||r.source&&!e&&!S(r.source)){e=be}return he(t,n,S(r.source),r.event,{handler:r.handler,headers:r.headers,values:r.values,targetOverride:e,swapOverride:r.swap,select:r.select,returnPromise:true,push:r.push,replace:r.replace,selectOOB:r.selectOOB})}}else{return he(t,n,null,null,{returnPromise:true})}}function In(e){const t=[];while(e){t.push(e);e=e.parentElement}return t}function Ln(e,t,n){const r=new URL(t,location.protocol!=="about:"?location.href:window.origin);const o=location.protocol!=="about:"?location.origin:window.origin;const i=o===r.origin;if(Q.config.selfRequestsOnly){if(!i){return false}}return ae(e,"htmx:validateUrl",le({url:r,sameHost:i},n))}function Dn(e){if(e instanceof FormData)return e;const t=new FormData;for(const n in e){if(e.hasOwnProperty(n)){if(e[n]&&typeof e[n].forEach==="function"){e[n].forEach(function(e){t.append(n,e)})}else if(typeof e[n]==="object"&&!(e[n]instanceof Blob)){t.append(n,JSON.stringify(e[n]))}else{t.append(n,e[n])}}}return t}function Pn(r,o,e){return new Proxy(e,{get:function(t,e){if(typeof e==="number")return t[e];if(e==="length")return t.length;if(e==="push"){return function(e){t.push(e);r.append(o,e)}}if(typeof t[e]==="function"){return function(){t[e].apply(t,arguments);r.delete(o);t.forEach(function(e){r.append(o,e)})}}if(t[e]&&t[e].length===1){return t[e][0]}else{return t[e]}},set:function(e,t,n){e[t]=n;r.delete(o);e.forEach(function(e){r.append(o,e)});return true}})}function kn(o){return new Proxy(o,{get:function(e,t){if(typeof t==="symbol"){const r=Reflect.get(e,t);if(typeof r==="function"){return function(){return r.apply(o,arguments)}}else{return r}}if(t==="toJSON"){return()=>Object.fromEntries(o)}if(t in e){if(typeof e[t]==="function"){return function(){return o[t].apply(o,arguments)}}}const n=o.getAll(t);if(n.length===0){return undefined}else if(n.length===1){return n[0]}else{return Pn(e,t,n)}},set:function(t,n,e){if(typeof n!=="string"){return false}t.delete(n);if(e&&typeof e.forEach==="function"){e.forEach(function(e){t.append(n,e)})}else if(typeof e==="object"&&!(e instanceof Blob)){t.append(n,JSON.stringify(e))}else{t.append(n,e)}return true},deleteProperty:function(e,t){if(typeof t==="string"){e.delete(t)}return true},ownKeys:function(e){return Reflect.ownKeys(Object.fromEntries(e))},getOwnPropertyDescriptor:function(e,t){return Reflect.getOwnPropertyDescriptor(Object.fromEntries(e),t)}})}function he(t,n,r,o,i,k){let s=null;let l=null;i=i!=null?i:{};if(i.returnPromise&&typeof Promise!=="undefined"){var e=new Promise(function(e,t){s=e;l=t})}if(r==null){r=te().body}const M=i.handler||Vn;const F=i.select||null;if(!se(r)){re(s);return e}const u=i.targetOverride||ue(Se(r));if(u==null||u==be){fe(r,"htmx:targetError",{target:ne(r,"hx-target")});re(l);return e}let c=oe(r);const f=c.lastButtonClicked;if(f){const A=ee(f,"formaction");if(A!=null){n=A}const N=ee(f,"formmethod");if(N!=null){if(de.includes(N.toLowerCase())){t=N}else{re(s);return e}}}const a=ne(r,"hx-confirm");if(k===undefined){const K=function(e){return he(t,n,r,o,i,!!e)};const G={target:u,elt:r,path:n,verb:t,triggeringEvent:o,etc:i,issueRequest:K,question:a};if(ae(r,"htmx:confirm",G)===false){re(s);return e}}let h=r;let d=ne(r,"hx-sync");let p=null;let B=false;if(d){const I=d.split(":");const L=I[0].trim();if(L==="this"){h=we(r,"hx-sync")}else{h=ue(ce(r,L))}d=(I[1]||"drop").trim();c=oe(h);if(d==="drop"&&c.xhr&&c.abortable!==true){re(s);return e}else if(d==="abort"){if(c.xhr){re(s);return e}else{B=true}}else if(d==="replace"){ae(h,"htmx:abort")}else if(d.indexOf("queue")===0){const W=d.split(" ");p=(W[1]||"last").trim()}}if(c.xhr){if(c.abortable){ae(h,"htmx:abort")}else{if(p==null){if(o){const D=oe(o);if(D&&D.triggerSpec&&D.triggerSpec.queue){p=D.triggerSpec.queue}}if(p==null){p="last"}}if(c.queuedRequests==null){c.queuedRequests=[]}if(p==="first"&&c.queuedRequests.length===0){c.queuedRequests.push(function(){he(t,n,r,o,i)})}else if(p==="all"){c.queuedRequests.push(function(){he(t,n,r,o,i)})}else if(p==="last"){c.queuedRequests=[];c.queuedRequests.push(function(){he(t,n,r,o,i)})}re(s);return e}}const g=new XMLHttpRequest;c.xhr=g;c.abortable=B;const m=function(){c.xhr=null;c.abortable=false;if(c.queuedRequests!=null&&c.queuedRequests.length>0){const e=c.queuedRequests.shift();e()}};const X=ne(r,"hx-prompt");if(X){var y=prompt(X);if(y===null||!ae(r,"htmx:prompt",{prompt:y,target:u})){re(s);m();return e}}if(a&&!k){if(!confirm(a)){re(s);m();return e}}let x=mn(r,u,y);if(t!=="get"&&!vn(r)){x["Content-Type"]="application/x-www-form-urlencoded"}if(i.headers){x=le(x,i.headers)}const U=dn(r,t);let b=U.errors;const V=U.formData;if(i.values){hn(V,Dn(i.values))}const j=Dn(Rn(r,o));const v=hn(V,j);let w=yn(v,r);if(Q.config.getCacheBusterParam&&t==="get"){w.set("org.htmx.cache-buster",ee(u,"id")||"true")}if(n==null||n===""){n=location.href}const S=Cn(r,"hx-request");const $=oe(r).boosted;let E=Q.config.methodsThatUseUrlParams.indexOf(t)>=0;const C={boosted:$,useUrlParams:E,formData:w,parameters:kn(w),unfilteredFormData:v,unfilteredParameters:kn(v),headers:x,elt:r,target:u,verb:t,errors:b,withCredentials:i.credentials||S.credentials||Q.config.withCredentials,timeout:i.timeout||S.timeout||Q.config.timeout,path:n,triggeringEvent:o};if(!ae(r,"htmx:configRequest",C)){re(s);m();return e}n=C.path;t=C.verb;x=C.headers;w=Dn(C.parameters);b=C.errors;E=C.useUrlParams;if(b&&b.length>0){ae(r,"htmx:validation:halted",C);re(s);m();return e}const _=n.split("#");const z=_[0];const O=_[1];let H=n;if(E){H=z;const Z=!w.keys().next().done;if(Z){if(H.indexOf("?")<0){H+="?"}else{H+="&"}H+=gn(w);if(O){H+="#"+O}}}if(!Ln(r,H,C)){fe(r,"htmx:invalidPath",C);re(l);m();return e}g.open(t.toUpperCase(),H,true);g.overrideMimeType("text/html");g.withCredentials=C.withCredentials;g.timeout=C.timeout;if(S.noHeaders){}else{for(const P in x){if(x.hasOwnProperty(P)){const Y=x[P];qn(g,P,Y)}}}const T={xhr:g,target:u,requestConfig:C,etc:i,boosted:$,select:F,pathInfo:{requestPath:n,finalRequestPath:H,responsePath:null,anchor:O}};g.onload=function(){try{const t=In(r);T.pathInfo.responsePath=An(g);M(r,T);if(T.keepIndicators!==true){rn(R,q)}ae(r,"htmx:afterRequest",T);ae(r,"htmx:afterOnLoad",T);if(!se(r)){let e=null;while(t.length>0&&e==null){const n=t.shift();if(se(n)){e=n}}if(e){ae(e,"htmx:afterRequest",T);ae(e,"htmx:afterOnLoad",T)}}re(s)}catch(e){fe(r,"htmx:onLoadError",le({error:e},T));throw e}finally{m()}};g.onerror=function(){rn(R,q);fe(r,"htmx:afterRequest",T);fe(r,"htmx:sendError",T);re(l);m()};g.onabort=function(){rn(R,q);fe(r,"htmx:afterRequest",T);fe(r,"htmx:sendAbort",T);re(l);m()};g.ontimeout=function(){rn(R,q);fe(r,"htmx:afterRequest",T);fe(r,"htmx:timeout",T);re(l);m()};if(!ae(r,"htmx:beforeRequest",T)){re(s);m();return e}var R=tn(r);var q=nn(r);ie(["loadstart","loadend","progress","abort"],function(t){ie([g,g.upload],function(e){e.addEventListener(t,function(e){ae(r,"htmx:xhr:"+t,{lengthComputable:e.lengthComputable,loaded:e.loaded,total:e.total})})})});ae(r,"htmx:beforeSend",T);const J=E?null:wn(g,r,w);g.send(J);return e}function Mn(e,t){const n=t.xhr;let r=null;let o=null;if(T(n,/HX-Push:/i)){r=n.getResponseHeader("HX-Push");o="push"}else if(T(n,/HX-Push-Url:/i)){r=n.getResponseHeader("HX-Push-Url");o="push"}else if(T(n,/HX-Replace-Url:/i)){r=n.getResponseHeader("HX-Replace-Url");o="replace"}if(r){if(r==="false"){return{}}else{return{type:o,path:r}}}const i=t.pathInfo.finalRequestPath;const s=t.pathInfo.responsePath;let l=t.etc.push||ne(e,"hx-push-url");let u=t.etc.replace||ne(e,"hx-replace-url");if(l==="false")l=null;if(u==="false")u=null;const c=oe(e).boosted;let f=null;let a=null;if(l){f="push";a=l}else if(u){f="replace";a=u}else if(c){f="push";a=s||i}if(a){if(a==="true"){a=s||i}if(t.pathInfo.anchor&&a.indexOf("#")===-1){a=a+"#"+t.pathInfo.anchor}return{type:f,path:a}}else{return{}}}function Fn(e,t){var n=new RegExp(e.code);return n.test(t.toString(10))}function Bn(e){for(var t=0;t<Q.config.responseHandling.length;t++){var n=Q.config.responseHandling[t];if(Fn(n,e.status)){return n}}return{swap:false}}function Xn(e){if(e){const t=f("title");if(t){t.textContent=e}else{window.document.title=e}}}function Un(e,t){if(t==="this"){return e}const n=ue(ce(e,t));if(n==null){fe(e,"htmx:targetError",{target:t});throw new Error(`Invalid re-target ${t}`)}return n}function Vn(t,e){const n=e.xhr;let r=e.target;const o=e.etc;const i=e.select;if(!ae(t,"htmx:beforeOnLoad",e))return;if(T(n,/HX-Trigger:/i)){ze(n,"HX-Trigger",t)}if(T(n,/HX-Location:/i)){let e=n.getResponseHeader("HX-Location");var s={};if(e.indexOf("{")===0){s=v(e);e=s.path;delete s.path}s.push=s.push??"true";Nn("get",e,s);return}const l=T(n,/HX-Refresh:/i)&&n.getResponseHeader("HX-Refresh")==="true";if(T(n,/HX-Redirect:/i)){e.keepIndicators=true;Q.location.href=n.getResponseHeader("HX-Redirect");l&&Q.location.reload();return}if(l){e.keepIndicators=true;Q.location.reload();return}const u=Mn(t,e);const c=Bn(n);const f=c.swap;let a=!!c.error;let h=Q.config.ignoreTitle||c.ignoreTitle;let d=c.select;if(c.target){e.target=Un(t,c.target)}var p=o.swapOverride;if(p==null&&c.swapOverride){p=c.swapOverride}if(T(n,/HX-Retarget:/i)){e.target=Un(t,n.getResponseHeader("HX-Retarget"))}if(T(n,/HX-Reswap:/i)){p=n.getResponseHeader("HX-Reswap")}var g=n.response;var m=le({shouldSwap:f,serverResponse:g,isError:a,ignoreTitle:h,selectOverride:d,swapOverride:p},e);if(c.event&&!ae(r,c.event,m))return;if(!ae(r,"htmx:beforeSwap",m))return;r=m.target;g=m.serverResponse;a=m.isError;h=m.ignoreTitle;d=m.selectOverride;p=m.swapOverride;e.target=r;e.failed=a;e.successful=!a;if(m.shouldSwap){if(n.status===286){lt(t)}Vt(t,function(e){g=e.transformResponse(g,n,t)});if(u.type){Gt()}var y=bn(t,p);if(!y.hasOwnProperty("ignoreTitle")){y.ignoreTitle=h}w(r,Q.config.swappingClass);if(i){d=i}if(T(n,/HX-Reselect:/i)){d=n.getResponseHeader("HX-Reselect")}const x=o.selectOOB||ne(t,"hx-select-oob");const b=ne(t,"hx-select");_e(r,g,y,{select:d==="unset"?null:d||b,selectOOB:x,eventInfo:e,anchor:e.pathInfo.anchor,contextElement:t,afterSwapCallback:function(){if(T(n,/HX-Trigger-After-Swap:/i)){let e=t;if(!se(t)){e=te().body}ze(n,"HX-Trigger-After-Swap",e)}},afterSettleCallback:function(){if(T(n,/HX-Trigger-After-Settle:/i)){let e=t;if(!se(t)){e=te().body}ze(n,"HX-Trigger-After-Settle",e)}},beforeSwapCallback:function(){if(u.type){ae(te().body,"htmx:beforeHistoryUpdate",le({history:u},e));if(u.type==="push"){Wt(u.path);ae(te().body,"htmx:pushedIntoHistory",{path:u.path})}else{Zt(u.path);ae(te().body,"htmx:replacedInHistory",{path:u.path})}}}})}if(a){fe(t,"htmx:responseError",le({error:"Response Status Error Code "+n.status+" from "+e.pathInfo.requestPath},e))}}const jn={};function $n(){return{init:function(e){return null},getSelectors:function(){return null},onEvent:function(e,t){return true},transformResponse:function(e,t,n){return e},isInlineSwap:function(e){return false},handleSwap:function(e,t,n,r){return false},encodeParameters:function(e,t,n){return null}}}function _n(e,t){if(t.init){t.init(n)}jn[e]=le($n(),t)}function zn(e){delete jn[e]}function Jn(e,n,r){if(n==undefined){n=[]}if(e==undefined){return n}if(r==undefined){r=[]}const t=a(e,"hx-ext");if(t){ie(t.split(","),function(e){e=e.replace(/ /g,"");if(e.slice(0,7)=="ignore:"){r.push(e.slice(7));return}if(r.indexOf(e)<0){const t=jn[e];if(t&&n.indexOf(t)<0){n.push(t)}}})}return Jn(ue(c(e)),n,r)}var Kn=false;te().addEventListener("DOMContentLoaded",function(){Kn=true});function Gn(e){if(Kn||te().readyState==="complete"){e()}else{te().addEventListener("DOMContentLoaded",e)}}function Wn(){if(Q.config.includeIndicatorStyles!==false){const e=Q.config.inlineStyleNonce?` nonce="${Q.config.inlineStyleNonce}"`:"";const t=Q.config.indicatorClass;const n=Q.config.requestClass;te().head.insertAdjacentHTML("beforeend",`<style${e}>`+`.${t}{opacity:0;visibility: hidden} `+`.${n} .${t}, .${n}.${t}{opacity:1;visibility: visible;transition: opacity 200ms ease-in}`+"</style>")}}function Zn(){const e=te().querySelector('meta[name="htmx-config"]');if(e){return v(e.content)}else{return null}}function Yn(){const e=Zn();if(e){Q.config=le(Q.config,e)}}Gn(function(){Yn();Wn();let e=te().body;Ft(e);const t=te().querySelectorAll("[hx-trigger='restored'],[data-hx-trigger='restored']");e.addEventListener("htmx:abort",function(e){const t=e.detail.elt||e.target;const n=oe(t);if(n&&n.xhr){n.xhr.abort()}});const n=window.onpopstate?window.onpopstate.bind(window):null;window.onpopstate=function(e){if(e.state&&e.state.htmx){en();ie(t,function(e){ae(e,"htmx:restored",{document:te(),triggerEvent:ae})})}else{if(n){n(e)}}};x().setTimeout(function(){ae(e,"htmx:load",{});e=null},0)});return Q}();
```

## `theme/static_src/.gitignore`

Size: 13 B

```text
node_modules
```

## `theme/static_src/package-lock.json`

Size: 53.5 KB

```json
{
  "name": "theme",
  "version": "4.5.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "theme",
      "version": "4.5.0",
      "license": "MIT",
      "devDependencies": {
        "@tailwindcss/postcss": "^4.3.0",
        "cross-env": "^10.1.0",
        "daisyui": "^5.5.23",
        "postcss": "^8.5.15",
        "postcss-cli": "^11.0.1",
        "rimraf": "^6.1.3",
        "tailwindcss": "^4.3.0"
      }
    },
    "node_modules/@alloc/quick-lru": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/@alloc/quick-lru/-/quick-lru-5.2.0.tgz",
      "integrity": "sha512-UrcABB+4bUrFABwbluTIBErXwvbsU/V7TZWfmbgJfbkwiBuziS9gxdODUyuiecfdGQ85jglMW6juS3+z5TsKLw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/@epic-web/invariant": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/@epic-web/invariant/-/invariant-1.0.0.tgz",
      "integrity": "sha512-lrTPqgvfFQtR/eY/qkIzp98OGdNJu0m5ji3q/nJI8v3SXkRKEnWiOxMmbvcSoAIzv/cGiuvRy57k4suKQSAdwA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@jridgewell/gen-mapping": {
      "version": "0.3.13",
      "resolved": "https://registry.npmjs.org/@jridgewell/gen-mapping/-/gen-mapping-0.3.13.tgz",
      "integrity": "sha512-2kkt/7niJ6MgEPxF0bYdQ6etZaA+fQvDcLKckhy1yIQOzaoKjBBjSj63/aLVjYE3qhRt5dvM+uUyfCg6UKCBbA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/sourcemap-codec": "^1.5.0",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/remapping": {
      "version": "2.3.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/remapping/-/remapping-2.3.5.tgz",
      "integrity": "sha512-LI9u/+laYG4Ds1TDKSJW2YPrIlcVYOwi2fUC6xB43lueCjgxV4lffOCZCtYFiH6TNOX+tQKXx97T4IKHbhyHEQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.5",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/resolve-uri": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/@jridgewell/resolve-uri/-/resolve-uri-3.1.2.tgz",
      "integrity": "sha512-bRISgCIjP20/tbWSPWMEi54QVPRZExkuD9lJL+UIxUKtwVJA8wW1Trb1jMs1RFXo1CBTNZ/5hpC9QvmKWdopKw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@jridgewell/sourcemap-codec": {
      "version": "1.5.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/sourcemap-codec/-/sourcemap-codec-1.5.5.tgz",
      "integrity": "sha512-cYQ9310grqxueWbl+WuIUIaiUaDcj7WOq5fVhEljNVgRfOUhY9fy2zTvfoqWsnebh8Sl70VScFbICvJnLKB0Og==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@jridgewell/trace-mapping": {
      "version": "0.3.31",
      "resolved": "https://registry.npmjs.org/@jridgewell/trace-mapping/-/trace-mapping-0.3.31.tgz",
      "integrity": "sha512-zzNR+SdQSDJzc8joaeP8QQoCQr8NuYx2dIIytl1QeBEZHJ9uW6hebsrYgbz8hJwUQao3TWCMtmfV8Nu1twOLAw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/resolve-uri": "^3.1.0",
        "@jridgewell/sourcemap-codec": "^1.4.14"
      }
    },
    "node_modules/@tailwindcss/node": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/node/-/node-4.3.2.tgz",
      "integrity": "sha512-yWP/sqEcBLaD8JuA6zNwxoYKr75qxTioYwlRwekj5Jr/I5GXnoJfjetH/psLUIv74cYTH2lBUEzBkinthoYcBg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/remapping": "^2.3.5",
        "enhanced-resolve": "5.21.6",
        "jiti": "^2.7.0",
        "lightningcss": "1.32.0",
        "magic-string": "^0.30.21",
        "source-map-js": "^1.2.1",
        "tailwindcss": "4.3.2"
      }
    },
    "node_modules/@tailwindcss/oxide": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide/-/oxide-4.3.2.tgz",
      "integrity": "sha512-z8ZgnzX8gdNoWLBLqBPoh/sjnxkwvf9ZuWjnO0l0yIzbLa5/9S+eC5QxGZKRobVHIC3/1BoMWjHblqWjcgFgag==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 20"
      },
      "optionalDependencies": {
        "@tailwindcss/oxide-android-arm64": "4.3.2",
        "@tailwindcss/oxide-darwin-arm64": "4.3.2",
        "@tailwindcss/oxide-darwin-x64": "4.3.2",
        "@tailwindcss/oxide-freebsd-x64": "4.3.2",
        "@tailwindcss/oxide-linux-arm-gnueabihf": "4.3.2",
        "@tailwindcss/oxide-linux-arm64-gnu": "4.3.2",
        "@tailwindcss/oxide-linux-arm64-musl": "4.3.2",
        "@tailwindcss/oxide-linux-x64-gnu": "4.3.2",
        "@tailwindcss/oxide-linux-x64-musl": "4.3.2",
        "@tailwindcss/oxide-wasm32-wasi": "4.3.2",
        "@tailwindcss/oxide-win32-arm64-msvc": "4.3.2",
        "@tailwindcss/oxide-win32-x64-msvc": "4.3.2"
      }
    },
    "node_modules/@tailwindcss/oxide-android-arm64": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide-android-arm64/-/oxide-android-arm64-4.3.2.tgz",
      "integrity": "sha512-WHxqIuHpvZ5VtdX6GTl1Ik/Vp2YuN42Et+0CdeaVd/frQ9jAvGmvR8vLT+jk3e8/Q3x8kECB9+R17pgpp2BulA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">= 20"
      }
    },
    "node_modules/@tailwindcss/oxide-darwin-arm64": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide-darwin-arm64/-/oxide-darwin-arm64-4.3.2.tgz",
      "integrity": "sha512-GZypeUY/IDJW3877KeM+O67vbXr3MBnbtEL4aYhNErv/JWZhye2vGSWWG9tB6iiqR2MqRNkY8IOUy4NdSZV26w==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">= 20"
      }
    },
    "node_modules/@tailwindcss/oxide-darwin-x64": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide-darwin-x64/-/oxide-darwin-x64-4.3.2.tgz",
      "integrity": "sha512-UIIzmefR6KO1sDU7MzRqAxC8iBpft/VhkGjTjnhoS6k7Z3rQ9wEgA1ODSiyH/tcSYssulNm4Ci3hOeK1jH7ccQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">= 20"
      }
    },
    "node_modules/@tailwindcss/oxide-freebsd-x64": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide-freebsd-x64/-/oxide-freebsd-x64-4.3.2.tgz",
      "integrity": "sha512-GN+uAmcI6DNspnCDwtOAZrTz6oukJnp337qZvxqCGLd3BHBzJpO0ZbTLRvJNdztOeAmTzewewGIMPb0tk2R4WA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">= 20"
      }
    },
    "node_modules/@tailwindcss/oxide-linux-arm-gnueabihf": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide-linux-arm-gnueabihf/-/oxide-linux-arm-gnueabihf-4.3.2.tgz",
      "integrity": "sha512-4ABn7qSbdHRwTiDiuWNegCyb5+2FJ4vKIKc3DmKrvAFw7MU1Lm11dIkTPwUaFdTzc7IsOpDbqBrlh0x6y36U/w==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 20"
      }
    },
    "node_modules/@tailwindcss/oxide-linux-arm64-gnu": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide-linux-arm64-gnu/-/oxide-linux-arm64-gnu-4.3.2.tgz",
      "integrity": "sha512-wDgEIGwoM8w8pufh9LVt1PahDgNdKXrLC2qfAnV3vAmococ9RWbxeAw4pxPttd/TsJfwjyLf90Dg1y9y8I6Emw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 20"
      }
    },
    "node_modules/@tailwindcss/oxide-linux-arm64-musl": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide-linux-arm64-musl/-/oxide-linux-arm64-musl-4.3.2.tgz",
      "integrity": "sha512-J5Nuk0uZQIiMTJj3LEx4sAA9tMFUoXQZFv1J6An+QGYe53HKRJuFDi0rpq/tuouCZeAbOBY3kQ6g8qeD4TUjtA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 20"
      }
    },
    "node_modules/@tailwindcss/oxide-linux-x64-gnu": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide-linux-x64-gnu/-/oxide-linux-x64-gnu-4.3.2.tgz",
      "integrity": "sha512-kqCZpSKOBEJO4mz7OqWoofBZeXTAwaVGPj0ErAj7CojmhKpWVWVOnrt9dE8odoIraZq4oj3ausM37kXi+Tow8w==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 20"
      }
    },
    "node_modules/@tailwindcss/oxide-linux-x64-musl": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide-linux-x64-musl/-/oxide-linux-x64-musl-4.3.2.tgz",
      "integrity": "sha512-cixpqbh2toJDmkuCRI68nXA8ZxNmdK9Y+9v5h3MC3ZQKy/0BO8AWzlkWyRM7JAFSGBlfig4YVTPsK6MVgqz1uw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 20"
      }
    },
    "node_modules/@tailwindcss/oxide-wasm32-wasi": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide-wasm32-wasi/-/oxide-wasm32-wasi-4.3.2.tgz",
      "integrity": "sha512-4ec2Z/LOmRsAgU23CS4xeJfcJlmRg94A/XrbGRCF1gyU/zdDfRLYDVsS+ynSZCmGNxQ1jQriQOKMQeQxBA3Isw==",
      "bundleDependencies": [
        "@napi-rs/wasm-runtime",
        "@emnapi/core",
        "@emnapi/runtime",
        "@tybys/wasm-util",
        "@emnapi/wasi-threads",
        "tslib"
      ],
      "cpu": [
        "wasm32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "@emnapi/core": "^1.11.1",
        "@emnapi/runtime": "^1.11.1",
        "@emnapi/wasi-threads": "^1.2.2",
        "@napi-rs/wasm-runtime": "^1.1.4",
        "@tybys/wasm-util": "^0.10.2",
        "tslib": "^2.8.1"
      },
      "engines": {
        "node": ">=14.0.0"
      }
    },
    "node_modules/@tailwindcss/oxide-win32-arm64-msvc": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide-win32-arm64-msvc/-/oxide-win32-arm64-msvc-4.3.2.tgz",
      "integrity": "sha512-Zyr/M0+XcYZu3bZrUytc7TXvrk0ftWfl8gN2MwekNDzhqhKRUucMPSeOzM0o0wH5AWOU49BsKRrfKxI2atCPMQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 20"
      }
    },
    "node_modules/@tailwindcss/oxide-win32-x64-msvc": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/oxide-win32-x64-msvc/-/oxide-win32-x64-msvc-4.3.2.tgz",
      "integrity": "sha512-QI9BO7KlNZsp2GuO0jwAAj5jCDABOKXRkCk2XuKTSaNEFSdfzqswYVTtCHBNKHLsqyjFyFkqlDiwkNbTYSssMQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 20"
      }
    },
    "node_modules/@tailwindcss/postcss": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/@tailwindcss/postcss/-/postcss-4.3.2.tgz",
      "integrity": "sha512-rjVWYCa7Ngbi5AarT6k8TkxUG3Wl1QKzHdIZVsjZSzf36Jmo2IKZt/NHRAwly8oDkbBOH0YTu+CHuf9jPxMc+g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@alloc/quick-lru": "^5.2.0",
        "@tailwindcss/node": "4.3.2",
        "@tailwindcss/oxide": "4.3.2",
        "postcss": "^8.5.15",
        "tailwindcss": "4.3.2"
      }
    },
    "node_modules/ansi-regex": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/ansi-regex/-/ansi-regex-5.0.1.tgz",
      "integrity": "sha512-quJQXlTSUGL2LH9SUXo8VwsY4soanhgo6LNSm84E1LBcE8s3O0wpdiRzyR9z/ZZJMlMWv37qOOb9pdJlMUEKFQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/ansi-styles": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-4.3.0.tgz",
      "integrity": "sha512-zbB9rCJAT1rbjiVDb2hqKFHNYLxgtk8NURxZ3IZwD3F6NtxbXZQCnnSi1Lkx+IDohdPlFp222wVALIheZJQSEg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "color-convert": "^2.0.1"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-styles?sponsor=1"
      }
    },
    "node_modules/anymatch": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/anymatch/-/anymatch-3.1.3.tgz",
      "integrity": "sha512-KMReFUr0B4t+D+OBkjR3KYqvocp2XaSzO55UcB6mgQMd3KbcE+mWTyvVV7D/zsdEbNnV6acZUutkiHQXvTr1Rw==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "normalize-path": "^3.0.0",
        "picomatch": "^2.0.4"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/balanced-match": {
      "version": "4.0.4",
      "resolved": "https://registry.npmjs.org/balanced-match/-/balanced-match-4.0.4.tgz",
      "integrity": "sha512-BLrgEcRTwX2o6gGxGOCNyMvGSp35YofuYzw9h1IMTRmKqttAZZVU67bdb9Pr2vUHA8+j3i2tJfjO6C6+4myGTA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "18 || 20 || >=22"
      }
    },
    "node_modules/binary-extensions": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/binary-extensions/-/binary-extensions-2.3.0.tgz",
      "integrity": "sha512-Ceh+7ox5qe7LJuLHoY0feh3pHuUDHAcRUeyL2VYghZwfpkNIy/+8Ocg0a3UuSoYzavmylwuLWQOf3hl0jjMMIw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/brace-expansion": {
      "version": "5.0.7",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-5.0.7.tgz",
      "integrity": "sha512-7oFy703dxfY3/NLxC1fh2SUCQ0H9rmAY+5EpDVfXjUTTs+HEwR2nYaqLv+GWcTsumwxPfiz6CzCNkwXwBUwqCA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "balanced-match": "^4.0.2"
      },
      "engines": {
        "node": "18 || 20 || >=22"
      }
    },
    "node_modules/braces": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/braces/-/braces-3.0.3.tgz",
      "integrity": "sha512-yQbXgO/OSZVD2IsiLlro+7Hf6Q18EJrKSEsdoMzKePKXct3gvD8oLcOQdIzGupr5Fj+EDe8gO/lxc1BzfMpxvA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "fill-range": "^7.1.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/chokidar": {
      "version": "3.6.0",
      "resolved": "https://registry.npmjs.org/chokidar/-/chokidar-3.6.0.tgz",
      "integrity": "sha512-7VT13fmjotKpGipCW9JEQAusEPE+Ei8nl6/g4FBAmIm0GOOLMua9NDDo/DWp0ZAxCr3cPq5ZpBqmPAQgDda2Pw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "anymatch": "~3.1.2",
        "braces": "~3.0.2",
        "glob-parent": "~5.1.2",
        "is-binary-path": "~2.1.0",
        "is-glob": "~4.0.1",
        "normalize-path": "~3.0.0",
        "readdirp": "~3.6.0"
      },
      "engines": {
        "node": ">= 8.10.0"
      },
      "funding": {
        "url": "https://paulmillr.com/funding/"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.2"
      }
    },
    "node_modules/cliui": {
      "version": "8.0.1",
      "resolved": "https://registry.npmjs.org/cliui/-/cliui-8.0.1.tgz",
      "integrity": "sha512-BSeNnyus75C4//NQ9gQt1/csTXyo/8Sb+afLAkzAptFuMsod9HFokGNudZpi/oQV73hnVK+sR+5PVRMd+Dr7YQ==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "string-width": "^4.2.0",
        "strip-ansi": "^6.0.1",
        "wrap-ansi": "^7.0.0"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/color-convert": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/color-convert/-/color-convert-2.0.1.tgz",
      "integrity": "sha512-RRECPsj7iu/xb5oKYcsFHSppFNnsj/52OVTRKb4zP5onXwVF3zVmmToNcOfGC+CRDpfK/U584fMg38ZHCaElKQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "color-name": "~1.1.4"
      },
      "engines": {
        "node": ">=7.0.0"
      }
    },
    "node_modules/color-name": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/color-name/-/color-name-1.1.4.tgz",
      "integrity": "sha512-dOy+3AuW3a2wNbZHIuMZpTcgjGuLU/uBL/ubcZF9OXbDo8ff4O8yVp5Bf0efS8uEoYo5q4Fx7dY9OgQGXgAsQA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/cross-env": {
      "version": "10.1.0",
      "resolved": "https://registry.npmjs.org/cross-env/-/cross-env-10.1.0.tgz",
      "integrity": "sha512-GsYosgnACZTADcmEyJctkJIoqAhHjttw7RsFrVoJNXbsWWqaq6Ym+7kZjq6mS45O0jij6vtiReppKQEtqWy6Dw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@epic-web/invariant": "^1.0.0",
        "cross-spawn": "^7.0.6"
      },
      "bin": {
        "cross-env": "dist/bin/cross-env.js",
        "cross-env-shell": "dist/bin/cross-env-shell.js"
      },
      "engines": {
        "node": ">=20"
      }
    },
    "node_modules/cross-spawn": {
      "version": "7.0.6",
      "resolved": "https://registry.npmjs.org/cross-spawn/-/cross-spawn-7.0.6.tgz",
      "integrity": "sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "path-key": "^3.1.0",
        "shebang-command": "^2.0.0",
        "which": "^2.0.1"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/daisyui": {
      "version": "5.6.6",
      "resolved": "https://registry.npmjs.org/daisyui/-/daisyui-5.6.6.tgz",
      "integrity": "sha512-UFiuIZYucF7ylrnY3PT1SqwaEbVB10mqTZRyeRchZk0bud+HihYLLhXdxGDVmR/ftrM9G9YVr9FFPRVVIZJ5hA==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "url": "https://github.com/saadeghi/daisyui?sponsor=1"
      }
    },
    "node_modules/dependency-graph": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/dependency-graph/-/dependency-graph-1.0.0.tgz",
      "integrity": "sha512-cW3gggJ28HZ/LExwxP2B++aiKxhJXMSIt9K48FOXQkm+vuG5gyatXnLsONRJdzO/7VfjDIiaOOa/bs4l464Lwg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/detect-libc": {
      "version": "2.1.2",
      "resolved": "https://registry.npmjs.org/detect-libc/-/detect-libc-2.1.2.tgz",
      "integrity": "sha512-Btj2BOOO83o3WyH59e8MgXsxEQVcarkUOpEYrubB0urwnN10yQ364rsiByU11nZlqWYZm05i/of7io4mzihBtQ==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/emoji-regex": {
      "version": "8.0.0",
      "resolved": "https://registry.npmjs.org/emoji-regex/-/emoji-regex-8.0.0.tgz",
      "integrity": "sha512-MSjYzcWNOA0ewAHpz0MxpYFvwg6yjy1NG3xteoqz644VCo/RPgnr1/GGt+ic3iJTzQ8Eu3TdM14SawnVUmGE6A==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/enhanced-resolve": {
      "version": "5.21.6",
      "resolved": "https://registry.npmjs.org/enhanced-resolve/-/enhanced-resolve-5.21.6.tgz",
      "integrity": "sha512-aNnGCvbJ/RIyWo1IuhNdVjnNF+EjH9wpzpNHt+ci/m9He9LJvUN8wrCcXjp9cWsGNAuvSpVFTx/vraAFQ8qGjQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "graceful-fs": "^4.2.4",
        "tapable": "^2.3.3"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/escalade": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/escalade/-/escalade-3.2.0.tgz",
      "integrity": "sha512-WUj2qlxaQtO4g6Pq5c29GTcWGDyd8itL8zTlipgECz3JesAiiOKotd8JU6otB3PACgG6xkJUyVhboMS+bje/jA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/fill-range": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/fill-range/-/fill-range-7.1.1.tgz",
      "integrity": "sha512-YsGpe3WHLK8ZYi4tWDg2Jy3ebRz2rXowDxnld4bkQB00cc/1Zw9AWnC0i9ztDJitivtQvaI9KaLyKrc+hBW0yg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "to-regex-range": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/fs-extra": {
      "version": "11.3.6",
      "resolved": "https://registry.npmjs.org/fs-extra/-/fs-extra-11.3.6.tgz",
      "integrity": "sha512-w8ZNZr2mKIc7qeNaQ9AVPT1+iFaI+Avd4xudVOvdDJ8VytREi1Ft5Ih7hd9jjehod8vAM5GMsfQ/TpPf4EyoEA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "graceful-fs": "^4.2.0",
        "jsonfile": "^6.0.1",
        "universalify": "^2.0.0"
      },
      "engines": {
        "node": ">=14.14"
      }
    },
    "node_modules/fsevents": {
      "version": "2.3.3",
      "resolved": "https://registry.npmjs.org/fsevents/-/fsevents-2.3.3.tgz",
      "integrity": "sha512-5xoDfX+fL7faATnagmWPpbFtwh/R77WmMMqqHGS65C3vvB0YHrgF+B1YmZ3441tMj5n63k0212XNoJwzlhffQw==",
      "dev": true,
      "hasInstallScript": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^8.16.0 || ^10.6.0 || >=11.0.0"
      }
    },
    "node_modules/get-caller-file": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/get-caller-file/-/get-caller-file-2.0.5.tgz",
      "integrity": "sha512-DyFP3BM/3YHTQOCUL/w0OZHR0lpKeGrxotcHWcqNEdnltqFwXVfhEBQ94eIo34AfQpo0rGki4cyIiftY06h2Fg==",
      "dev": true,
      "license": "ISC",
      "engines": {
        "node": "6.* || 8.* || >= 10.*"
      }
    },
    "node_modules/glob": {
      "version": "13.0.6",
      "resolved": "https://registry.npmjs.org/glob/-/glob-13.0.6.tgz",
      "integrity": "sha512-Wjlyrolmm8uDpm/ogGyXZXb1Z+Ca2B8NbJwqBVg0axK9GbBeoS7yGV6vjXnYdGm6X53iehEuxxbyiKp8QmN4Vw==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "minimatch": "^10.2.2",
        "minipass": "^7.1.3",
        "path-scurry": "^2.0.2"
      },
      "engines": {
        "node": "18 || 20 || >=22"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/glob-parent": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-5.1.2.tgz",
      "integrity": "sha512-AOIgSQCepiJYwP3ARnGx+5VnTu2HBYdzbGP45eLw1vr3zB3vZLeyed1sC9hnbcOc9/SrMyM5RPQrkGz4aS9Zow==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "is-glob": "^4.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/graceful-fs": {
      "version": "4.2.11",
      "resolved": "https://registry.npmjs.org/graceful-fs/-/graceful-fs-4.2.11.tgz",
      "integrity": "sha512-RbJ5/jmFcNNCcDV5o9eTnBLJ/HszWV0P73bc+Ff4nS/rJj+YaS6IGyiOL0VoBYX+l1Wrl3k63h/KrH+nhJ0XvQ==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/is-binary-path": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/is-binary-path/-/is-binary-path-2.1.0.tgz",
      "integrity": "sha512-ZMERYes6pDydyuGidse7OsHxtbI7WVeUEozgR/g7rd0xUimYNlvZRE/K2MgZTjWy725IfelLeVcEM97mmtRGXw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "binary-extensions": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/is-extglob": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/is-extglob/-/is-extglob-2.1.1.tgz",
      "integrity": "sha512-SbKbANkN603Vi4jEZv49LeVJMn4yGwsbzZworEoyEiutsN3nJYdbO36zfhGJ6QEDpOZIFkDtnq5JRxmvl3jsoQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-fullwidth-code-point": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/is-fullwidth-code-point/-/is-fullwidth-code-point-3.0.0.tgz",
      "integrity": "sha512-zymm5+u+sCsSWyD9qNaejV3DFvhCKclKdizYaJUuHA83RLjb7nSuGnddCHGv0hk+KY7BMAlsWeK4Ueg6EV6XQg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/is-glob": {
      "version": "4.0.3",
      "resolved": "https://registry.npmjs.org/is-glob/-/is-glob-4.0.3.tgz",
      "integrity": "sha512-xelSayHH36ZgE7ZWhli7pW34hNbNl8Ojv5KVmkJD4hBdD3th8Tfk9vYasLM+mXWOZhFkgZfxhLSnrwRr4elSSg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-extglob": "^2.1.1"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-number": {
      "version": "7.0.0",
      "resolved": "https://registry.npmjs.org/is-number/-/is-number-7.0.0.tgz",
      "integrity": "sha512-41Cifkg6e8TylSpdtTpeLVMqvSBEVzTttHvERD741+pnZ8ANv0004MRL43QKPDlK9cGvNp6NZWZUBlbGXYxxng==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.12.0"
      }
    },
    "node_modules/isexe": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/isexe/-/isexe-2.0.0.tgz",
      "integrity": "sha512-RHxMLp9lnKHGHRng9QFhRCMbYAcVpn69smSGcq3f36xjgVVWThj4qqLbTLlq7Ssj8B+fIQ1EuCEGI2lKsyQeIw==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/jiti": {
      "version": "2.7.0",
      "resolved": "https://registry.npmjs.org/jiti/-/jiti-2.7.0.tgz",
      "integrity": "sha512-AC/7JofJvZGrrneWNaEnJeOLUx+JlGt7tNa0wZiRPT4MY1wmfKjt2+6O2p2uz2+skll8OZZmJMNqeke7kKbNgQ==",
      "dev": true,
      "license": "MIT",
      "bin": {
        "jiti": "lib/jiti-cli.mjs"
      }
    },
    "node_modules/jsonfile": {
      "version": "6.2.1",
      "resolved": "https://registry.npmjs.org/jsonfile/-/jsonfile-6.2.1.tgz",
      "integrity": "sha512-zwOTdL3rFQ/lRdBnntKVOX6k5cKJwEc1HdilT71BWEu7J41gXIB2MRp+vxduPSwZJPWBxEzv4yH1wYLJGUHX4Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "universalify": "^2.0.0"
      },
      "optionalDependencies": {
        "graceful-fs": "^4.1.6"
      }
    },
    "node_modules/lightningcss": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss/-/lightningcss-1.32.0.tgz",
      "integrity": "sha512-NXYBzinNrblfraPGyrbPoD19C1h9lfI/1mzgWYvXUTe414Gz/X1FD2XBZSZM7rRTrMA8JL3OtAaGifrIKhQ5yQ==",
      "dev": true,
      "license": "MPL-2.0",
      "dependencies": {
        "detect-libc": "^2.0.3"
      },
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      },
      "optionalDependencies": {
        "lightningcss-android-arm64": "1.32.0",
        "lightningcss-darwin-arm64": "1.32.0",
        "lightningcss-darwin-x64": "1.32.0",
        "lightningcss-freebsd-x64": "1.32.0",
        "lightningcss-linux-arm-gnueabihf": "1.32.0",
        "lightningcss-linux-arm64-gnu": "1.32.0",
        "lightningcss-linux-arm64-musl": "1.32.0",
        "lightningcss-linux-x64-gnu": "1.32.0",
        "lightningcss-linux-x64-musl": "1.32.0",
        "lightningcss-win32-arm64-msvc": "1.32.0",
        "lightningcss-win32-x64-msvc": "1.32.0"
      }
    },
    "node_modules/lightningcss-android-arm64": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-android-arm64/-/lightningcss-android-arm64-1.32.0.tgz",
      "integrity": "sha512-YK7/ClTt4kAK0vo6w3X+Pnm0D2cf2vPHbhOXdoNti1Ga0al1P4TBZhwjATvjNwLEBCnKvjJc2jQgHXH0NEwlAg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-darwin-arm64": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-darwin-arm64/-/lightningcss-darwin-arm64-1.32.0.tgz",
      "integrity": "sha512-RzeG9Ju5bag2Bv1/lwlVJvBE3q6TtXskdZLLCyfg5pt+HLz9BqlICO7LZM7VHNTTn/5PRhHFBSjk5lc4cmscPQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-darwin-x64": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-darwin-x64/-/lightningcss-darwin-x64-1.32.0.tgz",
      "integrity": "sha512-U+QsBp2m/s2wqpUYT/6wnlagdZbtZdndSmut/NJqlCcMLTWp5muCrID+K5UJ6jqD2BFshejCYXniPDbNh73V8w==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-freebsd-x64": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-freebsd-x64/-/lightningcss-freebsd-x64-1.32.0.tgz",
      "integrity": "sha512-JCTigedEksZk3tHTTthnMdVfGf61Fky8Ji2E4YjUTEQX14xiy/lTzXnu1vwiZe3bYe0q+SpsSH/CTeDXK6WHig==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-arm-gnueabihf": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-arm-gnueabihf/-/lightningcss-linux-arm-gnueabihf-1.32.0.tgz",
      "integrity": "sha512-x6rnnpRa2GL0zQOkt6rts3YDPzduLpWvwAF6EMhXFVZXD4tPrBkEFqzGowzCsIWsPjqSK+tyNEODUBXeeVHSkw==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-arm64-gnu": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-arm64-gnu/-/lightningcss-linux-arm64-gnu-1.32.0.tgz",
      "integrity": "sha512-0nnMyoyOLRJXfbMOilaSRcLH3Jw5z9HDNGfT/gwCPgaDjnx0i8w7vBzFLFR1f6CMLKF8gVbebmkUN3fa/kQJpQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-arm64-musl": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-arm64-musl/-/lightningcss-linux-arm64-musl-1.32.0.tgz",
      "integrity": "sha512-UpQkoenr4UJEzgVIYpI80lDFvRmPVg6oqboNHfoH4CQIfNA+HOrZ7Mo7KZP02dC6LjghPQJeBsvXhJod/wnIBg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-x64-gnu": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-x64-gnu/-/lightningcss-linux-x64-gnu-1.32.0.tgz",
      "integrity": "sha512-V7Qr52IhZmdKPVr+Vtw8o+WLsQJYCTd8loIfpDaMRWGUZfBOYEJeyJIkqGIDMZPwPx24pUMfwSxxI8phr/MbOA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-x64-musl": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-x64-musl/-/lightningcss-linux-x64-musl-1.32.0.tgz",
      "integrity": "sha512-bYcLp+Vb0awsiXg/80uCRezCYHNg1/l3mt0gzHnWV9XP1W5sKa5/TCdGWaR/zBM2PeF/HbsQv/j2URNOiVuxWg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-win32-arm64-msvc": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-win32-arm64-msvc/-/lightningcss-win32-arm64-msvc-1.32.0.tgz",
      "integrity": "sha512-8SbC8BR40pS6baCM8sbtYDSwEVQd4JlFTOlaD3gWGHfThTcABnNDBda6eTZeqbofalIJhFx0qKzgHJmcPTnGdw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-win32-x64-msvc": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-win32-x64-msvc/-/lightningcss-win32-x64-msvc-1.32.0.tgz",
      "integrity": "sha512-Amq9B/SoZYdDi1kFrojnoqPLxYhQ4Wo5XiL8EVJrVsB8ARoC1PWW6VGtT0WKCemjy8aC+louJnjS7U18x3b06Q==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lilconfig": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/lilconfig/-/lilconfig-3.1.3.tgz",
      "integrity": "sha512-/vlFKAoH5Cgt3Ie+JLhRbwOsCQePABiU3tJ1egGvyQ+33R/vcwM2Zl2QR/LzjsBeItPt3oSVXapn+m4nQDvpzw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=14"
      },
      "funding": {
        "url": "https://github.com/sponsors/antonk52"
      }
    },
    "node_modules/lru-cache": {
      "version": "11.5.1",
      "resolved": "https://registry.npmjs.org/lru-cache/-/lru-cache-11.5.1.tgz",
      "integrity": "sha512-RPimw/7aMdv2oqRrxKwvZXcPfwBrn/JZ2xYcY9Hus/6LaS3VOAKVWKWgNLCFSiOm1ESXinjsDlidVU7JlnCN2A==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "engines": {
        "node": "20 || >=22"
      }
    },
    "node_modules/magic-string": {
      "version": "0.30.21",
      "resolved": "https://registry.npmjs.org/magic-string/-/magic-string-0.30.21.tgz",
      "integrity": "sha512-vd2F4YUyEXKGcLHoq+TEyCjxueSeHnFxyyjNp80yg0XV4vUhnDer/lvvlqM/arB5bXQN5K2/3oinyCRyx8T2CQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/sourcemap-codec": "^1.5.5"
      }
    },
    "node_modules/minimatch": {
      "version": "10.2.5",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-10.2.5.tgz",
      "integrity": "sha512-MULkVLfKGYDFYejP07QOurDLLQpcjk7Fw+7jXS2R2czRQzR56yHRveU5NDJEOviH+hETZKSkIk5c+T23GjFUMg==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "brace-expansion": "^5.0.5"
      },
      "engines": {
        "node": "18 || 20 || >=22"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/minipass": {
      "version": "7.1.3",
      "resolved": "https://registry.npmjs.org/minipass/-/minipass-7.1.3.tgz",
      "integrity": "sha512-tEBHqDnIoM/1rXME1zgka9g6Q2lcoCkxHLuc7ODJ5BxbP5d4c2Z5cGgtXAku59200Cx7diuHTOYfSBD8n6mm8A==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "engines": {
        "node": ">=16 || 14 >=14.17"
      }
    },
    "node_modules/nanoid": {
      "version": "3.3.15",
      "resolved": "https://registry.npmjs.org/nanoid/-/nanoid-3.3.15.tgz",
      "integrity": "sha512-y7Wygv/7mEOvxTuEQDB8StXdMRBWf1kR/tlhAzBRUFkB2jfcLOAxO/SHmOO2zgz1pVgK29/kyupn059/bCHdjA==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "bin": {
        "nanoid": "bin/nanoid.cjs"
      },
      "engines": {
        "node": "^10 || ^12 || ^13.7 || ^14 || >=15.0.1"
      }
    },
    "node_modules/normalize-path": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/normalize-path/-/normalize-path-3.0.0.tgz",
      "integrity": "sha512-6eZs5Ls3WtCisHWp9S2GUy8dqkpGi4BVSz3GaqiE6ezub0512ESztXUwUB6C6IKbQkY2Pnb/mD4WYojCRwcwLA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/package-json-from-dist": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/package-json-from-dist/-/package-json-from-dist-1.0.1.tgz",
      "integrity": "sha512-UEZIS3/by4OC8vL3P2dTXRETpebLI2NiI5vIrjaD/5UtrkFX/tNbwjTSRAGC/+7CAo2pIcBaRgWmcBBHcsaCIw==",
      "dev": true,
      "license": "BlueOak-1.0.0"
    },
    "node_modules/path-key": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/path-key/-/path-key-3.1.1.tgz",
      "integrity": "sha512-ojmeN0qd+y0jszEtoY48r0Peq5dwMEkIlCOu6Q5f41lfkswXuKtYrhgoTpLnyIcHm24Uhqx+5Tqm2InSwLhE6Q==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-scurry": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/path-scurry/-/path-scurry-2.0.2.tgz",
      "integrity": "sha512-3O/iVVsJAPsOnpwWIeD+d6z/7PmqApyQePUtCndjatj/9I5LylHvt5qluFaBT3I5h3r1ejfR056c+FCv+NnNXg==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "lru-cache": "^11.0.0",
        "minipass": "^7.1.2"
      },
      "engines": {
        "node": "18 || 20 || >=22"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/picocolors": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-1.1.1.tgz",
      "integrity": "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/picomatch": {
      "version": "2.3.2",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-2.3.2.tgz",
      "integrity": "sha512-V7+vQEJ06Z+c5tSye8S+nHUfI51xoXIXjHQ99cQtKUkQqqO1kO/KCJUfZXuB47h/YBlDhah2H3hdUGXn8ie0oA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/pify": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/pify/-/pify-2.3.0.tgz",
      "integrity": "sha512-udgsAY+fTnvv7kI7aaxbqwWNb0AHiB0qBO89PZKPkoTmGOgdbrHDKD+0B2X4uTfJ/FT1R09r9gTsjUjNJotuog==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/postcss": {
      "version": "8.5.16",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-8.5.16.tgz",
      "integrity": "sha512-vuwillviilfKZsg0VGj5R/YwwcHx4SLsIOI/7K6mQkWx+l5cUHTjj5g0AasTBcyXsbfTgrwsUNmVUb5xVwyPwg==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/postcss"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "nanoid": "^3.3.12",
        "picocolors": "^1.1.1",
        "source-map-js": "^1.2.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      }
    },
    "node_modules/postcss-cli": {
      "version": "11.0.1",
      "resolved": "https://registry.npmjs.org/postcss-cli/-/postcss-cli-11.0.1.tgz",
      "integrity": "sha512-0UnkNPSayHKRe/tc2YGW6XnSqqOA9eqpiRMgRlV1S6HdGi16vwJBx7lviARzbV1HpQHqLLRH3o8vTcB0cLc+5g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "chokidar": "^3.3.0",
        "dependency-graph": "^1.0.0",
        "fs-extra": "^11.0.0",
        "picocolors": "^1.0.0",
        "postcss-load-config": "^5.0.0",
        "postcss-reporter": "^7.0.0",
        "pretty-hrtime": "^1.0.3",
        "read-cache": "^1.0.0",
        "slash": "^5.0.0",
        "tinyglobby": "^0.2.12",
        "yargs": "^17.0.0"
      },
      "bin": {
        "postcss": "index.js"
      },
      "engines": {
        "node": ">=18"
      },
      "peerDependencies": {
        "postcss": "^8.0.0"
      }
    },
    "node_modules/postcss-load-config": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-load-config/-/postcss-load-config-5.1.0.tgz",
      "integrity": "sha512-G5AJ+IX0aD0dygOE0yFZQ/huFFMSNneyfp0e3/bT05a8OfPC5FUoZRPfGijUdGOJNMewJiwzcHJXFafFzeKFVA==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "lilconfig": "^3.1.1",
        "yaml": "^2.4.2"
      },
      "engines": {
        "node": ">= 18"
      },
      "peerDependencies": {
        "jiti": ">=1.21.0",
        "postcss": ">=8.0.9",
        "tsx": "^4.8.1"
      },
      "peerDependenciesMeta": {
        "jiti": {
          "optional": true
        },
        "postcss": {
          "optional": true
        },
        "tsx": {
          "optional": true
        }
      }
    },
    "node_modules/postcss-reporter": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/postcss-reporter/-/postcss-reporter-7.1.0.tgz",
      "integrity": "sha512-/eoEylGWyy6/DOiMP5lmFRdmDKThqgn7D6hP2dXKJI/0rJSO1ADFNngZfDzxL0YAxFvws+Rtpuji1YIHj4mySA==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "picocolors": "^1.0.0",
        "thenby": "^1.3.4"
      },
      "engines": {
        "node": ">=10"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/pretty-hrtime": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/pretty-hrtime/-/pretty-hrtime-1.0.3.tgz",
      "integrity": "sha512-66hKPCr+72mlfiSjlEB1+45IjXSqvVAIy6mocupoww4tBFE9R9IhwwUGoI4G++Tc9Aq+2rxOt0RFU6gPcrte0A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/read-cache": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/read-cache/-/read-cache-1.0.0.tgz",
      "integrity": "sha512-Owdv/Ft7IjOgm/i0xvNDZ1LrRANRfew4b2prF3OWMQLxLfu3bS8FVhCsrSCMK4lR56Y9ya+AThoTpDCTxCmpRA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "pify": "^2.3.0"
      }
    },
    "node_modules/readdirp": {
      "version": "3.6.0",
      "resolved": "https://registry.npmjs.org/readdirp/-/readdirp-3.6.0.tgz",
      "integrity": "sha512-hOS089on8RduqdbhvQ5Z37A0ESjsqz6qnRcffsMU3495FuTdqSm+7bhJ29JvIOsBDEEnan5DPu9t3To9VRlMzA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "picomatch": "^2.2.1"
      },
      "engines": {
        "node": ">=8.10.0"
      }
    },
    "node_modules/require-directory": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/require-directory/-/require-directory-2.1.1.tgz",
      "integrity": "sha512-fGxEI7+wsG9xrvdjsrlmL22OMTTiHRwAMroiEeMgq8gzoLC/PQr7RsRDSTLUg/bZAZtF+TVIkHc6/4RIKrui+Q==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/rimraf": {
      "version": "6.1.3",
      "resolved": "https://registry.npmjs.org/rimraf/-/rimraf-6.1.3.tgz",
      "integrity": "sha512-LKg+Cr2ZF61fkcaK1UdkH2yEBBKnYjTyWzTJT6KNPcSPaiT7HSdhtMXQuN5wkTX0Xu72KQ1l8S42rlmexS2hSA==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "glob": "^13.0.3",
        "package-json-from-dist": "^1.0.1"
      },
      "bin": {
        "rimraf": "dist/esm/bin.mjs"
      },
      "engines": {
        "node": "20 || >=22"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/shebang-command": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/shebang-command/-/shebang-command-2.0.0.tgz",
      "integrity": "sha512-kHxr2zZpYtdmrN1qDjrrX/Z1rR1kG8Dx+gkpK1G4eXmvXswmcE1hTWBWYUzlraYw1/yZp6YuDY77YtvbN0dmDA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "shebang-regex": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/shebang-regex": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/shebang-regex/-/shebang-regex-3.0.0.tgz",
      "integrity": "sha512-7++dFhtcx3353uBaq8DDR4NuxBetBzC7ZQOhmTQInHEd6bSrXdiEyzCvG07Z44UYdLShWUyXt5M/yhz8ekcb1A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/slash": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/slash/-/slash-5.1.0.tgz",
      "integrity": "sha512-ZA6oR3T/pEyuqwMgAKT0/hAv8oAXckzbkmR0UkUosQ+Mc4RxGoJkRmwHgHufaenlyAgE1Mxgpdcrf75y6XcnDg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=14.16"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/source-map-js": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/source-map-js/-/source-map-js-1.2.1.tgz",
      "integrity": "sha512-UXWMKhLOwVKb728IUtQPXxfYU+usdybtUrK/8uGE8CQMvrhOpwvzDBwj0QhSL7MQc7vIsISBG8VQ8+IDQxpfQA==",
      "dev": true,
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/string-width": {
      "version": "4.2.3",
      "resolved": "https://registry.npmjs.org/string-width/-/string-width-4.2.3.tgz",
      "integrity": "sha512-wKyQRQpjJ0sIp62ErSZdGsjMJWsap5oRNihHhu6G7JVO/9jIB6UyevL+tXuOqrng8j/cxKTWyWUwvSTriiZz/g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "emoji-regex": "^8.0.0",
        "is-fullwidth-code-point": "^3.0.0",
        "strip-ansi": "^6.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/strip-ansi": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-6.0.1.tgz",
      "integrity": "sha512-Y38VPSHcqkFrCpFnQ9vuSXmquuv5oXOKpGeT6aGrr3o3Gc9AlVa6JBfUSOCnbxGGZF+/0ooI7KrPuUSztUdU5A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/tailwindcss": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/tailwindcss/-/tailwindcss-4.3.2.tgz",
      "integrity": "sha512-WtctNNSH8A9jlMIqxzuYumOHU5uGZyRv0Q5svQl+oEPy5w84YpBxdb7MdqyiSPQge5jTJ6zFQLq0PFygdccSBA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/tapable": {
      "version": "2.3.3",
      "resolved": "https://registry.npmjs.org/tapable/-/tapable-2.3.3.tgz",
      "integrity": "sha512-uxc/zpqFg6x7C8vOE7lh6Lbda8eEL9zmVm/PLeTPBRhh1xCgdWaQ+J1CUieGpIfm2HdtsUpRv+HshiasBMcc6A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      }
    },
    "node_modules/thenby": {
      "version": "1.4.1",
      "resolved": "https://registry.npmjs.org/thenby/-/thenby-1.4.1.tgz",
      "integrity": "sha512-D5a/bO0KdalOE3q8MlrRmSxjbKZHT3MQmXkJP+r97Vw8MMwOZKOwUSEyTtK7eSMj2y0kyAjpYMRMZmmLw1FtNQ==",
      "dev": true,
      "license": "Apache-2.0"
    },
    "node_modules/tinyglobby": {
      "version": "0.2.17",
      "resolved": "https://registry.npmjs.org/tinyglobby/-/tinyglobby-0.2.17.tgz",
      "integrity": "sha512-wXR/dYpcqKmfWpEdZjiKJOwCNFndD0DMnrW/cYjVGttEkBfVgcLFHoNrlj47mjOVic9yyNu65alsgF4NQyTa2g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "fdir": "^6.5.0",
        "picomatch": "^4.0.4"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/SuperchupuDev"
      }
    },
    "node_modules/tinyglobby/node_modules/fdir": {
      "version": "6.5.0",
      "resolved": "https://registry.npmjs.org/fdir/-/fdir-6.5.0.tgz",
      "integrity": "sha512-tIbYtZbucOs0BRGqPJkshJUYdL+SDH7dVM8gjy+ERp3WAUjLEFJE+02kanyHtwjWOnwrKYBiwAmM0p4kLJAnXg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12.0.0"
      },
      "peerDependencies": {
        "picomatch": "^3 || ^4"
      },
      "peerDependenciesMeta": {
        "picomatch": {
          "optional": true
        }
      }
    },
    "node_modules/tinyglobby/node_modules/picomatch": {
      "version": "4.0.4",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-4.0.4.tgz",
      "integrity": "sha512-QP88BAKvMam/3NxH6vj2o21R6MjxZUAd6nlwAS/pnGvN9IVLocLHxGYIzFhg6fUQ+5th6P4dv4eW9jX3DSIj7A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/to-regex-range": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/to-regex-range/-/to-regex-range-5.0.1.tgz",
      "integrity": "sha512-65P7iz6X5yEr1cwcgvQxbbIw7Uk3gOy5dIdtZ4rDveLqhrdJP+Li/Hx6tyK0NEb+2GCyneCMJiGqrADCSNk8sQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-number": "^7.0.0"
      },
      "engines": {
        "node": ">=8.0"
      }
    },
    "node_modules/universalify": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/universalify/-/universalify-2.0.1.tgz",
      "integrity": "sha512-gptHNQghINnc/vTGIk0SOFGFNXw7JVrlRUtConJRlvaw6DuX0wO5Jeko9sWrMBhh+PsYAZ7oXAiOnf/UKogyiw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 10.0.0"
      }
    },
    "node_modules/which": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/which/-/which-2.0.2.tgz",
      "integrity": "sha512-BLI3Tl1TW3Pvl70l3yq3Y64i+awpwXqsGBYWkkqMtnbXgrMD+yj7rhW0kuEDxzJaYXGjEW5ogapKNMEKNMjibA==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "isexe": "^2.0.0"
      },
      "bin": {
        "node-which": "bin/node-which"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/wrap-ansi": {
      "version": "7.0.0",
      "resolved": "https://registry.npmjs.org/wrap-ansi/-/wrap-ansi-7.0.0.tgz",
      "integrity": "sha512-YVGIj2kamLSTxw6NsZjoBxfSwsn0ycdesmc4p+Q21c5zPuZ1pl+NfxVdxPtdHvmNVOQ6XSYG4AUtyt/Fi7D16Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^4.0.0",
        "string-width": "^4.1.0",
        "strip-ansi": "^6.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/wrap-ansi?sponsor=1"
      }
    },
    "node_modules/y18n": {
      "version": "5.0.8",
      "resolved": "https://registry.npmjs.org/y18n/-/y18n-5.0.8.tgz",
      "integrity": "sha512-0pfFzegeDWJHJIAmTLRP2DwHjdF5s7jo9tuztdQxAhINCdvS+3nGINqPd00AphqJR/0LhANUS6/+7SCb98YOfA==",
      "dev": true,
      "license": "ISC",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/yaml": {
      "version": "2.9.0",
      "resolved": "https://registry.npmjs.org/yaml/-/yaml-2.9.0.tgz",
      "integrity": "sha512-2AvhNX3mb8zd6Zy7INTtSpl1F15HW6Wnqj0srWlkKLcpYl/gMIMJiyuGq2KeI2YFxUPjdlB+3Lc10seMLtL4cA==",
      "dev": true,
      "license": "ISC",
      "bin": {
        "yaml": "bin.mjs"
      },
      "engines": {
        "node": ">= 14.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/eemeli"
      }
    },
    "node_modules/yargs": {
      "version": "17.7.3",
      "resolved": "https://registry.npmjs.org/yargs/-/yargs-17.7.3.tgz",
      "integrity": "sha512-GZtjxm/J/4TSxuL3FNYjCmLktBTnIw/rVmKSIyKeYAZpmJB2ig9VauCC5xsa82GNKVKDAqpOn3KVzNt0zmrU0g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "cliui": "^8.0.1",
        "escalade": "^3.1.1",
        "get-caller-file": "^2.0.5",
        "require-directory": "^2.1.1",
        "string-width": "^4.2.3",
        "y18n": "^5.0.5",
        "yargs-parser": "^21.1.1"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/yargs-parser": {
      "version": "21.1.1",
      "resolved": "https://registry.npmjs.org/yargs-parser/-/yargs-parser-21.1.1.tgz",
      "integrity": "sha512-tVpsJW7DdjecAiFpbIB1e3qxIQsE6NoPc5/eTdrbbIC4h0LVsWhnoa3g+m2HclBIujHzsxZ4VJVA+GUuc2/LBw==",
      "dev": true,
      "license": "ISC",
      "engines": {
        "node": ">=12"
      }
    }
  }
}
```

## `theme/static_src/package.json`

Size: 781 B

```json
{
  "name": "theme",
  "version": "4.5.0",
  "description": "",
  "scripts": {
    "start": "npm run dev",
    "build": "npm run build:clean && npm run build:tailwind",
    "build:clean": "rimraf ../static/css/dist",
    "build:tailwind": "cross-env NODE_ENV=production postcss ./src/styles.css -o ../static/css/dist/styles.css --minify",
    "dev": "cross-env NODE_ENV=development CHOKIDAR_USEPOLLING=1 CHOKIDAR_INTERVAL=300 postcss ./src/styles.css -o ../static/css/dist/styles.css --watch"
  },
  "keywords": [],
  "author": "",
  "license": "MIT",
  "devDependencies": {
    "@tailwindcss/postcss": "^4.3.0",
    "daisyui": "^5.5.23",
    "cross-env": "^10.1.0",
    "postcss": "^8.5.15",
    "postcss-cli": "^11.0.1",
    "rimraf": "^6.1.3",
    "tailwindcss": "^4.3.0"
  }
}
```

## `theme/static_src/postcss.config.js`

Size: 70 B

```javascript
module.exports = {
  plugins: {
    "@tailwindcss/postcss": {}
  },
}
```

## `theme/static_src/src/styles.css`

Size: 27.0 KB

```css
@import "tailwindcss";
@source "../../../apps/flota/**/*.{html,py,js}";
@plugin "daisyui" {
    themes: false;
}
@plugin "daisyui/theme" {
    name: "tuvtk";
    default: true;
    prefersdark: false;
    color-scheme: light;

    --tuvtk-brand-primary: #164194;
    --tuvtk-brand-secondary: #d41131;
    --tuvtk-brand-accent: #7c8f9e;
    --tuvtk-page-bg: #ffffff;
    --tuvtk-panel-bg: #ffffff;
    --tuvtk-panel-muted-bg: #f7f9fb;
    --tuvtk-heading-text: #17212b;
    --tuvtk-body-text: #304253;
    --tuvtk-muted-text: #5d6b79;
    --tuvtk-border-default: #cfd7df;
    --tuvtk-border-hover: #b8c4cf;
    --tuvtk-control-hover-bg: #edf3f9;
    --tuvtk-primary-tint-bg: #dbe6ef;
    --tuvtk-primary-tint-border: #c9d9e6;
    --tuvtk-text-on-brand: #ffffff;

    --color-base-100: var(--tuvtk-panel-bg);
    --color-base-200: var(--tuvtk-panel-muted-bg);
    --color-base-300: var(--tuvtk-border-default);
    --color-base-content: var(--tuvtk-body-text);
    --color-primary: var(--tuvtk-brand-primary);
    --color-primary-content: var(--tuvtk-text-on-brand);
    --color-secondary: var(--tuvtk-brand-secondary);
    --color-secondary-content: var(--tuvtk-text-on-brand);
    --color-accent: var(--tuvtk-brand-accent);
    --color-accent-content: var(--tuvtk-heading-text);
    --color-neutral: var(--tuvtk-heading-text);
    --color-neutral-content: var(--tuvtk-text-on-brand);
    --color-info: #165d8d;
    --color-info-content: #ffffff;
    --color-success: #2f6f4e;
    --color-success-content: #ffffff;
    --color-warning: #8a5a00;
    --color-warning-content: #ffffff;
    --color-error: #b4233c;
    --color-error-content: #ffffff;

    --radius-selector: 0.5rem;
    --radius-field: 0.25rem;
    --radius-box: 0.5rem;
    --size-selector: 0.25rem;
    --size-field: 0.25rem;
    --border: 1px;
    --depth: 1;
    --noise: 0;

    --sidebar-bg: #ffffff;
    --sidebar-border: #d5dee7;
    --sidebar-heading-bg: #f1f5f8;
    --sidebar-heading-text: #52697d;
    --sidebar-heading-border: #d5dee7;
    --sidebar-heading-accent: var(--tuvtk-brand-primary);
    --sidebar-item-text: var(--tuvtk-brand-primary);
    --sidebar-item-icon: var(--tuvtk-brand-primary);
    --sidebar-item-hover-bg: #edf3f9;
    --sidebar-item-hover-text: var(--tuvtk-brand-secondary);
    --sidebar-item-hover-icon: var(--tuvtk-brand-secondary);
    --sidebar-item-hover-indicator: var(--tuvtk-brand-secondary);
    --sidebar-item-hover-indicator-width: 3px;
    --sidebar-item-hover-shift: 3px;
    --sidebar-item-pressed-bg: #d7e3ef;
    --sidebar-item-pressed-text: #0f3268;
    --sidebar-item-pressed-icon: #0f3268;
    --sidebar-item-current-bg: #e1eaf4;
    --sidebar-item-current-text: #123b77;
    --sidebar-item-current-icon: var(--tuvtk-brand-primary);
    --sidebar-item-current-indicator: var(--tuvtk-brand-secondary);
    --sidebar-child-guide: #c8d4df;
    --sidebar-child-text: #405d73;
    --sidebar-child-hover-bg: #edf3f9;
    --sidebar-child-hover-text: #123b77;
    --sidebar-child-current-bg: #dce7f2;
    --sidebar-child-current-text: #123b77;
    --sidebar-footer-bg: #ffffff;
    --sidebar-footer-border: #d5dee7;
    --sidebar-footer-divider: rgb(255 255 255 / 0.1);
    --sidebar-footer-heading-text: #223241;
    --sidebar-footer-text: #6b7a88;
    --sidebar-tooltip-bg: var(--tuvtk-brand-primary);
    --sidebar-tooltip-text: #ffffff;
    --scrollbar-thumb: var(--tuvtk-brand-primary);
    --scrollbar-track: transparent;
}

@source "../../../core/**/*.{html,py,js}";
@source "../../../apps/dashboard/**/*.{html,py,js}";
@source "../../../apps/planificator/**/*.{html,py,js}";
@source "../../../apps/diplome/**/*.{html,py,js}";
@source "../../../apps/media_library/**/*.{html,py,js}";
@source "../../../apps/tasks/**/*.{html,py,js}";
@source "../../static/**/*.js";
@source not "../../static/js/vendor";

@font-face {
    font-family: "InterVariable";
    font-style: normal;
    font-weight: 100 900;
    font-display: optional;
    src: url("../../fonts/inter/InterVariable.woff2") format("woff2");
}

@theme inline {
    --font-sans: "InterVariable", "Inter", "Segoe UI", sans-serif;
    --color-muted: var(--tuvtk-muted-text);
}

@layer base {
    html,
    body {
        font-family: var(--font-sans);
        font-optical-sizing: auto;
    }

    body {
        background: var(--color-base-100);
        color: var(--color-base-content);
    }

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: var(--tuvtk-heading-text);
    }

    :focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }
}

@layer components {
    .dropdown-content {
        border-radius: 0.65rem;
        box-shadow: none;
    }

    .ops-shell {
        background: var(--color-base-100);
    }

    .ops-topbar {
        position: relative;
        z-index: 50;
        height: 4rem;
        border-bottom: 1px solid var(--color-primary);
        background: var(--color-base-100);
    }

    .ops-logo {
        width: 3.5rem;
        height: 3.5rem;
        flex: none;
        object-fit: contain;
    }

    .ops-header-chip {
        align-items: center;
        gap: 0.45rem;
        border: 1px solid var(--color-base-300);
        border-radius: 0.45rem;
        background: var(--color-base-100);
        padding: 0.45rem 0.65rem;
        color: var(--tuvtk-muted-text);
        font-size: 0.75rem;
        font-weight: 600;
    }

    .ops-sidebar-toggle {
        display: inline-flex;
        width: 2.75rem;
        height: 2.75rem;
        min-height: 2.75rem;
        flex: none;
        cursor: pointer;
        align-items: center;
        justify-content: center;
        border: 1px solid var(--color-base-300);
        border-radius: var(--radius-field);
        background: var(--color-base-100);
        color: var(--color-primary);
        transition: border-color 150ms ease, background-color 150ms ease, color 150ms ease;
    }

    .ops-sidebar-toggle:hover {
        border-color: var(--tuvtk-border-hover);
        background: var(--tuvtk-control-hover-bg);
        color: var(--color-secondary);
    }

    .ops-user-trigger {
        display: inline-flex;
        align-items: center;
        cursor: pointer;
        border: 1px solid var(--color-base-300);
        border-radius: 9999px;
        background: var(--color-base-100);
        padding: 0.3rem;
        color: var(--sidebar-item-text);
        list-style: none;
    }

    .ops-user-flyout {
        position: relative;
        flex: none;
        line-height: 0;
    }

    .ops-user-menu {
        position: absolute;
        top: 100%;
        right: 0;
        line-height: normal;
    }

    .ops-user-trigger::-webkit-details-marker {
        display: none;
    }

    .ops-user-trigger:hover,
    .ops-user-trigger:focus-visible,
    .ops-user-flyout[open] > .ops-user-trigger {
        border-color: var(--tuvtk-border-hover);
        background: var(--sidebar-item-hover-bg);
        color: var(--sidebar-item-hover-text);
    }

    .ops-avatar-frame {
        display: inline-grid;
        padding: 0.15rem;
        place-items: center;
        border: 1px solid var(--sidebar-border);
        border-radius: 9999px;
        background: var(--color-base-100);
    }

    .ops-user-trigger:hover .ops-avatar-frame,
    .ops-user-trigger:focus-visible .ops-avatar-frame,
    .ops-user-flyout[open] > .ops-user-trigger .ops-avatar-frame {
        border-color: var(--sidebar-item-hover-indicator);
    }

    .ops-avatar {
        display: grid;
        width: 2.4rem;
        height: 2.4rem;
        flex: none;
        place-items: center;
        overflow: hidden;
        border-radius: 9999px;
        background: var(--color-primary);
        color: var(--color-primary-content);
        font-size: 0.8125rem;
        font-weight: 800;
        letter-spacing: 0.04em;
    }

    .ops-avatar-status {
        position: absolute;
        right: -0.05rem;
        bottom: -0.05rem;
        width: 0.7rem;
        height: 0.7rem;
        border: 2px solid var(--color-base-100);
        border-radius: 9999px;
        background: var(--color-success);
    }

    .ops-title {
        color: var(--color-primary);
        letter-spacing: -0.025em;
    }

    .generator-step-card {
        overflow: hidden;
        border: 1px solid var(--tuvtk-border-hover);
        border-top: 4px solid var(--color-secondary);
        border-radius: 0;
        transition: opacity 180ms ease;
    }

    .card.generator-step-card {
        border-radius: 0 !important;
    }

    .generator-card-header {
        border-bottom: 1px solid var(--tuvtk-border-hover);
    }

    .generator-card-step .steps,
    .generator-card-step .step,
    .generator-card-step-copy {
        width: 100%;
        min-width: 0;
    }

    .generator-card-step .steps {
        overflow: visible;
    }

    .generator-card-step .step {
        min-height: 3.5rem;
        text-align: left;
    }

    .generator-card-step-copy {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        padding-block: 0.45rem;
    }

    .generator-card-step-copy .card-title {
        display: block;
        width: 100%;
        line-height: 1.25;
    }

    .generator-step-card.generator-card-complete {
        opacity: 0.64;
    }

    .ops-schedule-table thead th {
        position: sticky !important;
        top: 0 !important;
    }

    .ops-word-match-scroll {
        max-height: 36rem;
        overscroll-behavior-inline: contain;
        scrollbar-gutter: stable;
        scrollbar-width: auto;
    }

    .ops-word-match-scroll::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    .ops-word-match-scroll::-webkit-scrollbar-track {
        background: var(--scrollbar-track);
        border-top: 1px solid var(--tuvtk-border-default);
    }

    .ops-word-match-scroll::-webkit-scrollbar-thumb {
        border: 2px solid var(--scrollbar-track);
        border-radius: 9999px;
        background: var(--scrollbar-thumb);
    }

    .ops-word-match-table {
        width: 73.75rem;
        min-width: 73.75rem;
        table-layout: fixed;
    }

    .ops-word-match-table :where(th, td) {
        overflow-wrap: anywhere;
        white-space: normal;
        vertical-align: top;
    }

    .ops-course-updater-top-scroll {
        overflow-x: auto;
        overflow-y: hidden;
        height: 0.75rem;
        margin-bottom: 0.25rem;
        scrollbar-width: auto;
    }

    .ops-course-updater-top-scroll > div {
        height: 1px;
    }

    .ops-course-updater-scroll {
        max-height: 38rem;
        overflow: auto;
        overscroll-behavior-inline: contain;
        scrollbar-gutter: stable;
    }

    .ops-course-updater-table {
        width: 72.5rem;
        min-width: 72.5rem;
        table-layout: fixed;
    }

    .ops-course-updater-table thead th {
        position: sticky;
        top: 0;
        z-index: 10;
        background: var(--color-base-200);
    }

    .ops-course-updater-table :where(th, td) {
        overflow-wrap: anywhere;
        padding: 0.45rem 0.5rem;
        white-space: normal;
        vertical-align: top !important;
    }

    .ops-word-match-table thead th {
        position: sticky;
        top: 0;
        z-index: 5;
        background: var(--color-base-200);
    }

    .ops-word-match-course {
        text-align: center !important;
        vertical-align: middle !important;
    }

    .ops-word-match-periods {
        text-align: center !important;
        vertical-align: middle !important;
    }

    .ops-word-select-clip {
        overflow: hidden;
        border-radius: var(--radius-field);
    }

    .ops-word-match-table select {
        display: block;
        width: 100%;
        min-width: 0;
        max-width: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    @media (max-width: 639px) {
        .ops-word-match-scroll {
            max-height: 26rem;
        }
    }

    .ops-schedule-course-column {
        position: sticky !important;
        left: 0 !important;
        width: var(--course-width) !important;
        min-width: var(--course-width) !important;
        max-width: var(--course-width) !important;
    }

    .ops-schedule-duration-column {
        position: sticky !important;
        left: var(--course-width) !important;
        width: var(--duration-width) !important;
        min-width: var(--duration-width) !important;
        max-width: var(--duration-width) !important;
    }

    .ops-schedule-investment-column {
        position: sticky !important;
        left: calc(var(--course-width) + var(--duration-width)) !important;
        width: var(--investment-width) !important;
        min-width: var(--investment-width) !important;
        max-width: var(--investment-width) !important;
    }

    .ops-sidebar {
        border-right: 1px solid var(--sidebar-border);
        background: var(--sidebar-bg);
        color: var(--sidebar-item-text);
    }

    .ops-sidebar-nav {
        scrollbar-width: thin;
        scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);
    }

    .ops-sidebar-nav::-webkit-scrollbar,
    .ops-scrollbar::-webkit-scrollbar {
        width: 4px;
        height: 4px;
    }

    .ops-sidebar-nav::-webkit-scrollbar-track,
    .ops-scrollbar::-webkit-scrollbar-track {
        background: var(--scrollbar-track);
    }

    .ops-sidebar-nav::-webkit-scrollbar-thumb,
    .ops-scrollbar::-webkit-scrollbar-thumb {
        border-radius: 9999px;
        background: var(--scrollbar-thumb);
    }

    .ops-sidebar-heading {
        border-block: 1px solid var(--sidebar-heading-border);
        border-left: 3px solid var(--sidebar-heading-accent);
        background: var(--sidebar-heading-bg);
        padding-block: 0.48rem;
        color: var(--sidebar-heading-text);
    }

    .ops-sidebar-nav ul.menu {
        display: flex;
        width: 100%;
        flex-flow: column nowrap;
        align-items: stretch;
    }

    .ops-sidebar-nav ul.menu > li,
    .ops-sidebar-nav ul.menu > li > details {
        width: 100%;
    }

    .ops-sidebar-nav ul.menu > li > a,
    .ops-sidebar-nav ul.menu > li > details > summary {
        display: flex;
        width: 100%;
        min-height: 2.45rem;
        cursor: pointer;
        align-items: center;
        justify-content: flex-start;
        border-radius: 0;
        padding-inline: 1rem;
        color: var(--sidebar-item-text);
        text-align: left;
    }

    .ops-sidebar-nav ul.menu > li > details > summary::after {
        display: none;
    }

    .ops-sidebar-nav ul.menu > li > a:hover,
    .ops-sidebar-nav ul.menu > li > details > summary:hover {
        background: var(--sidebar-item-hover-bg);
        color: var(--sidebar-item-hover-text);
        box-shadow: inset 3px 0 var(--sidebar-item-current-indicator);
    }

    .ops-sidebar-nav ul.menu > li > a.active {
        background: var(--sidebar-item-current-bg);
        color: var(--sidebar-item-current-text);
        box-shadow: inset 3px 0 var(--sidebar-item-current-indicator);
    }

    .ops-nav-icon {
        display: inline-flex;
        flex: none;
        align-items: center;
        justify-content: center;
    }

    .ops-nav-glyph,
    .ops-nav-chevron {
        width: 1rem;
        height: 1rem;
        flex: none;
        color: inherit;
    }

    .ops-nav-chevron {
        margin-left: auto;
    }

    details[open] > summary .ops-nav-chevron {
        transform: rotate(90deg);
    }

    .ops-sidebar-nav ul.ops-submenu {
        width: 100%;
        margin: 0;
        padding: 0.2rem 0 0.35rem;
    }

    .ops-sidebar-nav ul.ops-submenu::before {
        background: var(--sidebar-child-guide);
    }

    .ops-sidebar-nav ul.ops-submenu > li > a {
        min-height: 2rem;
        padding-left: 3rem;
        color: var(--sidebar-child-text);
        font-size: 0.8125rem;
    }

    .ops-sidebar-nav ul.ops-submenu > li > a:hover {
        background: var(--sidebar-child-hover-bg);
    }

    .ops-sidebar-nav ul.ops-submenu > li > a.active {
        background: var(--sidebar-child-current-bg);
        color: var(--sidebar-item-current-text);
    }

    .ops-sidebar-note {
        border: 1px solid var(--sidebar-footer-border);
        border-radius: 0.6rem;
        background: var(--sidebar-footer-bg);
    }

}

.drawer:not([data-sidebar-ready="true"]) .ops-sidebar {
    transition: none;
}

/* Sidebar rules share daisyUI's utility layer so its menu defaults cannot
   flatten the established expanded/collapsed navigation treatment. */
@layer utilities {
    .dropdown > .ops-user-menu {
        border-color: var(--sidebar-border);
        border-radius: 0;
        background: var(--sidebar-bg);
        box-shadow: none;
        color: var(--sidebar-child-text);
        animation: none;
        transition: none;
    }

    .ops-user-menu.menu > li > a,
    .ops-user-menu.menu > li > form > button {
        display: flex;
        width: 100%;
        min-height: 2.75rem;
        align-items: center;
        gap: 0.7rem;
        border-radius: 0;
        background: transparent;
        box-shadow: inset 0 0 var(--sidebar-item-hover-indicator);
        padding: 0.6rem 0.85rem;
        color: var(--sidebar-child-text);
        font-size: 0.875rem;
        text-align: left;
    }

    .ops-user-menu.menu > li > form {
        display: block;
        width: 100%;
        margin: 0;
        border-radius: 0;
        background: transparent !important;
        padding: 0;
    }

    .ops-user-menu.menu > li > form:hover,
    .ops-user-menu.menu > li > form:focus-within {
        background: transparent !important;
    }

    .ops-user-menu.menu > li.ops-user-logout,
    .ops-user-menu.menu > li.ops-user-logout:hover,
    .ops-user-menu.menu > li.ops-user-logout:focus-within,
    .ops-user-menu.menu > li.ops-user-logout > form,
    .ops-user-menu.menu > li.ops-user-logout > form:hover,
    .ops-user-menu.menu > li.ops-user-logout > form:focus-within,
    .ops-user-menu.menu > li.ops-user-logout > form > button:hover,
    .ops-user-menu.menu > li.ops-user-logout > form > button:focus-visible {
        background: transparent !important;
        background-image: none !important;
    }

    .ops-user-menu.menu > li > a:hover,
    .ops-user-menu.menu > li > a:focus-visible,
    .ops-user-menu.menu > li > form > button:hover,
    .ops-user-menu.menu > li > form > button:focus-visible {
        background: var(--sidebar-item-hover-bg);
        color: var(--sidebar-item-hover-text);
        box-shadow: inset var(--sidebar-item-hover-indicator-width) 0 var(--sidebar-item-hover-indicator);
    }

    .ops-user-menu-icon {
        display: grid;
        width: 1.25rem;
        height: 1.25rem;
        flex: none;
        place-items: center;
        color: var(--sidebar-item-icon);
    }

    .ops-user-menu-icon > svg {
        width: 100%;
        height: 100%;
    }

    .ops-user-menu.menu > li > a:hover .ops-user-menu-icon,
    .ops-user-menu.menu > li > a:focus-visible .ops-user-menu-icon,
    .ops-user-menu.menu > li > form > button:hover .ops-user-menu-icon,
    .ops-user-menu.menu > li > form > button:focus-visible .ops-user-menu-icon {
        color: var(--sidebar-item-hover-icon);
    }

    .drawer-side .ops-sidebar,
    .ops-sidebar-nav {
        background-color: var(--sidebar-bg);
    }

    .ops-sidebar-nav ul.menu {
        display: flex;
        width: 100%;
        flex-flow: column nowrap;
        align-items: stretch;
    }

    .ops-sidebar-nav ul.menu > li {
        display: flex;
        width: 100%;
        max-width: none;
        flex-flow: column nowrap;
        align-self: stretch;
    }

    .ops-sidebar-nav ul.menu > li > details {
        width: 100%;
    }

    .ops-sidebar-nav ul.menu > li > details > summary,
    .ops-sidebar-nav ul.menu > li > a {
        display: flex;
        width: 100%;
        max-width: none;
        cursor: pointer;
        align-items: center;
        justify-content: flex-start;
        color: var(--sidebar-item-text);
        text-align: left;
    }

    .ops-sidebar-nav ul.menu > li > details > summary::after {
        display: none;
    }

    .ops-sidebar-nav ul.menu > li > details > summary:hover,
    .ops-sidebar-nav ul.menu > li > a:hover {
        background: var(--sidebar-item-hover-bg);
        color: var(--sidebar-item-hover-text);
    }

    .ops-sidebar-nav ul.menu > li > details > summary:hover svg,
    .ops-sidebar-nav ul.menu > li > a:hover svg {
        color: var(--sidebar-item-hover-icon);
    }

    .ops-sidebar-nav ul.menu > li > details > summary:active,
    .ops-sidebar-nav ul.menu > li > a:active {
        background: var(--sidebar-item-pressed-bg);
        color: var(--sidebar-item-pressed-text);
    }

    .ops-sidebar-nav ul.menu > li > details > summary:active svg,
    .ops-sidebar-nav ul.menu > li > a:active svg {
        color: var(--sidebar-item-pressed-icon);
    }

    .ops-sidebar-nav ul.menu > li > a.active {
        background: var(--sidebar-item-current-bg);
        color: var(--sidebar-item-current-text);
    }

    .ops-sidebar-nav ul.menu > li > a.active svg {
        color: var(--sidebar-item-current-icon);
    }

    .ops-sidebar-nav ul.ops-submenu {
        width: 100%;
        margin: 0;
        padding: 0.2rem 0 0.35rem;
    }

    .ops-sidebar-nav ul.ops-submenu::before {
        background: var(--sidebar-child-guide);
    }

    .ops-sidebar-nav ul.ops-submenu > li > a {
        min-height: 2rem;
        padding-left: 3rem;
        color: var(--sidebar-child-text);
        font-size: 0.8125rem;
    }

    .ops-sidebar-nav ul.ops-submenu > li > a:hover {
        background: var(--sidebar-child-hover-bg);
        color: var(--sidebar-child-hover-text);
    }

    .ops-sidebar-nav ul.ops-submenu > li > a.active {
        background: var(--sidebar-child-current-bg);
        color: var(--sidebar-child-current-text);
    }

}

.drawer-toggle:not(:checked) ~ .drawer-side,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav,
.drawer-toggle:checked ~ .drawer-side:has(.ops-sidebar) {
    overflow: visible;
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav > div,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav section,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.menu,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.menu > li,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav details {
    width: 100%;
    max-width: 100%;
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav details {
    margin: 0;
    padding: 0;
    overflow: visible;
    background: transparent;
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.menu > li > a,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.menu > li > details > summary {
    display: flex;
    width: 100%;
    min-width: 0;
    max-width: 100%;
    margin: 0;
    justify-content: center;
    gap: 0;
    padding-inline: 0;
    box-sizing: border-box;
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.menu > li > details:hover,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.menu > li > details:focus-within {
    background: transparent;
}

@media (min-width: 1024px) {
    .drawer > .drawer-toggle ~ .drawer-side > .drawer-overlay {
        display: none;
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group {
        position: relative;
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group > .ops-submenu {
        position: absolute;
        z-index: 110;
        top: 0;
        left: calc(100% + 0.45rem);
        display: block;
        width: 14rem;
        margin: 0;
        border: 1px solid var(--sidebar-border);
        border-radius: 0;
        background: var(--sidebar-bg);
        box-shadow: none;
        opacity: 0;
        padding: 0;
        pointer-events: none;
        transform: translateX(-0.35rem) scale(0.98);
        transform-origin: left top;
        transition: opacity 160ms ease, transform 160ms ease;
        visibility: hidden;
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group > .ops-submenu::after {
        position: absolute;
        top: 0;
        right: 100%;
        width: 0.5rem;
        height: 100%;
        content: "";
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group.is-flyout-active > .ops-submenu {
        opacity: 1;
        pointer-events: auto;
        transform: translateX(0) scale(1);
        visibility: visible;
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group.is-flyout-active.is-flyout-preparing > .ops-submenu,
    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group.is-flyout-active.is-flyout-closing > .ops-submenu {
        opacity: 0;
        pointer-events: none;
        transform: translateX(-0.35rem) scale(0.98);
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group[open] > summary[data-tip]::before,
    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group[open] > summary[data-tip]::after {
        display: none;
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.ops-submenu > li > a {
        min-height: 2.25rem;
        padding-inline: 0.85rem;
        box-shadow: inset 0 0 var(--sidebar-item-hover-indicator);
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.ops-submenu > li > a:hover,
    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.ops-submenu > li > a:focus-visible {
        color: var(--sidebar-item-hover-text);
        box-shadow: inset var(--sidebar-item-hover-indicator-width) 0 var(--sidebar-item-hover-indicator);
    }

}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav [data-tip] {
    --tt-bg: var(--sidebar-tooltip-bg);
    overflow: visible;
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav [data-tip]::before {
    color: var(--sidebar-tooltip-text);
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav [data-tip]:hover,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav [data-tip]:focus-visible {
    z-index: 100;
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav [data-tip]::before,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav [data-tip]::after {
    z-index: 101;
}

.ops-sidebar-nav ul.menu a,
.ops-sidebar-nav ul.menu summary {
    border-radius: 0;
}

.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > a,
.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > details > summary {
    box-shadow: inset 0 0 var(--sidebar-item-hover-indicator);
}

.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > a:hover,
.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > details > summary:hover {
    box-shadow: inset var(--sidebar-item-hover-indicator-width) 0 var(--sidebar-item-hover-indicator);
}

.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > a.active {
    box-shadow: inset 3px 0 var(--sidebar-item-current-indicator);
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
    }
}
```
