# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import (CreateView,
                                       DeleteView,
                                       UpdateView,
                                       FormView)
from django_filters.views import FilterView
from rest_framework import viewsets
from django.http import JsonResponse
from common_data.utilities import ContextMixin
from common_data.views import PaginationMixin
from common_data.forms import IndividualForm
from invoicing import filters, forms, serializers
from invoicing.models import Customer, Invoice, CreditNote, Lead, CustomerNote
from common_data.models import Individual, Organization
import openpyxl
import json
import urllib


#########################################
#           Customer Views              #
#########################################

class CustomerAPIViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer

# No customer list, overlooked!


class CustomerCreateView(ContextMixin,
                         CreateView):
    extra_context = {
        "title": "New  Customer",
        'description': 'Add individuals and organizations that buy your'
        ' products to your records',

    }
    template_name = os.path.join("invoicing", "customer", "create.html")
    form_class = forms.CustomerForm


    def get_initial(self):
        return {
            'customer_type': 'individual'
        }

class CustomerUpdateView(ContextMixin, UpdateView):
    extra_context = {"title": "Update Existing Customer"}
    template_name = os.path.join("invoicing", "customer", "create.html")
    form_class = forms.CustomerForm
    model = Customer

   
class CustomerListView(ContextMixin, PaginationMixin, FilterView):
    extra_context = {"title": "List of Customers",
                     "new_link": reverse_lazy(
                         "invoicing:create-customer"),
                     "action_list": [
                         {
                             'label': 'Import Customers from Excel',
                             'icon': 'file-excel',
                             'link': reverse_lazy('invoicing:import-customers-from-excel')
                         },
                         {
                             'label': 'Create Multiple Customers',
                             'icon': 'file-alt',
                             'link': reverse_lazy('invoicing:create-multiple-customers')
                         },
                     ]
                     }
    template_name = os.path.join("invoicing", "customer", "list.html")
    filterset_class = filters.CustomerFilter
    paginate_by = 20

    def get_queryset(self):
        return Customer.objects.all().order_by('pk')


class CustomerDeleteView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template.html')
    model = Customer
    success_url = reverse_lazy('invoicing:customers-list')


class CustomerDetailView(DetailView):
    template_name = os.path.join('invoicing', 'customer', 'detail.html')
    model = Customer

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'invoices': Invoice.objects.filter(
                customer=self.object,
                status='invoice'),
            'quotations': Invoice.objects.filter(
                customer=self.object,
                status='quotation'),
            'credit_notes': CreditNote.objects.filter(
                invoice__customer=self.object
            ),
            'leads': Lead.objects.filter(organization=self.object.organization),
        })

        return context

# TODO test


class AddCustomerIndividualView(ContextMixin, CreateView):
    template_name = os.path.join('common_data', 'crispy_create_template.html')
    form_class = IndividualForm
    success_url = reverse_lazy('invoicing:customers-list')  # wont redirect

    extra_context = {
        'title': 'Add member to organization'
    }

    def get_initial(self):
        return {
            'organization': self.kwargs['pk']
        }


class RemoveCustomerIndividualView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template.html')

class CreateMultipleCustomersView(FormView):
    template_name = os.path.join('invoicing', 'customer',
                                 'create_multiple.html')
    form_class = forms.CreateMultipleCustomersForm
    success_url = reverse_lazy('invoicing:customers-list')

    def form_valid(self, form):
        resp = super().form_valid(form)
        data = json.loads(urllib.parse.unquote(form.cleaned_data['data']))

        def null_buster(arg):
            if not arg:
                return ''
            return arg

        for line in data:
            cus = None
            if line['type'] == 'organization':
                cus = Customer.objects.create(
                    customer_name=line['name'],
                    customer_type=line['type'],
                    physical_address=null_buster(line['address']),
                    email=null_buster(line['email']),
                    phone=null_buster(line['phone']),
                )
            else:
                cus = Customer.objects.create(
                    customer_name=line['name'],
                    customer_type=line['type'],
                    physical_address=null_buster(line['address']),
                    email=null_buster(line['email']),
                    phone=null_buster(line['phone']),
                )

            if line['account_balance']:
                cus.account.balance = line['account_balance']
                cus.account.save()

        return resp

class ImportCustomersView(ContextMixin, FormView):
    extra_context = {
        'title': 'Import Customers from Excel File'
    }
    template_name = os.path.join('common_data', 'crispy_create_template.html')
    form_class = forms.ImportCustomersForm
    success_url = reverse_lazy('invoicing:customers-list')

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
                form.cleaned_data['type'],
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
                cus = None
                if row[form.cleaned_data['type']-1].value == 0:
                    
                    cus = Customer.objects.create(
                        customer_name=row[form.cleaned_data['name']-1].value,
                        customer_type="organization",
                        physical_address=null_buster(
                            row[form.cleaned_data['address']-1].value),
                        email=null_buster(
                            row[form.cleaned_data['email']-1].value),
                        phone=null_buster(
                            row[form.cleaned_data['phone']-1].value),
                    )
                else:
                    cus = Customer.objects.create(
                        customer_type="organization",
                        customer_name=row[form.cleaned_data['name']-1].value,
                        address=null_buster(
                            row[form.cleaned_data['address']-1].value),
                        email=null_buster(
                            row[form.cleaned_data['email']-1].value),
                        phone=null_buster(
                            row[form.cleaned_data['phone']-1].value),
                    )

                    if row[form.cleaned_data['account_balance'] - 1].value:
                        cus.account.balance = row[
                            form.cleaned_data['account_balance'] - 1].value

                        cus.account.save()

        return resp


def create_customer_note(request, customer=None):
    customer = Customer.objects.get(pk=customer)
    author = str(request.user.employee) if hasattr(request.user, 'employee') \
        else str(request.user)
    obj = CustomerNote.objects.create(
        customer=customer,
        note=request.POST['note'],
        author=author
    )

    return JsonResponse({
        'status': 'ok',
        'data': {
            'date': obj.timestamp.date(),
            'note': obj.note,
            'author': obj.author
        }
    })
