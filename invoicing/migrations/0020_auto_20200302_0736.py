# Generated by Django 2.1 on 2020-03-02 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0019_auto_20200302_0714'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesrepresentative',
            old_name='can_reverse_invoices',
            new_name='can_validate_invoices',
        ),

    ]
