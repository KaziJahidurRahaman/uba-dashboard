# Generated by Django 4.1.12 on 2024-04-06 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="activitytype",
            name="activity_type_comment",
            field=models.TextField(default=None, null=True),
        ),
    ]
