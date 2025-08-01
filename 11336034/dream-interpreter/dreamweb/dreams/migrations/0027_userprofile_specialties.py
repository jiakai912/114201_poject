# Generated by Django 5.1.6 on 2025-07-31 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dreams", "0026_chatinvitation_delete_dreamemotionscore"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="specialties",
            field=models.TextField(
                blank=True,
                help_text="用逗號分隔多個專長，例如：焦慮治療, 兒童心理, 認知行為療法",
                null=True,
                verbose_name="專長領域",
            ),
        ),
    ]
