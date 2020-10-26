# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import urllib

from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView)
from django_filters.views import FilterView
from rest_framework.generics import ListCreateAPIView

from common_data.models import Individual, Organization
from common_data.utilities import *
from common_data.views import PaginationMixin
from common_data.forms import IndividualForm
from inventory import filters, forms, models, serializers
from invoicing.models import SalesConfig
import openpyxl


class SupplierCreateView(ContextMixin, CreateView):
    form_class = forms.SupplierForm
    template_name = os.path.join('inventory', 'supplier', 'create.html')
    extra_context = {
        "title": "Add Vendor",
        "description": "Record details of business partners that provide your organization with goods and services"
    }

    success_url = '/inventory/supplier/list'

    def get_initial(self):
        return {
            'vendor_type': 'organization'
        }


class SupplierUpdateView(ContextMixin, UpdateView):
    form_class = forms.SupplierForm
    template_name = os.path.join('inventory', 'supplier', 'create.html')
    extra_context = {"title": "Update Existing Vendor"}
    model = models.Supplier

    def get_success_url(self):
        return reverse('inventory:supplier-detail',
                       kwargs={'pk': self.kwargs['pk']
                               })


class SupplierListView(ContextMixin,
                       PaginationMixin, FilterView):
    paginate_by = 20
    filterset_class = filters.SupplierFilter
    template_name = os.path.join("inventory", "supplier", "list.html")
    extra_context = {"title": "Vendor List",
                     "new_link": reverse_lazy(
                         "inventory:supplier-create"),
                     "action_list": [
                         {
                             'label': 'Import Suppliers from Excel',
                             'icon': 'file-excel',
                             'link': reverse_lazy('inventory:import-suppliers-from-excel')
                         },
                         {
                             'label': 'Create Multiple Suppliers',
                             'icon': 'file-alt',
                             'link': reverse_lazy('inventory:create-multiple-suppliers')
                         },
                     ]}

    def get_queryset(self):
        return models.Supplier.objects.all().order_by('pk')


class SupplierDeleteView(
        DeleteView):
    template_name = os.path.join('common_data',
                                 'delete_template.html')
    success_url = reverse_lazy('inventory:organization-supplier-list')
    model = models.Supplier


class SupplierListAPIView(ListCreateAPIView):
    serializer_class = serializers.SupplierSerializer
    queryset = models.Supplier.objects.all()


class SupplierDetailView(
        DetailView):
    template_name = os.path.join('inventory', 'supplier', 'detail.html')
    model = models.Supplier


class AddSupplierIndividualView(ContextMixin, CreateView):
    template_name = os.path.join('common_data', 'crispy_create_template.html')
    form_class = IndividualForm
    success_url = reverse_lazy('inventory:supplier-list')  # wont redirect

    extra_context = {
        'title': 'Add member to organization'
    }

    def get_initial(self):
        return {
            'organization': self.kwargs['pk']
        }


class CreateMultipleSuppliersView(FormView):
    template_name = os.path.join('inventory', 'supplier',
                                 'create_multiple.html')
    form_class = forms.CreateMultipleSuppliersForm
    success_url = reverse_lazy('inventory:supplier-list')

    def form_valid(self, form):
        resp = super().form_valid(form)
        data = json.loads(urllib.parse.unquote(form.cleaned_data['data']))

        settings = SalesConfig.objects.first()

        for line in data:
            sup = models.Supplier.objects.create(
                supplier_name=line['name'],
                business_address=line['address'],
                email=line['email'],
                phone_1=line['phone'],
            )
            if line['account_balance']:
                sup.account.balance = line['account_balance']
                sup.account.save()

        return resp


class ImportSuppliersView(ContextMixin, FormView):
    extra_context = {
        'title': 'Import Vendors from Excel File'
    }
    template_name = os.path.join('common_data', 'crispy_create_template.html')
    form_class = forms.ImportSuppliersForm
    success_url = reverse_lazy('inventory:supplier-list')

    def form_valid(self, form):
        # assumes all suppliers are organizations
        resp = super().form_valid(form)

        def null_buster(arg):
            if not arg:
                return ''
            return arg

        file = form.cleaned_data['file']
        if file.name.endswith('.csv'):
            # process csv
            pass
        else:
            cols = [
                form.cleaned_data['name'],
                form.cleaned_data['phone'],
                form.cleaned_data['address'],
                form.cleaned_data['email'],
                form.cleaned_data['account_balance'],
            ]
            wb = openpyxl.load_workbook(file.file)
            try:
                ws = wb.get_sheet_by_name(form.cleaned_data['sheet_name'])
            except:
                ws = wb.active

            for row in ws.iter_rows(min_row=form.cleaned_data['start_row'],
                                    max_row=form.cleaned_data['end_row'],
                                    max_col=max(cols)):

                org = Organization.objects.create(
                    legal_name=row[form.cleaned_data['name'] - 1].value,
                    business_address=null_buster(row[
                        form.cleaned_data['address'] - 1].value),
                    email=null_buster(row[
                        form.cleaned_data['email'] - 1].value),
                    phone=null_buster(row[
                        form.cleaned_data['phone'] - 1].value),
                )

                sup = models.Supplier.objects.create(
                    organization=org
                )
                if row[form.cleaned_data['account_balance'] - 1].value:
                    sup.account.balance = row[
                        form.cleaned_data['account_balance'] - 1].value

                    sup.account.save()

        return resp
