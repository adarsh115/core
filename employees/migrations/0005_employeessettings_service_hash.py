# Generated by Django 2.1.8 on 2019-05-01 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_employeessettings_is_configured'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeessettings',
            name='service_hash',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
