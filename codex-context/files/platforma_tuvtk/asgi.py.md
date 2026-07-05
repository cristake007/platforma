# platforma_tuvtk/asgi.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `platforma_tuvtk/asgi.py`
- App: none
- Role: `project-config`
- Size: 423 bytes
- Source SHA-256: `fdd1edbcf9f3299b38a26ec73c3a807ee9d868cc980c689bc3f6de2c3215987a`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
"""
ASGI config for platforma_tuvtk project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma_tuvtk.settings')

application = get_asgi_application()
```
