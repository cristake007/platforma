# core/templatetags/optional_browser_reload.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `core/templatetags/optional_browser_reload.py`
- App: none
- Role: `core`
- Size: 410 bytes
- Source SHA-256: `2906211370e9cbe7dec5d9ed9145e81cb76a4d74f09e4db02d35b16c1700c82b`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.conf import settings
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def optional_browser_reload_script(context):
    if not getattr(settings, "HAS_DJANGO_BROWSER_RELOAD", False):
        return ""
    from django_browser_reload.jinja import django_browser_reload_script

    return django_browser_reload_script(nonce=context.get("csp_nonce"))
```
