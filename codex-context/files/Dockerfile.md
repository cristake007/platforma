# Dockerfile

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `Dockerfile`
- App: none
- Role: `source`
- Size: 1192 bytes
- Source SHA-256: `8a6aedddd45977e70d842b8dc600cf7dcc3d2f196f71d8c6c15b30043d2b557f`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```text
FROM node:22-bookworm-slim AS frontend

WORKDIR /build

COPY theme/static_src/package.json theme/static_src/package-lock.json ./theme/static_src/
RUN npm --prefix theme/static_src ci

COPY . .
RUN npm --prefix theme/static_src run build


FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install --yes --no-install-recommends ca-certificates fonts-liberation2 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 10001 tuvtk \
    && useradd --uid 10001 --gid tuvtk --create-home --home-dir /home/tuvtk tuvtk

WORKDIR /app

COPY requirements.txt requirements-deploy.txt ./
RUN python -m pip install --requirement requirements-deploy.txt

COPY . .
COPY --from=frontend /build/theme/static/css/dist/styles.css ./theme/static/css/dist/styles.css

RUN mkdir -p /app/staticfiles /app/media /app/private_media /app/.bootstrap_icons_cache \
    && chmod +x /app/docker/start-web.sh \
    && chown -R tuvtk:tuvtk /app/staticfiles /app/media /app/private_media /app/.bootstrap_icons_cache

USER tuvtk

EXPOSE 8000

CMD ["/app/docker/start-web.sh"]
```
