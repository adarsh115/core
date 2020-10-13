from django.db import models

from inventory.models import Product

# Create your models here.

class WebSettings(models.Model):
    shop_address = models.TextField()
    shop_email = models.TextField()


class WishlistItem(models.Model):
    product = models.ForeignKey('app.Inventory.InventoryItem', on_delete=models.CASCADE)
    customer = models.ForeignKey('app.Customer', on_delete=models.CASCADE)
    date_added = models.DateField(auto_now=True)

class FaqCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.Charfield(max_length=64)

    def __str__(self):
        return str(self.name)

class FaqItem(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    department = models.ForeignKey('website.WebFaqCategory', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.question)

class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    show_in_navigation = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    parent_category =  models.ForeignKey('website:Category',on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('website:Department', on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Web Categories"

class ProductImage(models.Model):
    product = models.ForeignKey('app:Products', on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return "PRODUCT (%s) IMAGE " % str(self.product)

class SKU(models.Model):
    sku_id = models.CharField(max_length=64)
    attribute = models.CharField(max_length=255)
    value  = models.CharField(max_length=255)
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.sku_id

