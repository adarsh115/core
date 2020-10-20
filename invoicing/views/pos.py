from invoicing import models
from employees import models as employee_models
from django.http import JsonResponse
import json
import datetime
from inventory.models import InventoryItem
from accounting.models import Tax
from invoicing.models import ProductLineComponent, SalesConfig
from django.views.generic import TemplateView
import os


class POSAppView(TemplateView):
    template_name = os.path.join('invoicing', 'pos.html')


def process_sale(request):
    data = json.loads(request.body)
    timestamp = datetime.datetime.strptime(data['timestamp'].split('.')[0],
                                           '%Y-%m-%dT%H:%M:%S')
    session = models.POSSession.objects.get(pk=data['sessionID'])
    
    sales_person = models.SalesRepresentative.objects.get(
        pk=data['salesPersonID']
    )

    # support having a generic customer
    customer = models.Customer.objects.get(
        pk=data['customer_id']
    )

    invoice = models.Invoice.objects.create(
        date=timestamp.date(),
        due=timestamp.date(),
        customer=customer,
        salesperson=sales_person,
        draft=False,
        status='paid',
        ship_from=SalesConfig.objects.first().default_warehouse
    )

    for line in data['products']:
        product = InventoryItem.objects.get(pk=line['id'])
        component = ProductLineComponent.objects.create(
            product=product,
            unit_price=line['price'],
            quantity=line['quantity']

        )
        tax = None
        if line['tax_id']:
            tax = Tax.objects.get(pk=line['tax_id'])

        models.InvoiceLine.objects.create(
            invoice=invoice,
            product=component,
            line_type=1,
            tax=tax
        )

    sale = models.POSSale.objects.create(
        session=session,
        invoice=invoice,
        timestamp=timestamp
    )

    for payment in data['payments']:
        method = models.PaymentMethod.objects.get(pk=payment['method_id'])
        models.Payment.objects.create(
            invoice=invoice,
            amount=payment['tendered'],
            date=timestamp.date(),
            sales_rep=sales_person,
            timestamp=timestamp,
            method=method
        )

    

    # update inventory
    invoice.update_inventory()

    return JsonResponse({'sale_id': invoice.pk})


def start_session(request):
    data = json.loads(request.body)
    timestamp = datetime.datetime.strptime(data['timestamp'].split('.')[0],
                                           '%Y-%m-%dT%H:%M:%S')

    
    sales_person = employee_models.Employee.objects.filter(
        user=request.user
    )
    if not sales_person.exists():
        sales_person = employee_models.Employee.objects.first()
    else:
        sales_person = sales_person.first()
    
    session = models.POSSession.objects.create(
        start=timestamp,
        sales_person=sales_person
    )

    # return a session id
    return JsonResponse({
        'id': session.pk,
        'rep': sales_person.short_name, 
        'rep_id': sales_person.pk, 
        })


# if a session is unended, use the timestamp of the last sale to end the session
def end_session(request):
    data = json.loads(request.body)
    timestamp = datetime.datetime.strptime(data['timestamp'].split('.')[0],
                                           '%Y-%m-%dT%H:%M:%S')
    session = models.POSSession.objects.get(pk=data['id'])
    session.end = timestamp
    session.save()
    return JsonResponse({
        'status': 'OK'
    })
