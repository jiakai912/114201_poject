# Generated by Django 5.1.6 on 2025-07-25 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dreams", "0022_commentlike_postlike"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="coin_price",
            field=models.PositiveIntegerField(
                default=10, help_text="每次預約所需點券數"
            ),
        ),
    ]
