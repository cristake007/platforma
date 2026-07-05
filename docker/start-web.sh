#!/bin/sh
set -eu

exec gunicorn platforma_tuvtk.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-2}" \
    --timeout "${GUNICORN_TIMEOUT:-900}" \
    --access-logfile - \
    --error-logfile -
