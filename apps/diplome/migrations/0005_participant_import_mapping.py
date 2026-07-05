from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diplome", "0004_participant_list_import"),
    ]

    operations = [
        migrations.AddField(
            model_name="participantimportdraft",
            name="source_columns_json",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="participantimportdraft",
            name="source_rows_json",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="participantimportdraft",
            name="column_mapping_json",
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name="participantimportdraft",
            name="mapping_confirmed",
            field=models.BooleanField(default=False),
        ),
    ]
