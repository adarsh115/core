import django_filters
from website.models import InventoryItem

class InventoryFilter(django_filters.FilterSet):

    class Meta:
        model = InventoryItem
        fields = {
            'name': ['icontains'],
        }

        field_labels ={
            'name': 'Product Name',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['name_icontains'].label = "Product Name"
        self.filters['unit_price__lte'].label = "Price(Max)"
        self.filters['unit_price__gte'].label = "Price(Min"
