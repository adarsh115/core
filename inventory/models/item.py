# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from decimal import Decimal as D

from django.db import models
from django.db.models import Q

import inventory
import invoicing
import services
from common_data.models import SoftDeletionModel
from django.shortcuts import reverse
from common_data.models import QuickEntry 
import accounting

class ItemPrice(models.Model):
    item = models.ForeignKey('inventory.inventoryitem', on_delete=models.CASCADE)
    buying = models.BooleanField(default=False)
    selling = models.BooleanField(default=True)
    currency = models.ForeignKey('accounting.currency', on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=16,
                               decimal_places=2,
                               default=0.0)

    def get_absolute_url(self):
        return reverse("inventory:update-item-price", kwargs={"pk": self.pk})

class InventoryItem(QuickEntry, SoftDeletionModel):
    quick_entry_fields = ['name', 'type', 'description']

    INVENTORY_TYPES = [
        (0, 'Product'),
        (1, 'Equipment'),
        (2, 'Consumables')
    ]
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('poor', 'Poor'),
        ('broken', 'Not Functioning')
    ]
    

    name = models.CharField(max_length=64)
    type = models.PositiveSmallIntegerField(choices=INVENTORY_TYPES)
    category = models.ForeignKey('inventory.Category',
                                 on_delete=models.SET_NULL, null=True, default=1)
    length = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    image = models.FileField(blank=True, null=True)
    description = models.TextField(blank=True, default="")
    featured = models.BooleanField(default=False, null=True)
    unit = models.ForeignKey('inventory.UnitOfMeasure',
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             default=1)
    supplier = models.ForeignKey("inventory.Supplier",
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True)
    minimum_order_level = models.IntegerField(default=0)
    maximum_stock_level = models.IntegerField(default=0)
    sku = models.CharField(max_length=16, blank=True)
    tax = models.ForeignKey('accounting.tax',
                            default=1,
                            on_delete=models.SET_DEFAULT)
    condition = models.CharField(max_length=16,
                                 choices=CONDITION_CHOICES, default='excellent')
    asset_data = models.ForeignKey('accounting.Asset',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)

    @property
    def url(self):
        if self.type == 0:
            return reverse("inventory:product-detail", kwargs={"pk": self.pk})
        elif self.type == 1:
            return reverse("inventory:equipment-detail", kwargs={"pk": self.pk})
        else:
            return reverse("inventory:consumable-detail", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return self.url

    def __str__(self):
        return str(self.id) + " - " + self.name

    def set_purchase_price(self, price):
        ItemPrice.objects.create(
            item=self,
            buying=True,
            selling=False,
            currency= accounting.models.AccountingSettings.objects.first().active_currency,
            rate= price
        )

    def set_sales_price(self, price):
        ItemPrice.objects.create(
            item=self,
            buying=False,
            selling=True,
            currency= accounting.models.AccountingSettings.objects.first().active_currency,
            rate= price
        )


    @property
    def unit_purchase_price(self):
        prices = self.itemprice_set.filter(buying=True)
        if prices:
            return prices.latest('pk').rate

        return D(0)

    @property
    def quantity(self):
        # returns quantity from all warehouses
        items = inventory.models.WareHouseItem.objects.filter(item=self)
        return sum([i.quantity for i in items])

    @property
    def locations(self):
        return inventory.models.WareHouseItem.objects.filter(
            Q(item=self),
            Q(quantity__gt=0)
        )

    @property
    def unit_sales_price(self):
        prices = self.itemprice_set.filter(selling=True)
        if prices:
            return prices.latest('pk').rate

        return D(0)

    @staticmethod
    def total_inventory_value():
        return sum([p.stock_value for p in InventoryItem.objects.filter(
            type=0,
            active=True)])

    def quantity_on_date(self, date):
        '''
        Starts with current quantity
        going back subtract the received inventory
        add the sold inventory
        return the result
        i.e.
            on_date = current - orders( + debit notes ) + sold(- credit notes) + scrapped inventory
        '''
        current_quantity = self.quantity
        total_orders = inventory.models.order.OrderItem.objects.filter(
            Q(order__date__gte=date) &
            Q(order__date__lte=datetime.date.today()) &
            Q(item=self)
        ).exclude(order__status="draft")

        ordered_quantity = sum([i.received for i in total_orders])

        # will eventually replace with dispatch data
        total_sales = invoicing.models.InvoiceLine.objects.filter(
            Q(invoice__date__gte=date) &
            Q(invoice__date__lte=datetime.date.today()) &
            Q(product__product=self) &
            Q(invoice__draft=False) &
            Q(
                Q(invoice__status="paid") |
                Q(invoice__status="invoice") |
                Q(invoice__status="paid-partially")
            )
        )

        sold_quantity = sum(
            [(i.product.quantity - D(i.product.returned_quantity))
                for i in total_sales])

        return D(current_quantity) + sold_quantity - D(ordered_quantity)

 
    @property
    def unit_value(self):
        '''the value of inventory on a per item basis'''
        if self.quantity == 0 or self.stock_value == 0:
            return self.unit_purchase_price
        return self.stock_value / D(self.quantity)

    @property
    def stock_value(self):
        '''.
        averaging- calculating the overall stock value on the average of all
        the values for the quantity in stock.
        '''
        current_quantity = self.quantity
        cummulative_quantity = 0
        orders_with_items_in_stock = []
        partial_orders = False
        if current_quantity == 0:
            return 0

        # getting the latest orderitems in order of date ordered
        order_items = inventory.models.OrderItem.objects.filter(
            Q(item=self) &
            Q(
                Q(order__status="order") |
                Q(order__status="received-partially") |
                Q(order__status="received")
            )).order_by("order__date").reverse()

        if order_items.count() == 0:
            return D(current_quantity) * self.unit_purchase_price

        # iterate over items
        for item in order_items:
            # orders for which cumulative ordered quantities are less than
            # inventory in hand are considered
            if (item.quantity + cummulative_quantity) < current_quantity:
                orders_with_items_in_stock.append(item)
                cummulative_quantity += item.quantity

            else:
                if cummulative_quantity < current_quantity:
                    partial_orders = True
                    orders_with_items_in_stock.append(item)

                else:
                    break

        cumulative_value = D(0)
        if not partial_orders:
            for item in orders_with_items_in_stock:
                cumulative_value += D(item.quantity) * item.order_price

        else:
            for item in orders_with_items_in_stock[:-1]:
                cumulative_value += D(item.quantity) * item.order_price

            remainder = current_quantity - cummulative_quantity
            cumulative_value += D(remainder) * \
                orders_with_items_in_stock[-1].order_price

        return cumulative_value

    @property
    def sales_to_date(self):
        items = invoicing.models.ProductLineComponent.objects.filter(
            product=self)
        total_sales = sum(
            [(item.invoiceline.subtotal - item.invoiceline.tax_) for item in items])
        return total_sales

    @property
    def requisitions(self):
        return services.models.EquipmentRequisitionLine.objects.filter(
            Q(equipment=self) &
            Q(quantity_returned=0) &
            Q(requisition__released_by__isnull=False)
        )

    @property
    def in_use(self):
        return sum((line.quantity - line.quantity_returned \
            for line in self.requisitions), 0)

    @property
    def in_storage(self):
        return self.quantity - self.in_use
