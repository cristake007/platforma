# Project and shared context

Project-level, configuration, deployment, shared Django, and frontend source files. Generated snapshots under `codex-context/files/` contain the same authoritative-at-generation content.

## `AGENTS.md`

Size: 5.6 KB

````markdown
# Platforma TUVTK — Agent Router

Operating rules for coding agents working in this repository.

Working code only. Minimal context. Verified changes.

## Project

- Server-rendered Django application.
- Stack: Django, PostgreSQL, Tailwind CSS, daisyUI, HTMX, Alpine.js.
- Django templates and PostgreSQL are the source of truth.
- HTMX returns server-rendered partial HTML.
- Alpine.js owns local browser state only.
- Existing scoped custom JavaScript may remain when it is safer or clearer.
- Do not convert the project into a SPA.
- Do not add another frontend framework unless explicitly requested.

## Required reading order

Read only what the task needs:

1. `AGENTS.md`.
2. `coding-standards.md`.
3. `frontend.md` when templates, CSS, JavaScript, HTMX, Alpine, UX, or UI are involved.
4. The deeper `apps/<app>/AGENTS.md` for the target app.
5. The exact source files needed for the requested workflow.
6. Directly referenced imports, includes, templates, forms, services, selectors, or tests only when required.

Do not preload:

- the whole repository;
- all generated `codex-context/` files;
- unrelated apps;
- unrelated tests;
- migration history;
- Docker/deployment files;
- generated/runtime folders.

Use `codex-context/apps/<app>.md` only when source paths are unknown.

Use `codex-file-map.txt` only to locate an unknown file.

Open real source files before editing. Generated context is navigation support, not authority.

## App boundaries

- `platforma_tuvtk/`: settings, root URLs, ASGI, WSGI.
- `core/`: shared shell, navigation, middleware, context processors, shared templates.
- `theme/`: Tailwind/daisyUI theme, global frontend assets.
- `apps/`: domain apps. Each app owns its routes, views, forms, services, selectors, templates, static files, and tests.

Do not duplicate an existing model, service, selector, route, template, include, component pattern, or workflow.

## Coding standards

Detailed coding standards live in `coding-standards.md`.

Default split:

- Views orchestrate HTTP only.
- `forms.py` validates request/form input.
- `services.py` performs writes, transactions, and multi-step workflows.
- `selectors.py` performs permission-filtered reads.
- `validators.py` contains reusable validation rules.
- Templates render state and submit forms; they do not own business rules.
- JavaScript improves interaction only.

Before adding new code, search the target app for an existing form, include, table, action-button, message, service, selector, or validator pattern.

If the same pattern appears twice and is stable, reuse or extract it. If it appears once, keep it explicit.

## Frontend standards

Detailed frontend rules live in `frontend.md`.

Default frontend split:

- Tailwind/daisyUI: layout and components.
- HTMX: server-rendered partial updates, forms, filters, pagination, table/list refreshes.
- Alpine.js: local toggles, dialogs, selected state, loading flags, upload labels.
- Custom JavaScript: complex JSON, downloads, drag/drop, file parsing, canvas/editor workflows.

Use shared semantic theme tokens. Do not introduce app-local color systems.

New business screens should use sharp, professional, enterprise-grade layouts. Avoid childish, oversized, rounded card-heavy screens.

## Commands

Use the repository wrapper. `install.sh` routes ordinary commands through the Python command router.

Linux/Debian:

```bash
./install.sh check
./install.sh test <app-or-test-path>
./install.sh npm run build
./install.sh context --max-file-kb 80
```

Windows:

```powershell
.\install.ps1 check
.\install.ps1 test <app-or-test-path>
.\install.ps1 npm run build
.\install.ps1 context --max-file-kb 80
```

Do not reconstruct raw Docker Compose commands unless the task is Compose-specific.

## Verification

- Prefer the smallest focused test or check.
- Do not run full test suites by default.
- Do not claim tests passed unless you ran them and read the output.
- If verification cannot be run, say why.
- For UI changes, report the manual browser checks still needed.
- For visual work, inspect before/after behavior when tooling allows it.
- Do not weaken tests to make a failure disappear.

## Safety

- Preserve unrelated tracked and untracked changes.
- Never inspect or expose `.env` or `/etc/tuvtk/tuvtk.env` unless explicitly authorized.
- Do not delete database volumes, PostgreSQL data, media, private media, secrets, or environment files.
- Do not run clean, restore, SQL import, database reset, production restart, or destructive commands unless explicitly requested.
- Do not claim HTTPS works; current production Compose/Nginx is HTTP-only.

Avoid generated, runtime, dependency, binary, and local-tool paths unless directly required:

- `.tuvtk/`
- `.venv/`
- `.git/`
- `.postgresql/`
- `node_modules/`
- `staticfiles/`
- `media/`
- `private_media/`
- `.playwright-mcp/`
- `test-results/`
- `playwright-report/`
- `theme/static/css/dist/`
- `theme/static/fonts/`
- `theme/static/images/`

## Stop conditions

Stop and ask before expanding scope when:

- the named file is missing;
- another app must be changed but was not listed;
- a schema migration is needed but not requested;
- a workflow would require a broad rewrite;
- validation would require destructive commands or full test suites;
- two attempted fixes fail for the same issue.

## Completion report

Always report:

- files changed;
- behavior changed;
- migrations created, if any;
- checks run;
- checks skipped and why;
- context regeneration status;
- manual checks still needed.
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
FROM node:24-bookworm-slim AS frontend

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

Size: 23.8 KB

Redacted secret-like assignments: 1

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

if [[ "${TUVTK_LEGACY_INSTALL:-false}" != true ]]; then
    legacy_action=false
    for argument in "$@"; do
        case "$argument" in
            --dev|--production|--environment|--command|--clean) legacy_action=true ;;
        esac
    done
    if [[ "$legacy_action" != true ]]; then
        case "${OSTYPE:-}" in
            msys*|mingw*|cygwin*)
                exec powershell.exe -NoProfile -ExecutionPolicy Bypass \
                    -File "$(cygpath -w "$SCRIPT_DIR/install.ps1")" "$@"
                ;;
        esac
        if command -v python3 >/dev/null 2>&1; then
            exec python3 "$SCRIPT_DIR/scripts/tuvtk_cli.py" "$@"
        elif command -v python >/dev/null 2>&1; then
            exec python "$SCRIPT_DIR/scripts/tuvtk_cli.py" "$@"
        fi
        if command -v apt-get >/dev/null 2>&1; then
            printf '[tuvtk] Installing Python 3 for the command router.\n'
            if [[ "$EUID" -eq 0 ]]; then
                apt-get update
                apt-get install --yes python3
            elif command -v sudo >/dev/null 2>&1; then
                sudo apt-get update
                sudo apt-get install --yes python3
            else
                printf '[tuvtk] ERROR: sudo is required to install Python 3.\n' >&2
                exit 1
            fi
            exec python3 "$SCRIPT_DIR/scripts/tuvtk_cli.py" "$@"
        fi
        printf '[tuvtk] ERROR: Python 3 is required and no supported package manager was found.\n' >&2
        exit 1
    fi
fi

readonly DEFAULT_PROD_ENV_FILE="/etc/tuvtk/tuvtk.env"
readonly DEFAULT_PROJECT_NAME="tuvtk"
readonly DEFAULT_DATA_DIR="/var/lib/tuvtk"
readonly DEFAULT_BACKUP_PATH="/opt/tuvtk-backups"
readonly SYSTEM_COMMAND_PATH="/usr/local/bin/tuvtk"
readonly POSTGRES_IMAGE="postgres:17-bookworm"

APP_DIR="$SCRIPT_DIR"
ENV_FILE=""
ENV_FILE_EXPLICIT=false
PROD_ENV_FILE="$DEFAULT_PROD_ENV_FILE"
DEV_ENV_FILE=""
COMPOSE_FILE=""
DEV_COMPOSE_FILE=""
PROJECT_NAME="$DEFAULT_PROJECT_NAME"
DATA_DIR="$DEFAULT_DATA_DIR"
BACKUP_PATH="$DEFAULT_BACKUP_PATH"
DEFAULT_MODE=""
DEV_PORT="8000"
DOMAIN=""
HTTP_PORT="80"
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
SECRET_KEY=<redacted>
ACTION=""
YES=false
DRY_RUN=false
SSL=false
LETSENCRYPT=false
OWN_CERTIFICATE=false

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
Usage: install.sh ACTION [OPTIONS]

Actions:
  --dev                      Prepare development config and install command.sh
  --production               Prepare production config and install command.sh
  --environment              Install/verify server prerequisites only
  --command                  Update command.sh and /usr/local/bin/tuvtk only
  --clean                    Remove safe generated caches only; never data/media

General options:
  -h, --help                 Show this help
  -y, --yes                  Skip ordinary confirmation prompts
  --dry-run                  Validate and print planned actions without changes
  --app-dir=PATH             Application checkout (default: directory containing install.sh)
  --env-file=PATH            Active mode environment path
  --project-name=NAME        Compose project name (default: tuvtk)
  --backup-path=PATH         Default backup directory (default: /opt/tuvtk-backups)
  --dev-port=PORT            Published development port (default: 8000)
  --default-mode=dev|prod    Mode embedded by --command (existing mode is preferred)

Production options:
  --domain=HOST              Required production domain or IPv4 address
  --http-port=PORT           Production HTTP port (default: 80)
  --data-dir=PATH            Production bind-mount root (default: /var/lib/tuvtk)
  --db-name=NAME
  --db-user=USER
  --db-password=PASSWORD
  --secret-key=KEY

Compatibility options:
  --install-dir=PATH         Alias for --app-dir
  --public-host=HOST         Alias for --domain
  --ssl --letsencrypt       Refused: current deployment is HTTP-only
  --ssl --owncertificate    Refused: current deployment is HTTP-only

Examples:
  sudo bash install.sh --dev --yes
  sudo bash install.sh --production --yes --domain=example.com
  sudo bash install.sh --environment
  sudo bash install.sh --command
  sudo bash install.sh --clean
  sudo bash install.sh --dev --yes --app-dir="$(pwd)" --dev-port=8001 --dry-run

The installer prepares configuration and command launchers. It does not start,
stop, build, migrate, restore, or reset an application stack.
EOF
}

require_option_value() {
    local option="$1" value="${2:-}"
    [[ -n "$value" && "$value" != --* ]] || fail "$option requires a value."
}

set_action() {
    local requested="$1"
    [[ -z "$ACTION" || "$ACTION" == "$requested" ]] \
        || fail "installer actions --$ACTION and --$requested cannot be combined."
    ACTION="$requested"
}

parse_arguments() {
    while (($#)); do
        case "$1" in
            -h|--help) set_action help; shift ;;
            -y|--yes) YES=true; shift ;;
            --dry-run) DRY_RUN=true; shift ;;
            --dev) set_action dev; DEFAULT_MODE=dev; shift ;;
            --production) set_action production; DEFAULT_MODE=prod; shift ;;
            --environment) set_action environment; shift ;;
            --command) set_action command; shift ;;
            --clean) set_action clean; shift ;;
            --app-dir=*|--install-dir=*) APP_DIR="${1#*=}"; shift ;;
            --app-dir|--install-dir) require_option_value "$1" "${2:-}"; APP_DIR="$2"; shift 2 ;;
            --env-file=*) ENV_FILE="${1#*=}"; ENV_FILE_EXPLICIT=true; shift ;;
            --env-file) require_option_value "$1" "${2:-}"; ENV_FILE="$2"; ENV_FILE_EXPLICIT=true; shift 2 ;;
            --project-name=*) PROJECT_NAME="${1#*=}"; shift ;;
            --project-name) require_option_value "$1" "${2:-}"; PROJECT_NAME="$2"; shift 2 ;;
            --backup-path=*) BACKUP_PATH="${1#*=}"; shift ;;
            --backup-path) require_option_value "$1" "${2:-}"; BACKUP_PATH="$2"; shift 2 ;;
            --data-dir=*) DATA_DIR="${1#*=}"; shift ;;
            --data-dir) require_option_value "$1" "${2:-}"; DATA_DIR="$2"; shift 2 ;;
            --dev-port=*) DEV_PORT="${1#*=}"; shift ;;
            --dev-port) require_option_value "$1" "${2:-}"; DEV_PORT="$2"; shift 2 ;;
            --default-mode=*) DEFAULT_MODE="${1#*=}"; shift ;;
            --default-mode) require_option_value "$1" "${2:-}"; DEFAULT_MODE="$2"; shift 2 ;;
            --domain=*|--public-host=*) DOMAIN="${1#*=}"; shift ;;
            --domain|--public-host) require_option_value "$1" "${2:-}"; DOMAIN="$2"; shift 2 ;;
            --http-port=*) HTTP_PORT="${1#*=}"; shift ;;
            --http-port) require_option_value "$1" "${2:-}"; HTTP_PORT="$2"; shift 2 ;;
            --db-name=*) DB_NAME="${1#*=}"; shift ;;
            --db-name) require_option_value "$1" "${2:-}"; DB_NAME="$2"; shift 2 ;;
            --db-user=*) DB_USER="${1#*=}"; shift ;;
            --db-user) require_option_value "$1" "${2:-}"; DB_USER="$2"; shift 2 ;;
            --db-password=*) DB_PASSWORD="${1#*=}"; shift ;;
            --db-password) require_option_value "$1" "${2:-}"; DB_PASSWORD="$2"; shift 2 ;;
            --secret-key=*) SECRET_KEY="${1#*=}"; shift ;;
            --secret-key) require_option_value "$1" "${2:-}"; SECRET_KEY="$2"; shift 2 ;;
            --ssl) SSL=true; shift ;;
            --letsencrypt) LETSENCRYPT=true; shift ;;
            --owncertificate) OWN_CERTIFICATE=true; shift ;;
            *) fail "unknown argument: $1" ;;
        esac
    done
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

read_installed_mode() {
    local file="$APP_DIR/command.sh"
    [[ -f "$file" ]] || return 0
    sed -n 's/^export TUVTK_DEFAULT_MODE=\(dev\|prod\)$/\1/p' "$file" | head -n 1
}

resolve_paths_and_mode() {
    COMPOSE_FILE="$APP_DIR/compose.yaml"
    DEV_COMPOSE_FILE="$APP_DIR/compose.dev.yaml"
    DEV_ENV_FILE="$APP_DIR/.env.dev"

    if [[ "$ACTION" == command && -z "$DEFAULT_MODE" ]]; then
        DEFAULT_MODE="$(read_installed_mode)"
    fi
    if [[ -z "$DEFAULT_MODE" ]]; then
        DEFAULT_MODE=prod
    fi
    case "$DEFAULT_MODE" in dev|prod) ;; *) fail "--default-mode must be dev or prod." ;; esac

    if [[ "$ENV_FILE_EXPLICIT" == true ]]; then
        if [[ "$DEFAULT_MODE" == dev ]]; then DEV_ENV_FILE="$ENV_FILE"; else PROD_ENV_FILE="$ENV_FILE"; fi
    fi
    if [[ "$DEFAULT_MODE" == dev ]]; then
        ENV_FILE="$DEV_ENV_FILE"
    else
        ENV_FILE="$PROD_ENV_FILE"
    fi
}

validate_absolute_path() {
    local label="$1" path="$2"
    [[ "$path" == /* && "$path" != "/" ]] || fail "$label must be an absolute path other than /."
    [[ "$path" != *$'\n'* && "$path" != *$'\r'* ]] || fail "$label contains a newline."
}

validate_domain() {
    [[ -n "$DOMAIN" ]] || fail "--production requires --domain (or --public-host)."
    [[ ${#DOMAIN} -le 253 ]] || fail "domain/public host is too long."
    [[ "$DOMAIN" =~ ^[A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?$ && "$DOMAIN" != *".."* ]] \
        || fail "invalid domain or IPv4 address: $DOMAIN"
}

validate_options() {
    [[ -n "$ACTION" ]] || fail "choose one action: --dev, --production, --environment, --command, or --clean."
    [[ "$ACTION" == help ]] && return 0
    validate_absolute_path "application directory" "$APP_DIR"
    validate_absolute_path "production environment file" "$PROD_ENV_FILE"
    validate_absolute_path "development environment file" "$DEV_ENV_FILE"
    validate_absolute_path "backup path" "$BACKUP_PATH"
    validate_absolute_path "production data directory" "$DATA_DIR"
    [[ "$PROJECT_NAME" =~ ^[A-Za-z0-9][A-Za-z0-9_.-]*$ ]] || fail "invalid project name: $PROJECT_NAME"
    [[ "$DEV_PORT" =~ ^[0-9]+$ && "$DEV_PORT" -ge 1 && "$DEV_PORT" -le 65535 ]] || fail "invalid development port: $DEV_PORT"
    [[ "$HTTP_PORT" =~ ^[0-9]+$ && "$HTTP_PORT" -ge 1 && "$HTTP_PORT" -le 65535 ]] || fail "invalid HTTP port: $HTTP_PORT"
    [[ "$DATA_DIR" != "$APP_DIR" && "$DATA_DIR" != "$APP_DIR/"* && "$APP_DIR" != "$DATA_DIR/"* ]] \
        || fail "application and production data directories must not overlap."
    case "$(readlink -m -- "$DATA_DIR")" in
        /bin|/boot|/dev|/etc|/home|/lib|/lib64|/media|/mnt|/opt|/proc|/root|/run|/sbin|/srv|/sys|/tmp|/usr|/var|/var/lib)
            fail "production data directory is too broad or system-critical: $DATA_DIR"
            ;;
    esac
    if [[ -n "$DB_NAME" ]]; then
        [[ "$DB_NAME" =~ ^[A-Za-z_][A-Za-z0-9_.-]*$ ]] || fail "invalid database name."
    fi
    if [[ -n "$DB_USER" ]]; then
        [[ "$DB_USER" =~ ^[A-Za-z_][A-Za-z0-9_.-]*$ ]] || fail "invalid database user."
    fi
    if [[ "$SSL" == true || "$LETSENCRYPT" == true || "$OWN_CERTIFICATE" == true ]]; then
        fail "SSL was requested, but current Compose/Nginx is HTTP-only. No changes were made."
    fi
    if [[ "$ACTION" == production ]]; then validate_domain; fi
    if [[ "$ACTION" == dev || "$ACTION" == production || "$ACTION" == command ]]; then
        [[ -f "$APP_DIR/bin/tuvtk" && -f "$COMPOSE_FILE" ]] \
            || fail "application checkout is missing bin/tuvtk or compose.yaml: $APP_DIR"
    fi
    if [[ "$ACTION" == dev ]]; then
        [[ -f "$DEV_COMPOSE_FILE" && -f "$APP_DIR/.env.example" ]] \
            || fail "development install requires compose.dev.yaml and .env.example."
    fi
}

require_root() {
    [[ "$EUID" -eq 0 ]] || fail "this action requires root; run it through sudo."
}

load_supported_os() {
    [[ -r /etc/os-release ]] || fail "/etc/os-release is missing; Debian or Ubuntu is required."
    # shellcheck disable=SC1091
    . /etc/os-release
    case "${ID:-}" in debian|ubuntu) ;; *) fail "unsupported distribution '${ID:-unknown}'; Debian or Ubuntu is required." ;; esac
    command -v dpkg >/dev/null 2>&1 || fail "dpkg is required."
    case "$(dpkg --print-architecture)" in amd64|arm64) ;; *) fail "only amd64 and arm64 are supported." ;; esac
}

configure_docker_repository() {
    local docker_distribution="$ID" docker_codename="${VERSION_CODENAME:-}"
    if [[ "$ID" == ubuntu && -n "${UBUNTU_CODENAME:-}" ]]; then docker_codename="$UBUNTU_CODENAME"; fi
    [[ -n "$docker_codename" ]] || fail "could not determine distribution codename."
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
    apt-get install --yes ca-certificates curl git openssh-client openssl iproute2 python3
    if ! command -v docker >/dev/null 2>&1; then
        configure_docker_repository
        apt-get update
        apt-get install --yes docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    elif ! docker compose version >/dev/null 2>&1; then
        configure_docker_repository
        apt-get update
        apt-get install --yes docker-compose-plugin
    fi
    if command -v systemctl >/dev/null 2>&1; then systemctl enable --now docker; fi
    docker info >/dev/null 2>&1 || fail "Docker daemon is unavailable."
    docker compose version >/dev/null 2>&1 || fail "Docker Compose plugin is unavailable."
}

set_env_value() {
    local file="$1" key="$2" value="$3" temporary
    [[ "$value" != *$'\n'* && "$value" != *$'\r'* ]] || fail "environment value for $key contains a newline."
    temporary="$(mktemp "${file}.tmp.XXXXXX")"
    awk -v key="$key" '$0 ~ "^[[:space:]]*" key "=" { next } { print }' "$file" >"$temporary"
    printf '%s=%s\n' "$key" "$value" >>"$temporary"
    chmod 0600 "$temporary"
    mv -f -- "$temporary" "$file"
}

ensure_env_value() {
    local file="$1" key="$2" value="$3"
    [[ -n "$(read_env_value_from "$file" "$key")" ]] || set_env_value "$file" "$key" "$value"
}

backup_environment() {
    local file="$1" backup
    [[ -f "$file" ]] || return 0
    install -d -m 0700 "$BACKUP_PATH"
    backup="$BACKUP_PATH/$(basename "$file").$(date -u +%Y-%m-%d_%H%M%S).bak"
    cp -p -- "$file" "$backup"
    chmod 0600 "$backup"
    log "Environment backed up: $backup"
}

prepare_dev_environment() {
    if [[ ! -f "$DEV_ENV_FILE" ]]; then
        install -m 0600 "$APP_DIR/.env.example" "$DEV_ENV_FILE"
        log "Created development environment from .env.example: $DEV_ENV_FILE"
    else
        chmod 0600 "$DEV_ENV_FILE"
    fi
    ensure_env_value "$DEV_ENV_FILE" TUVTK_DATA_DIR "/var/lib/${PROJECT_NAME}-dev"
    ensure_env_value "$DEV_ENV_FILE" TUVTK_IMAGE_TAG local
    ensure_env_value "$DEV_ENV_FILE" TUVTK_PUBLIC_HOST localhost
    set_env_value "$DEV_ENV_FILE" TUVTK_HTTP_PORT "$DEV_PORT"
    ensure_env_value "$DEV_ENV_FILE" POSTGRES_DB platforma_tuvtk
    ensure_env_value "$DEV_ENV_FILE" POSTGRES_USER postgres
    ensure_env_value "$DEV_ENV_FILE" POSTGRES_PASSWORD "$(openssl rand -hex 32)"
    ensure_env_value "$DEV_ENV_FILE" DJANGO_SECRET_KEY "$(openssl rand -hex 48)"
    ensure_env_value "$DEV_ENV_FILE" DJANGO_ALLOWED_HOSTS "127.0.0.1,localhost,[::1]"
    set_env_value "$DEV_ENV_FILE" DJANGO_CSRF_TRUSTED_ORIGINS "http://127.0.0.1:${DEV_PORT},http://localhost:${DEV_PORT}"
    chmod 0600 "$DEV_ENV_FILE"
    if [[ -n "${SUDO_UID:-}" && -n "${SUDO_GID:-}" ]]; then
        chown "$SUDO_UID:$SUDO_GID" "$DEV_ENV_FILE"
    fi
}

prepare_prod_environment() {
    local csrf_origin="http://$DOMAIN"
    if [[ "$HTTP_PORT" != 80 ]]; then csrf_origin="${csrf_origin}:$HTTP_PORT"; fi
    install -d -m 0700 "$(dirname "$PROD_ENV_FILE")"
    if [[ -f "$PROD_ENV_FILE" ]]; then
        backup_environment "$PROD_ENV_FILE"
    else
        umask 077
        : >"$PROD_ENV_FILE"
    fi
    ensure_env_value "$PROD_ENV_FILE" TUVTK_IMAGE_TAG local
    set_env_value "$PROD_ENV_FILE" TUVTK_DATA_DIR "$DATA_DIR"
    set_env_value "$PROD_ENV_FILE" TUVTK_PUBLIC_HOST "$DOMAIN"
    set_env_value "$PROD_ENV_FILE" TUVTK_HTTP_PORT "$HTTP_PORT"
    ensure_env_value "$PROD_ENV_FILE" NGINX_PROXY_TIMEOUT 900s
    if [[ -n "$SECRET_KEY" ]]; then set_env_value "$PROD_ENV_FILE" DJANGO_SECRET_KEY "$SECRET_KEY"; else ensure_env_value "$PROD_ENV_FILE" DJANGO_SECRET_KEY "$(openssl rand -hex 48)"; fi
    set_env_value "$PROD_ENV_FILE" DJANGO_DEPLOYMENT_MODE container
    set_env_value "$PROD_ENV_FILE" DJANGO_DEBUG false
    set_env_value "$PROD_ENV_FILE" DJANGO_ALLOWED_HOSTS "$DOMAIN"
    set_env_value "$PROD_ENV_FILE" DJANGO_CSRF_TRUSTED_ORIGINS "$csrf_origin"
    set_env_value "$PROD_ENV_FILE" DJANGO_TRUST_PROXY_HEADERS true
    set_env_value "$PROD_ENV_FILE" DJANGO_USE_X_FORWARDED_HOST true
    set_env_value "$PROD_ENV_FILE" DJANGO_SECURE_SSL_REDIRECT false
    set_env_value "$PROD_ENV_FILE" DJANGO_SESSION_COOKIE_SECURE false
    set_env_value "$PROD_ENV_FILE" DJANGO_CSRF_COOKIE_SECURE false
    if [[ -n "$DB_NAME" ]]; then set_env_value "$PROD_ENV_FILE" POSTGRES_DB "$DB_NAME"; else ensure_env_value "$PROD_ENV_FILE" POSTGRES_DB platforma_tuvtk; fi
    if [[ -n "$DB_USER" ]]; then set_env_value "$PROD_ENV_FILE" POSTGRES_USER "$DB_USER"; else ensure_env_value "$PROD_ENV_FILE" POSTGRES_USER tuvtk; fi
    if [[ -n "$DB_PASSWORD" ]]; then set_env_value "$PROD_ENV_FILE" POSTGRES_PASSWORD "$DB_PASSWORD"; else ensure_env_value "$PROD_ENV_FILE" POSTGRES_PASSWORD "$(openssl rand -hex 32)"; fi
    set_env_value "$PROD_ENV_FILE" POSTGRES_HOST db
    set_env_value "$PROD_ENV_FILE" POSTGRES_PORT 5432
    ensure_env_value "$PROD_ENV_FILE" POSTGRES_CONN_MAX_AGE 60
    ensure_env_value "$PROD_ENV_FILE" POSTGRES_CONN_HEALTH_CHECKS true
    ensure_env_value "$PROD_ENV_FILE" GUNICORN_WORKERS 2
    ensure_env_value "$PROD_ENV_FILE" GUNICORN_TIMEOUT 900
    chmod 0600 "$PROD_ENV_FILE"
}

prepare_data_directories() {
    docker pull "$POSTGRES_IMAGE" >/dev/null
    local postgres_uid postgres_gid
    postgres_uid="$(docker run --rm --entrypoint sh "$POSTGRES_IMAGE" -c 'id -u postgres')"
    postgres_gid="$(docker run --rm --entrypoint sh "$POSTGRES_IMAGE" -c 'id -g postgres')"
    install -d -m 0750 -o "$postgres_uid" -g "$postgres_gid" "$DATA_DIR/postgres"
    install -d -m 0755 -o 10001 -g 10001 "$DATA_DIR/media" "$DATA_DIR/static"
    install -d -m 0750 -o 10001 -g 10001 "$DATA_DIR/private-media"
}

write_command_launchers() {
    local command_path="$APP_DIR/command.sh" command_tmp global_tmp
    command_tmp="$(mktemp "${TMPDIR:-/tmp}/tuvtk-command.XXXXXX")"
    {
        printf '#!/usr/bin/env bash\nset -Eeuo pipefail\n'
        printf 'export TUVTK_APP_DIR=%q\n' "$APP_DIR"
        printf 'export TUVTK_ENV_FILE=%q\n' "$ENV_FILE"
        printf 'export TUVTK_PROD_ENV_FILE=%q\n' "$PROD_ENV_FILE"
        printf 'export TUVTK_DEV_ENV_FILE=%q\n' "$DEV_ENV_FILE"
        printf 'export TUVTK_COMPOSE_FILE=%q\n' "$COMPOSE_FILE"
        printf 'export TUVTK_DEV_COMPOSE_FILE=%q\n' "$DEV_COMPOSE_FILE"
        printf 'export TUVTK_PROJECT_NAME=%q\n' "$PROJECT_NAME"
        printf 'export TUVTK_DEFAULT_MODE=%q\n' "$DEFAULT_MODE"
        printf 'export TUVTK_DEV_PORT=%q\n' "$DEV_PORT"
        printf 'export TUVTK_BACKUP_DIR=%q\n' "$BACKUP_PATH"
        printf 'exec %q "$@"\n' "$APP_DIR/bin/tuvtk"
    } >"$command_tmp"
    install -m 0755 "$command_tmp" "${command_path}.tmp.$$"
    mv -f -- "${command_path}.tmp.$$" "$command_path"
    rm -f -- "$command_tmp"

    global_tmp="$(mktemp "${TMPDIR:-/tmp}/tuvtk-global.XXXXXX")"
    {
        printf '#!/usr/bin/env bash\nset -Eeuo pipefail\n'
        printf 'exec %q "$@"\n' "$command_path"
    } >"$global_tmp"
    install -m 0755 "$global_tmp" "${SYSTEM_COMMAND_PATH}.tmp.$$"
    mv -f -- "${SYSTEM_COMMAND_PATH}.tmp.$$" "$SYSTEM_COMMAND_PATH"
    rm -f -- "$global_tmp"
    chmod 0755 "$APP_DIR/bin/tuvtk"
}

maybe_write_command_launchers() {
    if [[ "${TUVTK_SKIP_COMMAND:-false}" == true ]]; then
        log "Skipped legacy command.sh generation; install.sh remains the command entry point."
        return 0
    fi
    write_command_launchers
}

confirm_clean() {
    [[ "$YES" == true ]] && return 0
    [[ -t 0 ]] || fail "--clean requires interactive confirmation or --yes."
    local answer
    printf 'Remove only generated caches under %s? [y/N] ' "$APP_DIR"
    read -r answer
    [[ "$answer" == y || "$answer" == Y || "$answer" == yes || "$answer" == YES ]] || fail "clean cancelled."
}

confirm_install() {
    [[ "$YES" == true ]] && return 0
    [[ -t 0 ]] || fail "confirmation is required; rerun interactively or pass --yes."
    local answer
    printf 'Prepare TUVTK %s mode in %s without starting services? [y/N] ' "$ACTION" "$APP_DIR"
    read -r answer
    [[ "$answer" == y || "$answer" == Y || "$answer" == yes || "$answer" == YES ]] \
        || fail "installation cancelled."
}

print_dry_run() {
    cat <<EOF
[tuvtk] Dry run; no files, packages, or services will be changed.
[tuvtk] Action: $ACTION
[tuvtk] Application: $APP_DIR
[tuvtk] Default mode: $DEFAULT_MODE
[tuvtk] Production environment: $PROD_ENV_FILE
[tuvtk] Development environment: $DEV_ENV_FILE
[tuvtk] Installed command: $APP_DIR/command.sh
[tuvtk] Global shortcut: $SYSTEM_COMMAND_PATH
EOF
    case "$ACTION" in
        dev) log "Would install prerequisites, create/update missing dev config, and install launchers. No stack would start." ;;
        production) log "Would install prerequisites, prepare production config/data directories, and install launchers. No stack would start." ;;
        environment) log "Would install or verify Debian/Ubuntu, Docker Engine, and Docker Compose prerequisites only." ;;
        command) log "Would update command launchers only." ;;
        clean) log "Would remove safe generated caches only; database, media, env, source, and .git would remain." ;;
    esac
}

print_summary() {
    if [[ "${TUVTK_SKIP_COMMAND:-false}" == true ]]; then
        cat <<EOF

TUVTK $ACTION preparation completed.

Application:  $APP_DIR
Default mode: $DEFAULT_MODE
Environment:  $ENV_FILE

No application stack was started.
Next command: $APP_DIR/install.sh $([[ "$DEFAULT_MODE" == dev ]] && printf dev || printf start)
EOF
        return 0
    fi
    cat <<EOF

TUVTK $ACTION preparation completed.

Application:      $APP_DIR
Default mode:     $DEFAULT_MODE
Environment:      $ENV_FILE
Installed command: $APP_DIR/command.sh
Global shortcut:   $SYSTEM_COMMAND_PATH -> $APP_DIR/command.sh

No application stack was started.
Next command: sudo $APP_DIR/command.sh $([[ "$DEFAULT_MODE" == dev ]] && printf dev || printf start)
EOF
}

run_action() {
    if [[ "$DRY_RUN" == true ]]; then print_dry_run; return 0; fi
    require_root
    case "$ACTION" in
        environment)
            install_prerequisites
            log "Server prerequisites are ready. No application files or services were changed."
            ;;
        command)
            write_command_launchers
            print_summary
            ;;
        dev)
            confirm_install
            install_prerequisites
            prepare_dev_environment
            maybe_write_command_launchers
            print_summary
            ;;
        production)
            confirm_install
            install_prerequisites
            prepare_prod_environment
            prepare_data_directories
            maybe_write_command_launchers
            print_summary
            ;;
        clean)
            confirm_clean
            TUVTK_APP_DIR="$APP_DIR" "$APP_DIR/bin/tuvtk" clean
            log "Database, media, static data, environments, application source, and .git were not deleted."
            ;;
        *) fail "internal error: unsupported action $ACTION" ;;
    esac
}

main() {
    parse_arguments "$@"
    if [[ "$ACTION" == help ]]; then usage; return 0; fi
    resolve_paths_and_mode
    validate_options
    run_action
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

Size: 4.3 KB

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

Size: 167 B

```text
*.sh text eol=lf
Dockerfile text eol=lf
*.yaml text eol=lf
*.template text eol=lf
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf
*.py text eol=lf
```

## `.github/agents/codex.agent.md`

Size: 570 B

```markdown
---
name: codex
description: Describe what this custom agent does and when to use it.
argument-hint: The inputs this agent expects, e.g., "a task to implement" or "a question to answer".
# tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo'] # specify the tools this agent can use. If not set, all enabled tools are allowed.
---

<!-- Tip: Use /create-agent in chat to generate content with agent assistance -->

Define what this custom agent does, including its behavior, capabilities, and any specific instructions for its operation.
```

## `.github/workflows/ci.yml`

Size: 2.7 KB

Redacted secret-like assignments: 3

```yaml
name: CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  checks:
    name: Django checks and tests
    if: >-
      github.event_name == 'workflow_dispatch' ||
      (github.event_name == 'push' && contains(github.event.head_commit.message, '[run-ci]')) ||
      (github.event_name == 'pull_request' && contains(format('{0} {1}', github.event.pull_request.title, github.event.pull_request.body), '[run-ci]'))
    runs-on: ubuntu-latest
    timeout-minutes: 20

    services:
      postgres:
        image: postgres:17-bookworm
        env:
          POSTGRES_DB: platforma_tuvtk
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: <redacted>
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U postgres -d platforma_tuvtk"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 20

    env:
      DJANGO_DEPLOYMENT_MODE: development
      DJANGO_DEBUG: "true"
      DJANGO_SECRET_KEY: <redacted>
      DJANGO_ALLOWED_HOSTS: 127.0.0.1,localhost,testserver
      POSTGRES_DB: platforma_tuvtk
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: <redacted>
      POSTGRES_HOST: 127.0.0.1
      POSTGRES_PORT: "5432"
      POSTGRES_CONN_MAX_AGE: "0"
      POSTGRES_CONN_HEALTH_CHECKS: "true"
      NPM_BIN_PATH: npm

    steps:
      - name: Check out repository
        uses: actions/checkout@v5

      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: |
            requirements.txt
            requirements-dev.txt
            requirements-deploy.txt

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements-dev.txt

      - name: Set up Node.js
        uses: actions/setup-node@v5
        with:
          node-version: "24"
          cache: npm
          cache-dependency-path: theme/static_src/package-lock.json

      - name: Install frontend dependencies
        run: npm --prefix theme/static_src ci

      - name: Build frontend assets
        run: npm --prefix theme/static_src run build

      - name: Check Django configuration
        run: python manage.py check

      - name: Check for missing migrations
        run: python manage.py makemigrations --check --dry-run

      - name: Run tests
        run: python manage.py test --verbosity 2
```

## `.gitignore`

Size: 320 B

```text
# Editor and local environment
.vscode/
.venv/
.tuvtk/

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
.env.dev
command.sh
.postgresql/
media/
private_media/
staticfiles/
theme/static/css/dist/
theme/static/js/vendor/
repomix-output.*
```

## `.tuvtk/config.json`

Size: 84 B

```json
{
  "backend": "windows-native",
  "default_mode": "dev",
  "dev_port": 8027
}
```

## `activate_venv.bat`

Size: 358 B

```batch
@echo off
setlocal
set "ROOT=%~dp0"
if not exist "%ROOT%.venv\Scripts\Activate.ps1" (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ROOT%install.ps1" setup dev
    if errorlevel 1 exit /b %ERRORLEVEL%
)
powershell.exe -NoExit -ExecutionPolicy Bypass -Command "Set-Location -LiteralPath '%ROOT%'; & '%ROOT%.venv\Scripts\Activate.ps1'"
```

## `apps/__init__.py`

Size: 0 B

```python
```

## `bin/tuvtk`

Size: 32.0 KB

```text
#!/usr/bin/env bash
set -Eeuo pipefail

readonly APP_DIR="${TUVTK_APP_DIR:-/opt/tuvtk}"
readonly COMPOSE_FILE="${TUVTK_COMPOSE_FILE:-$APP_DIR/compose.yaml}"
readonly DEV_COMPOSE_FILE="${TUVTK_DEV_COMPOSE_FILE:-$APP_DIR/compose.dev.yaml}"
readonly PROJECT_NAME="${TUVTK_PROJECT_NAME:-tuvtk}"
readonly DEFAULT_MODE="${TUVTK_DEFAULT_MODE:-prod}"
readonly DEV_PORT="${TUVTK_DEV_PORT:-8000}"
readonly PROD_ENV_FILE="${TUVTK_PROD_ENV_FILE:-${TUVTK_ENV_FILE:-/etc/tuvtk/tuvtk.env}}"
readonly DEV_ENV_FILE="${TUVTK_DEV_ENV_FILE:-$APP_DIR/.env.dev}"
readonly DEFAULT_BACKUP_DIR="${TUVTK_BACKUP_DIR:-/opt/tuvtk-backups}"
readonly DB_SERVICE="db"
readonly WEB_SERVICE="web"
readonly BACKUP_FORMAT="tuvtk-backup-v2"

DOCKER_COMMAND=()

fail() {
    printf 'tuvtk: ERROR: %s\n' "$*" >&2
    exit 1
}

warn() {
    printf 'tuvtk: WARNING: %s\n' "$*" >&2
}

usage() {
    cat <<EOF
Usage: ./install.sh COMMAND [ARGS...]

Default mode: $DEFAULT_MODE

Default-mode lifecycle:
  status, ps                     Show service status
  start, up                      Start the configured default stack
  stop, down                     Stop the configured default stack
  restart                        Restart the configured default stack
  build                          Build and start the configured default stack
  rebuild                        Rebuild without cache and start the default stack
  logs [SERVICE]                 Follow logs

Explicit production lifecycle:
  prod-status                    Show production status
  prod-start                     Start production
  prod-stop                      Stop production
  prod-restart                   Restart production
  prod-build                     Build and start production
  prod-rebuild                   Rebuild production without cache and start it
  prod-logs [SERVICE]            Follow production logs

Development:
  dev, dev-start                 Start isolated db, Django, and Tailwind
  dev-build                      Build and start development
  dev-stop                       Stop development without deleting volumes
  dev-status                     Show development status
  dev-logs [SERVICE]             Follow development logs
  tailwind                       Start and follow the Tailwind watcher
  npm COMMAND...                 Run npm in the development Node service

Django (uses the default mode):
  check                          Run Django system checks
  test [TARGET] [ARGS...]        Run tests; defaults to verbosity 0
  migrate [ARGS...]              Apply migrations
  makemigrations [APP] [ARGS...] Create migrations
  collectstatic                  Collect static files non-interactively
  shell, dbshell                 Open a Django or database shell
  django COMMAND [ARGS...]       Run any manage.py command
  exec SERVICE COMMAND [ARGS...] Run a command in a default-mode service
  prod-django COMMAND [ARGS...]  Run manage.py in production
  dev-django COMMAND [ARGS...]   Run manage.py in development

Backup, restore, and SQL:
  backup DIRECTORY               Back up the default mode
  restore ARCHIVE [--yes]        Restore the default mode
  export-sql PATH                Export default-mode PostgreSQL
  import-sql FILE [--yes]        Replace the default-mode database from SQL
  prod-backup DIRECTORY          Back up production
  prod-restore ARCHIVE [--yes]   Restore production
  prod-export-sql PATH           Export production SQL
  prod-import-sql FILE [--yes]   Replace production from SQL
  dev-backup DIRECTORY           Back up development
  dev-restore ARCHIVE [--yes]    Restore development
  dev-export-sql PATH            Export development SQL
  dev-import-sql FILE [--yes]    Replace development from SQL

Database reset:
  fresh-db [--yes] [--start]     Reset the development database only
  dev-db-reset [--yes] [--start] Same as fresh-db
  prod-db-reset --yes-i-understand-this-deletes-production-data
                [--no-backup] [--backup-dir=PATH]

Maintenance:
  context [ARGS...]              Generate Codex context
  clean                          Remove safe local generated caches only

Installed configuration:
  Application:      $APP_DIR
  Production env:  $PROD_ENV_FILE
  Development env: $DEV_ENV_FILE
  Production project: $PROJECT_NAME
  Development project: ${PROJECT_NAME}-dev
  Development port: $DEV_PORT
EOF
}

validate_mode() {
    case "$1" in
        prod|dev) ;;
        *) fail "invalid mode '$1'; expected prod or dev." ;;
    esac
}

validate_mode "$DEFAULT_MODE"

mode_env_file() {
    case "$1" in
        prod) printf '%s\n' "$PROD_ENV_FILE" ;;
        dev) printf '%s\n' "$DEV_ENV_FILE" ;;
        *) fail "invalid mode: $1" ;;
    esac
}

mode_project_name() {
    if [[ "$1" == dev ]]; then
        printf '%s-dev\n' "$PROJECT_NAME"
    else
        printf '%s\n' "$PROJECT_NAME"
    fi
}

require_app_dir() {
    [[ -d "$APP_DIR" ]] || fail "application directory not found: $APP_DIR"
}

require_mode_paths() {
    local mode="$1" env_file
    env_file="$(mode_env_file "$mode")"
    require_app_dir
    [[ -f "$env_file" ]] || fail "$mode environment file not found: $env_file"
    [[ -f "$COMPOSE_FILE" ]] || fail "Compose file not found: $COMPOSE_FILE"
    if [[ "$mode" == dev ]]; then
        [[ -f "$DEV_COMPOSE_FILE" ]] || fail "development Compose file not found: $DEV_COMPOSE_FILE"
    fi
}

prepare_docker() {
    command -v docker >/dev/null 2>&1 || fail "Docker is not installed or is not in PATH."
    docker compose version >/dev/null 2>&1 || fail "the Docker Compose plugin is unavailable."

    if docker info >/dev/null 2>&1; then
        DOCKER_COMMAND=(docker)
        return
    fi
    if command -v sudo >/dev/null 2>&1 && sudo -n docker info >/dev/null 2>&1; then
        DOCKER_COMMAND=(sudo docker)
        return
    fi
    if [[ -t 0 && -t 1 ]] && command -v sudo >/dev/null 2>&1; then
        printf 'tuvtk: Docker access requires sudo; sudo may prompt for your password.\n' >&2
        DOCKER_COMMAND=(sudo docker)
        return
    fi
    fail "Docker is unavailable to this user. Run ./install.sh through sudo or grant Docker access."
}

prepare_mode() {
    require_mode_paths "$1"
    prepare_docker
}

compose_for() {
    local mode="$1" env_file project
    shift
    env_file="$(mode_env_file "$mode")"
    project="$(mode_project_name "$mode")"
    if [[ "$mode" == dev ]]; then
        "${DOCKER_COMMAND[@]}" compose \
            --env-file "$env_file" \
            --project-directory "$APP_DIR" \
            -f "$COMPOSE_FILE" \
            -f "$DEV_COMPOSE_FILE" \
            -p "$project" \
            "$@"
    else
        "${DOCKER_COMMAND[@]}" compose \
            --env-file "$env_file" \
            --project-directory "$APP_DIR" \
            -f "$COMPOSE_FILE" \
            -p "$project" \
            "$@"
    fi
}

django_for() {
    local mode="$1"
    shift
    compose_for "$mode" exec "$WEB_SERVICE" python manage.py "$@"
}

env_value_for() {
    local mode="$1" key="$2" env_file
    env_file="$(mode_env_file "$mode")"
    awk -v key="$key" '
        $0 ~ "^[[:space:]]*" key "=" {
            sub("^[[:space:]]*" key "=", "")
            sub("\\r$", "")
            value=$0
        }
        END { print value }
    ' "$env_file"
}

database_identity() {
    local mode="$1"
    DB_NAME="$(env_value_for "$mode" POSTGRES_DB)"
    DB_USER="$(env_value_for "$mode" POSTGRES_USER)"
    [[ -n "$DB_NAME" ]] || fail "POSTGRES_DB is missing from $(mode_env_file "$mode")."
    [[ -n "$DB_USER" ]] || fail "POSTGRES_USER is missing from $(mode_env_file "$mode")."
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

confirm_action() {
    local confirmed="$1" prompt="$2" answer
    [[ "$confirmed" == true ]] && return 0
    [[ -t 0 ]] || fail "confirmation is required; rerun interactively or pass --yes."
    printf '%s [y/N] ' "$prompt"
    read -r answer
    [[ "$answer" == y || "$answer" == Y || "$answer" == yes || "$answer" == YES ]] \
        || fail "operation cancelled."
}

mode_start() {
    local mode="$1"
    prepare_mode "$mode"
    if [[ "$mode" == dev ]]; then
        compose_for dev up -d db
        compose_for dev run --rm init
        compose_for dev up -d web tailwind
    else
        compose_for prod up -d --wait "$DB_SERVICE"
        compose_for prod run --rm init
        compose_for prod up -d "$WEB_SERVICE" nginx
    fi
}

mode_build() {
    local mode="$1" no_cache="${2:-false}"
    prepare_mode "$mode"
    if [[ "$mode" == dev ]]; then
        if [[ "$no_cache" == true ]]; then
            compose_for dev build --no-cache web
        else
            compose_for dev build web
        fi
        mode_start dev
    else
        if [[ "$no_cache" == true ]]; then
            compose_for prod build --no-cache
        else
            compose_for prod build
        fi
        mode_start prod
    fi
}

mode_stop() {
    local mode="$1"
    prepare_mode "$mode"
    compose_for "$mode" down
}

mode_restart() {
    local mode="$1"
    prepare_mode "$mode"
    if [[ "$mode" == dev ]]; then
        compose_for dev down
        mode_start dev
    else
        compose_for prod restart
    fi
}

timestamp() {
    date -u +%Y-%m-%d_%H%M%S
}

sql_destination() {
    local mode="$1" requested="$2" suffix destination parent
    suffix="$(timestamp)"
    if [[ "$requested" == *.sql ]]; then
        destination="$requested"
        parent="$(dirname "$destination")"
        [[ -d "$parent" ]] || fail "output directory does not exist: $parent"
    else
        mkdir -p "$requested"
        destination="${requested%/}/tuvtk-${mode}-${suffix}.sql"
    fi
    printf '%s\n' "$destination"
}

write_sql_dump() {
    local mode="$1" destination="$2" temporary
    database_identity "$mode"
    temporary="${destination}.tmp.$$"
    umask 077
    {
        printf '%s\n' "-- TUVTK_MODE=$mode" "-- TUVTK_PROJECT=$(mode_project_name "$mode")"
        compose_for "$mode" exec -T "$DB_SERVICE" pg_dump -U "$DB_USER" -d "$DB_NAME"
    } >"$temporary" || {
        rm -f -- "$temporary"
        fail "PostgreSQL export failed for $mode."
    }
    mv -f -- "$temporary" "$destination"
    chmod 0600 "$destination"
}

export_sql() {
    local mode="$1" requested="$2" destination
    prepare_mode "$mode"
    destination="$(sql_destination "$mode" "$requested")"
    write_sql_dump "$mode" "$destination"
    printf 'Database exported: %s\n' "$destination"
}

sql_declared_mode() {
    sed -n '1,20{s/^-- TUVTK_MODE=\(prod\|dev\)$/\1/p;}' "$1" | head -n 1
}

recreate_database() {
    local mode="$1" source="$2"
    database_identity "$mode"
    compose_for "$mode" exec -T "$DB_SERVICE" dropdb --force --if-exists -U "$DB_USER" "$DB_NAME"
    compose_for "$mode" exec -T "$DB_SERVICE" createdb -U "$DB_USER" -O "$DB_USER" "$DB_NAME"
    compose_for "$mode" exec -T "$DB_SERVICE" psql -v ON_ERROR_STOP=1 -U "$DB_USER" -d "$DB_NAME" <"$source"
}

import_sql() {
    local mode="$1" source="$2" confirmed="$3" declared_mode
    [[ -f "$source" ]] || fail "SQL file not found: $source"
    declared_mode="$(sql_declared_mode "$source")"
    if [[ -n "$declared_mode" && "$declared_mode" != "$mode" ]]; then
        fail "SQL dump is marked '$declared_mode' and cannot be imported into '$mode'."
    fi
    prepare_mode "$mode"
    database_identity "$mode"
    printf 'Target mode: %s\nTarget project: %s\nTarget service: %s\nTarget database: %s\n' \
        "$mode" "$(mode_project_name "$mode")" "$DB_SERVICE" "$DB_NAME"
    if [[ -z "$declared_mode" ]]; then
        warn "SQL file has no TUVTK mode marker; verify its origin before continuing."
    fi
    confirm_action "$confirmed" "Replace the $mode database from $source?"
    if [[ "$mode" == dev ]]; then
        compose_for dev stop web tailwind 2>/dev/null || true
    else
        compose_for prod stop web nginx 2>/dev/null || true
    fi
    compose_for "$mode" up -d --wait "$DB_SERVICE"
    recreate_database "$mode" "$source"
    printf 'Database imported into %s (%s). Application services were not restarted.\n' \
        "$(mode_project_name "$mode")" "$mode"
}

archive_directory() {
    local source="$1" destination="$2"
    [[ -d "$source" ]] || return 1
    tar -C "$source" -cf "$destination" .
}

archive_dev_service_path() {
    local container_path="$1" destination="$2"
    compose_for dev run --rm --no-deps -T --entrypoint tar "$WEB_SERVICE" \
        -C "$container_path" -cf - . >"$destination"
}

create_backup() (
    set -Eeuo pipefail
    local mode="$1" backup_directory="$2" env_file work archive stamp data_dir
    local -a included=() skipped=()
    work=""
    trap '[[ -z "$work" ]] || rm -rf -- "$work"' EXIT
    prepare_mode "$mode"
    mkdir -p "$backup_directory"
    chmod 0700 "$backup_directory"
    [[ -d "$backup_directory" && -w "$backup_directory" ]] \
        || fail "backup directory is not writable: $backup_directory"
    database_identity "$mode"

    stamp="$(timestamp)"
    archive="${backup_directory%/}/${stamp}-tuvtk-${mode}.tar.gz"
    work="$(mktemp -d "${TMPDIR:-/tmp}/tuvtk-backup.XXXXXX")"
    mkdir -p "$work/database" "$work/env" "$work/deployment" "$work/data"
    printf '%s\n' "$BACKUP_FORMAT" >"$work/BACKUP_FORMAT"
    printf 'mode=%s\ncreated_utc=%s\nproject_name=%s\ndatabase_name=%s\ndatabase_user=%s\n' \
        "$mode" "$stamp" "$(mode_project_name "$mode")" "$DB_NAME" "$DB_USER" >"$work/manifest"

    env_file="$(mode_env_file "$mode")"
    cp -p -- "$env_file" "$work/env/environment"
    included+=("env/environment ($env_file)")
    cp -p -- "$COMPOSE_FILE" "$work/deployment/compose.yaml"
    if [[ -f "$DEV_COMPOSE_FILE" ]]; then
        cp -p -- "$DEV_COMPOSE_FILE" "$work/deployment/compose.dev.yaml"
    fi
    if [[ -f "$APP_DIR/command.sh" ]]; then
        cp -p -- "$APP_DIR/command.sh" "$work/deployment/command.sh"
    else
        skipped+=("command.sh (not installed)")
    fi
    local relative
    for relative in Dockerfile docker/nginx.conf.template docker/start-web.sh; do
        if [[ -f "$APP_DIR/$relative" ]]; then
            mkdir -p "$work/deployment/$(dirname "$relative")"
            cp -p -- "$APP_DIR/$relative" "$work/deployment/$relative"
        fi
    done

    write_sql_dump "$mode" "$work/database/database.sql"
    included+=("database/database.sql")

    if [[ "$mode" == prod ]]; then
        data_dir="$(env_value_for prod TUVTK_DATA_DIR)"
        if [[ -n "$data_dir" ]] && archive_directory "$data_dir/media" "$work/data/media.tar"; then
            included+=("data/media.tar ($data_dir/media)")
        else
            rm -f -- "$work/data/media.tar"
            skipped+=("media (path unavailable)")
        fi
        if [[ -n "$data_dir" ]] && archive_directory "$data_dir/private-media" "$work/data/private-media.tar"; then
            included+=("data/private-media.tar ($data_dir/private-media)")
        else
            rm -f -- "$work/data/private-media.tar"
            skipped+=("private media (path unavailable)")
        fi
    else
        if archive_dev_service_path /app/media "$work/data/media.tar"; then
            included+=("data/media.tar (development volume)")
        else
            rm -f -- "$work/data/media.tar"
            skipped+=("development media (volume unavailable)")
        fi
        if archive_dev_service_path /app/private_media "$work/data/private-media.tar"; then
            included+=("data/private-media.tar (development volume)")
        else
            rm -f -- "$work/data/private-media.tar"
            skipped+=("development private media (volume unavailable)")
        fi
    fi
    skipped+=("static output (regenerable; intentionally excluded)")

    if ! tar -C "$work" -czf "$archive" .; then
        rm -rf -- "$work"
        fail "unable to create backup archive."
    fi
    rm -rf -- "$work"
    work=""
    chmod 0600 "$archive"

    printf 'Backup created: %s\n' "$archive"
    printf 'Included database dump: database/database.sql\n'
    printf 'Included environment: %s\n' "$env_file"
    for relative in "${included[@]}"; do printf 'Included: %s\n' "$relative"; done
    for relative in "${skipped[@]}"; do printf 'Skipped: %s\n' "$relative"; done
    if [[ "$mode" == dev ]]; then
        printf 'Restore with: sudo ./install.sh dev-restore %q\n' "$archive"
    else
        printf 'Restore with: sudo ./install.sh restore %q\n' "$archive"
    fi
)

archive_is_safe() {
    local archive="$1" entry normalized
    while IFS= read -r entry; do
        normalized="${entry#./}"
        [[ -z "$normalized" || "$normalized" == "." ]] && continue
        [[ "$normalized" != /* && "$normalized" != ".." && "$normalized" != ../* && "$normalized" != */../* && "$normalized" != */.. ]] \
            || return 1
        case "$normalized" in
            BACKUP_FORMAT|manifest|database/|database/database.sql|env/|env/environment|deployment/|deployment/compose.yaml|deployment/compose.dev.yaml|deployment/command.sh|deployment/Dockerfile|deployment/docker/|deployment/docker/nginx.conf.template|deployment/docker/start-web.sh|data/|data/media.tar|data/private-media.tar) ;;
            *) return 1 ;;
        esac
    done < <(tar -tzf "$archive")
    ! tar -tvzf "$archive" | awk 'substr($1,1,1) == "l" || substr($1,1,1) == "h" { found=1 } END { exit found ? 0 : 1 }'
}

manifest_value() {
    local file="$1" key="$2"
    sed -n "s/^${key}=//p" "$file" | head -n 1
}

inner_tar_is_safe() {
    local archive="$1" entry
    while IFS= read -r entry; do
        entry="${entry#./}"
        [[ -z "$entry" || "$entry" == "." ]] && continue
        [[ "$entry" != /* && "$entry" != ".." && "$entry" != ../* && "$entry" != */../* && "$entry" != */.. ]] || return 1
    done < <(tar -tf "$archive")
    ! tar -tvf "$archive" | awk 'substr($1,1,1) == "l" || substr($1,1,1) == "h" { found=1 } END { exit found ? 0 : 1 }'
}

restore_service_path() {
    local mode="$1" source="$2" target="$3"
    inner_tar_is_safe "$source" || fail "backup contains an unsafe data archive: $(basename "$source")"
    compose_for "$mode" run --rm --no-deps -T --entrypoint sh "$WEB_SERVICE" -ec '
        target="$1"
        find "$target" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
        tar -C "$target" -xf -
    ' sh "$target" <"$source"
}

restore_backup() (
    set -Eeuo pipefail
    local mode="$1" archive="$2" confirmed="$3" work archive_mode archive_project env_file env_backup
    [[ -f "$archive" ]] || fail "backup archive not found: $archive"
    archive_is_safe "$archive" || fail "archive has an unknown or unsafe structure."
    work="$(mktemp -d "${TMPDIR:-/tmp}/tuvtk-restore.XXXXXX")"
    trap 'rm -rf -- "$work"' EXIT
    tar --no-same-owner --no-same-permissions -xzf "$archive" -C "$work"
    [[ -f "$work/BACKUP_FORMAT" && "$(<"$work/BACKUP_FORMAT")" == "$BACKUP_FORMAT" ]] \
        || fail "unsupported backup format."
    [[ -f "$work/manifest" && -f "$work/database/database.sql" && -f "$work/env/environment" ]] \
        || fail "backup is incomplete."
    archive_mode="$(manifest_value "$work/manifest" mode)"
    archive_project="$(manifest_value "$work/manifest" project_name)"
    [[ "$archive_mode" == "$mode" ]] \
        || fail "backup mode is '$archive_mode'; refusing to restore it into '$mode'."
    [[ "$archive_project" == "$(mode_project_name "$mode")" ]] \
        || fail "backup project '$archive_project' does not match '$(mode_project_name "$mode")'."

    prepare_mode "$mode"
    printf 'Restore target mode: %s\nRestore target project: %s\nArchive: %s\n' \
        "$mode" "$(mode_project_name "$mode")" "$archive"
    confirm_action "$confirmed" "Stop and replace the $mode database and included media?"
    compose_for "$mode" down

    env_file="$(mode_env_file "$mode")"
    env_backup="${env_file}.pre-restore-$(timestamp).bak"
    cp -p -- "$env_file" "$env_backup"
    install -m 0600 "$work/env/environment" "$env_file"
    printf 'Preserved previous environment: %s\n' "$env_backup"

    compose_for "$mode" up -d --wait "$DB_SERVICE"
    recreate_database "$mode" "$work/database/database.sql"
    printf 'Restored database: %s\n' "$(env_value_for "$mode" POSTGRES_DB)"
    if [[ -f "$work/data/media.tar" ]]; then
        restore_service_path "$mode" "$work/data/media.tar" /app/media
        printf 'Restored media.\n'
    else
        printf 'Skipped media: not included in archive.\n'
    fi
    if [[ -f "$work/data/private-media.tar" ]]; then
        restore_service_path "$mode" "$work/data/private-media.tar" /app/private_media
        printf 'Restored private media.\n'
    else
        printf 'Skipped private media: not included in archive.\n'
    fi
    printf 'Application services were not restarted.\n'
    if [[ "$mode" == dev ]]; then
        printf 'Next command: sudo ./install.sh dev\n'
    else
        printf 'Next command: sudo ./install.sh start\n'
    fi
)

safe_data_root() {
    local raw="$1" canonical_app canonical
    [[ "$raw" == /* && "$raw" != "/" ]] || fail "unsafe TUVTK_DATA_DIR: $raw"
    canonical="$(readlink -m -- "$raw")"
    canonical_app="$(readlink -m -- "$APP_DIR")"
    case "$canonical" in
        /bin|/boot|/dev|/etc|/home|/lib|/lib64|/media|/mnt|/opt|/proc|/root|/run|/sbin|/srv|/sys|/tmp|/usr|/var|/var/lib)
            fail "production data root is too broad or system-critical: $canonical"
            ;;
    esac
    [[ "$canonical" != "/" && "$canonical" != "$canonical_app" && "$canonical" != "$canonical_app/"* && "$canonical_app" != "$canonical/"* ]] \
        || fail "production data path overlaps the application directory: $canonical"
    printf '%s\n' "$canonical"
}

remove_directory_contents() {
    local path="$1"
    [[ -d "$path" ]] || return 0
    find "$path" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
}

dev_db_reset() {
    local confirmed="$1" start_after="$2"
    prepare_mode dev
    printf 'Development project: %s\n' "$(mode_project_name dev)"
    printf 'Volume removed: dev-postgres\n'
    confirm_action "$confirmed" "Delete and recreate the isolated development database?"
    compose_for dev down --remove-orphans
    "${DOCKER_COMMAND[@]}" volume rm "$(mode_project_name dev)_dev-postgres" >/dev/null 2>&1 || true
    printf 'Development database reset completed. Media, private media, static output, and Node modules were not deleted. Production was not changed.\n'
    if [[ "$start_after" == true ]]; then
        mode_start dev
    else
        printf 'Next command: sudo ./install.sh dev\n'
    fi
}

prod_db_reset() {
    local acknowledged="$1" no_backup="$2" backup_dir="$3" data_root env_file env_backup
    [[ "$acknowledged" == true ]] \
        || fail "production reset requires --yes-i-understand-this-deletes-production-data; --yes is not accepted."
    prepare_mode prod
    data_root="$(safe_data_root "$(env_value_for prod TUVTK_DATA_DIR)")"
    printf 'Production project: %s\n' "$(mode_project_name prod)"
    printf 'Production DB service: %s\n' "$DB_SERVICE"
    printf 'Production DB path: %s/postgres\n' "$data_root"
    printf 'Production media paths: %s/media, %s/private-media\n' "$data_root" "$data_root"
    printf 'Production static path: %s/static\n' "$data_root"
    if [[ "$no_backup" == false ]]; then
        create_backup prod "$backup_dir"
    else
        warn "production backup explicitly disabled with --no-backup."
    fi
    env_file="$(mode_env_file prod)"
    env_backup="${env_file}.pre-reset-$(timestamp).bak"
    cp -p -- "$env_file" "$env_backup"
    chmod 0600 "$env_backup"
    printf 'Environment preserved: %s\n' "$env_backup"
    compose_for prod down
    remove_directory_contents "$data_root/postgres"
    remove_directory_contents "$data_root/media"
    remove_directory_contents "$data_root/private-media"
    remove_directory_contents "$data_root/static"
    printf 'Production data reset completed. Application source, .git, and environment files were not deleted.\n'
    printf '%s\n' \
        'Next commands:' \
        '  sudo ./install.sh start' \
        '  sudo ./install.sh migrate' \
        '  sudo ./install.sh collectstatic' \
        '  sudo ./install.sh django createsuperuser'
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

parse_confirmed_file() {
    local usage_text="$1"
    shift
    CONFIRMED=false
    TARGET_FILE=""
    while (($#)); do
        case "$1" in
            --yes) CONFIRMED=true ;;
            --*) fail "usage: $usage_text" ;;
            *) [[ -z "$TARGET_FILE" ]] || fail "usage: $usage_text"; TARGET_FILE="$1" ;;
        esac
        shift
    done
    [[ -n "$TARGET_FILE" ]] || fail "usage: $usage_text"
}

run_context() {
    require_app_dir
    if command -v python3 >/dev/null 2>&1; then
        (cd "$APP_DIR" && python3 scripts/generate_codex_context.py "$@")
    elif command -v python >/dev/null 2>&1; then
        (cd "$APP_DIR" && python scripts/generate_codex_context.py "$@")
    else
        fail "Python 3 is required for context generation."
    fi
}

command_name="${1:-help}"
if (($#)); then shift; fi

case "$command_name" in
    help|-h|--help) usage ;;
    status|ps) (($# == 0)) || fail "usage: $command_name"; prepare_mode "$DEFAULT_MODE"; compose_for "$DEFAULT_MODE" ps ;;
    start|up) (($# == 0)) || fail "usage: $command_name"; mode_start "$DEFAULT_MODE" ;;
    stop|down) (($# == 0)) || fail "usage: $command_name"; mode_stop "$DEFAULT_MODE" ;;
    restart) (($# == 0)) || fail "usage: restart"; mode_restart "$DEFAULT_MODE" ;;
    build) (($# == 0)) || fail "usage: build"; mode_build "$DEFAULT_MODE" false ;;
    rebuild) (($# == 0)) || fail "usage: rebuild"; mode_build "$DEFAULT_MODE" true ;;
    logs) (($# <= 1)) || fail "usage: logs [SERVICE]"; prepare_mode "$DEFAULT_MODE"; compose_for "$DEFAULT_MODE" logs -f "$@" ;;

    prod-status) (($# == 0)) || fail "usage: prod-status"; prepare_mode prod; compose_for prod ps ;;
    prod-start) (($# == 0)) || fail "usage: prod-start"; mode_start prod ;;
    prod-stop) (($# == 0)) || fail "usage: prod-stop"; mode_stop prod ;;
    prod-restart) (($# == 0)) || fail "usage: prod-restart"; mode_restart prod ;;
    prod-build) (($# == 0)) || fail "usage: prod-build"; mode_build prod false ;;
    prod-rebuild) (($# == 0)) || fail "usage: prod-rebuild"; mode_build prod true ;;
    prod-logs) (($# <= 1)) || fail "usage: prod-logs [SERVICE]"; prepare_mode prod; compose_for prod logs -f "$@" ;;

    dev|dev-start) (($# == 0)) || fail "usage: $command_name"; mode_start dev ;;
    dev-build) (($# == 0)) || fail "usage: dev-build"; mode_build dev false ;;
    dev-stop) (($# == 0)) || fail "usage: dev-stop"; mode_stop dev ;;
    dev-status) (($# == 0)) || fail "usage: dev-status"; prepare_mode dev; compose_for dev ps ;;
    dev-logs) (($# <= 1)) || fail "usage: dev-logs [SERVICE]"; prepare_mode dev; compose_for dev logs -f "$@" ;;
    tailwind) (($# == 0)) || fail "usage: tailwind"; prepare_mode dev; compose_for dev up -d tailwind; compose_for dev logs -f tailwind ;;
    npm) (($# > 0)) || fail "usage: npm COMMAND [ARGS...]"; prepare_mode dev; compose_for dev run --rm --no-deps tailwind npm "$@" ;;

    check) (($# == 0)) || fail "usage: check"; prepare_mode "$DEFAULT_MODE"; django_for "$DEFAULT_MODE" check ;;
    test)
        prepare_mode "$DEFAULT_MODE"
        if has_verbosity "$@"; then django_for "$DEFAULT_MODE" test "$@"; else django_for "$DEFAULT_MODE" test "$@" -v 0; fi
        ;;
    migrate) prepare_mode "$DEFAULT_MODE"; django_for "$DEFAULT_MODE" migrate "$@" ;;
    makemigrations) prepare_mode "$DEFAULT_MODE"; django_for "$DEFAULT_MODE" makemigrations "$@" ;;
    collectstatic) (($# == 0)) || fail "usage: collectstatic"; prepare_mode "$DEFAULT_MODE"; django_for "$DEFAULT_MODE" collectstatic --noinput ;;
    shell) (($# == 0)) || fail "usage: shell"; prepare_mode "$DEFAULT_MODE"; django_for "$DEFAULT_MODE" shell ;;
    dbshell) (($# == 0)) || fail "usage: dbshell"; prepare_mode "$DEFAULT_MODE"; django_for "$DEFAULT_MODE" dbshell ;;
    django) (($# > 0)) || fail "usage: django COMMAND [ARGS...]"; prepare_mode "$DEFAULT_MODE"; django_for "$DEFAULT_MODE" "$@" ;;
    prod-django) (($# > 0)) || fail "usage: prod-django COMMAND [ARGS...]"; prepare_mode prod; django_for prod "$@" ;;
    dev-django) (($# > 0)) || fail "usage: dev-django COMMAND [ARGS...]"; prepare_mode dev; django_for dev "$@" ;;
    exec) (($# >= 2)) || fail "usage: exec SERVICE COMMAND [ARGS...]"; prepare_mode "$DEFAULT_MODE"; compose_for "$DEFAULT_MODE" exec "$@" ;;

    export-sql) (($# == 1)) || fail "usage: export-sql PATH"; export_sql "$DEFAULT_MODE" "$1" ;;
    prod-export-sql) (($# == 1)) || fail "usage: prod-export-sql PATH"; export_sql prod "$1" ;;
    dev-export-sql) (($# == 1)) || fail "usage: dev-export-sql PATH"; export_sql dev "$1" ;;
    import-sql) parse_confirmed_file "import-sql SQL_FILE [--yes]" "$@"; import_sql "$DEFAULT_MODE" "$TARGET_FILE" "$CONFIRMED" ;;
    prod-import-sql) parse_confirmed_file "prod-import-sql SQL_FILE [--yes]" "$@"; import_sql prod "$TARGET_FILE" "$CONFIRMED" ;;
    dev-import-sql) parse_confirmed_file "dev-import-sql SQL_FILE [--yes]" "$@"; import_sql dev "$TARGET_FILE" "$CONFIRMED" ;;
    backup) (($# == 1)) || fail "usage: backup DIRECTORY"; create_backup "$DEFAULT_MODE" "$1" ;;
    prod-backup) (($# == 1)) || fail "usage: prod-backup DIRECTORY"; create_backup prod "$1" ;;
    dev-backup) (($# == 1)) || fail "usage: dev-backup DIRECTORY"; create_backup dev "$1" ;;
    restore) parse_confirmed_file "restore ARCHIVE [--yes]" "$@"; restore_backup "$DEFAULT_MODE" "$TARGET_FILE" "$CONFIRMED" ;;
    prod-restore) parse_confirmed_file "prod-restore ARCHIVE [--yes]" "$@"; restore_backup prod "$TARGET_FILE" "$CONFIRMED" ;;
    dev-restore) parse_confirmed_file "dev-restore ARCHIVE [--yes]" "$@"; restore_backup dev "$TARGET_FILE" "$CONFIRMED" ;;

    fresh-db|dev-db-reset)
        confirmed=false; start_after=false
        for argument in "$@"; do
            case "$argument" in --yes) confirmed=true ;; --start) start_after=true ;; *) fail "usage: $command_name [--yes] [--start]" ;; esac
        done
        dev_db_reset "$confirmed" "$start_after"
        ;;
    prod-db-reset)
        acknowledged=false; no_backup=false; backup_dir="$DEFAULT_BACKUP_DIR"
        for argument in "$@"; do
            case "$argument" in
                --yes-i-understand-this-deletes-production-data) acknowledged=true ;;
                --no-backup) no_backup=true ;;
                --backup-dir=*) backup_dir="${argument#*=}" ;;
                --yes) fail "--yes is insufficient for production reset; use the exact long confirmation flag." ;;
                *) fail "usage: prod-db-reset --yes-i-understand-this-deletes-production-data [--no-backup] [--backup-dir=PATH]" ;;
            esac
        done
        prod_db_reset "$acknowledged" "$no_backup" "$backup_dir"
        ;;

    context) run_context "$@" ;;
    clean) (($# == 0)) || fail "usage: clean"; clean_generated ;;
    *) fail "unknown command: $command_name (run './install.sh help')" ;;
esac
```

## `codex-prompt-demos/custom-js-to-alpine.md`

Size: 4.0 KB

````markdown
# Custom JavaScript to Alpine.js Prompt Guide

Use this when you want Codex to check whether an existing custom JavaScript behavior can be replaced by Alpine.js.

The goal is not to delete all JavaScript. The goal is to move simple local UI state into templates with Alpine and keep custom JavaScript for workflows that truly need it.

## Decision rule

Alpine.js is a good replacement when the behavior is local to the page and does not own business state.

Good Alpine candidates:

- dropdown open/close state;
- modal/dialog visibility;
- tabs and disclosure panels;
- selected row/card visual state;
- upload filename labels;
- local loading indicators;
- simple counters;
- mobile filter/sidebar toggles;
- show/hide advanced filters.

Keep custom JavaScript for:

- drag and drop;
- canvas/template editors;
- direct download flows;
- file parsing;
- JSON-heavy workflows;
- row-by-row remote updates;
- complex preview/rendering logic;
- browser APIs that are clearer in a dedicated file.

Never move these to Alpine:

- validation authority;
- permissions;
- ownership checks;
- persistence;
- business workflow state;
- anything that must survive refresh unless the server also stores it.

## Investigation prompt

```text
Investigate whether this app/page can replace scoped custom JavaScript with Alpine.js.
Do not edit files.

Target app:
- apps/<app>

Target page or workflow:
- <describe page/workflow>

Read only:
- AGENTS.md
- frontend.md
- apps/<app>/AGENTS.md
- the target template
- the related view only if needed
- the existing app-specific JS file

Output:
1. Custom JS behaviors found
2. Which behaviors can move to Alpine.js
3. Which behaviors should stay as custom JS
4. Risks
5. Exact implementation prompt for the first small change

Rules:
- Do not inspect unrelated apps.
- Do not implement.
- Do not propose a SPA pattern.
- Keep Django as source of truth.
```

## First implementation prompt

```text
Replace only one simple custom JavaScript behavior with Alpine.js.

Target app:
- apps/<app>

Behavior:
- <example: upload filename display>

Allowed files:
- <template path>
- <existing JS path only if removing now-unused code is necessary>

Rules:
- Alpine may handle local UI state only.
- Do not change backend behavior.
- Do not change validation, permissions, or persistence.
- Do not remove custom JS that still handles complex workflows.
- Keep the visual behavior the same or simpler.
- Return a minimal diff.

Checks:
- ./install.sh check
- git diff --check

Manual browser checks:
- open the target page;
- trigger the changed UI behavior;
- confirm there are no console errors;
- confirm the form/action still works after refresh.
```

## Example: upload filename display

Before asking for a full conversion, ask only for this:

```text
Replace only the upload filename preview custom JS with Alpine.js.
Do not touch upload processing.
Do not touch HTMX endpoints.
Do not touch unrelated JS behavior.
```

Expected Alpine shape:

```html
<div x-data="{ fileName: '' }">
  <input
    type="file"
    name="file"
    @change="fileName = $event.target.files[0]?.name || ''"
  >
  <p x-show="fileName" x-text="fileName"></p>
</div>
```

## Example: modal visibility

```html
<div x-data="{ open: false }">
  <button type="button" @click="open = true">Open</button>

  <div x-show="open" x-cloak>
    <button type="button" @click="open = false">Close</button>
    <!-- modal content -->
  </div>
</div>
```

## Example: advanced filters toggle

```html
<section x-data="{ filtersOpen: false }">
  <button type="button" @click="filtersOpen = !filtersOpen">
    Filters
  </button>

  <div x-show="filtersOpen" x-cloak>
    <!-- filter form fields -->
  </div>
</section>
```

## Anti-patterns

Do not ask Codex:

```text
Replace all custom JS with Alpine.
```

Ask instead:

```text
Investigate this one JS file and classify each behavior as Alpine, HTMX, keep custom JS, or remove.
```

Then implement one behavior at a time.
````

## `codex-prompt-demos/htmx-alpine-phased-migration.md`

Size: 4.4 KB

````markdown
# HTMX + Alpine Phased Migration Prompts

Use these prompts when converting ordinary Django HTML pages into a more dynamic server-rendered interface.

Do not migrate a whole app in one prompt. Migrate one behavior at a time.

## Phase 0 — investigation only

```text
Investigate only. Do not edit files.

Target app:
- apps/<app>

Goal:
I want this app/page to feel more dynamic with HTMX and Alpine.js, but I do not want a SPA.

Read only:
- AGENTS.md
- frontend.md
- apps/<app>/AGENTS.md
- the templates/views directly related to this page
- existing app-specific JS only if the page uses it

Output:
1. Existing page flow
2. Candidate HTMX partials
3. Candidate Alpine local state
4. Custom JS that should remain
5. Risks
6. Recommended first implementation phase
7. Exact next prompt

Do not inspect unrelated apps.
Do not load the whole generated context unless file paths are unknown.
```

## Phase 1 — list/table refresh only

```text
Convert only this list/table area to HTMX.

Target app:
- apps/<app>

Target page:
- <template path>

Goal:
The table/list should refresh without a full page reload when filters/search/pagination change.

Allowed files:
- the target view
- the target template
- new partial template(s) only if needed
- the app tests file only if behavior changes

Rules:
- Keep full-page fallback working.
- Use server-rendered HTML partials.
- Preserve existing permissions and query filtering.
- Do not change create/edit/delete flows.
- Do not redesign the page.
- Do not touch unrelated apps.

Output:
- minimal diff
- files changed
- focused tests/checks
- manual browser checks
```

## Phase 2 — form validation partial only

```text
Convert only this form to HTMX partial submission.

Target app:
- apps/<app>

Target form/page:
- <template path>

Goal:
Submit the form with HTMX and show validation errors without a full page reload.

Rules:
- POST must keep CSRF.
- Django form validation remains authoritative.
- On validation error, return the form partial.
- On success, return the smallest useful updated partial or preserve existing redirect fallback.
- Do not change models or migrations.
- Do not change unrelated forms.

Output:
- minimal diff
- files changed
- tests/checks
- manual browser checks
```

## Phase 3 — Alpine local UI state only

```text
Add Alpine.js only for local UI state on this page.

Target app:
- apps/<app>

Target behavior:
- <dropdown/modal/tabs/selected rows/upload filename/filter drawer>

Rules:
- Alpine may not own server state.
- Do not move validation, permissions, or persistence into Alpine.
- Do not add global JS.
- Do not duplicate Alpine loading.
- Keep keyboard and refresh behavior acceptable.

Output:
- minimal diff
- files changed
- manual browser checks
```

## Phase 4 — extract shared table partials only after repetition exists

```text
Extract reusable table/list partials only where duplication already exists.

Target app:
- apps/<app>

Candidate templates:
- <list templates>

Rules:
- Do not create an over-generic table framework.
- Keep different column sets explicit and readable.
- Extract only shared shell pieces: empty state, loading area, pagination, table wrapper, action button patterns.
- Do not hide business-specific columns in complex template magic.
- Preserve existing visual output.

Output:
- minimal diff
- files changed
- before/after template structure
- manual browser checks
```

## Phase 5 — infinite scroll / lazy rows

Use only when pagination is not desired and the data set is not too large for the browser over time.

```text
Implement lazy row loading for this list/table.

Target app:
- apps/<app>

Target page:
- <template path>

Goal:
The table area stays inside a fixed-height scroll container. Rows load in chunks as the user scrolls near the bottom.

Rules:
- Keep a normal fallback if practical.
- Use server-rendered row partials.
- Do not load all rows at once.
- Use stable ordering.
- Preserve filters/search.
- Do not use frontend-owned data state.
- Add clear empty/end-of-list behavior.

Output:
- minimal diff
- files changed
- manual browser checks with 2,000 rows or fixture data
```

Notes:
- Infinite scroll is useful for visual flow, but pagination is easier to debug and bookmark.
- For internal operations, consider a fixed-height table with HTMX-loaded pages/chunks rather than endless browser memory growth.
````

## `codex-prompt-demos/README.md`

Size: 6.9 KB

````markdown
# Codex Prompt Demos

Copy one prompt, replace the placeholders, and use it in Codex.

Keep each Codex session limited to one app, one workflow, and one safe change.

## Required reading for normal tasks

```text
Read only:
- AGENTS.md
- coding-standards.md
- frontend.md if UI/templates/CSS/JS/HTMX/Alpine are involved
- apps/<app>/AGENTS.md
- exact files needed for this workflow
```

Do not read:

```text
- the whole repository
- all codex-context files
- unrelated apps
- unrelated tests
- migration history unless schema is involved
- Docker/deployment files unless deployment is the task
```

## Daily Safe Task

```text
Work only on this task:

[describe the task]

Target app:
- apps/<app>

Read only:
- AGENTS.md
- coding-standards.md
- frontend.md if frontend is involved
- apps/<app>/AGENTS.md
- exact files needed for this workflow

Before editing, report:
- files you need to inspect
- why each file is needed
- whether this is app-local or cross-app

Rules:
- Implement the smallest safe change.
- Reuse existing forms, selectors, services, templates, partials, tables, action buttons, and message patterns.
- Do not create a new abstraction unless the pattern is already repeated and stable.
- Stop if another app, schema migration, or broad rewrite becomes necessary.

Checks:
- focused check for the changed app/workflow
- ./install.sh check if backend behavior changed
- git diff --check
```

## Investigation Only

```text
Investigate only. Do not edit files.

Task idea:
[describe what I want visually or functionally]

Target app:
- apps/<app>

Read only:
- AGENTS.md
- coding-standards.md
- frontend.md if frontend is involved
- apps/<app>/AGENTS.md
- exact files directly related to this workflow

Output:
- recommended approach
- files that would need editing
- existing patterns to reuse
- HTMX vs Alpine vs custom JS decision, if frontend is involved
- risks
- focused test commands
- exact implementation prompt I can use next

Do not inspect unrelated apps.
Do not read generated context unless source paths are unknown.
Do not implement.
```

## Frontend Page Improvement

```text
Improve only this page:

Target app:
- apps/<app>

Target page:
- <template path>

Read only:
- AGENTS.md
- coding-standards.md
- frontend.md
- apps/<app>/AGENTS.md
- <template path>
- related view only if needed
- related tests only if rendered behavior changes

Rules:
- Use Django templates, Tailwind, and daisyUI.
- Use shared `tuvtk` semantic tokens.
- Keep the page sharp, compact, professional, and enterprise-grade.
- Use `rounded-none` for new business panels, settings rows, menus, and tables.
- Avoid childish rounded card-heavy layouts.
- Reuse existing form, table, action-button, empty-state, and message/toast patterns.
- Use HTMX only if server-rendered partial updates are needed.
- Use Alpine only for local UI state.
- Do not introduce a SPA pattern.
- Do not touch unrelated pages.

Goal:
[describe visual/UX improvement]

Checks:
- ./install.sh check
- ./install.sh test apps.<app> only if behavior changed
- git diff --check

Report files changed and manual browser checks needed.
```

## HTMX Workflow Conversion

```text
Convert only this workflow to HTMX:

Target app:
- apps/<app>

Workflow:
- [example: upload form + asset grid refresh]

Read only:
- AGENTS.md
- coding-standards.md
- frontend.md
- apps/<app>/AGENTS.md
- the view file for this workflow
- the template file for this workflow
- the app tests file

Use HTMX for:
- server-rendered partial updates
- form validation errors
- refreshed messages
- refreshed list/table/grid sections

Do not use HTMX for:
- direct downloads
- JSON APIs consumed elsewhere
- replacing Django validation or permissions

Preserve:
- normal full-page fallback
- POST + CSRF for state changes
- ownership checks
- existing URLs unless a new partial endpoint is necessary

Stop if this requires touching another app.

Checks:
- ./install.sh test apps.<app>
- ./install.sh check
- git diff --check
```

## Alpine Local UI Only

```text
Add Alpine.js only for local UI state.

Target app:
- apps/<app>

Target template:
- <template path>

Read only:
- AGENTS.md
- coding-standards.md
- frontend.md
- apps/<app>/AGENTS.md
- <template path>
- related app JS file only if one already exists

Use Alpine only for:
- toggles
- dialogs
- disclosure panels
- selected row/card state
- loading indicators
- upload filename display

Do not use Alpine for:
- validation
- authorization
- persistence
- server state
- business workflow state

Do not touch Django models, services, or migrations.

Checks:
- ./install.sh check
- git diff --check

Report manual browser checks needed.
```

## UI Consistency Cleanup

```text
Clean up UI consistency only.

Target app:
- apps/<app>

Target page or workflow:
- <path/workflow>

Read only:
- AGENTS.md
- coding-standards.md
- frontend.md
- apps/<app>/AGENTS.md
- exact templates/includes/static files for this page

Goals:
- remove childish rounded card-heavy layout
- use sharp bordered sections
- unify forms, tables, action buttons, and messages
- reuse existing partials where practical
- keep behavior unchanged

Do not:
- change models
- change services/selectors unless a template contract requires it
- touch unrelated pages
- add a frontend framework
- introduce app-local colors

Checks:
- ./install.sh check
- app test only if rendered behavior changed
- git diff --check
```

## Bug Fix

```text
Fix only this bug:

Bug:
[paste exact bug/error/behavior]

Target app:
- apps/<app>

Read only:
- AGENTS.md
- coding-standards.md
- apps/<app>/AGENTS.md
- frontend.md if UI is involved
- exact files needed to reproduce or fix the bug

Before editing:
- identify likely cause
- list files to inspect
- say whether this is frontend, backend, or template-only

Rules:
- Implement the smallest safe fix.
- Reuse existing patterns.
- Do not weaken tests to make the failure disappear.

Checks:
- focused test for the changed app/file
- ./install.sh check
- git diff --check

Stop if the bug requires a broad rewrite.
```

## Documentation Only

```text
Update documentation only.

Read only:
- AGENTS.md
- coding-standards.md
- README.md
- frontend.md
- the exact docs mentioned below

Task:
[describe doc update]

Do not edit application code.
Do not inspect unrelated apps.
Do not regenerate codex context unless explicitly requested.

Checks:
- git diff --check

Report files changed.
```

## After Codex Finishes

Check status:

```bash
git status --short
git diff --check
```

Commit tracked modified files only:

```bash
git add -u
git commit -m "Your commit message"
```

Commit new files too:

```bash
git add path/to/new-file
git add -u
git commit -m "Your commit message"
```
````

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

## `core/AGENTS.md`

Size: 1.7 KB

````markdown
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
````

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

Size: 2.9 KB

```python
import re

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
    return {
        "app_navigation": build_navigation(request, permissions),
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

Size: 5.4 KB

```python
NAVIGATION = (
    {
        "label": "Overview",
        "items": (
            {"label": "Dashboard", "icon": "grid-1x2-fill", "url_name": "dashboard:index"},
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

## `core/templates/includes/sidebar.html`

Size: 5.6 KB

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
                                                            <a href="{% url child.url_name %}" class="transition-none{% if child.is_active %} active font-semibold{% endif %}" {% if child.is_active %}aria-current="page"{% endif %}><span class="ops-submenu-label">{{ child.label }}</span></a>
                                                        {% else %}
                                                            <a href="#" class="transition-none"><span class="ops-submenu-label">{{ child.label }}</span></a>
                                                        {% endif %}
                                                    </li>
                                                {% endfor %}
                                            </ul>
                                        </details>
                                    {% else %}
                                        {% if item.url_name %}
                                            <a href="{% url item.url_name %}" class="is-drawer-close:tooltip is-drawer-close:tooltip-right is-drawer-close:justify-center transition-none{% if item.is_active %} active font-semibold{% endif %}" data-tip="{{ item.label }}" {% if item.is_active %}aria-current="page"{% endif %}>
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

Size: 7.9 KB

```html
{% load static tailwind_tags optional_browser_reload %}
<!DOCTYPE html>
<html lang="ro" data-theme="tuvtk">
<head>
    <title>{% block title %}Platforma TUVTK{% endblock %}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preload" href="{% static 'fonts/inter/InterVariable.woff2' %}" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="{% static 'bootstrap_icons/css/bootstrap_icons.css' %}">
    {% tailwind_css %}
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
            <script src="{% static 'js/sidebar_state.js' %}"></script>
            <div class="drawer-content h-full min-h-0 overflow-hidden">
                <main class="ops-scrollbar h-full overflow-y-auto">
                    <div class="mx-auto w-full max-w-[1600px] px-4 py-4 sm:px-5 sm:py-5 lg:px-6 lg:py-5">
                        {% block content %}{% endblock %}
                    </div>
                </main>
            </div>
            {% include "includes/sidebar.html" %}
        </div>
    </div>
    <script src="{% static 'js/vendor/htmx.min.js' %}" defer></script>
    <script>
        (() => {
            const safeMethods = new Set(["GET", "HEAD", "OPTIONS", "TRACE"]);
            const csrfToken = () => {
                const fieldToken = document.querySelector('[name="csrfmiddlewaretoken"]')?.value;
                if (fieldToken) return fieldToken;

                const cookie = document.cookie
                    .split(";")
                    .map((value) => value.trim())
                    .find((value) => value.startsWith("csrftoken="));
                return cookie ? decodeURIComponent(cookie.slice("csrftoken=".length)) : "";
            };

            document.body.addEventListener("htmx:configRequest", (event) => {
                if (!event.detail?.headers) return;
                const method = String(event.detail.verb || event.detail.requestConfig?.verb || "GET").toUpperCase();
                if (safeMethods.has(method)) return;

                const token = csrfToken();
                if (token) event.detail.headers["X-CSRFToken"] = token;
            });
        })();
    </script>
    <script src="{% static 'js/vendor/alpine.min.js' %}" defer></script>
    <script src="{% static 'js/sidebar.js' %}" defer></script>
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

Size: 3.4 KB

```python
import json

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.conf import settings
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

    def test_frontend_enhancement_dependencies_are_local_and_pinned(self):
        package_json = settings.BASE_DIR / "theme" / "static_src" / "package.json"
        package = json.loads(package_json.read_text(encoding="utf-8"))

        self.assertEqual(package["dependencies"]["htmx.org"], "2.0.10")
        self.assertEqual(package["dependencies"]["alpinejs"], "3.15.12")
        self.assertIn("build:vendor", package["scripts"])

    def test_navigation_marks_current_route(self):
        request = RequestFactory().get('/')
        request.resolver_match = resolve('/')
        request.user = AnonymousUser()

        context = application_shell(request)
        dashboard_item = context['app_navigation'][0]['items'][0]

        self.assertTrue(dashboard_item['is_active'])
        self.assertEqual(dashboard_item['url_name'], 'dashboard:index')

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

## `docs/frontend/table-patterns.md`

Size: 5.8 KB

````markdown
# Frontend Table Patterns

Guidance for Django templates, HTMX, Alpine.js, Tailwind, and daisyUI table/list screens.

Use this together with `frontend.md` and `coding-standards.md`.

## Preferred default

Use ordinary Django pagination first unless the workflow clearly benefits from lazy loading.

For internal operations, tables must stay:

- readable;
- filterable;
- debuggable;
- safe with permissions;
- usable after refresh;
- friendly to browser memory;
- consistent with the rest of the app.

## Template structure

A good list page usually has:

```text
templates/<app>/<model>_list.html
templates/<app>/partials/<model>_filters.html
templates/<app>/partials/<model>_table.html
templates/<app>/partials/<model>_rows.html
templates/<app>/partials/<model>_empty.html
templates/<app>/partials/<model>_messages.html
```

Use partials for repeated page sections, but do not make a generic table engine too early.

Different tables may have different columns. That is normal.

Extract common pieces only when they are truly shared:

- table wrapper;
- filter bar;
- empty state;
- pagination controls;
- loading indicator;
- bulk action toolbar;
- row action button group;
- message/toast region.

Keep business columns explicit in the app template.

## Visual style

- Use sharp, bordered, operational tables.
- Prefer `rounded-none` for new table wrappers and action regions.
- Prefer borders and compact spacing over shadows and decorative cards.
- Keep row height consistent.
- Keep action columns aligned and predictable.
- Keep empty/loading/error states inside or directly above the table region.

## Filters and search

Filters should be compact and easy to reset.

Recommended structure:

- search field first;
- high-value filters next;
- reset/clear action last;
- advanced filters hidden behind a disclosure only when needed;
- applied state visible after refresh.

HTMX filters should preserve the same server-side query logic as full-page requests.

## Row actions

Use consistent action hierarchy:

- view/open: normal compact action;
- edit/change: secondary compact action;
- archive/restore/delete: clearly marked destructive or recovery action;
- icon-only actions require an accessible label or title.

Do not hide unavailable actions only with CSS.

If an action is disabled, the reason should be obvious from nearby copy, title text, or state messaging.

## HTMX table refresh

Good for:

- search;
- filters;
- sorting;
- pagination;
- local list refresh after create/edit/delete;
- row archive/restore;
- message area refresh.

Pattern:

```html
<form
  hx-get="{% url 'app:list' %}"
  hx-target="#table-region"
  hx-trigger="change, keyup delay:300ms from:input[name='q']"
>
  <!-- filters -->
</form>

<div id="table-region">
  {% include "app/partials/table.html" %}
</div>
```

In the view:

```python
def list_view(request):
    context = build_context(request)
    if getattr(request, "htmx", False):
        return render(request, "app/partials/table.html", context)
    return render(request, "app/list.html", context)
```

The partial should include the affected messages/empty state when the action changes what the user sees.

## Fixed-height lazy rows

Use this when the user wants the table to stay fixed size and load more rows while scrolling.

Recommended behavior:

- table wrapper has fixed height and `overflow-y-auto`;
- first request loads the first chunk;
- a sentinel row at the bottom triggers the next chunk;
- server returns only more rows and the next sentinel;
- filters/search reset the region;
- ordering is stable.

Example shape:

```html
<div id="table-scroll" class="max-h-[70vh] overflow-y-auto">
  <table class="table table-zebra w-full">
    <thead class="sticky top-0 z-10 bg-base-100">
      <!-- headings -->
    </thead>
    <tbody id="rows">
      {% include "app/partials/rows.html" %}
    </tbody>
  </table>
</div>
```

Sentinel idea:

```html
<tr
  hx-get="{% url 'app:list_rows' %}?page={{ next_page }}{{ current_querystring }}"
  hx-trigger="revealed"
  hx-swap="outerHTML"
>
  <td colspan="99">Loading more...</td>
</tr>
```

The server should include a next sentinel only while more results exist.

## When not to use infinite scroll

Avoid it when users need:

- exact page numbers;
- bookmarking a result page;
- easy browser back/forward behavior;
- exporting exact filtered result sets;
- comparing items across many pages;
- very large result sets that would stay in the browser for a long session.

For those cases, use normal pagination with HTMX partial refresh.

## Alpine usage in tables

Good Alpine uses:

- selected row visual state;
- bulk action toolbar visibility;
- filter drawer open/close;
- column help/tooltips;
- local loading indicator;
- mobile details expansion.

Do not use Alpine for:

- ownership checks;
- permissions;
- deciding which rows the user may see;
- saving selected records to the database without a POST;
- replacing Django form validation.

## Codex prompt for table work

```text
Work only on this table/list page.

Target app:
- apps/<app>

Target page:
- <template path>

Goal:
[describe: HTMX filter refresh / fixed-height lazy rows / selected row UI / action column cleanup]

Rules:
- Read AGENTS.md, coding-standards.md, frontend.md, and apps/<app>/AGENTS.md.
- Keep Django as source of truth.
- Use HTMX only for server-rendered partial updates.
- Use Alpine only for local UI state.
- Preserve full-page fallback where practical.
- Preserve permissions and filters.
- Reuse existing table, message, empty-state, and action-button patterns.
- Keep the visual style sharp, compact, and professional.
- Do not touch unrelated apps.
- Return a minimal diff.
```
````

## `frontend.md`

Size: 7.0 KB

```markdown
# Frontend Rules

Frontend standards for Django templates, Tailwind CSS, daisyUI, HTMX, Alpine.js, and scoped custom JavaScript.

The application stays server-rendered. Do not turn it into a SPA.

## Stack

- Django templates.
- Tailwind CSS.
- daisyUI.
- HTMX.
- Alpine.js.
- Scoped custom JavaScript when safer than forcing HTMX/Alpine.

Do not add React, Vue, Svelte, Angular, Inertia, Next.js, Nuxt, or another frontend framework unless explicitly requested.

## Source of truth

- Django views choose responses.
- Django forms validate requests.
- Django services perform writes.
- PostgreSQL stores business state.
- JavaScript improves interaction only.

Do not move validation, authorization, routing, ownership checks, or persistence into JavaScript.

## Brand and theme

Use the `tuvtk` daisyUI theme.

Current brand tokens are defined in `theme/static_src/src/styles.css`:

- primary blue: `#164194`.
- secondary red: `#d41131`.
- accent grey-green: `#7c8f9e`.
- page/panel background: white.
- muted panel background: `#f7f9fb`.
- default border: `#cfd7df`.

Use semantic utilities and CSS variables:

- `base-*`.
- `base-content`.
- `primary`.
- `secondary`.
- `accent`.
- `info`.
- `success`.
- `warning`.
- `error`.
- `text-muted`.

Do not add literal colors or app-local color systems.

Literal colors belong only in global token definitions, brand assets, or user-authored document/canvas data.

## Visual style

Target look:

- professional;
- enterprise-grade;
- compact;
- calm;
- operational;
- clear hierarchy;
- no decorative clutter.

Avoid:

- childish card-heavy layouts;
- oversized rounded cards;
- pastel dashboard blocks;
- decorative gradients;
- random shadows;
- app-local colors;
- inconsistent button shapes;
- large empty spacing on internal tools.

Use sharp business UI by default:

- prefer `rounded-none` for new business panels, tables, settings rows, menus, and action areas;
- prefer borders over shadows;
- prefer compact sections over large cards;
- keep spacing tight but readable;
- use rounded exceptions only for avatars, status dots, badges, or legacy elements already styled that way.

## Layout principles

Standard page shape:

- page title;
- short description only if useful;
- primary action near the title;
- filters/search in a compact section;
- main table/list/form region;
- messages/toasts in one predictable place;
- empty state close to the affected region.

Settings pages should use:

- section heading;
- short explanation;
- structured rows;
- setting name on the left;
- setting purpose under the name;
- control on the right;
- obvious disabled/error/destructive states.

Do not make every setting a separate card.

## Tailwind and daisyUI

- Use Tailwind for layout and spacing.
- Use daisyUI for standard components.
- Prefer existing classes and includes before adding new CSS.
- Add Tailwind `@source` entries only when a new app template/static path needs class scanning.
- Keep component size consistent across pages.
- Do not create one-off utility piles when an include or component pattern already exists.

## Common component standards

### Forms

- Keep forms compact and readable.
- Use server-rendered errors.
- Put non-field errors above the action row.
- Use one clear primary submit button.
- Put cancel/back/secondary actions beside it with lower emphasis.
- Keep destructive actions separated or clearly marked.

### Tables and lists

- Prefer tables for operational comparison and management.
- Keep headers readable.
- Keep action columns consistent.
- Keep wide tables horizontally scrollable.
- Use `docs/frontend/table-patterns.md` for detailed table/list work.

### Action buttons

- Primary action: `btn btn-primary`.
- Secondary action: `btn btn-outline` or low-emphasis link/button.
- Destructive action: `btn btn-error` or clearly marked icon button.
- Compact row actions should use the same size across the page.
- Icon-only buttons require an accessible label or title.
- Disabled buttons must use a real disabled state where possible.

### Messages and toasts

- Use one message area per workflow.
- Map state to semantic tokens: success, info, warning, error.
- HTMX updates that change state should refresh the message region.
- Avoid app-local alert colors.
- Error messages should explain the next useful action.

## HTMX

Use HTMX when the server returns HTML.

Good HTMX uses:

- form submissions with partial refresh;
- validation-error partials;
- filters;
- search;
- pagination;
- table/list refreshes;
- archive/restore actions;
- delete actions;
- message areas;
- targeted swaps;
- small server-rendered polling.

Do not use HTMX for:

- direct downloads unless intentionally designed and tested;
- canvas/editor state;
- drag-and-drop state ownership;
- large JSON workflows where JSON is clearer;
- replacing Django validation or permissions.

State-changing HTMX requests must remain POST with CSRF.

## Alpine.js

Use Alpine.js only for local browser state.

Good Alpine uses:

- dropdowns;
- dialogs;
- disclosure panels;
- tabs without server state;
- selected rows/cards;
- loading flags;
- upload filename labels;
- small counters;
- narrow-screen filter toggles.

Do not use Alpine.js for:

- database state;
- validation;
- authorization;
- ownership checks;
- business workflows;
- state that must survive refresh.

## Custom JavaScript

Keep or add scoped custom JavaScript when it is safer than forcing HTMX/Alpine.

Good custom JavaScript cases:

- drag and drop;
- canvas/template editors;
- file parsing;
- JSON-heavy workflows;
- direct download flows;
- remote row-by-row updates;
- complex preview/rendering logic.

Application-specific JavaScript belongs to the owning Django app.

Shared JavaScript belongs in `theme/` or `core/` only when it is truly global.

## Templates

- Standard pages extend `core/templates/layouts/base.html`.
- Standalone pages must still use the shared theme and compiled stylesheet.
- Prefer existing includes before new markup.
- Keep tables horizontally scrollable on narrow screens.
- Preserve native links/forms where practical.
- Preserve keyboard access, visible focus, and native scrolling.

## Kanban and drag/drop interfaces

- Dragging must have an obvious active state.
- Drop targets must be visually clear.
- Moved/reordered stages must show immediate feedback.
- Destructive actions should use a bin/trash icon only with an accessible label.
- Replacement actions must explain what will be replaced and what stays unchanged.
- Do not hide critical ordering state in subtle card movement only.

## Global assets

HTMX and Alpine are loaded once from the base layout.

Apps may add scoped behavior, but must not duplicate global library loading.

## Visual verification

For UI work, report:

- before/after browser check if available;
- disabled states checked;
- empty states checked;
- error states checked;
- narrow-screen behavior checked;
- manual checks still needed.
```

## `generate_codex_context.bat`

Size: 85 B

```batch
@echo off
python "%~dp0scripts\generate_codex_context.py" %*
exit /b %ERRORLEVEL%
```

## `generate_codex_context.ps1`

Size: 86 B

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

## `HTMX_ALPINE_IMPLEMENTATION_PLAN.md`

Size: 13.4 KB

```markdown
# HTMX and Alpine.js Implementation Plan

This plan migrates the project toward HTMX and Alpine.js without turning the
application into a SPA and without replacing working custom JavaScript in one
large pass. The order matters: install the shared foundation first, convert
low-risk CRUD/list pages next, then handle custom interactive workflows after
their surrounding pages are stable.

The shared foundation and the first Flota conversion pass are complete, so they
are not repeated as active implementation phases below.

## Ground Rules

- Keep Django templates and PostgreSQL as the source of truth.
- Use HTMX for server-rendered partial updates, form submissions, table/list
  refreshes, small polling/refresh needs, and targeted swaps.
- Use Alpine.js for local-only UI state: toggles, dialogs, filters, disclosure
  panels, selected-row state, loading flags, and small reactive counters.
- Keep validation, authorization, ownership checks, and persistence server-side.
- Preserve native links/forms as fallbacks wherever practical.
- Keep state-changing requests POST-only with CSRF protection.
- Do not rewrite heavy custom JavaScript until the workflow is specifically in
  scope.
- Add focused tests for partial-response behavior when a view gains HTMX support.

## Completed Baseline

Already implemented:

1. Shared HTMX and Alpine package dependencies, script loading, CSRF request
   handling, frontend rules, and shell/dashboard script-contract tests.
2. Flota HTMX partial responses for fleet filters, pagination, vehicle
   archive/restore, and maintenance-type archive flows.
3. Flota Alpine confirmation state for archive/restore actions.
4. Flota deadline badge refresh after HTMX swaps.
5. Focused Flota tests for partial responses and preserved native behavior.

## Flota Follow-Up Improvements

Goal: improve the completed Flota pass without reworking the whole app.

Files:

1. `apps/flota/views.py`
2. `apps/flota/templates/flota/includes/fleet_panel.html`
3. `apps/flota/templates/flota/includes/vehicle_detail_panel.html`
4. `apps/flota/templates/flota/includes/maintenance_type_panel.html`
5. `apps/flota/static/flota/flota.js`
6. `apps/flota/tests.py`

Tasks:

1. Replace the subtle filter spinner with a clearly visible loading state:
   disabled controls, `aria-busy`, an obvious table-level loading row or overlay,
   and focused tests for the rendered loading hooks.
2. Use `hx-sync` on the fleet filter form so rapid typing or select changes
   replace stale requests instead of queueing outdated table refreshes.
3. Add active filter chips with one-click removal while preserving the normal
   query-string fallback.
4. Consider an Alpine disclosure for the filter panel on narrow screens if the
   filter grid takes too much vertical space.
5. Add archive/restore actions from the fleet list only if row-level partials can
   keep ownership, CSRF, confirmation, and fallback behavior straightforward.
6. Consider HTMX out-of-band message swaps if a future flow needs global message
   updates outside the swapped panel.
7. Add manual browser QA under slow network throttling for filter loading state,
   archive confirmation, refresh/back navigation, and narrow-screen layout.

Checks:

1. `.\install.ps1 test apps.flota`
2. `.\install.ps1 check`
3. Manual browser check with network throttling.
4. `git diff --check`

## Phase 3: Media Library

Goal: convert the small upload/list/delete workflow before larger consumers use
it.

Files:

1. `apps/media_library/AGENTS.md`
2. `apps/media_library/views.py`
3. `apps/media_library/urls.py`
4. `apps/media_library/forms.py`
5. `apps/media_library/templates/media_library/library.html`
6. New partial templates under `apps/media_library/templates/media_library/includes/`
   if needed.
7. `apps/media_library/tests.py`

Tasks:

1. Add HTMX upload handling that returns the refreshed upload form, messages,
   and asset grid as partial HTML.
2. Add HTMX delete handling for owned assets.
3. Use Alpine for local upload filename/preview/loading state only.
4. Keep JSON API endpoints for existing `diplome` editor integration.
5. Preserve private asset serving and ownership behavior.

Checks:

1. `.\install.ps1 test apps.media_library`
2. `.\install.ps1 check`
3. `git diff --check`

## Phase 4: Tasks Static Pages and Lists

Goal: convert non-Kanban task workflows before touching drag-and-drop behavior.

Files:

1. `apps/tasks/AGENTS.md`
2. `apps/tasks/views.py`
3. `apps/tasks/urls.py`
4. `apps/tasks/forms.py`
5. `apps/tasks/templates/tasks/includes/messages.html`
6. `apps/tasks/templates/tasks/includes/form_fields.html`
7. `apps/tasks/templates/tasks/includes/timer.html`
8. `apps/tasks/templates/tasks/hub.html`
9. `apps/tasks/templates/tasks/board_list.html`
10. `apps/tasks/templates/tasks/board_settings.html`
11. `apps/tasks/templates/tasks/board_form.html`
12. `apps/tasks/templates/tasks/task_form.html`
13. `apps/tasks/static/tasks/tasks.js`
14. `apps/tasks/tests.py`

Tasks:

1. Add HTMX filtering for board/task lists.
2. Add HTMX form handling for settings actions where the page can refresh a
   local section.
3. Use Alpine for dialogs, confirm state, local form sections, and loading flags.
4. Keep timers in existing JS unless replacing them is isolated and lower risk.
5. Preserve server-side permission behavior and native form fallbacks.

Checks:

1. `.\install.ps1 test apps.tasks`
2. `.\install.ps1 check`
3. `git diff --check`

## Phase 5: Tasks Kanban

Goal: integrate HTMX around Kanban without breaking drag-and-drop.

Files:

1. `apps/tasks/views.py`
2. `apps/tasks/templates/tasks/board_kanban.html`
3. New partial templates under `apps/tasks/templates/tasks/includes/` if needed.
4. `apps/tasks/static/tasks/tasks.js`
5. `apps/tasks/tests.py`

Tasks:

1. Keep drag-and-drop movement in custom JS initially.
2. Convert task creation and archive/restore flows to HTMX partial refreshes.
3. Evaluate whether board state polling can become `hx-trigger` polling or remain
   custom JSON polling.
4. Ensure swapped cards still have required drag/drop attributes and version
   fields.
5. Preserve native fallback forms for task movement.

Checks:

1. `.\install.ps1 test apps.tasks`
2. Manual browser check: drag/drop, create task, archive task, refresh/back.
3. `git diff --check`

## Phase 6: Diplome Lists, Generation, and Imports

Goal: convert ordinary diploma pages while leaving the editor intact.

Files:

1. `apps/diplome/AGENTS.md`
2. `apps/diplome/views.py`
3. `apps/diplome/urls.py`
4. `apps/diplome/forms.py`
5. `apps/diplome/templates/diplome/template_list.html`
6. `apps/diplome/templates/diplome/template_form.html`
7. `apps/diplome/templates/diplome/history_index.html`
8. `apps/diplome/templates/diplome/batch_detail.html`
9. `apps/diplome/templates/diplome/generation_index.html`
10. `apps/diplome/templates/diplome/generation_preview.html`
11. `apps/diplome/templates/diplome/participant_list.html`
12. `apps/diplome/templates/diplome/participant_list_detail.html`
13. `apps/diplome/templates/diplome/participant_import.html`
14. `apps/diplome/templates/diplome/participant_import_sheet.html`
15. `apps/diplome/templates/diplome/participant_import_mapping.html`
16. `apps/diplome/templates/diplome/participant_import_preview.html`
17. `apps/diplome/static/diplome/generation.js`
18. `apps/diplome/static/diplome/participant_import.js`
19. `apps/diplome/static/diplome/participant_mapping.js`
20. `apps/diplome/tests.py`
21. `apps/diplome/tests_generation.py`
22. `apps/diplome/tests_bulk_generation.py`
23. `apps/diplome/tests_participants.py`

Tasks:

1. Add HTMX partial refreshes for template list, participant list, history, and
   batch detail actions.
2. Use HTMX only where downloads and redirects are not the primary response.
3. Use Alpine for selection state, local filtering, confirm dialogs, and import
   form UI.
4. Keep generation/download validation and output server-owned.
5. Preserve owner scoping and history snapshot behavior.

Checks:

1. `.\install.ps1 test apps.diplome.tests`
2. `.\install.ps1 test apps.diplome.tests_participants`
3. `.\install.ps1 test apps.diplome.tests_generation`
4. `.\install.ps1 test apps.diplome.tests_bulk_generation`
5. Use only the focused command matching the edited workflow when possible.
6. `git diff --check`

## Phase 7: Planificator Generator and History

Goal: convert the schedule generator shell and history before the JSON-heavy
converter/updater workflows.

Files:

1. `apps/planificator/AGENTS.md`
2. `apps/planificator/views.py`
3. `apps/planificator/urls.py`
4. `apps/planificator/forms.py`
5. `apps/planificator/templates/planificator/generator_perioade.html`
6. `apps/planificator/templates/planificator/includes/upload.html`
7. `apps/planificator/templates/planificator/includes/settings.html`
8. `apps/planificator/templates/planificator/includes/result_table.html`
9. `apps/planificator/templates/planificator/includes/actions.html`
10. `apps/planificator/templates/planificator/includes/messages.html`
11. `apps/planificator/templates/planificator/istoric.html`
12. `apps/planificator/static/planificator/generator.js`
13. `apps/planificator/tests.py`
14. `apps/planificator/tests_scheduler.py`

Tasks:

1. Add HTMX support around generator form errors, messages, and result sections
   where it does not interfere with file download/export flows.
2. Use Alpine for local month selection, holiday rows, upload filename state, and
   step UI where it reduces custom JavaScript.
3. Keep result tables horizontally scrollable.
4. Preserve schedule export response behavior.

Checks:

1. `.\install.ps1 test apps.planificator.tests`
2. `.\install.ps1 test apps.planificator.tests_scheduler`
3. `.\install.ps1 check`
4. `git diff --check`

## Phase 8: Planificator XML and Word Converter Workflows

Goal: migrate JSON/download workflows only after their boundaries are mapped.

Files:

1. `apps/planificator/views.py`
2. `apps/planificator/templates/planificator/xml_formatter.html`
3. `apps/planificator/templates/planificator/word_converter.html`
4. `apps/planificator/static/planificator/xml_formatter.js`
5. `apps/planificator/static/planificator/word_converter.js`
6. `apps/planificator/tests_xml_export.py`
7. `apps/planificator/tests_word_converter.py`

Tasks:

1. Keep direct file download responses outside HTMX swaps unless using an
   intentional download pattern.
2. Convert preview/error sections to HTMX only if the endpoint can return HTML
   partials without weakening the JSON contract used by existing code.
3. Use Alpine for file labels, preview selection, and loading state.
4. Preserve untrusted file validation and neutralization behavior.

Checks:

1. `.\install.ps1 test apps.planificator.tests_xml_export`
2. `.\install.ps1 test apps.planificator.tests_word_converter`
3. `git diff --check`

## Phase 9: Planificator Course Updater

Goal: handle the highest-risk Planificator workflow after the simpler workflows.

Files:

1. `apps/planificator/views.py`
2. `apps/planificator/templates/planificator/actualizeaza_cursuri.html`
3. `apps/planificator/static/planificator/course_updater.js`
4. `apps/planificator/tests_course_updater.py`

Tasks:

1. Preserve SSRF defenses, redirect handling, and secret non-persistence.
2. Keep JSON endpoints if they remain the clearest contract for row-by-row
   updates.
3. Use HTMX for isolated row/status replacement only when the response shape is
   simpler than the current JSON flow.
4. Use Alpine for connection state, input state, progress indicators, and local
   row UI.

Checks:

1. `.\install.ps1 test apps.planificator.tests_course_updater`
2. Manual browser check: connect, fetch dates, update row, disconnect.
3. `git diff --check`

## Phase 10: Diplome Template Preview and Editor

Goal: review the editor last. This is not a first-pass HTMX conversion target.

Files:

1. `apps/diplome/templates/diplome/template_preview.html`
2. `apps/diplome/templates/diplome/template_editor.html`
3. `apps/diplome/static/diplome/template_preview.js`
4. `apps/diplome/static/diplome/template_renderer.js`
5. `apps/diplome/static/diplome/template_editor.js`
6. `apps/diplome/tests.py`

Tasks:

1. Keep `template_renderer.js` compatible with preview, editor, and PDF-related
   assumptions.
2. Do not replace canvas/layout editing state with HTMX.
3. Consider Alpine only for isolated chrome state if it does not conflict with
   editor selection, history, keyboard, pointer, media picker, or save behavior.
4. Consider HTMX only for surrounding shell actions, not the editor layout model.
5. Keep JSON layout validation canonical in server validators.

Checks:

1. `.\install.ps1 test apps.diplome.tests`
2. Manual browser check: create template, edit, media picker, save, preview,
   discard, back/refresh behavior.
3. `git diff --check`

## Phase 11: Cleanup and Context Refresh

Goal: remove dead code and update generated context after the staged migration.

Files:

1. Any app static JS file made obsolete by earlier phases.
2. Any new partial templates created during the migration.
3. `theme/static_src/src/styles.css` if new template/static paths require
   Tailwind `@source` entries.
4. `codex-context/` generated files after context regeneration.

Tasks:

1. Remove unused custom JavaScript only after the replacement behavior is tested.
2. Confirm no app-local colors or duplicate UI tokens were introduced.
3. Confirm all HTMX partials preserve authorization, CSRF, and fallback behavior.
4. Regenerate context from the repository root.

Checks:

1. `.\install.ps1 check`
2. Focused app tests for every app touched in the cleanup.
3. `.\install.ps1 npm run build`
4. `.\install.ps1 context`
5. `git diff --check`
```

## `install.cmd`

Size: 112 B

```batch
@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*
exit /b %ERRORLEVEL%
```

## `install.ps1`

Size: 2.7 KB

```powershell
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$CommandArgs
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$router = Join-Path $root 'scripts\tuvtk_cli.py'
$runtimeRoot = Join-Path $root '.tuvtk\runtime\python'
$runtimePython = Join-Path $runtimeRoot 'python.exe'
$minimumVersion = [Version]'3.12'

function Test-TuvtkPython {
    param([string]$Executable)

    if (-not (Test-Path -LiteralPath $Executable -PathType Leaf)) {
        return $false
    }
    try {
        $versionText = & $Executable -c "import sys; print('.'.join(map(str, sys.version_info[:3])))" 2>$null
        return ([Version]$versionText -ge $minimumVersion)
    }
    catch {
        return $false
    }
}

$python = $null
$candidates = @(
    $runtimePython,
    (Join-Path $root '.venv\Scripts\python.exe')
)

$pathPython = Get-Command python.exe -ErrorAction SilentlyContinue
if ($pathPython) {
    $candidates += $pathPython.Source
}

foreach ($candidate in $candidates) {
    if (Test-TuvtkPython -Executable $candidate) {
        $python = $candidate
        break
    }
}

if (-not $python) {
    $version = '3.12.10'
    $installerName = "python-$version-amd64.exe"
    $downloadDir = Join-Path $root '.tuvtk\downloads'
    $installer = Join-Path $downloadDir $installerName
    $url = "https://www.python.org/ftp/python/$version/$installerName"

    New-Item -ItemType Directory -Force -Path $downloadDir | Out-Null
    New-Item -ItemType Directory -Force -Path $runtimeRoot | Out-Null
    if (-not (Test-Path -LiteralPath $installer)) {
        Write-Host "[tuvtk] Downloading $url"
        $partial = "$installer.part"
        Invoke-WebRequest -Uri $url -OutFile $partial -UseBasicParsing
        Move-Item -Force -LiteralPath $partial -Destination $installer
    }

    $signature = Get-AuthenticodeSignature -LiteralPath $installer
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'Python Software Foundation') {
        throw "Python installer signature validation failed: $($signature.Status)"
    }

    Write-Host "[tuvtk] Installing a private Python runtime"
    $arguments = @(
        '/quiet',
        'InstallAllUsers=0',
        "TargetDir=`"$runtimeRoot`"",
        'Include_pip=1',
        'Include_launcher=0',
        'PrependPath=0',
        'Shortcuts=0'
    )
    $process = Start-Process -FilePath $installer -ArgumentList $arguments -Wait -PassThru -WindowStyle Hidden
    if ($process.ExitCode -ne 0 -or -not (Test-TuvtkPython -Executable $runtimePython)) {
        throw "Private Python installation failed with exit code $($process.ExitCode)."
    }
    $python = $runtimePython
}

& $python $router @CommandArgs
exit $LASTEXITCODE
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

## `runserver.bat`

Size: 116 B

```batch
@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" dev %*
exit /b %ERRORLEVEL%
```

## `runserver.ps1`

Size: 151 B

```powershell
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $root 'install.ps1') dev @args
exit $LASTEXITCODE
```

## `scripts/generate_codex_context.py`

Size: 23.7 KB

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

EXCLUDED_DIRECTORY_PATHS = {
    "theme/static/js/vendor",
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
            elif relative in EXCLUDED_DIRECTORY_PATHS:
                reason = "generated frontend vendor assets"
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
            content = content.replace("\r\n", "\n").replace("\r", "\n")

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

## `scripts/tests/__init__.py`

Size: 36 B

```python
"""Tests for repository tooling."""
```

## `scripts/tests/test_tuvtk_cli.py`

Size: 8.8 KB

```python
from __future__ import annotations

import hashlib
import io
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from scripts import tuvtk_cli


class EnvironmentFileTests(unittest.TestCase):
    def test_write_env_preserves_comments_and_updates_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / ".env"
            path.write_text("# retained\nOLD=value\nKEEP=yes\n", encoding="utf-8")

            tuvtk_cli.write_env(path, {"OLD": "new", "ADDED": "value"})

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                "# retained\nOLD=new\nKEEP=yes\n\nADDED=value\n",
            )

    def test_windows_environment_replaces_example_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".env.example").write_text(
                "POSTGRES_DB=platforma_tuvtk\n"
                "POSTGRES_USER=postgres\n"
                "POSTGRES_PASSWORD=postgres\n"
                "POSTGRES_PORT=5432\n"
                "DJANGO_SECRET_KEY=\n",
                encoding="utf-8",
            )
            env_file = root / ".env"
            with mock.patch.object(tuvtk_cli, "ROOT", root), mock.patch.object(tuvtk_cli, "ENV_FILE", env_file):
                values = tuvtk_cli.WindowsNativeBackend({}).prepare_environment()

            self.assertNotEqual(values["POSTGRES_PASSWORD"], "postgres")
            self.assertTrue(values["DJANGO_SECRET_KEY"])
            self.assertEqual(tuvtk_cli.read_env(env_file)["POSTGRES_PASSWORD"], values["POSTGRES_PASSWORD"])


class ArchiveSafetyTests(unittest.TestCase):
    def test_zip_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "unsafe.zip"
            with zipfile.ZipFile(archive, "w") as bundle:
                bundle.writestr("../outside.txt", "unsafe")

            with self.assertRaises(tuvtk_cli.CliError):
                tuvtk_cli.safe_extract_zip(archive, root / "output")


class DownloadTests(unittest.TestCase):
    def test_download_verifies_sha256(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.bin"
            source.write_bytes(b"verified")
            expected = hashlib.sha256(b"verified").hexdigest()

            destination = tuvtk_cli.download(source.as_uri(), root / "destination.bin", expected)

            self.assertEqual(destination.read_bytes(), b"verified")


class ArgumentTests(unittest.TestCase):
    def test_help_names_primary_windows_and_linux_launchers(self) -> None:
        self.assertIn("Windows: install.cmd COMMAND", tuvtk_cli.HELP)
        self.assertIn("Linux:   ./install.sh COMMAND", tuvtk_cli.HELP)
        self.assertIn("fresh-db [--yes] [--start]", tuvtk_cli.HELP)

    def test_option_value_supports_both_forms(self) -> None:
        self.assertEqual(tuvtk_cli.option_value(["--port=9000"], "--port"), "9000")
        self.assertEqual(tuvtk_cli.option_value(["--port", "9001"], "--port"), "9001")

    def test_invalid_port_is_rejected(self) -> None:
        with self.assertRaises(tuvtk_cli.CliError):
            tuvtk_cli.validate_port(0)

    def test_setup_port_supports_public_and_legacy_names(self) -> None:
        self.assertEqual(tuvtk_cli.selected_setup_port(["--port=9000"], {}), 9000)
        self.assertEqual(tuvtk_cli.selected_setup_port(["--dev-port", "9001"], {}), 9001)

    def test_setup_domain_supports_public_host_alias(self) -> None:
        self.assertEqual(tuvtk_cli.selected_setup_domain(["--public-host=example.com"]), "example.com")

    def test_linux_setup_passthrough_keeps_installer_options(self) -> None:
        self.assertEqual(
            tuvtk_cli.linux_setup_passthrough(
                [
                    "production",
                    "--port=9000",
                    "--domain=example.com",
                    "--http-port",
                    "8080",
                    "--data-dir=/srv/tuvtk",
                    "--force",
                ]
            ),
            ["--domain=example.com", "--http-port", "8080", "--data-dir=/srv/tuvtk"],
        )


class LinuxBackendTests(unittest.TestCase):
    def test_fresh_db_targets_linux_development(self) -> None:
        backend = mock.Mock()
        with mock.patch.object(tuvtk_cli, "IS_WINDOWS", False), mock.patch.object(
            tuvtk_cli, "load_config", return_value={"default_mode": "prod"}
        ), mock.patch.object(tuvtk_cli, "LinuxDockerBackend", return_value=backend):
            tuvtk_cli.main(["fresh-db", "--yes"])

        backend.invoke.assert_called_once_with("fresh-db", ["--yes"], "dev")

    def test_setup_passes_linux_installer_options(self) -> None:
        backend = tuvtk_cli.LinuxDockerBackend({})

        with mock.patch.object(backend, "_sudo", side_effect=lambda command: command), mock.patch.object(
            tuvtk_cli, "run"
        ) as runner, mock.patch.object(tuvtk_cli, "save_config"):
            backend.setup("prod", domain="example.com", passthrough=["--http-port=8080"])

        command = runner.call_args.args[0]
        self.assertIn("--domain=example.com", command)
        self.assertIn("--http-port=8080", command)

    def test_sudo_preserves_internal_installer_flags(self) -> None:
        backend = tuvtk_cli.LinuxDockerBackend({})
        with mock.patch.object(tuvtk_cli.os, "geteuid", return_value=1000, create=True), mock.patch.object(
            tuvtk_cli.shutil, "which", return_value="/usr/bin/sudo"
        ):
            command = backend._sudo(["bash", "install.sh", "--dev"])

        self.assertEqual(command[:2], ["sudo", "env"])
        self.assertIn("TUVTK_SKIP_COMMAND=true", command)

    def test_doctor_reports_missing_commands(self) -> None:
        backend = tuvtk_cli.LinuxDockerBackend({})
        output = io.StringIO()
        with mock.patch.object(tuvtk_cli.shutil, "which", return_value=None), mock.patch("sys.stdout", output):
            backend.doctor()

        self.assertIn("docker: missing/unavailable", output.getvalue())


@unittest.skipUnless(os.name == "nt", "Windows process flags")
class WindowsProcessTests(unittest.TestCase):
    def test_fresh_db_resets_windows_development_database(self) -> None:
        backend = mock.Mock()
        with mock.patch.object(tuvtk_cli, "IS_WINDOWS", True), mock.patch.object(
            tuvtk_cli, "load_config", return_value={}
        ), mock.patch.object(tuvtk_cli, "WindowsNativeBackend", return_value=backend):
            tuvtk_cli.main(["fresh-db", "--yes", "--start"])

        backend.reset_database.assert_called_once_with(True, True)

    def test_background_process_uses_no_window_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            process = mock.Mock(pid=1234)
            process.poll.return_value = None
            backend = tuvtk_cli.WindowsNativeBackend({})
            with mock.patch.object(tuvtk_cli, "ROOT", root), mock.patch.object(
                tuvtk_cli, "PID_DIR", root / "pids"
            ), mock.patch.object(tuvtk_cli, "LOG_DIR", root / "logs"), mock.patch.object(
                backend, "process_running", return_value=False
            ), mock.patch.object(backend, "process_environment", return_value={}), mock.patch.object(
                tuvtk_cli.time, "sleep"
            ), mock.patch.object(tuvtk_cli.subprocess, "Popen", return_value=process) as popen:
                backend.spawn("web", ["fake.exe"])

            self.assertEqual(popen.call_args.kwargs["creationflags"], tuvtk_cli.WINDOWS_BACKGROUND_FLAGS)

    def test_foreground_processes_inherit_current_terminal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tailwind = mock.Mock(pid=1234)
            tailwind.poll.side_effect = [0, 0]
            web = mock.Mock(pid=1235)
            web.poll.return_value = None
            backend = tuvtk_cli.WindowsNativeBackend({})
            with mock.patch.object(tuvtk_cli, "ROOT", root), mock.patch.object(
                tuvtk_cli, "PID_DIR", root / "pids"
            ), mock.patch.object(backend, "stop_process"), mock.patch.object(
                backend, "prepare_development", return_value=Path("npm.cmd")
            ), mock.patch.object(backend, "process_environment", return_value={}), mock.patch.object(
                tuvtk_cli.subprocess, "Popen", side_effect=[tailwind, web]
            ) as popen, mock.patch.object(tuvtk_cli, "run"):
                backend.dev_foreground(prepared=True)

            self.assertEqual(popen.call_count, 2)
            for call in popen.call_args_list:
                self.assertNotIn("creationflags", call.kwargs)
                self.assertNotIn("stdout", call.kwargs)


if __name__ == "__main__":
    unittest.main()
```

## `scripts/tuvtk_cli.py`

Size: 46.0 KB

```python
#!/usr/bin/env python3
"""Cross-platform TUVTK setup and command router."""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / ".tuvtk"
CONFIG_FILE = STATE_DIR / "config.json"
RUNTIME_DIR = STATE_DIR / "runtime"
DOWNLOAD_DIR = STATE_DIR / "downloads"
LOG_DIR = STATE_DIR / "logs"
PID_DIR = STATE_DIR / "pids"
VENV_DIR = ROOT / ".venv"
POSTGRES_ROOT = ROOT / ".postgresql"
POSTGRES_DATA = POSTGRES_ROOT / "data"
ENV_FILE = ROOT / ".env"
DEV_ENV_FILE = ROOT / ".env.dev"
IS_WINDOWS = os.name == "nt"
POSTGRES_VERSION = "17.10-1"
POSTGRES_ARCHIVE = f"postgresql-{POSTGRES_VERSION}-windows-x64-binaries.zip"
POSTGRES_URL = f"https://get.enterprisedb.com/postgresql/{POSTGRES_ARCHIVE}"
POSTGRES_SHA256 = "f9aafca58e7026a1ef2caeee711acf761671e57904d430adc85f468374f5a821"
NODE_VERSION = "22.17.0"
NODE_ARCHIVE = f"node-v{NODE_VERSION}-win-x64.zip"
NODE_BASE_URL = f"https://nodejs.org/dist/v{NODE_VERSION}"
NODE_SHA256 = "721ab118a3aac8584348b132767eadf51379e0616f0db802cc1e66d7f0d98f85"
WINDOWS_BACKGROUND_FLAGS = getattr(subprocess, "CREATE_NO_WINDOW", 0)


class CliError(RuntimeError):
    pass


def info(message: str) -> None:
    print(f"[tuvtk] {message}")


def run(
    command: list[str | Path],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    check: bool = True,
    capture: bool = False,
    stdin=None,
    stdout=None,
) -> subprocess.CompletedProcess[str]:
    rendered = [str(part) for part in command]
    kwargs: dict[str, object] = {
        "cwd": str(cwd),
        "env": env,
        "check": check,
        "text": True,
    }
    if capture:
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.PIPE
    else:
        if stdin is not None:
            kwargs["stdin"] = stdin
        if stdout is not None:
            kwargs["stdout"] = stdout
    try:
        return subprocess.run(rendered, **kwargs)
    except FileNotFoundError as exc:
        raise CliError(f"required command was not found: {rendered[0]}") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip() if isinstance(exc.stderr, str) else ""
        suffix = f": {detail}" if detail else ""
        raise CliError(f"command failed with exit code {exc.returncode}: {' '.join(rendered)}{suffix}") from exc


def load_config() -> dict[str, object]:
    if not CONFIG_FILE.exists():
        return {}
    try:
        value = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CliError(f"invalid configuration file: {CONFIG_FILE}") from exc
    if not isinstance(value, dict):
        raise CliError(f"configuration root must be an object: {CONFIG_FILE}")
    return value


def save_config(config: dict[str, object]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    temporary = CONFIG_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(CONFIG_FILE)


def read_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def write_env(path: Path, values: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    remaining = dict(values)
    output: list[str] = []
    for line in existing_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=", 1)[0].strip()
            if key in remaining:
                output.append(f"{key}={remaining.pop(key)}")
                continue
        output.append(line)
    if output and output[-1] != "":
        output.append("")
    output.extend(f"{key}={value}" for key, value in remaining.items())
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    temporary.replace(path)


def file_digest(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, destination: Path, expected_sha256: str = "") -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and expected_sha256:
        if sha256_file(destination).lower() == expected_sha256.lower():
            return destination
    if destination.exists() and not expected_sha256:
        return destination
    temporary = destination.with_suffix(destination.suffix + ".part")
    info(f"Downloading {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "TUVTK installer/1"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response, temporary.open("wb") as output:
            shutil.copyfileobj(response, output, length=1024 * 1024)
    except Exception as exc:
        temporary.unlink(missing_ok=True)
        raise CliError(f"download failed: {url}: {exc}") from exc
    actual = sha256_file(temporary)
    if expected_sha256 and actual.lower() != expected_sha256.lower():
        temporary.unlink(missing_ok=True)
        raise CliError(f"checksum mismatch for {destination.name}")
    temporary.replace(destination)
    return destination


def safe_extract_zip(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            target = (destination / member.filename).resolve()
            if target != root and root not in target.parents:
                raise CliError(f"unsafe ZIP member: {member.filename}")
        bundle.extractall(destination)


def safe_extract_tar(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with tarfile.open(archive, "r:gz") as bundle:
        for member in bundle.getmembers():
            target = (destination / member.name).resolve()
            if target != root and root not in target.parents:
                raise CliError(f"unsafe backup member: {member.name}")
            if member.issym() or member.islnk():
                raise CliError(f"links are not allowed in backups: {member.name}")
        bundle.extractall(destination)


def validate_name(label: str, value: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.-]*", value):
        raise CliError(f"invalid {label}: {value}")
    return value


def validate_port(value: int) -> int:
    if not 1 <= value <= 65535:
        raise CliError(f"invalid port: {value}")
    return value


class LinuxDockerBackend:
    def __init__(self, config: dict[str, object]) -> None:
        self.config = config

    def _sudo(self, command: list[str]) -> list[str]:
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            return command
        if not shutil.which("sudo"):
            raise CliError("sudo is required to install Debian/Docker prerequisites")
        return ["sudo", "env", "TUVTK_LEGACY_INSTALL=1", "TUVTK_SKIP_COMMAND=true", *command]

    def setup(self, mode: str, *, domain: str = "", port: int = 8000, passthrough: list[str] | None = None) -> None:
        if mode == "prod" and not domain:
            raise CliError("production setup requires --domain=HOST")
        command = [
            "bash",
            str(ROOT / "install.sh"),
            "--production" if mode == "prod" else "--dev",
            "--yes",
            f"--app-dir={ROOT}",
        ]
        if mode == "prod":
            command.append(f"--domain={domain}")
        else:
            command.append(f"--dev-port={port}")
        command.extend(passthrough or [])
        environment = os.environ.copy()
        environment["TUVTK_LEGACY_INSTALL"] = "1"
        environment["TUVTK_SKIP_COMMAND"] = "true"
        run(self._sudo(command), env=environment)
        self.config.update(
            {
                "backend": "linux-docker",
                "default_mode": mode,
                "dev_port": port,
                "domain": domain,
            }
        )
        save_config(self.config)

    def ensure_setup(self, mode: str) -> None:
        env_file = DEV_ENV_FILE if mode == "dev" else Path("/etc/tuvtk/tuvtk.env")
        if env_file.exists():
            return
        if mode == "prod":
            raise CliError("production is not configured; run './install.sh deploy --domain=HOST'")
        self.setup("dev", port=int(self.config.get("dev_port", 8000)))

    def legacy_environment(self, mode: str) -> dict[str, str]:
        environment = os.environ.copy()
        environment.update(
            {
                "TUVTK_APP_DIR": str(ROOT),
                "TUVTK_COMPOSE_FILE": str(ROOT / "compose.yaml"),
                "TUVTK_DEV_COMPOSE_FILE": str(ROOT / "compose.dev.yaml"),
                "TUVTK_PROJECT_NAME": "tuvtk",
                "TUVTK_DEFAULT_MODE": mode,
                "TUVTK_DEV_PORT": str(self.config.get("dev_port", 8000)),
                "TUVTK_DEV_ENV_FILE": str(DEV_ENV_FILE),
                "TUVTK_PROD_ENV_FILE": "/etc/tuvtk/tuvtk.env",
                "TUVTK_BACKUP_DIR": str(self.config.get("backup_dir", "/opt/tuvtk-backups")),
            }
        )
        return environment

    def invoke(self, command: str, arguments: list[str], mode: str) -> None:
        self.ensure_setup(mode)
        run(["bash", ROOT / "bin" / "tuvtk", command, *arguments], env=self.legacy_environment(mode))

    def doctor(self) -> None:
        print("Backend: Linux Docker")
        print(f"Application: {ROOT}")
        print(f"Python router: {sys.version.split()[0]}")
        for label, command in (("bash", ["bash", "--version"]), ("docker", ["docker", "--version"]), ("compose", ["docker", "compose", "version"])):
            if not shutil.which(command[0]):
                state = "missing/unavailable"
            else:
                result = run(command, capture=True, check=False)
                state = "ok" if result.returncode == 0 else "missing/unavailable"
            print(f"{label}: {state}")
        print(f"Development environment: {'ready' if DEV_ENV_FILE.exists() else 'not configured'}")
        print(f"Production environment: {'ready' if Path('/etc/tuvtk/tuvtk.env').exists() else 'not configured'}")


class WindowsNativeBackend:
    def __init__(self, config: dict[str, object]) -> None:
        self.config = config
        self.port = int(config.get("dev_port", 8000))

    @property
    def venv_python(self) -> Path:
        return VENV_DIR / "Scripts" / "python.exe"

    def ensure_venv(self, *, force: bool = False) -> None:
        if self.venv_python.exists():
            result = run(
                [self.venv_python, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
                capture=True,
                check=False,
            )
            try:
                supported = result.returncode == 0 and tuple(map(int, result.stdout.strip().split("."))) >= (3, 12)
            except ValueError:
                supported = False
            if not supported:
                backup = ROOT / f".venv.python-backup-{time.strftime('%Y%m%d-%H%M%S')}"
                info(f"Preserving incompatible virtual environment as {backup.name}")
                VENV_DIR.replace(backup)
        if not self.venv_python.exists():
            if sys.version_info < (3, 12):
                raise CliError("Python 3.12+ is required; run through install.ps1 so it can bootstrap Python")
            info("Creating Python virtual environment")
            run([sys.executable, "-m", "venv", VENV_DIR])
        fingerprint = file_digest([ROOT / "requirements.txt", ROOT / "requirements-dev.txt"])
        marker = STATE_DIR / "requirements.sha256"
        if force or not marker.exists() or marker.read_text(encoding="ascii").strip() != fingerprint:
            info("Installing Python development requirements")
            run([self.venv_python, "-m", "pip", "install", "--disable-pip-version-check", "-r", ROOT / "requirements-dev.txt"])
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.write_text(fingerprint + "\n", encoding="ascii")

    def find_npm(self) -> Path | None:
        configured = self.config.get("npm")
        if configured and Path(str(configured)).exists():
            return Path(str(configured))
        found = shutil.which("npm.cmd") or shutil.which("npm")
        return Path(found) if found else None

    def node_supported(self, npm: Path) -> bool:
        node = npm.parent / "node.exe"
        found = shutil.which("node.exe")
        if not node.exists() and not found:
            return False
        executable = node if node.exists() else Path(found)
        result = run([executable, "--version"], capture=True, check=False)
        match = re.fullmatch(r"v(\d+)\.\d+\.\d+", result.stdout.strip())
        return result.returncode == 0 and bool(match) and int(match.group(1)) >= 22

    def ensure_node(self, *, force: bool = False) -> Path:
        npm = self.find_npm()
        if npm and not force and self.node_supported(npm):
            return npm
        archive = DOWNLOAD_DIR / NODE_ARCHIVE
        download(f"{NODE_BASE_URL}/{NODE_ARCHIVE}", archive, NODE_SHA256)
        node_root = RUNTIME_DIR / "node"
        if force and node_root.exists():
            shutil.rmtree(node_root)
        if not node_root.exists():
            with tempfile.TemporaryDirectory(dir=STATE_DIR) as temporary:
                temp_path = Path(temporary)
                safe_extract_zip(archive, temp_path)
                extracted = next(temp_path.glob("node-v*-win-x64"), None)
                if not extracted:
                    raise CliError("unexpected Node archive structure")
                node_root.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(extracted), str(node_root))
        npm = node_root / "npm.cmd"
        self.config["npm"] = str(npm)
        save_config(self.config)
        return npm

    def postgres_bin(self) -> Path | None:
        configured = self.config.get("postgres_bin")
        if configured and (Path(str(configured)) / "pg_ctl.exe").exists():
            return Path(str(configured))
        for candidate in POSTGRES_ROOT.glob("**/bin/pg_ctl.exe"):
            return candidate.parent
        return None

    def ensure_postgres_binaries(self, *, force: bool = False) -> Path:
        pg_bin = self.postgres_bin()
        if pg_bin and not force:
            return pg_bin
        url = os.environ.get("TUVTK_POSTGRES_URL", POSTGRES_URL)
        expected = os.environ.get("TUVTK_POSTGRES_SHA256", POSTGRES_SHA256 if url == POSTGRES_URL else "")
        if not expected:
            raise CliError("TUVTK_POSTGRES_SHA256 is required when TUVTK_POSTGRES_URL overrides the pinned archive")
        archive = download(url, DOWNLOAD_DIR / POSTGRES_ARCHIVE, expected)
        runtime = POSTGRES_ROOT / "runtime"
        if force and runtime.exists():
            shutil.rmtree(runtime)
        if not runtime.exists():
            safe_extract_zip(archive, runtime)
        pg_ctl = next(runtime.glob("**/bin/pg_ctl.exe"), None)
        if not pg_ctl:
            raise CliError("unexpected PostgreSQL archive structure")
        pg_bin = pg_ctl.parent
        version = run([pg_bin / "postgres.exe", "--version"], capture=True)
        if "postgres" not in version.stdout.lower():
            raise CliError("downloaded PostgreSQL runtime failed validation")
        self.config["postgres_bin"] = str(pg_bin)
        save_config(self.config)
        return pg_bin

    def prepare_environment(self) -> dict[str, str]:
        existing = read_env(ENV_FILE)
        values = read_env(ROOT / ".env.example")
        values.update(existing)
        values.update(
            {
                "POSTGRES_DB": values.get("POSTGRES_DB") or "platforma_tuvtk",
                "POSTGRES_USER": values.get("POSTGRES_USER") or "postgres",
                "POSTGRES_PASSWORD": existing.get("POSTGRES_PASSWORD") or secrets.token_hex(24),
                "POSTGRES_HOST": "127.0.0.1",
                "POSTGRES_PORT": values.get("POSTGRES_PORT") or "5432",
                "POSTGRES_CONN_MAX_AGE": "0",
                "DJANGO_DEPLOYMENT_MODE": "development",
                "DJANGO_SECRET_KEY": existing.get("DJANGO_SECRET_KEY") or secrets.token_urlsafe(48),
                "DJANGO_DEBUG": "true",
                "DJANGO_ALLOWED_HOSTS": "127.0.0.1,localhost,testserver",
                "DJANGO_CSRF_TRUSTED_ORIGINS": f"http://127.0.0.1:{self.port},http://localhost:{self.port}",
            }
        )
        validate_name("database name", values["POSTGRES_DB"])
        validate_name("database user", values["POSTGRES_USER"])
        validate_port(int(values["POSTGRES_PORT"]))
        write_env(ENV_FILE, values)
        return values

    def process_environment(self) -> dict[str, str]:
        environment = os.environ.copy()
        environment.update(read_env(ENV_FILE))
        npm = self.find_npm()
        pg_bin = self.postgres_bin()
        path_parts = []
        if npm:
            path_parts.append(str(npm.parent))
        if pg_bin:
            path_parts.append(str(pg_bin))
        if path_parts:
            environment["PATH"] = os.pathsep.join([*path_parts, environment.get("PATH", "")])
        if npm:
            environment["NPM_BIN_PATH"] = str(npm)
        environment["PGPASSWORD"] = environment.get("POSTGRES_PASSWORD", "")
        return environment

    def init_postgres(self, values: dict[str, str], pg_bin: Path) -> None:
        if (POSTGRES_DATA / "PG_VERSION").exists():
            return
        info(f"Initializing PostgreSQL data directory at {POSTGRES_DATA}")
        POSTGRES_DATA.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=STATE_DIR) as password_file:
            password_file.write(values["POSTGRES_PASSWORD"])
            password_path = Path(password_file.name)
        try:
            run(
                [
                    pg_bin / "initdb.exe",
                    "-D",
                    POSTGRES_DATA,
                    "-U",
                    values["POSTGRES_USER"],
                    "--encoding=UTF8",
                    "--locale=C",
                    "--auth=scram-sha-256",
                    f"--pwfile={password_path}",
                ],
                env=self.process_environment(),
            )
        finally:
            password_path.unlink(missing_ok=True)

    def postgres_ready(self, values: dict[str, str], pg_bin: Path) -> bool:
        result = run(
            [pg_bin / "pg_isready.exe", "-h", "127.0.0.1", "-p", values["POSTGRES_PORT"]],
            env=self.process_environment(),
            check=False,
            capture=True,
        )
        return result.returncode == 0

    def postgres_owned_running(self, pg_bin: Path) -> bool:
        result = run(
            [pg_bin / "pg_ctl.exe", "-D", POSTGRES_DATA, "status"],
            env=self.process_environment(),
            check=False,
            capture=True,
        )
        return result.returncode == 0

    def start_postgres(self) -> None:
        values = self.prepare_environment()
        pg_bin = self.ensure_postgres_binaries()
        self.init_postgres(values, pg_bin)
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        ready = self.postgres_ready(values, pg_bin)
        owned = self.postgres_owned_running(pg_bin)
        if ready and not owned:
            raise CliError(f"port {values['POSTGRES_PORT']} is already used by another PostgreSQL instance")
        if owned and not ready:
            raise CliError("the TUVTK PostgreSQL cluster is running on an unexpected host or port")
        if not owned:
            info("Starting PostgreSQL")
            run(
                [
                    pg_bin / "pg_ctl.exe",
                    "-D",
                    POSTGRES_DATA,
                    "-l",
                    LOG_DIR / "postgres.log",
                    "-o",
                    f"-h 127.0.0.1 -p {values['POSTGRES_PORT']}",
                    "start",
                ],
                env=self.process_environment(),
            )
        for _ in range(30):
            if self.postgres_ready(values, pg_bin):
                break
            time.sleep(1)
        else:
            raise CliError(f"PostgreSQL did not become ready; inspect {LOG_DIR / 'postgres.log'}")
        query = f"SELECT 1 FROM pg_database WHERE datname = '{values['POSTGRES_DB']}';"
        result = run(
            [pg_bin / "psql.exe", "-h", "127.0.0.1", "-p", values["POSTGRES_PORT"], "-U", values["POSTGRES_USER"], "-d", "postgres", "-Atc", query],
            env=self.process_environment(),
            capture=True,
        )
        if result.stdout.strip() != "1":
            info(f"Creating PostgreSQL database {values['POSTGRES_DB']}")
            run(
                [pg_bin / "createdb.exe", "-h", "127.0.0.1", "-p", values["POSTGRES_PORT"], "-U", values["POSTGRES_USER"], "--encoding=UTF8", "--template=template0", values["POSTGRES_DB"]],
                env=self.process_environment(),
            )

    def install_node_modules(self, *, force: bool = False) -> None:
        npm = self.ensure_node()
        package_files = [ROOT / "theme" / "static_src" / "package.json", ROOT / "theme" / "static_src" / "package-lock.json"]
        fingerprint = file_digest(package_files)
        marker = STATE_DIR / "node-modules.sha256"
        modules = ROOT / "theme" / "static_src" / "node_modules"
        if force or not modules.exists() or not marker.exists() or marker.read_text(encoding="ascii").strip() != fingerprint:
            info("Installing frontend dependencies")
            run([npm, "--prefix", ROOT / "theme" / "static_src", "ci"], env=self.process_environment())
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.write_text(fingerprint + "\n", encoding="ascii")

    def build_css(self) -> None:
        npm = self.ensure_node()
        self.install_node_modules()
        run([npm, "--prefix", ROOT / "theme" / "static_src", "run", "build"], env=self.process_environment())

    def setup(self, *, port: int = 8000, force: bool = False) -> None:
        if force:
            self.stop()
        self.port = port
        self.config.update({"backend": "windows-native", "default_mode": "dev", "dev_port": port})
        save_config(self.config)
        self.ensure_venv(force=force)
        self.prepare_environment()
        self.ensure_node(force=force)
        self.install_node_modules(force=force)
        self.ensure_postgres_binaries(force=force)
        self.start_postgres()
        self.build_css()
        self.django(["migrate", "--noinput"])
        info("Windows development environment is ready")

    def ensure_setup(self) -> bool:
        if not self.venv_python.exists() or not ENV_FILE.exists() or not self.postgres_bin():
            self.setup(port=self.port)
            return True
        return False

    def django(self, arguments: list[str]) -> None:
        self.ensure_venv()
        self.start_postgres()
        run([self.venv_python, ROOT / "manage.py", *arguments], env=self.process_environment())

    def pid_file(self, service: str) -> Path:
        return PID_DIR / f"{service}.pid"

    def process_running(self, service: str) -> bool:
        path = self.pid_file(service)
        if not path.exists():
            return False
        try:
            pid = int(path.read_text(encoding="ascii").strip())
            os.kill(pid, 0)
            return True
        except (OSError, ValueError):
            path.unlink(missing_ok=True)
            return False

    def spawn(self, service: str, command: list[str | Path]) -> None:
        if self.process_running(service):
            return
        PID_DIR.mkdir(parents=True, exist_ok=True)
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log = (LOG_DIR / f"{service}.log").open("a", encoding="utf-8")
        try:
            process = subprocess.Popen(
                [str(part) for part in command],
                cwd=str(ROOT),
                env=self.process_environment(),
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                creationflags=WINDOWS_BACKGROUND_FLAGS,
                close_fds=True,
            )
        finally:
            log.close()
        self.pid_file(service).write_text(f"{process.pid}\n", encoding="ascii")
        time.sleep(0.5)
        if process.poll() is not None:
            self.pid_file(service).unlink(missing_ok=True)
            raise CliError(f"{service} failed to start; inspect {LOG_DIR / (service + '.log')}")

    def prepare_development(self, *, prepared: bool = False) -> Path:
        prepared = self.ensure_setup() or prepared
        self.start_postgres()
        if not prepared:
            self.django(["migrate", "--noinput"])
            self.build_css()
        return self.ensure_node()

    def start(self, *, prepared: bool = False) -> None:
        npm = self.prepare_development(prepared=prepared)
        self.spawn("tailwind", [npm, "--prefix", ROOT / "theme" / "static_src", "run", "dev"])
        try:
            self.spawn("web", [self.venv_python, ROOT / "manage.py", "runserver", f"127.0.0.1:{self.port}"])
        except Exception:
            self.stop_process("tailwind")
            raise
        info(f"Development server: http://127.0.0.1:{self.port}")

    def dev_foreground(self, *, prepared: bool = False) -> None:
        self.stop_process("web")
        self.stop_process("tailwind")
        npm = self.prepare_development(prepared=prepared)
        commands = {
            "tailwind": [npm, "--prefix", ROOT / "theme" / "static_src", "run", "dev"],
            "web": [self.venv_python, ROOT / "manage.py", "runserver", f"127.0.0.1:{self.port}"],
        }
        environment = self.process_environment()
        processes: dict[str, subprocess.Popen[bytes]] = {}
        PID_DIR.mkdir(parents=True, exist_ok=True)
        try:
            for service, command in commands.items():
                process = subprocess.Popen(
                    [str(part) for part in command],
                    cwd=str(ROOT),
                    env=environment,
                )
                processes[service] = process
                self.pid_file(service).write_text(f"{process.pid}\n", encoding="ascii")
            info(f"Development server: http://127.0.0.1:{self.port} (press Ctrl+C to stop)")
            while True:
                for service, process in processes.items():
                    return_code = process.poll()
                    if return_code is None:
                        continue
                    if return_code != 0:
                        raise CliError(f"{service} exited with code {return_code}")
                    return
                time.sleep(0.25)
        except KeyboardInterrupt:
            info("Stopping Django and Tailwind")
        finally:
            for service, process in processes.items():
                if process.poll() is None:
                    run(["taskkill.exe", "/PID", str(process.pid), "/T", "/F"], check=False, capture=True)
                self.pid_file(service).unlink(missing_ok=True)

    def stop_process(self, service: str) -> None:
        path = self.pid_file(service)
        if not path.exists():
            return
        try:
            pid = int(path.read_text(encoding="ascii").strip())
        except ValueError:
            path.unlink(missing_ok=True)
            return
        run(["taskkill.exe", "/PID", str(pid), "/T", "/F"], check=False, capture=True)
        path.unlink(missing_ok=True)

    def stop(self) -> None:
        self.stop_process("web")
        self.stop_process("tailwind")
        pg_bin = self.postgres_bin()
        if pg_bin and (POSTGRES_DATA / "PG_VERSION").exists():
            run([pg_bin / "pg_ctl.exe", "-D", POSTGRES_DATA, "stop", "-m", "fast"], env=self.process_environment(), check=False)
        info("Windows development services stopped")

    def status(self) -> None:
        pg_bin = self.postgres_bin()
        postgres = bool(pg_bin and (POSTGRES_DATA / "PG_VERSION").exists() and self.postgres_owned_running(pg_bin))
        print(f"postgres: {'running' if postgres else 'stopped'}")
        print(f"web: {'running' if self.process_running('web') else 'stopped'}")
        print(f"tailwind: {'running' if self.process_running('tailwind') else 'stopped'}")
        if self.process_running("web"):
            print(f"url: http://127.0.0.1:{self.port}")

    def logs(self, service: str = "") -> None:
        services = [service] if service else ["postgres", "web", "tailwind"]
        positions: dict[Path, int] = {}
        for name in services:
            path = LOG_DIR / f"{name}.log"
            if path.exists():
                positions[path] = 0
        if not positions:
            raise CliError("no logs are available")
        try:
            while True:
                for path, position in list(positions.items()):
                    with path.open("r", encoding="utf-8", errors="replace") as source:
                        source.seek(position)
                        for line in source:
                            print(f"[{path.stem}] {line}", end="")
                        positions[path] = source.tell()
                time.sleep(0.5)
        except KeyboardInterrupt:
            return

    def npm(self, arguments: list[str]) -> None:
        npm = self.ensure_node()
        self.install_node_modules()
        run([npm, "--prefix", ROOT / "theme" / "static_src", *arguments], env=self.process_environment())

    def export_sql(self, destination: str) -> Path:
        self.start_postgres()
        values = read_env(ENV_FILE)
        pg_bin = self.ensure_postgres_binaries()
        requested = Path(destination).expanduser()
        if requested.suffix.lower() != ".sql":
            requested.mkdir(parents=True, exist_ok=True)
            requested = requested / f"tuvtk-dev-{time.strftime('%Y-%m-%d_%H%M%S', time.gmtime())}.sql"
        requested.parent.mkdir(parents=True, exist_ok=True)
        temporary = requested.with_suffix(requested.suffix + ".tmp")
        with temporary.open("w", encoding="utf-8", newline="\n") as output:
            output.write("-- TUVTK_MODE=dev\n")
            run(
                [pg_bin / "pg_dump.exe", "-h", "127.0.0.1", "-p", values["POSTGRES_PORT"], "-U", values["POSTGRES_USER"], "-d", values["POSTGRES_DB"]],
                env=self.process_environment(),
                stdout=output,
            )
        temporary.replace(requested)
        info(f"Database exported: {requested}")
        return requested

    def import_sql(self, source: str, confirmed: bool) -> None:
        sql = Path(source).expanduser().resolve()
        if not sql.is_file():
            raise CliError(f"SQL file not found: {sql}")
        first_lines = "\n".join(sql.read_text(encoding="utf-8", errors="replace").splitlines()[:20])
        if "TUVTK_MODE=prod" in first_lines:
            raise CliError("production SQL cannot be imported into Windows development")
        if not confirmed:
            answer = input(f"Replace the Windows development database from {sql}? [y/N] ").strip().lower()
            if answer not in {"y", "yes"}:
                raise CliError("operation cancelled")
        self.stop_process("web")
        self.stop_process("tailwind")
        self.start_postgres()
        values = read_env(ENV_FILE)
        pg_bin = self.ensure_postgres_binaries()
        common = ["-h", "127.0.0.1", "-p", values["POSTGRES_PORT"], "-U", values["POSTGRES_USER"]]
        run([pg_bin / "dropdb.exe", *common, "--force", "--if-exists", values["POSTGRES_DB"]], env=self.process_environment())
        run([pg_bin / "createdb.exe", *common, "--encoding=UTF8", "--template=template0", values["POSTGRES_DB"]], env=self.process_environment())
        with sql.open("r", encoding="utf-8") as input_file:
            run([pg_bin / "psql.exe", *common, "-v", "ON_ERROR_STOP=1", "-d", values["POSTGRES_DB"]], env=self.process_environment(), stdin=input_file)
        info("Database imported; application services remain stopped")

    def backup(self, destination: str) -> None:
        output_dir = Path(destination).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        archive = output_dir / f"{time.strftime('%Y-%m-%d_%H%M%S', time.gmtime())}-tuvtk-dev.tar.gz"
        with tempfile.TemporaryDirectory(dir=STATE_DIR) as temporary:
            staging = Path(temporary)
            self.export_sql(str(staging / "database.sql"))
            shutil.copy2(ENV_FILE, staging / ".env")
            (staging / "manifest.json").write_text(json.dumps({"format": "tuvtk-backup-v2", "mode": "dev"}) + "\n", encoding="utf-8")
            with tarfile.open(archive, "w:gz") as bundle:
                for item in (staging / "manifest.json", staging / "database.sql", staging / ".env"):
                    bundle.add(item, arcname=item.name)
                for directory in (ROOT / "media", ROOT / "private_media"):
                    if directory.exists():
                        bundle.add(directory, arcname=directory.name)
        info(f"Backup created: {archive}")

    def restore(self, archive_name: str, confirmed: bool) -> None:
        archive = Path(archive_name).expanduser().resolve()
        if not archive.is_file():
            raise CliError(f"backup not found: {archive}")
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        if not confirmed:
            answer = input(f"Restore Windows development from {archive}? [y/N] ").strip().lower()
            if answer not in {"y", "yes"}:
                raise CliError("operation cancelled")
        with tempfile.TemporaryDirectory(dir=STATE_DIR) as temporary:
            staging = Path(temporary)
            safe_extract_tar(archive, staging)
            manifest = json.loads((staging / "manifest.json").read_text(encoding="utf-8"))
            if manifest.get("format") != "tuvtk-backup-v2" or manifest.get("mode") != "dev":
                raise CliError("backup is not a compatible development archive")
            self.import_sql(str(staging / "database.sql"), True)
            for name in ("media", "private_media"):
                source = staging / name
                target = ROOT / name
                if source.exists():
                    target.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(source, target, dirs_exist_ok=True)
        info("Backup restored; application services remain stopped")

    def reset_database(self, confirmed: bool, start_after: bool) -> None:
        if not confirmed:
            answer = input("Delete and recreate the Windows development database? [y/N] ").strip().lower()
            if answer not in {"y", "yes"}:
                raise CliError("operation cancelled")
        self.stop()
        if POSTGRES_DATA.exists():
            shutil.rmtree(POSTGRES_DATA)
        self.start_postgres()
        self.django(["migrate", "--noinput"])
        if start_after:
            self.start()

    def clean(self) -> None:
        for path in ROOT.rglob("__pycache__"):
            if ".venv" not in path.parts and ".git" not in path.parts:
                shutil.rmtree(path, ignore_errors=True)
        for relative in ("tmp", "test-results", "playwright-report"):
            shutil.rmtree(ROOT / relative, ignore_errors=True)
        info("Removed safe generated caches; runtimes, database, media, and environments were preserved")

    def doctor(self) -> None:
        print("Backend: Windows native")
        print(f"Application: {ROOT}")
        print(f"Router Python: {sys.version.split()[0]}")
        print(f"Virtual environment: {'ready' if self.venv_python.exists() else 'not configured'}")
        print(f"Node: {self.find_npm() or 'not configured'}")
        print(f"PostgreSQL: {self.postgres_bin() or 'not configured'}")
        print(f"Environment: {'ready' if ENV_FILE.exists() else 'not configured'}")
        self.status()


HELP = """\
Use the launcher for your OS:
  Windows: install.cmd COMMAND [ARGS...]
  Linux:   ./install.sh COMMAND [ARGS...]

PowerShell can use .\\install.ps1 COMMAND [ARGS...].

Setup and servers:
  setup dev [--port=PORT]        Prepare development without starting servers
  dev [--port=PORT]              Start the development server in this terminal
  start, stop, restart, status   Manage the configured default stack
  logs [SERVICE]                 Follow default-stack logs
  deploy --domain=HOST           Prepare, build, and start Linux production
  prod-start, prod-stop          Start or stop Linux production explicitly
  prod-status, prod-logs [SVC]   Inspect Linux production explicitly

Database and data:
  fresh-db [--yes] [--start]     Reset the development database and optionally start dev
  dev-db-reset [--yes] [--start] Same as fresh-db
  backup DIRECTORY               Back up the default mode
  restore ARCHIVE [--yes]        Restore the default mode
  export-sql PATH                Export default-mode PostgreSQL
  import-sql FILE [--yes]        Replace default-mode PostgreSQL from SQL
  prod-db-reset --yes-i-understand-this-deletes-production-data
                                  Reset Linux production data; creates a backup first

Django and frontend:
  check
  test [TARGET] [ARGS...]
  migrate [ARGS...]
  makemigrations [APP] [ARGS...]
  collectstatic
  shell, dbshell
  django COMMAND [ARGS...]
  tailwind
  npm COMMAND [ARGS...]

Maintenance:
  build, rebuild                 Build or rebuild the configured stack
  doctor                         Report dependency and service status
  context [ARGS...]
  clean                          Remove safe caches and temporary test artifacts

The command vocabulary is shared. Windows production commands are visible but
exit with an explanation because production deployment is Debian/Docker only.
Linux production setup accepts installer options such as --http-port=PORT,
--data-dir=PATH, --env-file=PATH, --project-name=NAME, and database credentials.
"""


def option_value(arguments: list[str], name: str, default: str = "") -> str:
    for index, argument in enumerate(arguments):
        if argument.startswith(name + "="):
            return argument.split("=", 1)[1]
        if argument == name and index + 1 < len(arguments):
            return arguments[index + 1]
    return default


def selected_setup_domain(arguments: list[str]) -> str:
    return option_value(arguments, "--domain") or option_value(arguments, "--public-host")


def selected_setup_port(arguments: list[str], config: dict[str, object]) -> int:
    default = str(config.get("dev_port", 8000))
    return validate_port(int(option_value(arguments, "--port", option_value(arguments, "--dev-port", default))))


def linux_setup_passthrough(arguments: list[str]) -> list[str]:
    remaining = list(arguments)
    if remaining and remaining[0] in {"dev", "prod", "production"}:
        remaining = remaining[1:]
    passthrough: list[str] = []
    skip_next = False
    for argument in remaining:
        if skip_next:
            skip_next = False
            continue
        if argument == "--force":
            continue
        if argument == "--port":
            skip_next = True
            continue
        if argument.startswith("--port="):
            continue
        passthrough.append(argument)
    return passthrough


def selected_mode(config: dict[str, object]) -> str:
    mode = str(config.get("default_mode", "dev"))
    return mode if mode in {"dev", "prod"} else "dev"


def main(arguments: list[str]) -> int:
    command = arguments[0] if arguments else "help"
    rest = arguments[1:]
    if command in {"help", "-h", "--help"}:
        print(HELP)
        return 0
    if command == "context":
        run([self_python(), ROOT / "scripts" / "generate_codex_context.py", *rest])
        return 0

    config = load_config()
    backend = WindowsNativeBackend(config) if IS_WINDOWS else LinuxDockerBackend(config)
    mode = selected_mode(config)

    if command == "doctor":
        backend.doctor()
        return 0
    if command == "setup":
        requested = rest[0] if rest and not rest[0].startswith("-") else "dev"
        if requested not in {"dev", "prod", "production"}:
            raise CliError("setup mode must be dev or production")
        requested_mode = "prod" if requested in {"prod", "production"} else "dev"
        port = selected_setup_port(rest, config)
        if IS_WINDOWS:
            if requested_mode == "prod":
                raise CliError("production deployment is supported only on Debian/Docker")
            backend.setup(port=port, force="--force" in rest)
        else:
            backend.setup(
                requested_mode,
                domain=selected_setup_domain(rest),
                port=port,
                passthrough=linux_setup_passthrough(rest),
            )
        return 0
    if command in {"dev", "dev-start"}:
        port = selected_setup_port(rest, config)
        if IS_WINDOWS:
            prepared = False
            if not config or port != backend.port:
                backend.setup(port=port)
                prepared = True
            backend.dev_foreground(prepared=prepared)
        else:
            if not DEV_ENV_FILE.exists() or port != int(config.get("dev_port", -1)):
                backend.setup("dev", port=port, passthrough=linux_setup_passthrough(rest))
            backend.invoke("dev", [], "dev")
        return 0
    if command == "deploy":
        if IS_WINDOWS:
            raise CliError("production deployment is supported only on Debian/Docker")
        domain = selected_setup_domain(rest)
        backend.setup("prod", domain=domain, passthrough=linux_setup_passthrough(rest))
        backend.invoke("prod-build", [], "prod")
        return 0

    if IS_WINDOWS:
        if command in {"prod-start", "prod-stop", "prod-status", "prod-build", "prod-rebuild", "prod-logs", "prod-django", "prod-backup", "prod-restore", "prod-export-sql", "prod-import-sql", "prod-db-reset"}:
            raise CliError("production commands are supported only on Debian/Docker")
        if command in {"start", "up"}:
            backend.start()
        elif command in {"stop", "down", "dev-stop"}:
            backend.stop()
        elif command == "restart":
            backend.stop(); backend.start()
        elif command in {"status", "ps", "dev-status"}:
            backend.status()
        elif command in {"logs", "dev-logs"}:
            backend.logs(rest[0] if rest else "")
        elif command in {"build", "rebuild", "dev-build"}:
            backend.setup(port=backend.port, force=command == "rebuild")
            backend.start(prepared=True)
        elif command == "check":
            backend.django(["check"])
        elif command == "test":
            test_args = list(rest)
            if not any(item in {"-v", "--verbosity"} or item.startswith("--verbosity=") for item in test_args):
                test_args.extend(["-v", "0"])
            backend.django(["test", *test_args])
        elif command in {"migrate", "makemigrations"}:
            backend.django([command, *rest])
        elif command == "collectstatic":
            backend.django(["collectstatic", "--noinput"])
        elif command in {"shell", "dbshell"}:
            backend.django([command])
        elif command in {"django", "dev-django"}:
            if not rest:
                raise CliError(f"usage: {command} COMMAND [ARGS...]")
            backend.django(rest)
        elif command == "tailwind":
            backend.npm(["run", "dev"])
        elif command == "npm":
            if not rest:
                raise CliError("usage: npm COMMAND [ARGS...]")
            backend.npm(rest)
        elif command in {"export-sql", "dev-export-sql"}:
            if len(rest) != 1:
                raise CliError(f"usage: {command} PATH")
            backend.export_sql(rest[0])
        elif command in {"import-sql", "dev-import-sql"}:
            files = [item for item in rest if item != "--yes"]
            if len(files) != 1:
                raise CliError(f"usage: {command} FILE [--yes]")
            backend.import_sql(files[0], "--yes" in rest)
        elif command in {"backup", "dev-backup"}:
            if len(rest) != 1:
                raise CliError(f"usage: {command} DIRECTORY")
            backend.backup(rest[0])
        elif command in {"restore", "dev-restore"}:
            files = [item for item in rest if item != "--yes"]
            if len(files) != 1:
                raise CliError(f"usage: {command} ARCHIVE [--yes]")
            backend.restore(files[0], "--yes" in rest)
        elif command in {"dev-db-reset", "fresh-db"}:
            backend.reset_database("--yes" in rest, "--start" in rest)
        elif command == "clean":
            backend.clean()
        elif command == "exec":
            raise CliError("exec targets Compose services and is unavailable in Windows-native development")
        else:
            raise CliError(f"unknown command: {command} (run './install.sh help')")
        return 0

    if command == "clean":
        run(["bash", ROOT / "bin" / "tuvtk", "clean"], env=backend.legacy_environment(mode))
        return 0
    if command == "fresh-db":
        backend.invoke("fresh-db", rest, "dev")
        return 0
    command_mode = "prod" if command.startswith("prod-") else "dev" if command.startswith("dev-") else mode
    backend.invoke(command, rest, command_mode)
    return 0


def self_python() -> str:
    return str(sys.executable)


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (CliError, ValueError) as exc:
        print(f"tuvtk: ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
```

## `start_postgres.bat`

Size: 119 B

```batch
@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" setup dev
exit /b %ERRORLEVEL%
```

## `stop_postgres.bat`

Size: 114 B

```batch
@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" stop
exit /b %ERRORLEVEL%
```

## `theme/__init__.py`

Size: 0 B

```python
```

## `theme/AGENTS.md`

Size: 1.3 KB

````markdown
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
````

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

## `theme/static/js/sidebar_state.js`

Size: 561 B

```javascript
(() => {
    const toggle = document.getElementById("ops-sidebar");
    if (!toggle) return;

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
})();
```

## `theme/static_src/.gitignore`

Size: 13 B

```text
node_modules
```

## `theme/static_src/package-lock.json`

Size: 73.8 KB

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
      "dependencies": {
        "alpinejs": "3.15.12",
        "htmx.org": "2.0.10"
      },
      "devDependencies": {
        "@tailwindcss/postcss": "^4.3.0",
        "cross-env": "^10.1.0",
        "daisyui": "^5.5.23",
        "postcss": "^8.5.15",
        "postcss-cli": "^11.0.1",
        "rimraf": "^6.1.3",
        "shx": "0.4.0",
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
    "node_modules/@tailwindcss/oxide-wasm32-wasi/node_modules/@emnapi/core": {
      "version": "1.11.1",
      "dev": true,
      "inBundle": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "@emnapi/wasi-threads": "1.2.2",
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@tailwindcss/oxide-wasm32-wasi/node_modules/@emnapi/runtime": {
      "version": "1.11.1",
      "dev": true,
      "inBundle": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@tailwindcss/oxide-wasm32-wasi/node_modules/@emnapi/wasi-threads": {
      "version": "1.2.2",
      "dev": true,
      "inBundle": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@tailwindcss/oxide-wasm32-wasi/node_modules/@napi-rs/wasm-runtime": {
      "version": "1.1.4",
      "dev": true,
      "inBundle": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "@tybys/wasm-util": "^0.10.1"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/Brooooooklyn"
      },
      "peerDependencies": {
        "@emnapi/core": "^1.7.1",
        "@emnapi/runtime": "^1.7.1"
      }
    },
    "node_modules/@tailwindcss/oxide-wasm32-wasi/node_modules/@tybys/wasm-util": {
      "version": "0.10.2",
      "dev": true,
      "inBundle": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@tailwindcss/oxide-wasm32-wasi/node_modules/tslib": {
      "version": "2.8.1",
      "dev": true,
      "inBundle": true,
      "license": "0BSD",
      "optional": true
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
    "node_modules/@vue/reactivity": {
      "version": "3.1.5",
      "resolved": "https://registry.npmjs.org/@vue/reactivity/-/reactivity-3.1.5.tgz",
      "integrity": "sha512-1tdfLmNjWG6t/CsPldh+foumYFo3cpyCHgBYQ34ylaMsJ+SNHQ1kApMIa8jN+i593zQuaw3AdWH0nJTARzCFhg==",
      "license": "MIT",
      "dependencies": {
        "@vue/shared": "3.1.5"
      }
    },
    "node_modules/@vue/shared": {
      "version": "3.1.5",
      "resolved": "https://registry.npmjs.org/@vue/shared/-/shared-3.1.5.tgz",
      "integrity": "sha512-oJ4F3TnvpXaQwZJNF3ZK+kLPHKarDmJjJ6jyzVNDKH9md1dptjC7lWR//jrGuLdek/U6iltWxqAnYOu8gCiOvA==",
      "license": "MIT"
    },
    "node_modules/alpinejs": {
      "version": "3.15.12",
      "resolved": "https://registry.npmjs.org/alpinejs/-/alpinejs-3.15.12.tgz",
      "integrity": "sha512-nJvPAQVNPdZZ0NrExJ/kzQco3ijR8LwvCOadQecllESiqT4NyZ/57sN9V2XyvhlBGAbmlKYgeWZvYdKq99ij/Q==",
      "license": "MIT",
      "dependencies": {
        "@vue/reactivity": "~3.1.1"
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
    "node_modules/end-of-stream": {
      "version": "1.4.5",
      "resolved": "https://registry.npmjs.org/end-of-stream/-/end-of-stream-1.4.5.tgz",
      "integrity": "sha512-ooEGc6HP26xXq/N+GCGOT0JKCLDGrq2bQUZrQ7gyrJiZANJ/8YDTxTpQBXGMn+WbIQXNVpyWymm7KYVICQnyOg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "once": "^1.4.0"
      }
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
    "node_modules/execa": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/execa/-/execa-1.0.0.tgz",
      "integrity": "sha512-adbxcyWV46qiHyvSp50TKt05tB4tK3HcmF7/nxfAdhnox83seTDbwnaqKO4sXRy7roHAIFqJP/Rw/AuEbX61LA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "cross-spawn": "^6.0.0",
        "get-stream": "^4.0.0",
        "is-stream": "^1.1.0",
        "npm-run-path": "^2.0.0",
        "p-finally": "^1.0.0",
        "signal-exit": "^3.0.0",
        "strip-eof": "^1.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/execa/node_modules/cross-spawn": {
      "version": "6.0.6",
      "resolved": "https://registry.npmjs.org/cross-spawn/-/cross-spawn-6.0.6.tgz",
      "integrity": "sha512-VqCUuhcd1iB+dsv8gxPttb5iZh/D0iubSP21g36KXdEuf6I5JiioesUVjpCdHV9MZRUfVFlvwtIUyPfxo5trtw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "nice-try": "^1.0.4",
        "path-key": "^2.0.1",
        "semver": "^5.5.0",
        "shebang-command": "^1.2.0",
        "which": "^1.2.9"
      },
      "engines": {
        "node": ">=4.8"
      }
    },
    "node_modules/execa/node_modules/path-key": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/path-key/-/path-key-2.0.1.tgz",
      "integrity": "sha512-fEHGKCSmUSDPv4uoj8AlD+joPlq3peND+HRYyxFz4KPw4z926S/b8rIuFs2FYJg3BwsxJf6A9/3eIdLaYC+9Dw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/execa/node_modules/shebang-command": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/shebang-command/-/shebang-command-1.2.0.tgz",
      "integrity": "sha512-EV3L1+UQWGor21OmnvojK36mhg+TyIKDh3iFBKBohr5xeXIhNBcx8oWdgkTEEQ+BEFFYdLRuqMfd5L84N1V5Vg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "shebang-regex": "^1.0.0"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/execa/node_modules/shebang-regex": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/shebang-regex/-/shebang-regex-1.0.0.tgz",
      "integrity": "sha512-wpoSFAxys6b2a2wHZ1XpDSgD7N9iVjg29Ph9uV/uaP9Ex/KXlkTZTeddxDPSYQpgvzKLGJke2UU0AzoGCjNIvQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/execa/node_modules/which": {
      "version": "1.3.1",
      "resolved": "https://registry.npmjs.org/which/-/which-1.3.1.tgz",
      "integrity": "sha512-HxJdYWq1MTIQbJ3nw0cqssHoTNU267KlrDuGZ1WYlxDStUtKUhOaJmh112/TZmHxxUfuJqPXSOm7tDyas0OSIQ==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "isexe": "^2.0.0"
      },
      "bin": {
        "which": "bin/which"
      }
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
    "node_modules/get-stream": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/get-stream/-/get-stream-4.1.0.tgz",
      "integrity": "sha512-GMat4EJ5161kIy2HevLlr4luNjBgvmj413KaQA7jt4V8B4RDsfpHk7WQ9GVqfYyyx8OS/L66Kox+rJRNklLK7w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "pump": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
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
    "node_modules/htmx.org": {
      "version": "2.0.10",
      "resolved": "https://registry.npmjs.org/htmx.org/-/htmx.org-2.0.10.tgz",
      "integrity": "sha512-kdeJe7ZVwaS6QMz/ebBIVtZdpwen6L0OQ5GOhPV9MKBb196TCZeZu4yA7ZIQsaLKv7EpXz+So7KSXNuHXhj7Cw==",
      "license": "0BSD"
    },
    "node_modules/interpret": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/interpret/-/interpret-1.4.0.tgz",
      "integrity": "sha512-agE4QfB2Lkp9uICn7BAqoscw4SZP9kTE2hxiFI3jBPmXJfdqiahTbUuKGsMoN2GtqL9AxhYioAcVvgsb1HvRbA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.10"
      }
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
    "node_modules/is-core-module": {
      "version": "2.16.2",
      "resolved": "https://registry.npmjs.org/is-core-module/-/is-core-module-2.16.2.tgz",
      "integrity": "sha512-evOr8xfXKxE6qSR0hSXL2r3sd7ALj8+7jQEUvPYcm5sgZFdJ+AYzT6yNmJenvIYQBgIGwfwz08sL8zoL7yq2BA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "hasown": "^2.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
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
    "node_modules/is-stream": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/is-stream/-/is-stream-1.1.0.tgz",
      "integrity": "sha512-uQPm8kcs47jx38atAcWTVxyltQYoPT68y9aWYdV6yWXSyW8mzSat0TL6CiWdZeCdF3KrAvpVtnHbTv4RN+rqdQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
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
    "node_modules/nice-try": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/nice-try/-/nice-try-1.0.5.tgz",
      "integrity": "sha512-1nh45deeb5olNY7eX82BkPO7SSxR5SSYJiPTrTdFUVYwAl8CKMA5N9PjTYkHiRjisVcxcQ1HXdLhx2qxxJzLNQ==",
      "dev": true,
      "license": "MIT"
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
    "node_modules/npm-run-path": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/npm-run-path/-/npm-run-path-2.0.2.tgz",
      "integrity": "sha512-lJxZYlT4DW/bRUtFh1MQIWqmLwQfAxnqWG4HhEdjMlkrJYnJn0Jrr2u3mgxqaWsdiBc76TYkTG/mhrnYTuzfHw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "path-key": "^2.0.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/npm-run-path/node_modules/path-key": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/path-key/-/path-key-2.0.1.tgz",
      "integrity": "sha512-fEHGKCSmUSDPv4uoj8AlD+joPlq3peND+HRYyxFz4KPw4z926S/b8rIuFs2FYJg3BwsxJf6A9/3eIdLaYC+9Dw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=4"
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
    "node_modules/p-finally": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/p-finally/-/p-finally-1.0.0.tgz",
      "integrity": "sha512-LICb2p9CB7FS+0eR1oqWnHhp0FljGLZCWBE9aix0Uye9W8LTQPwMTYVGWQWIw9RdQiDg4+epXQODwIYJtSJaow==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=4"
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
    "node_modules/path-parse": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/path-parse/-/path-parse-1.0.7.tgz",
      "integrity": "sha512-LDJzPVEEEPR+y48z93A0Ed0yXb8pAByGWo/k5YYdYgpY2/2EsOsksJrq7lOHxryrVOn1ejG6oAp8ahvOIQD8sw==",
      "dev": true,
      "license": "MIT"
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
    "node_modules/pump": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/pump/-/pump-3.0.4.tgz",
      "integrity": "sha512-VS7sjc6KR7e1ukRFhQSY5LM2uBWAUPiOPa/A3mkKmiMwSmRFUITt0xuj+/lesgnCv+dPIEYlkzrcyXgquIHMcA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "end-of-stream": "^1.1.0",
        "once": "^1.3.1"
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
    "node_modules/rechoir": {
      "version": "0.6.2",
      "resolved": "https://registry.npmjs.org/rechoir/-/rechoir-0.6.2.tgz",
      "integrity": "sha512-HFM8rkZ+i3zrV+4LQjwQ0W+ez98pApMGM3HUrN04j3CqzPOzl9nmP15Y8YXNm8QHGv/eacOVEjqhmWpkRV0NAw==",
      "dev": true,
      "dependencies": {
        "resolve": "^1.1.6"
      },
      "engines": {
        "node": ">= 0.10"
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
    "node_modules/resolve": {
      "version": "1.22.12",
      "resolved": "https://registry.npmjs.org/resolve/-/resolve-1.22.12.tgz",
      "integrity": "sha512-TyeJ1zif53BPfHootBGwPRYT1RUt6oGWsaQr8UyZW/eAm9bKoijtvruSDEmZHm92CwS9nj7/fWttqPCgzep8CA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "is-core-module": "^2.16.1",
        "path-parse": "^1.0.7",
        "supports-preserve-symlinks-flag": "^1.0.0"
      },
      "bin": {
        "resolve": "bin/resolve"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
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
    "node_modules/semver": {
      "version": "5.7.2",
      "resolved": "https://registry.npmjs.org/semver/-/semver-5.7.2.tgz",
      "integrity": "sha512-cBznnQ9KjJqU67B52RMC65CMarK2600WFnbkcaiwWq3xy/5haFJlshgnpjovMVJ+Hff49d8GEn0b87C5pDQ10g==",
      "dev": true,
      "license": "ISC",
      "bin": {
        "semver": "bin/semver"
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
    "node_modules/shelljs": {
      "version": "0.9.2",
      "resolved": "https://registry.npmjs.org/shelljs/-/shelljs-0.9.2.tgz",
      "integrity": "sha512-S3I64fEiKgTZzKCC46zT/Ib9meqofLrQVbpSswtjFfAVDW+AZ54WTnAM/3/yENoxz/V1Cy6u3kiiEbQ4DNphvw==",
      "dev": true,
      "license": "BSD-3-Clause",
      "dependencies": {
        "execa": "^1.0.0",
        "fast-glob": "^3.3.2",
        "interpret": "^1.0.0",
        "rechoir": "^0.6.2"
      },
      "bin": {
        "shjs": "bin/shjs"
      },
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/shx": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/shx/-/shx-0.4.0.tgz",
      "integrity": "sha512-Z0KixSIlGPpijKgcH6oCMCbltPImvaKy0sGH8AkLRXw1KyzpKtaCTizP2xen+hNDqVF4xxgvA0KXSb9o4Q6hnA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "minimist": "^1.2.8",
        "shelljs": "^0.9.2"
      },
      "bin": {
        "shx": "lib/cli.js"
      },
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/signal-exit": {
      "version": "3.0.7",
      "resolved": "https://registry.npmjs.org/signal-exit/-/signal-exit-3.0.7.tgz",
      "integrity": "sha512-wnD2ZE+l+SPC/uoS0vXeE9L1+0wuaMqKlfz9AMUo38JsyLSBWSFcHR1Rri62LZc12vLr1gb3jl7iwQhgwpAbGQ==",
      "dev": true,
      "license": "ISC"
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
    "node_modules/strip-eof": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/strip-eof/-/strip-eof-1.0.0.tgz",
      "integrity": "sha512-7FCwGGmx8mD5xQd3RPUvnSpUXHM3BWuzjtpD4TXsfcZ9EL4azvVVUscFYwD9nx8Kh+uCBC00XBtAykoMHwTh8Q==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/supports-preserve-symlinks-flag": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/supports-preserve-symlinks-flag/-/supports-preserve-symlinks-flag-1.0.0.tgz",
      "integrity": "sha512-ot0WnXS9fgdkgIcePe6RHNk1WA8+muPa6cSjeR3V8K27q9BB1rTE3R1p7Hv0z1ZyAc8s6Vvv8DIyWf681MAt0w==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
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
    "node_modules/wrappy": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/wrappy/-/wrappy-1.0.2.tgz",
      "integrity": "sha512-l4Sp/DRseor9wL6EvV2+TuQn63dMkPjZ/sp9XkghTEbV9KlPS1xUsZ3u7/IQO4wxtcFB4bgpQPRcR3QCvezPcQ==",
      "dev": true,
      "license": "ISC"
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

Size: 1.1 KB

```json
{
  "name": "theme",
  "version": "4.5.0",
  "description": "",
  "scripts": {
    "start": "npm run dev",
    "build": "npm run build:clean && npm run build:tailwind && npm run build:vendor",
    "build:clean": "rimraf ../static/css/dist",
    "build:tailwind": "cross-env NODE_ENV=production postcss ./src/styles.css -o ../static/css/dist/styles.css --minify",
    "build:vendor": "shx mkdir -p ../static/js/vendor && shx cp node_modules/htmx.org/dist/htmx.min.js ../static/js/vendor/htmx.min.js && shx cp node_modules/alpinejs/dist/cdn.min.js ../static/js/vendor/alpine.min.js",
    "dev": "cross-env NODE_ENV=development CHOKIDAR_USEPOLLING=1 CHOKIDAR_INTERVAL=300 postcss ./src/styles.css -o ../static/css/dist/styles.css --watch"
  },
  "keywords": [],
  "author": "",
  "license": "MIT",
  "devDependencies": {
    "@tailwindcss/postcss": "^4.3.0",
    "cross-env": "^10.1.0",
    "daisyui": "^5.5.23",
    "postcss": "^8.5.15",
    "postcss-cli": "^11.0.1",
    "rimraf": "^6.1.3",
    "shx": "0.4.0",
    "tailwindcss": "^4.3.0"
  },
  "dependencies": {
    "alpinejs": "3.15.12",
    "htmx.org": "2.0.10"
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

Size: 26.6 KB

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

## `watch_tailwind.ps1`

Size: 156 B

```powershell
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $root 'install.ps1') tailwind @args
exit $LASTEXITCODE
```
