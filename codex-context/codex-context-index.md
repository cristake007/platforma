# Codex Context Index

Generated: `2026-07-05T22:50:42`

Use the smallest possible context. This generator creates one Markdown context file per included source file. It intentionally does not create broad app XML packs or full-repository Repomix output.

## Start here

1. Read the applicable repository/app `AGENTS.md` instructions.
2. If exact paths are known, open the real source files directly and skip their generated copies.
3. If paths are unknown, use only the relevant `apps/<app>.md` guide or `project-core.md`.
4. Use `codex-file-map.txt` only to locate an unknown file, then open the smallest matching set.
5. Treat file contexts as hashed snapshots; the real source remains authoritative before editing.

## Global guides

- [`project-core.md`](project-core.md) - settings, root URLs, core shell/navigation, theme source, and tooling.
- `codex-file-map.txt` - included real source file list.
- `codex-context-audit.md` - generated coverage and integrity summary.

## App guides

### `dashboard`

- Guide: [`apps/dashboard.md`](apps/dashboard.md)
- Files: 7
- Backend: 4
- Frontend/template/static: 1
- Tests: 1
- Migrations: 1

### `diplome`

- Guide: [`apps/diplome.md`](apps/diplome.md)
- Files: 47
- Backend: 11
- Frontend/template/static: 22
- Tests: 4
- Migrations: 10

### `flota`

- Guide: [`apps/flota.md`](apps/flota.md)
- Files: 25
- Backend: 11
- Frontend/template/static: 10
- Tests: 1
- Migrations: 3

### `media_library`

- Guide: [`apps/media_library.md`](apps/media_library.md)
- Files: 17
- Backend: 12
- Frontend/template/static: 2
- Tests: 1
- Migrations: 2

### `planificator`

- Guide: [`apps/planificator.md`](apps/planificator.md)
- Files: 46
- Backend: 21
- Frontend/template/static: 14
- Tests: 5
- Migrations: 6

### `tasks`

- Guide: [`apps/tasks.md`](apps/tasks.md)
- Files: 25
- Backend: 12
- Frontend/template/static: 10
- Tests: 1
- Migrations: 2

## Routing examples

- `apps/foo/models.py` -> `apps/foo.md` + `files/apps/foo/models.py.md`
- `apps/foo/templates/foo/list.html` -> `apps/foo.md` + `files/apps/foo/templates/foo/list.html.md`
- `platforma_tuvtk/urls.py` -> `project-core.md` + `files/platforma_tuvtk/urls.py.md`
