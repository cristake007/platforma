# Source snapshot

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
