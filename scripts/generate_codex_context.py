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
