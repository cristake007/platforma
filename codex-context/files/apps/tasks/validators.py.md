# apps/tasks/validators.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/tasks/validators.py`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `backend`
- Size: 630 bytes
- Source SHA-256: `08620bda7be3816e5dfb3fe6f123b18a09dd3b0c7bae896e74ec18586d1c90e8`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from urllib.parse import urlsplit

from django.core.exceptions import ValidationError


def validate_origin_url(value: str) -> None:
    if not value:
        return
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not value.startswith("/") or value.startswith("//"):
        raise ValidationError("Linkul sursă trebuie să fie o cale internă sigură.")


def validate_stage_balance(*, terminal_count: int, non_terminal_count: int) -> None:
    if terminal_count < 1 or non_terminal_count < 1:
        raise ValidationError("Board-ul trebuie să păstreze cel puțin o etapă activă și una terminală.")
```
