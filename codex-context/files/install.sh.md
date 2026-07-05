# install.sh

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `install.sh`
- App: none
- Role: `source`
- Size: 12535 bytes
- Source SHA-256: `d2e1b3c26e5590871269ecf84e0ffa2e46781c070cff7fd9f74227e61db341c9`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

readonly DEFAULT_INSTALL_DIR="/opt/tuvtk/app"
readonly DEFAULT_DATA_DIR="/var/lib/tuvtk"
readonly ENV_DIR="/etc/tuvtk"
readonly ENV_FILE="${ENV_DIR}/tuvtk.env"
readonly POSTGRES_IMAGE="postgres:17-bookworm"

REPO_URL=""
REF="main"
PUBLIC_HOST=""
SSH_KEY=""
INSTALL_DIR="${DEFAULT_INSTALL_DIR}"
DATA_DIR="${DEFAULT_DATA_DIR}"

log() {
    printf '[tuvtk] %s\n' "$*"
}

fail() {
    printf '[tuvtk] ERROR: %s\n' "$*" >&2
    exit 1
}

usage() {
    cat <<'EOF'
Usage: install.sh --repo-url URL --public-host HOST [options]

Required:
  --repo-url URL       Git repository to clone or update.
  --public-host HOST   Exact public IPv4 or DNS host accepted by Django.

Options:
  --ref REF            Git branch, tag, or commit to deploy (default: main).
  --ssh-key PATH       Read-only SSH deploy key for a private repository.
  --install-dir PATH   Application checkout (default: /opt/tuvtk/app).
  --data-dir PATH      Persistent data root (default: /var/lib/tuvtk).
  -h, --help           Show this help.

Private SSH repositories require a trusted host entry in
/etc/ssh/ssh_known_hosts. Tokens are intentionally not accepted as arguments.
EOF
}

require_value() {
    local option="$1"
    local value="${2:-}"
    [[ -n "${value}" && "${value}" != --* ]] || fail "${option} requires a value."
}

while (($#)); do
    case "$1" in
        --repo-url)
            require_value "$1" "${2:-}"
            REPO_URL="$2"
            shift 2
            ;;
        --ref)
            require_value "$1" "${2:-}"
            REF="$2"
            shift 2
            ;;
        --public-host)
            require_value "$1" "${2:-}"
            PUBLIC_HOST="$2"
            shift 2
            ;;
        --ssh-key)
            require_value "$1" "${2:-}"
            SSH_KEY="$2"
            shift 2
            ;;
        --install-dir)
            require_value "$1" "${2:-}"
            INSTALL_DIR="$2"
            shift 2
            ;;
        --data-dir)
            require_value "$1" "${2:-}"
            DATA_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            fail "Unknown argument: $1"
            ;;
    esac
done

[[ "${EUID}" -eq 0 ]] || fail "Run this installer as root, for example through sudo."
[[ -n "${REPO_URL}" ]] || fail "--repo-url is required."
[[ -n "${PUBLIC_HOST}" ]] || fail "--public-host is required."
[[ "${REPO_URL}" == https://* || "${REPO_URL}" == git@*:* ]] \
    || fail "--repo-url must use HTTPS or the git@host:path SSH form."
[[ "${REF}" =~ ^[A-Za-z0-9][A-Za-z0-9._/@+-]*$ ]] || fail "--ref is not a safe Git ref or commit."
[[ "${PUBLIC_HOST}" =~ ^[A-Za-z0-9.:-]+$ ]] || fail "--public-host contains unsupported characters."
[[ "${PUBLIC_HOST}" != *"*"* ]] || fail "Wildcard hosts are not allowed."
[[ "${PUBLIC_HOST}" != *":"* ]] || fail "IPv6 public hosts are not supported by this HTTP installer yet."
[[ "${INSTALL_DIR}" == /* && "${DATA_DIR}" == /* ]] || fail "Install and data directories must be absolute paths."
[[ "${INSTALL_DIR}" != "/" && "${DATA_DIR}" != "/" ]] || fail "Refusing to use / as an install or data directory."
[[ "${INSTALL_DIR}" =~ ^[A-Za-z0-9_./-]+$ && "${DATA_DIR}" =~ ^[A-Za-z0-9_./-]+$ ]] \
    || fail "Install and data directories may contain only letters, numbers, dot, underscore, slash, and hyphen."
[[ "${DATA_DIR}" != "${INSTALL_DIR}" && "${DATA_DIR}" != "${INSTALL_DIR}/"* \
    && "${INSTALL_DIR}" != "${DATA_DIR}/"* ]] \
    || fail "Install and data directories must not overlap."

if [[ -n "${SSH_KEY}" ]]; then
    [[ "${SSH_KEY}" == /* ]] || fail "--ssh-key must be an absolute path."
    [[ -f "${SSH_KEY}" ]] || fail "SSH deploy key not found: ${SSH_KEY}"
    [[ -s /etc/ssh/ssh_known_hosts ]] || fail "/etc/ssh/ssh_known_hosts must contain the repository host key."
    printf -v ssh_key_escaped '%q' "${SSH_KEY}"
    export GIT_SSH_COMMAND="ssh -i ${ssh_key_escaped} -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile=/etc/ssh/ssh_known_hosts"
fi

load_os_release() {
    [[ -r /etc/os-release ]] || fail "/etc/os-release is missing; Debian or Ubuntu is required."
    # shellcheck disable=SC1091
    . /etc/os-release
    case "${ID:-}" in
        debian|ubuntu) ;;
        *) fail "Unsupported distribution '${ID:-unknown}'. Only Debian and Ubuntu are supported." ;;
    esac
    case "$(dpkg --print-architecture)" in
        amd64|arm64) ;;
        *) fail "Unsupported architecture. Only amd64 and arm64 are supported." ;;
    esac
}

configure_docker_repository() {
    local docker_distribution="${ID}"
    local docker_codename="${VERSION_CODENAME:-}"
    if [[ "${ID}" == "ubuntu" && -n "${UBUNTU_CODENAME:-}" ]]; then
        docker_codename="${UBUNTU_CODENAME}"
    fi
    [[ -n "${docker_codename}" ]] || fail "Could not determine the distribution codename."

    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL "https://download.docker.com/linux/${docker_distribution}/gpg" \
        -o /etc/apt/keyrings/docker.asc
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
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get install --yes ca-certificates curl git openssh-client openssl

    if ! command -v docker >/dev/null 2>&1; then
        log "Installing Docker Engine and the Compose plugin from Docker's official repository..."
        local conflicting_packages=()
        local package
        for package in docker.io docker-compose docker-compose-v2 podman-docker containerd runc; do
            if dpkg-query --show --showformat='${Status}' "${package}" 2>/dev/null \
                | grep -q 'install ok installed'; then
                conflicting_packages+=("${package}")
            fi
        done
        if ((${#conflicting_packages[@]})); then
            apt-get remove --yes "${conflicting_packages[@]}"
        fi
        configure_docker_repository
        apt-get update
        apt-get install --yes docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    elif ! docker compose version >/dev/null 2>&1; then
        log "Installing the Docker Compose plugin from Docker's official repository..."
        configure_docker_repository
        apt-get update
        apt-get install --yes docker-compose-plugin
    fi

    if command -v systemctl >/dev/null 2>&1; then
        systemctl enable --now docker
    fi
    docker info >/dev/null 2>&1 || fail "Docker is installed but the daemon is unavailable."
    docker compose version >/dev/null 2>&1 || fail "The Docker Compose plugin is unavailable."
}

checkout_source() {
    local install_parent
    install_parent="$(dirname "${INSTALL_DIR}")"
    install -d -m 0755 "${install_parent}"

    if [[ -e "${INSTALL_DIR}" && ! -d "${INSTALL_DIR}/.git" ]]; then
        [[ -z "$(find "${INSTALL_DIR}" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]] \
            || fail "Install directory exists and is not an empty Git checkout: ${INSTALL_DIR}"
        rmdir "${INSTALL_DIR}"
    fi

    if [[ ! -d "${INSTALL_DIR}/.git" ]]; then
        log "Cloning ${REPO_URL}..."
        git clone --no-checkout -- "${REPO_URL}" "${INSTALL_DIR}"
    else
        local existing_remote
        existing_remote="$(git -C "${INSTALL_DIR}" remote get-url origin)"
        [[ "${existing_remote}" == "${REPO_URL}" ]] \
            || fail "Existing checkout remote '${existing_remote}' does not match '${REPO_URL}'."
        [[ -z "$(git -C "${INSTALL_DIR}" status --porcelain --untracked-files=normal)" ]] \
            || fail "Existing checkout has local changes; refusing to replace them."
    fi

    log "Fetching ref ${REF}..."
    git -C "${INSTALL_DIR}" fetch --force --prune --tags origin "${REF}"
    git -C "${INSTALL_DIR}" checkout --detach --force FETCH_HEAD
    [[ -f "${INSTALL_DIR}/compose.yaml" && -f "${INSTALL_DIR}/Dockerfile" ]] \
        || fail "The selected revision does not contain the Docker deployment files."
}

env_value() {
    local key="$1"
    sed -n "s/^${key}=//p" "${ENV_FILE}" | tail -n 1
}

write_environment() {
    install -d -m 0700 "${ENV_DIR}"

    local csrf_host="${PUBLIC_HOST}"
    if [[ "${PUBLIC_HOST}" == *:* && "${PUBLIC_HOST}" != \[*\] ]]; then
        csrf_host="[${PUBLIC_HOST}]"
    fi

    if [[ ! -f "${ENV_FILE}" ]]; then
        local django_secret postgres_password
        django_secret="$(openssl rand -hex 48)"
        postgres_password="$(openssl rand -hex 32)"
        umask 077
        cat > "${ENV_FILE}" <<EOF
TUVTK_DATA_DIR=${DATA_DIR}
TUVTK_IMAGE_TAG=local
TUVTK_PUBLIC_HOST=${PUBLIC_HOST}
TUVTK_HTTP_PORT=80
NGINX_PROXY_TIMEOUT=900s
DJANGO_DEPLOYMENT_MODE=container
DJANGO_SECRET_KEY=${django_secret}
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=${PUBLIC_HOST}
DJANGO_CSRF_TRUSTED_ORIGINS=http://${csrf_host}
DJANGO_TRUST_PROXY_HEADERS=true
DJANGO_USE_X_FORWARDED_HOST=true
DJANGO_SECURE_SSL_REDIRECT=false
DJANGO_SESSION_COOKIE_SECURE=false
DJANGO_CSRF_COOKIE_SECURE=false
POSTGRES_DB=platforma_tuvtk
POSTGRES_USER=tuvtk
POSTGRES_PASSWORD=${postgres_password}
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_CONN_MAX_AGE=60
POSTGRES_CONN_HEALTH_CHECKS=true
GUNICORN_WORKERS=2
GUNICORN_TIMEOUT=900
EOF
        chmod 0600 "${ENV_FILE}"
        log "Generated deployment secrets in ${ENV_FILE}."
        return
    fi

    chmod 0600 "${ENV_FILE}"
    [[ "$(env_value TUVTK_DATA_DIR)" == "${DATA_DIR}" ]] \
        || fail "Existing environment uses a different data directory: $(env_value TUVTK_DATA_DIR)"
    [[ "$(env_value TUVTK_PUBLIC_HOST)" == "${PUBLIC_HOST}" ]] \
        || fail "Existing environment uses a different public host: $(env_value TUVTK_PUBLIC_HOST)"
    [[ -n "$(env_value DJANGO_SECRET_KEY)" && -n "$(env_value POSTGRES_PASSWORD)" ]] \
        || fail "Existing environment is missing required persistent secrets."
    log "Preserving existing deployment secrets in ${ENV_FILE}."
}

prepare_data_directories() {
    log "Preparing persistent data directories under ${DATA_DIR}..."
    docker pull "${POSTGRES_IMAGE}" >/dev/null

    local postgres_uid postgres_gid
    postgres_uid="$(docker run --rm --entrypoint sh "${POSTGRES_IMAGE}" -c 'id -u postgres')"
    postgres_gid="$(docker run --rm --entrypoint sh "${POSTGRES_IMAGE}" -c 'id -g postgres')"

    install -d -m 0750 -o "${postgres_uid}" -g "${postgres_gid}" "${DATA_DIR}/postgres"
    install -d -m 0755 -o 10001 -g 10001 "${DATA_DIR}/media" "${DATA_DIR}/static"
    install -d -m 0750 -o 10001 -g 10001 "${DATA_DIR}/private-media"

    chown -R "${postgres_uid}:${postgres_gid}" "${DATA_DIR}/postgres"
    chown -R 10001:10001 "${DATA_DIR}/media" "${DATA_DIR}/private-media" "${DATA_DIR}/static"
}

deploy_application() {
    local compose=(docker compose --env-file "${ENV_FILE}" --project-directory "${INSTALL_DIR}" -f "${INSTALL_DIR}/compose.yaml")

    log "Validating the Compose configuration..."
    "${compose[@]}" config --quiet

    log "Building the application image..."
    "${compose[@]}" build --pull web

    log "Starting PostgreSQL..."
    "${compose[@]}" up --detach --wait --wait-timeout 180 db

    log "Applying migrations and collecting static files..."
    "${compose[@]}" run --rm init

    log "Starting Gunicorn and Nginx..."
    "${compose[@]}" up --detach --wait --wait-timeout 180 --remove-orphans web nginx
}

load_os_release
install_prerequisites
checkout_source
write_environment
prepare_data_directories
deploy_application

deployed_revision="$(git -C "${INSTALL_DIR}" rev-parse HEAD)"

cat <<EOF

TUVTK installation completed.

URL:               http://${PUBLIC_HOST}/
Revision:          ${deployed_revision}
Environment:       ${ENV_FILE}
Persistent data:   ${DATA_DIR}

Create an administrator:
  sudo docker compose --env-file ${ENV_FILE} --project-directory ${INSTALL_DIR} -f ${INSTALL_DIR}/compose.yaml exec web python manage.py createsuperuser

Follow logs:
  sudo docker compose --env-file ${ENV_FILE} --project-directory ${INSTALL_DIR} -f ${INSTALL_DIR}/compose.yaml logs --follow web nginx

WARNING: This deployment uses public HTTP. Credentials, session cookies, and
application data are not encrypted in transit. Configure HTTPS before using
the deployment for production or sensitive data.
EOF
```
