# Generated by Django 2.2 on 2019-04-27 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_auto_20190412_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeessettings',
            name='is_configured',
            field=models.BooleanField(default=False),
        ),
    ]
