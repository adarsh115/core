# Generated by Django 2.2.13 on 2020-10-16 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0025_auto_20200927_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='featured',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
