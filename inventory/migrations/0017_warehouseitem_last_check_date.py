# Generated by Django 2.1 on 2020-01-14 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_inventorysettings_default_warehouse'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouseitem',
            name='last_check_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
