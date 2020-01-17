# Generated by Django 2.1 on 2019-12-24 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0023_auto_20191126_1154'),
        ('invoicing', '0007_auto_20190923_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='POSSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('sales_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.Employee')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]