# core/models.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `core/models.py`
- App: none
- Role: `core`
- Size: 384 bytes
- Source SHA-256: `42649ba2978d08d4a3742dc0e4aa996154cc62e2568f4a1b362a028462653baa`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True)

    def __str__(self):
        return f'{self.user.get_username()} profile'
```
