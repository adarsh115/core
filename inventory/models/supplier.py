# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models

from accounting.models import Account
from common_data.models import SoftDeletionModel, QuickEntry, Individual, Organization
from inventory.models.item import InventoryItem
from inventory.models.item_management import StockReceipt
from inventory.models.order import Order

SUPPLIER_TYPE_CHOICES = [
    ('organization', 'Organization'), 
    ('individual', 'Individual')
]
class Supplier(QuickEntry, SoftDeletionModel):
    '''The businesses and individuals that provide the organization with 
    products it will sell. Basic features include contact details address and 
    contact people.
    The account of the supplier is for instances when orders are made on credit.'''
    # one or the other
    quick_entry_fields = ['supplier_type', 'supplier_name']

    supplier_type = models.CharField(max_length=255, choices=SUPPLIER_TYPE_CHOICES, default='individual')
    supplier_name = models.CharField(max_length=255, blank=True, null=True)
    organization = models.OneToOneField('common_data.Organization',
                                        on_delete=models.SET_NULL, blank=True,
                                        null=True)
    individual = models.OneToOneField('common_data.Individual',
                                      on_delete=models.SET_NULL, blank=True,
                                      null=True)
    phone_1 = models.CharField(max_length = 255,default="", blank=True)
    phone_2 = models.CharField(max_length = 255, default="",blank=True)
    tax_id = models.CharField(max_length = 255, default="",blank=True)
    email = models.CharField(max_length = 255, default="",blank=True)
    website = models.CharField(max_length = 255, default="",blank=True)
    business_address = models.TextField(default="",blank=True)
    photo = models.ImageField(null=True, blank=True) 
    logo = models.ImageField(null=True, blank=True)
    billing_address = models.TextField(default="", blank=True)
    banking_details = models.TextField(blank=True, default="")
    billing_currency = models.ForeignKey('accounting.currency', null=True,
        on_delete=models.SET_NULL)
    other_details = models.TextField(default="", blank=True)
    account = models.ForeignKey('accounting.Account',
                                on_delete=models.SET_NULL,
                                blank=True, null=True)
   
   
    def __str__(self):
        return self.supplier_name

    @property
    def products(self):
        return InventoryItem.objects.filter(type=0, supplier=self)

    @property
    def consumables(self):
        return InventoryItem.objects.filter(type=2, supplier=self)

    @property
    def equipment(self):
        return InventoryItem.objects.filter(type=1, supplier=self)

    @property
    def last_delivery(self):
        qs = StockReceipt.objects.filter(order__supplier=self)
        if qs.exists():
            return qs.latest('pk')
        return None

    @property
    def average_days_to_deliver(self):
        qs = Order.objects.filter(supplier=self)
        total_days = 0
        fully_received = 0
        for order in qs:
            if order.fully_received and order.stockreceipt_set.count() > 0:
                # orders can have multiple stock receipts
                fully_received += 1

                last_receipt = order.stockreceipt_set.latest('receive_date')
                total_days += (last_receipt.receive_date - order.date).days

        if fully_received > 0:
            return total_days / fully_received

        return 0

    def create_account(self):
        if self.account is None:
            n_suppliers = Supplier.objects.all().count()
            # will overwrite if error occurs
            self.account = Account.objects.create(
                name="Vendor: %s" % self.supplier_name,
                id=2100 + n_suppliers + 1,  # the + 1 for the default supplier
                balance=0,
                type='liability',
                description='Account which represents debt owed to a Vendor',
                balance_sheet_category='current-liabilities',
                parent_account=Account.objects.get(pk=2000)  # trade payables
            )

    def save(self, *args, **kwargs):
        if not self.pk and self.supplier_name:
            if self.supplier_type == "organization":
                self.organization = Organization.objects.create(
                    legal_name=self.supplier_name,
                    business_address=self.business_address,
                    website=self.website,
                    email=self.email,
                    phone=self.phone_1,
                    logo=self.logo
                )
            
            else:
                first, last = self.supplier_name.split(' ')
                self.individual = Individual.objects.create(
                    first_name=first,
                    last_name=last,
                    email=self.email,
                    phone=self.phone_1,
                    other_details=self.other_details,
                    photo=self.photo,
                    phone_two=self.phone_2
                )
        if self.account is None:
            self.create_account()

        super().save(*args, **kwargs)