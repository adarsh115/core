# Generated by Django 2.1 on 2020-03-02 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common_data', '0014_auto_20200204_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='author',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.Employee'),
        ),
    ]
