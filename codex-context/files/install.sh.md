# Source snapshot

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
