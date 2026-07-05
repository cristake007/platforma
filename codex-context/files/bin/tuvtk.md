# Source snapshot

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
