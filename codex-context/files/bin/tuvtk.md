# Source snapshot

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
