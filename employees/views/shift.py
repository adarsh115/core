import urllib
import json
import os
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from common_data.utilities import ContextMixin
from employees import models
from employees import forms
from django_filters.views import FilterView
from rest_framework.viewsets import ModelViewSet
from employees import serializers
from employees import filters
from common_data.views import PaginationMixin

CREATE_TEMPLATE = os.path.join('common_data', 'create_template.html')


class ShiftCreateView(ContextMixin, CreateView):
    template_name = CREATE_TEMPLATE
    form_class = forms.ShiftForm
    extra_context = {
        'title': 'Create Shift'
    }


class ShiftUpdateView(ContextMixin, UpdateView):
    template_name = CREATE_TEMPLATE
    form_class = forms.ShiftForm
    model = models.Shift
    extra_context = {
        'title': 'Update Shift'
    }


class ShiftScheduleListView(ContextMixin, PaginationMixin, FilterView):
    filterset_class = filters.ShiftScheduleFilter
    model = models.ShiftSchedule
    template_name = os.path.join('employees', 'shifts', 'schedule', 'list.html')
    extra_context = {
        'new_link':  '/employees/shift-schedule/create/'
    }


class ShiftListView(ContextMixin, PaginationMixin, FilterView):
    filterset_class = filters.ShiftFilter
    model = models.Shift
    template_name = os.path.join('employees', 'shifts', 'list.html')
    extra_context = {
        'new_link':  '/employees/shift/create'
    }


class ShiftScheduleDetailView(DetailView):
    template_name = os.path.join(
        'employees', 'shifts', 'schedule', 'detail.html')
    model = models.ShiftSchedule


class ShiftDetailView(DetailView):
    template_name = os.path.join('employees', 'shifts', 'detail.html')
    model = models.Shift


class ShiftScheduleCreateView(ContextMixin,CreateView):
    template_name = os.path.join(
        'employees', 'shifts', 'schedule', 'create.html')
    form_class = forms.ShiftScheduleForm

    extra_context = {
        'title': 'Create Shift Schedule'
    }

    def form_valid(self, form):
        resp = super().form_valid(form)
      
        data_string = form.cleaned_data['shift_lines']
        data = json.loads(urllib.parse.unquote(data_string))

        for line in data:
            models.ShiftScheduleLine.objects.create(
                schedule=self.object,
                start_time=line['startTime'],
                end_time=line['endTime'],
                shift=models.Shift.objects.get(
                    pk=line['shift'].split('-')[0]
                ),
                monday=line['monday'],
                tuesday=line['tuesday'],
                wednesday=line['wednesday'],
                thursday=line['thursday'],
                friday=line['friday'],
                saturday=line['saturday'],
                sunday=line['sunday'],
            )

        return resp


class ShiftScheduleUpdateView(ContextMixin, UpdateView):
    template_name = os.path.join(
        'employees', 'shifts', 'schedule', 'create.html')
    form_class = forms.ShiftScheduleForm
    model = models.ShiftSchedule
    extra_context = {
        'title': 'Update Shift Schedule'
    }


    def form_valid(self, form):
        resp = super().form_valid(form)
      
        data_string = form.cleaned_data['shift_lines']
        data = json.loads(urllib.parse.unquote(data_string))

        #clear all existing lines before reconstructing the lines
        models.ShiftScheduleLine.objects.filter(schedule=self.object).delete()

        for line in data:
            try: 
                shift = line['shift'].split('-')[0]
            except:
                #if not a string with -, then an integer
                shift = line['shift']

            models.ShiftScheduleLine.objects.create(
                schedule=self.object,
                start_time=line['startTime'],
                end_time=line['endTime'],
                shift=models.Shift.objects.get(
                    pk=shift
                ),
                monday=line['monday'],
                tuesday=line['tuesday'],
                wednesday=line['wednesday'],
                thursday=line['thursday'],
                friday=line['friday'],
                saturday=line['saturday'],
                sunday=line['sunday'],
            )

        return resp


class ShiftAPIView(ModelViewSet):
    queryset = models.Shift.objects.all()
    serializer_class = serializers.ShiftSerializer


class ShiftScheduleAPIView(ModelViewSet):
    queryset = models.ShiftSchedule.objects.all()
    serializer_class = serializers.ShiftScheduleSerializer