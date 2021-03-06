import random

import os
import datetime
import invoicing
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (DeleteView, DetailView, FormView, ListView,
                                  TemplateView)
from django.views.generic.edit import CreateView, FormView, UpdateView
from django_filters.views import FilterView
from wkhtmltopdf import utils as pdf_tools
from wkhtmltopdf.views import PDFTemplateView
from messaging.views import UserEmailConfiguredMixin
from messaging.models import UserProfile
from rest_framework.authtoken.models import Token

from common_data import filters, models, serializers, forms
from common_data.models import GlobalConfig, Organization
from common_data.utilities import (ContextMixin,
                                   apply_style,
                                   MultiPageDocument,
                                   MultiPagePDFDocument,
                                   ConfigWizardBase)
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from django.apps import apps
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import services
from messaging.email_api.email import EmailSMTP
from messaging.forms import PrePopulatedEmailForm
import json
from common_data.schedules import backup_db
from common_data.middleware.license import license_check
import urllib


try:
    backup_db(repeat=Task.DAILY)
except:
    pass


class DocumentPaginationMixin():
    pass


class PaginationMixin(object):
    '''quick and dirty mixin to support pagination on filterviews '''

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if not self.queryset and hasattr(self, 'get_queryset'):
            self.queryset = self.get_queryset()

        filter = self.filterset_class(self.request.GET, queryset=self.queryset)
        object_list = filter.qs

        if not self.paginate_by:
            self.paginate_by = 20

        p = Paginator(object_list, self.paginate_by)

        page_str = self.request.GET.get('page')
        try:
            page = p.page(page_str)
        except PageNotAnInteger:
            # gets first page
            page = p.page(1)
        except EmptyPage:
            # gets last page
            page = p.page(p.num_pages)

        context['object_list'] = page
        context['paginator'] = p
        context['is_paginated'] = True
        context['page_obj'] = page

        return context


CREATE_TEMPLATE = os.path.join('common_data', 'create_template.html')
CRISPY_TEMPLATE = os.path.join('common_data', 'crispy_create_template.html')

#########################################################
#                  Organization Views                   #
#########################################################


class OrganizationCreateView(ContextMixin, LoginRequiredMixin, CreateView):
    template_name = CRISPY_TEMPLATE
    form_class = forms.OrganizationForm
    extra_context = {
        'title': 'Add Organization'
    }


class OrganizationUpdateView(ContextMixin, LoginRequiredMixin, UpdateView):
    template_name = CRISPY_TEMPLATE
    form_class = forms.OrganizationForm
    model = models.Organization
    extra_context = {
        'title': 'Update Organization details'
    }


class OrganizationDetailView(ContextMixin, LoginRequiredMixin, DetailView):
    template_name = os.path.join('common_data', 'organization', 'detail.html')
    model = models.Organization


class OrganizationListView(ContextMixin,
                           PaginationMixin,
                           LoginRequiredMixin,
                           FilterView):
    template_name = os.path.join('common_data', 'organization', 'list.html')
    queryset = models.Organization.objects.all()
    filterset_class = filters.OrganizationFilter
    extra_context = {
        'title': 'Organization List',
        'new_link': reverse_lazy('base:organization-create')
    }


#########################################################
#                    Individual Views                   #
#########################################################

class IndividualCreateView(ContextMixin,  LoginRequiredMixin, CreateView):
    template_name = CRISPY_TEMPLATE
    form_class = forms.IndividualForm
    extra_context = {
        'title': 'Add Individual',
        'description': 'Register a human that interacts with your business either as a customer or supplier or an employee of one of the two.',
        'related_links': [{
            'name': 'Add Organization',
            'url': '/base/organization/create'
        }]
    }


class IndividualUpdateView(ContextMixin,  LoginRequiredMixin, UpdateView):
    template_name = CRISPY_TEMPLATE
    form_class = forms.IndividualForm
    model = models.Individual
    extra_context = {
        'title': 'Update Individual details',
        'description': 'Register a human that interacts with your business either as a customer or supplier or an employee of one of the two.',
        'related_links': [{
            'name': 'Add Organization',
            'url': '/base/organization/create'
        }]
    }


class IndividualDetailView(ContextMixin,  LoginRequiredMixin, DetailView):
    template_name = os.path.join('common_data', 'individual', 'detail.html')
    model = models.Individual


class IndividualListView(ContextMixin, PaginationMixin,  LoginRequiredMixin,
                         FilterView):
    template_name = os.path.join('common_data', 'individual', 'list.html')
    queryset = models.Individual.objects.all()
    filterset_class = filters.IndividualFilter
    extra_context = {
        'title': 'List of Individuals',
        'new_link': reverse_lazy('base:individual-create')
    }


class WorkFlowView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join("common_data", "workflow.html")

    def get(self, *args, **kwargs):
        if not GlobalConfig.objects.first().is_configured:
            return HttpResponseRedirect(reverse_lazy('base:config-wizard'))
        else:
            return super().get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        date = datetime.date.today()
        context["month"] = "{}/{}".format(date.year, date.month)
        return context


class ReactTestView(TemplateView):
    template_name = os.path.join("common_data", "react_test.html")


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join("common_data", "about.html")


class GlobalConfigView(ContextMixin,  LoginRequiredMixin, UpdateView):
    template_name = os.path.join("common_data", "config.html")
    model = models.GlobalConfig
    form_class = forms.GlobalConfigForm
    success_url = '/invoicing/'
    extra_context = {
        'title': 'Configure global application features'
    }

    def get_initial(self):
        if self.object.organization:
            return {
                'organization_name': self.object.organization.legal_name,
                'organization_logo': self.object.logo,
                'organization_address':
                self.object.organization.business_address,
                'organization_email': self.object.organization.email,
                'organization_phone': self.object.organization.phone,
                'organization_website': self.object.organization.website,
                'organization_business_partner_number':
                self.object.organization.bp_number
            }

        return None

    def form_valid(self, form):
        resp = super().form_valid(form)

        if self.object.organization:
            org = self.object.organization
        else:
            org = Organization()

        org.legal_name = form.cleaned_data['organization_name']
        org.business_address = form.cleaned_data['organization_address']
        org.website = form.cleaned_data['organization_website']
        org.bp_number = \
            form.cleaned_data['organization_business_partner_number']
        org.email = form.cleaned_data['organization_email']
        org.phone = form.cleaned_data['organization_phone']
        org.logo = form.cleaned_data['organization_logo']

        org.save()
        self.object.organization = org
        self.object.save()

        return resp


class AuthenticationView(FormView):
    # TODO add features to use as a plugin for views that require
    # authentication
    form_class = forms.AuthenticateForm
    template_name = os.path.join('common_data', 'authenticate.html')
    success_url = "/base/workflow"


def get_logo_url(request):
    return JsonResponse({'url': models.GlobalConfig.logo_url()})


# class SendEmail(ContextMixin,  LoginRequiredMixin, FormView):
#     template_name = CREATE_TEMPLATE
#     form_class = forms.SendMailForm
#     success_url = reverse_lazy('invoicing:home')
#     extra_context = {
#         'title': 'Compose New Email'
#     }

#     def post(self, request):
#         resp = super(SendEmail, self).post(request)
#         form = self.form_class(request.POST)
#         config = models.GlobalConfig.objects.first()
#         if form.is_valid():
#             send_mail(
#                 form.cleaned_data['subject'],
#                 form.cleaned_data['content'],
#                 config.email_user,
#                 [form.cleaned_data['recipient']])
#             return resp
#         return resp


class PDFException(Exception):
    pass


# class EmailPlusPDFView(UserEmailConfiguredMixin,
#                        CreateView,
#                        MultiPagePDFDocument):
#     '''THe pagination is optional, it will be ignored '''
#     form_class = PrePopulatedEmailForm  # SendMailForm
#     template_name = os.path.join('messaging', 'email', 'compose.html')
#     success_url = None
#     pdf_template_name = None
#     inv_class = None

#     def get(self, *args, **kwargs):
#         return super().get(*args, **kwargs)

#         try:
#             return super().get(*args, **kwargs)
#         except PDFException:
#             return HttpResponse('<p>An error occurred rendering the PDF</p>')

#         except Exception as e:
#             raise e

#     def get_initial(self):
#         if not self.inv_class:
#             raise ValueError(
#                 'Improperly configured, needs an inv_class attribute')

#         inv = self.inv_class.objects.get(pk=self.kwargs['pk'])

#         out_file = os.path.join(os.getcwd(), 'media', 'temp', 'out.pdf')
#         if os.path.exists(out_file):
#             out_file = os.path.join(
#                 os.getcwd(),
#                 'media',
#                 'temp',
#                 f'out_{random.randint(1, 100000)}.pdf')

#         # use the context for pagination and the object
#         obj = self.inv_class.objects.get(pk=self.kwargs['pk'])
#         context = {
#             'object': obj,
#         }
#         config = GlobalConfig.objects.first()
#         context.update(config.__dict__)
#         context.update({
#             'logo': config.logo,
#             'logo_width': config.logo_width,
#             'business_name': config.business_name,
#             'business_address': config.business_address
#         })
#         options = {
#             'output': out_file
#         }
#         try:
#             pdf_tools.render_pdf_from_template(
#                 self.pdf_template_name, None, None,
#                 apply_style(context),
#                 cmd_options=options)

#         except Exception as e:
#             print('Error occured creating pdf %s' % e)
#             raise PDFException()

#         return {
#             'owner': self.request.user.pk,
#             'folder': 'sent',
#             'attachment_path': out_file
#         }

#     def post(self, request, *args, **kwargs):
#         resp = super(EmailPlusPDFView, self).post(
#             request, *args, **kwargs)
#         form = self.form_class(request.POST)

#         if not form.is_valid():
#             return resp

#         u = UserProfile.objects.get(user=self.request.user)
#         e = EmailSMTP(u)

#         self.object.attachment.name = form.cleaned_data['attachment_path']
#         self.object.save()

#         e.send_email_with_attachment(
#             form.cleaned_data['subject'],
#             form.cleaned_data['to'].address,
#             form.cleaned_data['body'],
#             open(form.cleaned_data['attachment_path'], 'rb'),
#             html=True
#         )

#         if not self.pdf_template_name:
#             raise ValueError(
#                 'Improperly configured. Needs pdf_template_name attribute.')

#         if os.path.exists(form.cleaned_data['attachment_path']):
#             os.remove(form.cleaned_data['attachment_path'])

#         return resp


class UserAPIView(ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    model = User


class UserDetailAPIView(RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    model = User


def get_current_user(request):
    if request.user:
        return JsonResponse({
            'pk': request.user.pk,
            'name': request.user.username
        })

    return JsonResponse({'pk': None})


class LicenseErrorPage(TemplateView):
    template_name = os.path.join('common_data', 'licenses_error.html')


class LicenseFeaturesErrorPage(TemplateView):
    template_name = os.path.join('common_data', 'license_error_features.html')


class UsersErrorPage(TemplateView):
    template_name = os.path.join('common_data', 'users_error.html')


class CreateSuperUserView(FormView):
    form_class = forms.CreateSuperuserForm
    template_name = os.path.join('common_data', 'user_create.html')
    success_url = '/login'

    def get(self, request, *args, **kwargs):
        if User.objects.all().count() > 0:
            return HttpResponseRedirect('/login/')

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        resp = super().form_valid(form)
        User.objects.create_superuser(form.cleaned_data['username'],
                                      form.cleaned_data['email'],
                                      form.cleaned_data['password'],)
        return resp


class LicenseCheck(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if os.path.exists('license.json'):
            with open('license.json', 'r') as lic_f:
                data = json.load(lic_f)
                context.update(data)
        return context

    def get(self, *args, **kwargs):
        HID = models.GlobalConfig.generate_hardware_id()
        with open('key.txt', 'w') as f:
            f.write(HID)
        if not os.path.exists('license.json'):
            self.template_name = os.path.join(
                'common_data', 'licensing', 'no_license.html')
            # later implement a form where a person can send their hardware id
        else:
            output = license_check()
            if output == 'ok':
                self.template_name = os.path.join(
                    'common_data', 'licensing', 'valid_license.html')
            else:
                self.template_name = os.path.join(
                    'common_data', 'licensing', 'invalid_license.html')

        return super().get(*args, **kwargs)


NOTE_TARGET = {
    'work_order': services.models.ServiceWorkOrder,
    'lead': invoicing.models.Lead
}


def create_note(request):
    global NOTE_TARGET
    '''This simple function allows a large variety of objects to support 
    notes without modification. The global note target dictionary mapps 
    strings of notes with their corresponding objects to which the notes are 
    applied. Thus each note request must have an author, a message and 
    identification for the target namely its classname and the objects primary 
    key'''
    if not hasattr(request.user, 'employee'):
        messages.info(
            request, 'Only users linked to employees can write notes')
        return JsonResponse({'status': 'error'})

    attachment = request.FILES.get('attachment')

    note = models.Note.objects.create(
        author=request.user.employee,
        note=request.POST['note'],
        attachment=attachment
    )

    NOTE_TARGET[request.POST['target']].objects.get(
        pk=request.POST['target_id']
    ).notes.add(note)

    return JsonResponse({'status': 'ok'})


class PDFDetailView(PDFTemplateView):
    model = None
    context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.model.objects.get(pk=self.kwargs['pk'])
        context.update(self.context)
        return context

ALIAS_MAPPING = {
        'salesperson': 'salesrepresentative',
        'ship_from': 'warehouse',
        'account_paid_from': 'account',
        'ship_to': 'warehouse',
        'paid_to': 'supplier',
        'vendor': 'supplier',
        'parent_account': 'account',
        'procedure': 'serviceprocedure',
        'team': 'salesteam',
        'source': 'leadsource',
        'contacts': 'individual'
    }

APP_LIST = ['services', 'inventory', 'common_data', 'messaging',
                'accounting', 'employees', 'planner', 'messaging', 'invoicing']

def get_model_latest(request, model_name=None):
    model_name = ALIAS_MAPPING.get(model_name, model_name)
    latest = None
    for app in APP_LIST:
        try:
            model = apps.get_model(app_label=app, model_name=model_name)
            if model.objects.all().count() > 0:
                latest = model.objects.latest('pk')

        except LookupError:
            pass

    if not latest:
        return JsonResponse({'data': -1})

    return JsonResponse({'data': [latest.pk, str(latest)]})

def get_models_latest(request):
    mapping = {
        'organization': '/base/organization/create',
        'parent_account': '/accounting/create-account',
        'account_paid_from': '/accounting/create-account',
        'ship_from': '/inventory/warehouse-create/',
        'ship_to': '/inventory/warehouse-create/',
        'warehouse': '/inventory/warehouse-create/',
        'customer': '/invoicing/create-customer/',
        'salesperson': '/invoicing/create-sales-rep',
        'supplier': '/inventory/supplier/create',
        'paid_to': '/inventory/supplier/create',
        'vendor': '/inventory/supplier/create',
        'salesteam': '/invoicing/create-sales-team',
        'leadsource': '/invoicing/create-lead-source',
        'journal': '/accounting/create-journal',
        'procedure': '/services/create-procedure',
        'service': '/services/create-service',
        'contacts': '/base/individual/create',
        'interactiontype': '/invoicing/create-interaction-type',
    }

    payload = {}
    scraped = json.loads(request.POST['names'])
    for name in scraped:
        model_name = ALIAS_MAPPING.get(name, name)
        latest = None
        model = None
        for app in APP_LIST:
            try:
                model = apps.get_model(app_label=app, model_name=model_name)
                if model.objects.all().count() > 0:
                    latest = model.objects.latest('pk')

            except LookupError:
                pass

        if model:
            payload[name] = {
                'name': str(latest) if latest else '', 
                'value': latest.pk if latest else None,
                'link': mapping.get(name, '')}

    return JsonResponse(payload)



class ConfigWizard(ConfigWizardBase):
    template_name = os.path.join('common_data', 'wizard.html')
    form_list = [forms.GlobalConfigForm]
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'logo'))
    config_class = GlobalConfig
    success_url = reverse_lazy('base:workflow')

    # TODO fix logo and file handling
    def post(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)

    def done(self, form_list, **kwargs):
        """Because there is only one form"""
        for form in form_list:
            form.save()
        return super().done(form_list, **kwargs)


def document_notes_api(request, document=None, id=None):
    notes = []
    mapping = {
        'service': services.models.ServiceWorkOrder,
        'lead': invoicing.models.Lead
    }

    obj = mapping.get(document)
    if not obj:
        return JsonResponse({'status': 'not found'})
        
    doc = obj.objects.get(pk=id)

    notes = [{
        'note': i.note, 
        'author': i.author.pk,
        'timestamp': i.timestamp.strftime("%d %b '%y, %H:%M"),
        'attachment': i.attachment.url if i.attachment else ''
        
        }
                 for i in doc.notes.all()]

    return JsonResponse(notes, safe=False)


class ReportBlankView(TemplateView):
    template_name = os.path.join('common_data', 'reports', 'blank.html')


def current_db(request):
    # TODO support other database types
    with open(os.path.join('database', 'config.json')) as fil:
        config = json.load(fil)
        return JsonResponse({
            'db': config['current'].strip('sqlite3')
        })


class ConfigAPIView(RetrieveAPIView):
    queryset = GlobalConfig.objects.all()
    serializer_class = serializers.ConfigSerializer


def get_token_for_current_user(request):
    if not request.user.is_anonymous:
        token, _ = Token.objects.get_or_create(user=request.user)
        return JsonResponse({'token': token.key})

    return JsonResponse({
        'detail': "The request's user is not signed in",
        'token': ''
        })

class IndividualViewset(viewsets.ModelViewSet):
    queryset = models.Individual.objects.all()
    serializer_class = serializers.IndividualSerializer


class IndividualBulkCreateAPIView(generics.CreateAPIView):
    queryset = models.Individual.objects.all()
    
    def get_serializer(self, *args, **kwargs):
        return serializers.BulkIndividualSerializer(many=True, *args, **kwargs)    


class OrganizationViewset(viewsets.ModelViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer