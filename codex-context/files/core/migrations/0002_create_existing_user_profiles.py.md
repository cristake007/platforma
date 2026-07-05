# core/migrations/0002_create_existing_user_profiles.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `core/migrations/0002_create_existing_user_profiles.py`
- App: none
- Role: `migration`
- Size: 840 bytes
- Source SHA-256: `95fdd2c4ad6c26d6a471a38a5ee192d48e6cf600d0b21f8ac88902bd1ecab9f0`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.conf import settings
from django.db import migrations


def create_existing_user_profiles(apps, schema_editor):
    user_model = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    profile_model = apps.get_model('core', 'UserProfile')

    existing_user_ids = profile_model.objects.values_list('user_id', flat=True)
    profiles = [
        profile_model(user_id=user_id)
        for user_id in user_model.objects.exclude(pk__in=existing_user_ids)
        .values_list('pk', flat=True)
    ]
    profile_model.objects.bulk_create(profiles)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_existing_user_profiles, migrations.RunPython.noop),
    ]
```
