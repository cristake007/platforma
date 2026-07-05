from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diplome", "0008_history_snapshots_allow_source_deletion"),
    ]

    operations = [
        migrations.AddField(
            model_name="participantimportdraft",
            name="source_sheets_json",
            field=models.JSONField(default=list),
        ),
    ]
