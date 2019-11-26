# Generated by Django 2.1.8 on 2019-05-21 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0005_accountingsettings_service_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance_sheet_category',
            field=models.CharField(choices=[('current-assets', 'Current Assets'), ('non-current-assets', 'Long Term Assets'), ('current-liabilites', 'Current Liabilites'), ('long-term-liabilites', 'Long Term Liabilites'), ('equity', 'Equity'), ('not-included', 'Not Included')], default='current-assets', max_length=32),
        ),
        migrations.AlterField(
            model_name='asset',
            name='depreciation_method',
            field=models.IntegerField(choices=[(0, 'Straight Line')], default=0),
        ),
        migrations.AlterField(
            model_name='interestbearingaccount',
            name='balance_sheet_category',
            field=models.CharField(choices=[('current-assets', 'Current Assets'), ('non-current-assets', 'Long Term Assets'), ('current-liabilites', 'Current Liabilites'), ('long-term-liabilites', 'Long Term Liabilites'), ('equity', 'Equity'), ('not-included', 'Not Included')], default='current-assets', max_length=32),
        ),
    ]
