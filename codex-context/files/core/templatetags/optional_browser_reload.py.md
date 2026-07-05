# Source snapshot

## `core/templatetags/optional_browser_reload.py`

Size: 410 B

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
