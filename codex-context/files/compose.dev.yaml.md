# Source snapshot

## `compose.dev.yaml`

Size: 1.5 KB

```yaml
x-dev-app-volumes: &dev-app-volumes
  - type: bind
    source: .
    target: /app
  - type: volume
    source: dev-media
    target: /app/media
  - type: volume
    source: dev-private-media
    target: /app/private_media
  - type: volume
    source: dev-static
    target: /app/staticfiles
  - type: volume
    source: dev-bootstrap-cache
    target: /app/.bootstrap_icons_cache

services:
  db:
    volumes:
      - type: volume
        source: dev-postgres
        target: /var/lib/postgresql/data

  init:
    environment:
      DJANGO_DEBUG: "true"
    volumes: *dev-app-volumes

  web:
    command: ["python", "manage.py", "runserver", "0.0.0.0:8000"]
    environment:
      DJANGO_DEBUG: "true"
      DJANGO_ALLOWED_HOSTS: "127.0.0.1,localhost,[::1]"
      DJANGO_CSRF_TRUSTED_ORIGINS: "http://127.0.0.1:${TUVTK_DEV_PORT:-8000},http://localhost:${TUVTK_DEV_PORT:-8000}"
      DJANGO_TRUST_PROXY_HEADERS: "false"
      DJANGO_USE_X_FORWARDED_HOST: "false"
    ports:
      - "${TUVTK_DEV_PORT:-8000}:8000"
    volumes: *dev-app-volumes

  tailwind:
    image: node:22-bookworm-slim
    working_dir: /app/theme/static_src
    command:
      - /bin/sh
      - -ec
      - if [ ! -x node_modules/.bin/postcss ]; then npm ci; fi; exec npm run dev
    volumes:
      - type: bind
        source: .
        target: /app
      - type: volume
        source: dev-node-modules
        target: /app/theme/static_src/node_modules
    restart: unless-stopped

volumes:
  dev-postgres:
  dev-media:
  dev-private-media:
  dev-static:
  dev-bootstrap-cache:
  dev-node-modules:
```
