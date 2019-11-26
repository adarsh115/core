# Generated by Django 2.1 on 2019-09-12 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0017_auto_20190912_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='employee_category',
            field=models.CharField(choices=[('Temporary', 'Temporary Employee'), ('Subcontractor', 'Subcontractor'), ('Permanent Employee', 'Permanent Employee')], default='Permanent Employee', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contract',
            name='termination_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
