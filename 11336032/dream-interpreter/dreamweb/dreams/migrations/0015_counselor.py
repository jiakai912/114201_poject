# Generated by Django 5.1.6 on 2025-06-30 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dreams', '0014_delete_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counselor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='諮詢師姓名')),
                ('specialty', models.CharField(max_length=200, verbose_name='專長領域')),
                ('description', models.TextField(blank=True, null=True, verbose_name='簡介')),
                ('image_url', models.URLField(blank=True, null=True, verbose_name='頭像圖片網址')),
            ],
            options={
                'verbose_name': '諮詢師',
                'verbose_name_plural': '諮詢師',
            },
        ),
    ]
