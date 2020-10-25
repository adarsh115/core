from django.db import models

from inventory.models import InventoryItem
from invoicing.models import Customer

# Create your models here.

class WebSettings(models.Model):
    promo_title = models.CharField(max_length=255, blank=True, default="")
    promo_message = models.TextField(blank=True, default="")
    show_banner = models.BooleanField(default=False)
    banner_image = models.ImageField()
    default_currency = models.ForeignKey('accounting.currency', null=True, on_delete=models.SET_NULL)
    #about page fields
    about_page_text = models.TextField()
    about_page_image = models.ImageField(null=True)
    shop_address = models.TextField()
    shop_email = models.EmailField(max_length=254)
    shop_telephone = models.CharField(max_length=254)
    shop_alternate_telephone = models.CharField(
        max_length=254, blank=True, default="")
    shop_gps = models.CharField(max_length=254, blank=True, default="")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name_plural = "Website Settings"

class WishlistItem(models.Model):
    product = models.ForeignKey('inventory.InventoryItem', on_delete=models.CASCADE)
    customer = models.ForeignKey('invoicing.Customer', on_delete=models.CASCADE)
    date_added = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "Wishlist Items"

class FaqCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "FAQ Categories"

class FaqItem(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    department = models.ForeignKey('website.FaqCategory', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.question)

    class Meta:
        verbose_name_plural = "FAQ Items"

class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    show_in_navigation = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def products(self):
        return InventoryItem.objects.filter(category__department = self)

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    parent_category =  models.ForeignKey('website.Category',on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('website.Department', on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Web Categories"

class ProductImage(models.Model):
    product = models.ForeignKey('inventory.InventoryItem', on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return "PRODUCT (%s) IMAGE " % str(self.product)

class SKU(models.Model):
    sku_id = models.CharField(max_length=64)
    attribute = models.CharField(max_length=255)
    value  = models.CharField(max_length=255)
    product = models.ForeignKey('inventory.InventoryItem', on_delete=models.CASCADE, related_name="+")
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return self.sku_id

    class Meta:
        verbose_name_plural = "SKU"

class Order(models.Model):
    STATUS_OPTIONS = [
        ('cart', 'cart'),
        ('order', 'order'),
        ('paid', 'paid'),
        ('processing', 'processing'),
        ('shipped', 'shipped'),
        ('received', 'received')
    ]
    date = models.DateField()
    customer = models.ForeignKey(
        'invoicing.customer', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=32, choices=STATUS_OPTIONS)
    shipping_address = models.TextField(blank=True, default='')
    billing_address = models.TextField(blank=True, default='')
    currency = models.ForeignKey('accounting.currency', on_delete=models.CASCADE, related_name='currency')
    shipping_cost = models.DecimalField(decimal_places=2, max_digits=24)
    tax = models.DecimalField(decimal_places=2, max_digits=24, default=14.5, )

    @property
    def primary_img(self):
        if self.orderitem_set.first():
            return self.orderitem_set.first().item.primary_photo_url

    def __str__(self):
        return "ORD%d" % self.id

    @property
    def subtotal(self):
        return self.total - self.tax_amount

    # @property
    # def tax_amount(self):
    #     return self.total * (self.tax / D(100.0))

    @property
    def total(self):
        return sum(i.subtotal for i in self.orderitem_set.all())


class OrderItem(models.Model):
    item = models.ForeignKey(
        'inventory.InventoryItem', on_delete=models.SET_NULL, null=True, related_name='order')
    sku = models.ForeignKey('website.SKU', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(decimal_places=2, max_digits=24)
    discount = models.DecimalField(decimal_places=2, max_digits=6)
    order = models.ForeignKey(
        'website.Order', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "%s x %s" % (self.quantity, str(self.item))





