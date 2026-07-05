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
