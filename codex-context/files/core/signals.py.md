# core/signals.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `core/signals.py`
- App: none
- Role: `core`
- Size: 334 bytes
- Source SHA-256: `83a3fff6200ba0725bbbbadc55d9d8bcbe668f4056655417010ab71ae0f24e9d`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```
