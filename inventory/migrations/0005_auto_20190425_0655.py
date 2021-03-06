# Generated by Django 2.2 on 2019-04-25 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20190424_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorycheck',
            name='adjusted_by',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.InventoryController'),
        ),
        migrations.AlterField(
            model_name='inventoryscrappingrecord',
            name='controller',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.InventoryController'),
        ),
        migrations.AlterField(
            model_name='stockreceipt',
            name='received_by',
            field=models.ForeignKey(
                default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.InventoryController'),
        ),
        migrations.AlterField(
            model_name='transferorder',
            name='issuing_inventory_controller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='issuing_inventory_controller', to='inventory.InventoryController'),
        ),
        migrations.AlterField(
            model_name='transferorder',
            name='receiving_inventory_controller',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.InventoryController'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='inventory_controller',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.InventoryController'),
        ),
    ]
