# Generated by Django 5.1.6 on 2025-07-03 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dreams", "0006_userprofile_dreamshareauthorization"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="is_verified_therapist",
            field=models.BooleanField(default=False),
        ),
    ]
