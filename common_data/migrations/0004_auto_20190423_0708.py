# Generated by Django 2.2 on 2019-04-23 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_data', '0003_auto_20190422_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalconfig',
            name='backup_frequency',
            field=models.CharField(choices=[(
                'D', 'Daily'), ('M', 'Monthly'), ('W', 'Weekly')], default='D', max_length=32),
        ),
        migrations.AddField(
            model_name='globalconfig',
            name='backup_location',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='globalconfig',
            name='backup_location_type',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='globalconfig',
            name='use_backups',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
