# Generated by Django 2.2.13 on 2020-09-23 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0030_auto_20200920_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadsource',
            name='supports_quick_entry',
            field=models.BooleanField(default=True),
        ),
    ]