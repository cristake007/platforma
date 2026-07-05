from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("planificator", "0002_schedulegeneration_appsetting_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="schedulegeneration",
            name="source_file_data",
            field=models.BinaryField(default=bytes, editable=False),
        ),
    ]
