# platforma_tuvtk/wsgi.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `platforma_tuvtk/wsgi.py`
- App: none
- Role: `project-config`
- Size: 423 bytes
- Source SHA-256: `37dcb50febc0a7b7dcf1e8d41e816e9f1cccb9b4173733f959479c54b697acaa`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
"""
WSGI config for platforma_tuvtk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma_tuvtk.settings')

application = get_wsgi_application()
```
