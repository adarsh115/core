from website.models import Department
from website import models
from inventory.models import InventoryItem
import json
from accounting.models import Currency
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class ContextMixin(object):
    ctxt = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.ctxt)
        context['departments'] = Department.objects.all()
        if not self.request.session.get('currency'):
            self.request.session['currency'] = models.WebSettings.objects.first()
        context['currency'] = self.request.session.get('currency')
        if self.ctxt.get('crumbs'):
            context['crumb_title'] = self.ctxt['crumbs'][-1]['label']

        return context

class InventoryFilterMixin(object):
    pb = 2
    filtered_fields = ['name__icontains', 'unit_price__lte', 'unit_price__gte']

    def get_pg_qs(self, _qs):
        for arg in self.filtered_fields:
            if self.request.GET.get(arg):
                return _qs

        paginator = Paginator(_qs, self.pb)
        page = self.request.GET.get('page', 1)
        try:
            qs = paginator.page(page)
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.nume_pages)

        self.paginator = paginator
        self.page = qs
        return qs.object_list

    def update_context(self, context):
        if hasattr(self, 'paginator'):
            context['paginator'] = self.paginator
            context['page_obj'] = self.page
