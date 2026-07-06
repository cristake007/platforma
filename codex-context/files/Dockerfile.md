# Source snapshot

## `Dockerfile`

Size: 1.2 KB

```dockerfile
FROM node:24-bookworm-slim AS frontend

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
