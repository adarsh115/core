# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import urllib

from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django_filters.views import FilterView
from rest_framework import viewsets
from wkhtmltopdf.views import PDFTemplateView

from common_data.utilities import ConfigMixin, ContextMixin, MultiPageDocument
from common_data.views import PaginationMixin # EmailPlusPDFView,
from invoicing import filters, forms, serializers
from invoicing.models import *
from invoicing.views.invoice_views.util import InvoiceCreateMixin
from common_data.views import CREATE_TEMPLATE
from inventory.forms import ShippingAndHandlingForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import openpyxl
from django.contrib import messages
from services.models import Service
from inventory.models import InventoryItem, ProductComponent, UnitOfMeasure


def process_data(items, inv):
    if items:
        items = json.loads(urllib.parse.unquote(items))

        for item in items:
            inv.add_line(item)


class InvoiceListView(ContextMixin, PaginationMixin, FilterView):
    extra_context = {
        "title": "Quotations + Invoices",
        "new_link": reverse_lazy("invoicing:create-invoice"),
        "action_list": [
            {
                'label': 'Import Invoice from Excel',
                'icon': 'file-excel',
                'link': reverse_lazy('invoicing:import-invoice-from-excel')
            }
        ]
    }
    template_name = os.path.join("invoicing", "invoice", "list.html")
    filterset_class = filters.InvoiceFilter
    paginate_by = 20

    def get_queryset(self):
        # Dead???
        return Invoice.objects.filter(active=True).order_by('date').reverse()


class InvoiceAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InvoiceSerializer
    queryset = Invoice.objects.all()


class InvoiceDetailView(ContextMixin, ConfigMixin, MultiPageDocument, DetailView):
    model = Invoice
    template_name = os.path.join("invoicing", "invoice",
                                 'detail.html')
    page_length = 30
    first_page_length = 21
    extra_context = {
        'pdf_link': True,
    }

    def get_multipage_queryset(self):
        return InvoiceLine.objects.filter(invoice=Invoice.objects.get(pk=self.kwargs['pk']))


class InvoiceCreateView(ContextMixin, InvoiceCreateMixin, ConfigMixin, CreateView):
    '''Quotes and Invoices are created with React.js help.
    data is shared between the static form and django by means
    of a json urlencoded string stored in a list of hidden input 
    fields called 'items[]'. '''

    template_name = os.path.join("invoicing", "invoice", "create.html")
    form_class = forms.InvoiceForm

    def get_initial(self):
        initial = {}
        config = SalesConfig.objects.first()
        if self.kwargs.get('customer', None):
            initial['customer'] = self.kwargs['customer']
        initial.update({
            "status": "invoice",
            'terms': config.default_terms,
            'comments': config.default_invoice_comments,
            'invoice_number': config.next_invoice_number
        })
        return initial

    def post(self, request, *args, **kwargs):
        resp = super(InvoiceCreateView, self).post(request, *args, **kwargs)

        if not self.object:
            return resp

        inv = self.object
        items = request.POST.get("item_list", None)
        process_data(items, inv)

        self.object.verify_inventory()

        return resp


class InvoiceUpdateView(ContextMixin, UpdateView):
    template_name = os.path.join('invoicing', 'invoice', 'create.html')
    model = Invoice
    form_class = forms.InvoiceUpdateForm
    extra_context = {
        'title': 'Update  Invoice'
    }

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)

        if not self.object:
            return resp

        if not self.object.draft:
            return resp
        # remove existing items
        inv = self.object
        items = request.POST.get("item_list", None)

        if len(json.loads(urllib.parse.unquote(items))) > 0:
            for line in self.object.invoiceline_set.all():
                line.delete()

        self.object.verify_inventory()

        process_data(items, inv)

        if self.object.status in ["invoice", 'paid'] and not self.object.draft:
            self.object.create_entry()

        return resp


class InvoicePaymentView(ContextMixin, CreateView):
    model = Payment
    template_name = os.path.join('common_data', 'create_template.html')
    form_class = forms.InvoicePaymentForm
    extra_context = {
        'title': 'Apply Payment to  Invoice'
    }

    def get_initial(self):
        return {
            'invoice': self.kwargs['pk'],
        }

    def post(self, *args, **kwargs):
        resp = super().post(*args, **kwargs)
        if self.object:
            self.object.create_entry()

        return resp


class InvoicePaymentDetailView(ListView):
    template_name = os.path.join('invoicing', 'invoice',
                                 'payment', 'detail.html')

    def get_queryset(self):
        return Payment.objects.filter(invoice=Invoice.objects.get(
            pk=self.kwargs['pk']
        ))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(
            *args, **kwargs
        )
        context['invoice'] = Invoice.objects.get(pk=self.kwargs['pk'])
        return context


class InvoicePDFView(ConfigMixin, MultiPageDocument, PDFTemplateView):
    template_name = os.path.join("invoicing", "invoice",
                                 'pdf.html')
    file_name = 'invoice.pdf'
    page_length = 30
    first_page_length = 21

    def get_multipage_queryset(self):
        return InvoiceLine.objects.filter(invoice=Invoice.objects.get(pk=self.kwargs['pk']))

    def get_context_data(self, *args, **kwargs):
        context = super(InvoicePDFView, self).get_context_data(*args, **kwargs)
        context['object'] = Invoice.objects.get(pk=self.kwargs['pk'])
        return context


class InvoiceEmailSendView(ConfigMixin): #EmailPlusPDFView
    inv_class = Invoice
    success_url = reverse_lazy('invoicing:invoices-list')
    pdf_template_name = os.path.join("invoicing", "invoice",
                                     'pdf.html')


class InvoiceDraftDeleteView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template.html')
    success_url = reverse_lazy('invoicing:home')
    model = Invoice


class InvoiceReturnsDetailView(ListView):
    template_name = os.path.join('invoicing', 'invoice',
                                 'credit_note', 'detail_list.html')

    def get_queryset(self):
        return CreditNote.objects.filter(invoice=Invoice.objects.get(
            pk=self.kwargs['pk']
        ))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(
            *args, **kwargs
        )
        context['invoice'] = Invoice.objects.get(pk=self.kwargs['pk'])
        return context


class InvoiceDraftDeleteView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template.html')
    success_url = reverse_lazy('invoicing:home')
    model = Invoice


def verify_invoice(request, pk=None):
    inv = get_object_or_404(Invoice, pk=pk)
    if inv.status == "quotation":
        inv.draft = False
        inv.save()
        return HttpResponseRedirect('/invoicing/quotation-detail/{}'.format(pk))

    # validate against superuser or service person privileges
    if not request.user.is_superuser and not hasattr(request.user, 'employee'):
        messages.info(
            request, 'The current user is not linked to an employee and cannot validate this form.')
        return HttpResponseRedirect('/invoicing/invoice-detail/{}'.format(pk))

    valid = request.user.is_superuser or \
        (request.user.employee.is_sales_rep and
            request.user.employee.salesrepresentative.can_validate_invoices)

    if valid:
        inv.draft = False
        inv.save()

        if inv.status == "invoice":
            inv.create_entry()
            inv.update_inventory()
            inv.invoice_validated_by = request.user.employee
            inv.save()

    return HttpResponseRedirect('/invoicing/invoice-detail/{}'.format(pk))


# TODO test
class ShippingAndHandlingView(
        ContextMixin, FormView):
    template_name = CREATE_TEMPLATE
    form_class = ShippingAndHandlingForm
    success_url = reverse_lazy("invoicing:invoices-list")
    extra_context = {
        'title': 'Record Shipping and handling'
    }

    def get_initial(self):
        return {
            'reference': 'SINV{}'.format(self.kwargs['pk'])
        }

    def form_valid(self, form):
        resp = super().form_valid(form)

        invoice = Invoice.objects.get(pk=self.kwargs['pk'])

        expense = Expense.objects.create(
            category=14,
            amount=form.cleaned_data['amount'],
            description=form.cleaned_data['description'],
            debit_account=Account.objects.get(pk=1000),  # cash
            recorded_by=form.cleaned_data['recorded_by'],
            date=form.cleaned_data['date']
        )

        expense.create_entry()
        invoice.shipping_expenses.add(expense)
        invoice.save()  # necessary?

        return resp


class ShippingExpenseListView(DetailView):
    model = Invoice
    template_name = os.path.join("invoicing", "invoice",
                                 "shipping_list.html")


class ImportInvoiceFromExcelView(ContextMixin, FormView):
    form_class = forms.ImportInvoiceForm
    template_name = os.path.join('common_data', 'crispy_create_template.html')
    success_url = reverse_lazy('invoicing:invoices-list')
    extra_context = {
        'title': 'Import Invoices from Excel'
    }

    def form_valid(self, form):
        resp = super().form_valid(form)

        def null_buster(arg):
            return arg if arg else ''

        file = form.cleaned_data['file']
        if file.name.endswith('.csv'):
            # process csv
            pass
        else:

            cols = [
                form.cleaned_data['description'],
                form.cleaned_data['unit_price'],
                form.cleaned_data['unit'],
                form.cleaned_data['quantity'],
                form.cleaned_data['subtotal'],
            ]
            wb = openpyxl.load_workbook(file.file)
            try:
                ws = wb.get_sheet_by_name(form.cleaned_data['sheet_name'])
            except:
                ws = wb.active

            inv = Invoice.objects.create(
                date=form.cleaned_data['date'],
                due=form.cleaned_data['due'],
                status='invoice',
                invoice_number=form.cleaned_data['invoice_number'],
                draft=True,
                customer=form.cleaned_data['customer'],
                salesperson=form.cleaned_data['salesperson'],
            )
            start = int(form.cleaned_data['start_row'])
            index = 0
            for row in ws.iter_rows(min_row=form.cleaned_data['start_row'],
                                    max_row=form.cleaned_data['end_row'],
                                    max_col=max(cols)):
                index += 1
                current = start + index

                unit = None
                quantity = None
                unit_price = None
                item = None
                component = None

                try: 
                    quantity = float(row[form.cleaned_data['quantity']-1].value)
                except:
                    messages.info(self.request, 'Cannot process invoice line because of invalid'
                        ' quantity on row {}'.format(current))
                    continue

                try: 
                    unit_price = float(row[form.cleaned_data['unit_price']-1].value)
                except:
                    messages.info(self.request, 'Cannot process invoice line because of invalid'
                        ' unit price on row {}'.format(current))
                    continue

                qs = UnitOfMeasure.objects.filter(name=null_buster(row[
                    form.cleaned_data['unit'] - 1].value))
                if qs.exists():
                    unit = qs.first()
                else:
                    unit_string = null_buster(
                            row[form.cleaned_data['unit'] - 1].value)
                    if unit_string == '':
                        messages.info(self.request, 'Cannot process invoice line because of invalid'
                        ' unit on row {}'.format(current))
                        continue

                    unit = UnitOfMeasure.objects.create(
                        name=unit_string)
                desc = row[form.cleaned_data['description'] - 1].value
                if not desc:
                    messages.info(self.request, 'Cannot process invoice line because of invalid'
                        ' description on row {}'.format(current))
                    continue

                if desc.startswith('*'):
                    # if a sevice
                    qs = Service.objects.filter(name=desc[1:])
                    if qs.exists():
                        service = qs.first()
                    else:
                        service = Service.objects.create(
                            name=desc,
                            description=desc,
                            hourly_rate=0.0,
                            flat_fee=unit_price,
                            is_listed=True)

                    component = ServiceLineComponent.objects.create(
                        service=service,
                        hours=quantity,
                        flat_fee=unit_price
                    )
                    InvoiceLine.objects.create(
                        service=component,
                        tax=form.cleaned_data['sales_tax'],
                        line_type=2,
                        invoice=inv
                    )
                else:
                    qs = InventoryItem.objects.filter(name=desc)
                    if qs.exists():
                        item = qs.first()
                    else:
                        item = InventoryItem.objects.create(
                            name=desc,
                            type=0,
                            description=desc,
                            unit=unit,
                            product_component=ProductComponent.objects.create(
                                pricing_method=0,
                                direct_price=unit_price,
                                tax=form.cleaned_data['sales_tax']
                            ))

                    component = ProductLineComponent.objects.create(
                        product=item,
                        unit_price=unit_price,
                        quantity=quantity,
                    )
                    InvoiceLine.objects.create(
                        product=component,
                        tax=form.cleaned_data['sales_tax'],
                        line_type=1,
                        invoice=inv
                    )

        return resp
