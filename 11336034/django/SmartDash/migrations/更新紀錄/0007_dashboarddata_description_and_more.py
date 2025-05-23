# Generated by Django 5.1.6 on 2025-03-04 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SmartDash", "0006_alter_dashboarddata_progress"),
    ]

    operations = [
        migrations.AddField(
            model_name="dashboarddata",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="dashboarddata",
            name="progress",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="dashboarddata",
            name="task_name",
            field=models.CharField(max_length=255),
        ),
    ]
