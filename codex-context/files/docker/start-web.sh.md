# docker/start-web.sh

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `docker/start-web.sh`
- App: none
- Role: `source`
- Size: 225 bytes
- Source SHA-256: `f740b66c5cae08912938524a7cee384cdf5d8bece7a94951e11511946d6ca10b`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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
