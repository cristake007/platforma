# Source snapshot

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
