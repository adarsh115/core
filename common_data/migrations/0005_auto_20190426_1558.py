# Generated by Django 2.1.8 on 2019-04-26 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_data', '0004_auto_20190423_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalconfig',
            name='is_configured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='globalconfig',
            name='verification_task_id',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
