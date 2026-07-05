# Source snapshot

## `core/apps.py`

Size: 149 B

```python
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from . import signals  # noqa: F401
```
