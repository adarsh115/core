# Generated by Django 2.1.8 on 2019-07-23 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_data', '0010_auto_20190617_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalconfig',
            name='last_automated_service_run',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
