# Generated by Django 4.1.12 on 2024-03-22 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_alter_object_object_collector_alter_person_p_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="object",
            name="object_code",
            field=models.CharField(
                db_column="ObjectCode",
                default=None,
                max_length=12,
                unique=True,
                verbose_name="name/code of the object",
            ),
        ),
    ]