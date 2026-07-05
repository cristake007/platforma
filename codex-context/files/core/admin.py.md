# core/admin.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `core/admin.py`
- App: none
- Role: `core`
- Size: 386 bytes
- Source SHA-256: `4bf3b9aff942a2a42d221dccbd59c644f1da6a4bb2f2c881df4682ca86671b2e`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'has_avatar')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    @admin.display(boolean=True, description='Avatar')
    def has_avatar(self, profile):
        return bool(profile.avatar)
```
