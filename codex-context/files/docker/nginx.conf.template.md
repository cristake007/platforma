# docker/nginx.conf.template

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `docker/nginx.conf.template`
- App: none
- Role: `source`
- Size: 1425 bytes
- Source SHA-256: `eacbc09b05f55967ab74710660919c99cf78015b6fe120ee8e74fc8e61eb144e`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```text
server {
    listen 80 default_server;
    server_name _;

    location = /nginx-health {
        access_log off;
        default_type text/plain;
        return 200 "ok\n";
    }

    location / {
        return 444;
    }
}

server {
    listen 80;
    server_name ${TUVTK_PUBLIC_HOST};

    client_max_body_size 40m;

    location = /nginx-health {
        access_log off;
        default_type text/plain;
        return 200 "ok\n";
    }

    location ^~ /static/ {
        root /srv;
        try_files $uri =404;
        access_log off;
        expires 1h;
        add_header Cache-Control "public, max-age=3600";
    }

    location ^~ /media/avatars/ {
        root /srv;
        try_files $uri =404;
        add_header X-Content-Type-Options nosniff always;
    }

    location ^~ /media/flota/ {
        root /srv;
        try_files $uri =404;
        add_header X-Content-Type-Options nosniff always;
    }

    location ^~ /media/ {
        return 404;
    }

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout ${NGINX_PROXY_TIMEOUT};
        proxy_read_timeout ${NGINX_PROXY_TIMEOUT};
    }
}
```
