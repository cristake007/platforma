from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("planificator", "0003_schedulegeneration_source_file_data"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="appsetting",
            options={
                "permissions": [
                    ("use_course_planning", "Can use schedule generator"),
                    ("use_word_matcher", "Can use Word date matcher"),
                ],
            },
        ),
    ]
