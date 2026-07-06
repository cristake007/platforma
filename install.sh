#!/usr/bin/env bash
set -Eeuo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
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
SECRET_KEY=""
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
    apt-get install --yes ca-certificates curl git openssh-client openssl iproute2
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
    ensure_env_value "$DEV_ENV_FILE" TUVTK_HTTP_PORT "$DEV_PORT"
    ensure_env_value "$DEV_ENV_FILE" POSTGRES_DB platforma_tuvtk
    ensure_env_value "$DEV_ENV_FILE" POSTGRES_USER postgres
    ensure_env_value "$DEV_ENV_FILE" POSTGRES_PASSWORD "$(openssl rand -hex 32)"
    ensure_env_value "$DEV_ENV_FILE" DJANGO_SECRET_KEY "$(openssl rand -hex 48)"
    ensure_env_value "$DEV_ENV_FILE" DJANGO_ALLOWED_HOSTS "127.0.0.1,localhost,[::1]"
    ensure_env_value "$DEV_ENV_FILE" DJANGO_CSRF_TRUSTED_ORIGINS "http://127.0.0.1:${DEV_PORT},http://localhost:${DEV_PORT}"
    chmod 0600 "$DEV_ENV_FILE"
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
            write_command_launchers
            print_summary
            ;;
        production)
            confirm_install
            install_prerequisites
            prepare_prod_environment
            prepare_data_directories
            write_command_launchers
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
