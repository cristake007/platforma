from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("planificator", "0004_alter_appsetting_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="appsetting",
            options={
                "permissions": [
                    ("use_course_planning", "Can use schedule generator"),
                    ("use_word_matcher", "Can use Word date matcher"),
                    ("use_xml_export", "Can use XML export"),
                ],
            },
        ),
    ]
