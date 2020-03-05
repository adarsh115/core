# Generated by Django 2.1 on 2020-02-08 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_auto_20200207_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceworkorder',
            name='manual_progress',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='equipmentrequisition',
            name='requested_by',
            field=models.ForeignKey(limit_choices_to=models.Q(
                active=True), on_delete=django.db.models.deletion.CASCADE, related_name='requested_by', to='employees.Employee'),
        ),
    ]
