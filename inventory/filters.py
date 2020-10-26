
import django_filters

from .models import *


class ItemPriceFilter(django_filters.FilterSet):
    class Meta:
        model = ItemPrice
        fields = {
            'item': ['exact'],
            'buying': ['exact'],
            'selling': ['exact'],
            'currency': ['exact']
        }

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'tracking_number': ['icontains'],
            'supplier': ['exact'],
            'status': ['exact'],
            'date': ['exact'],
            'expected_receipt_date': ['exact']
        }


class SupplierFilter(django_filters.FilterSet):
    class Meta:
        model = Supplier
        fields = {
            'supplier_name': ['icontains'],
            'supplier_type': ['exact']
        }


class InventoryCheckFilter(django_filters.FilterSet):
    class Meta:
        model = InventoryCheck
        fields = {
            'date': ['exact'],
            'warehouse': ['exact'],
        }


class TransferOrderFilter(django_filters.FilterSet):
    class Meta:
        model = TransferOrder
        fields = {
            'date': ['exact'],
            'source_warehouse': ['exact'],
            'receiving_warehouse': ['exact']
        }


class UnitFilter(django_filters.FilterSet):
    class Meta:
        model = UnitOfMeasure
        fields = {
            'name': ['icontains'],
            'base_unit': ['exact']
        }


class ControllerFilter(django_filters.FilterSet):
    class Meta:
        model = InventoryController
        fields = {
            'employee': ['exact'],
        }


class InventoryItemFilter(django_filters.FilterSet):

    class Meta:
        model = InventoryItem
        fields = {
            'name': ['icontains'],
            'unit': ['exact'],
            'supplier': ['exact'],
            'category': ['exact'],
        }


class InventorySearchField(django_filters.FilterSet):

    class Meta:
        model = InventoryItem
        fields = {'name': ['icontains']}
