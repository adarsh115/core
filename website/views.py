from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import TemplateView, DetailView, CreateView, FormView, UpdateView, ListView
from website import models
import os
from app.utils import ContextMixin, ProductFilterMixin
from django_filters.views import FilterView
from app.filters import ProductFilter


# Create your views here.
class DepartmentView(ContextMixin, ProductFilterMixin, FilterView):
    model = models.WebDepartment
    template_name = os.path.join('website', 'department.html')
    filterset_class = ProductFilter

    def get_queryset(self):
        dept = models.WebDepartment.objects.get(pk=self.kwargs['pk'])
        _qs =  models.Product.objects.filter(category__department = dept)
        return self.get_pg_qs(_qs)

class CategoryView(ContextMixin, ProductFilterMixin, FilterView):
    model = models.Category
    template_name = os.path.join('website', 'category.html')
    filterset_class = ProductFilter

    def get_queryset(self):
        obj = models.Category.objects.get(pk=self.kwargs['pk'])
        _qs =  models.Product.objects.filter(category = obj)
        return self.get_pg_qs(_qs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.object = models.Category.objects.get(pk=self.kwargs['pk'])
        
        self.update_context(context)

        context['object'] = self.object
        context['crumbs'] = [{'label': self.object.department.name, 'link': reverse('app:department', kwargs={'pk': self.object.department.pk})}, {'label': self.object.name, 'link': '#'}]
        context['crumb_title'] = context['crumbs'][-1]['label']
        return context

class AboutView(ContextMixin, TemplateView):
    ctxt = {
        'crumbs':[{'label': 'Aout', 'link': '#'}]
    } 

    template_name = os.path.join('website', 'about.html')
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['settings'] = models.Settings.objects.first()
        return context

class FaqView(ContextMixin, TemplateView):
    template_name = os.path.join('website', 'faq.html')

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['faqs'] = models.FaqCategory.objects.all()
        return context

class WishlistView(ContextMixin, LoginRequiredMixin,TemplateView):
    ctxt = {
        'crumbs': [{'label': 'Wish List', 'link': '#'}]
    }
    template_name = os.path.join('website', 'wishlist.html')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context['items'] = self.request.user.wishlistitem_set.all()

        return context