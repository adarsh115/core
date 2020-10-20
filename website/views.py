from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import TemplateView, DetailView, CreateView, FormView, UpdateView, ListView
from website import models
import os
from website.utilities import ContextMixin, InventoryFilterMixin
from django_filters.views import FilterView
from website.filters import InventoryFilter
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse


# Create your views here.

class Home(ContextMixin, TemplateView):
    template_name = os.path.join('website', 'website_home.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured'] = models.InventoryItem.objects.filter(featured=True)[:3]

        #if none, select at random

        # context['best_sellers'] = models.InventoryItem.objects.filter(discount__gt=0)
        return context

class DepartmentView(ContextMixin, InventoryFilterMixin, FilterView):
    model = models.Department
    template_name = os.path.join('website', 'department.html')
    filterset_class = InventoryFilter

    def get_queryset(self):
        dept = models.Department.objects.get(pk=self.kwargs['pk'])
        _qs =  models.InventoryItem.objects.filter(category__department = dept)
        return self.get_pg_qs(_qs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.object = models.Department.objects.get(pk=self.kwargs['pk'])
        
        self.update_context(context)

        context['object'] = self.object
        context['crumbs'] = [{'label': self.object.name, 'link': '#'}]
        context['crumb_title'] = context['crumbs'][-1]['label']
        return context

class CategoryView(ContextMixin, InventoryFilterMixin, FilterView):
    model = models.Category
    template_name = os.path.join('website', 'category.html')
    filterset_class = InventoryFilter

    def get_queryset(self):
        obj = models.Category.objects.get(pk=self.kwargs['pk'])
        _qs =  models.InventoryItem.objects.filter(category = obj)
        return self.get_pg_qs(_qs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.object = models.Category.objects.get(pk=self.kwargs['pk'])
        
        self.update_context(context)

        context['object'] = self.object
        context['crumbs'] = [{'label': self.object.department.name, 'link': reverse('website:department', kwargs={'pk': self.object.department.pk})}, {'label': self.object.name, 'link': '#'}]
        context['crumb_title'] = context['crumbs'][-1]['label']
        return context

class AboutView(ContextMixin, TemplateView):
    ctxt = {
        'crumbs':[{'label': 'About', 'link': '#'}]
    } 

    template_name = os.path.join('website', 'about.html')
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['settings'] = models.WebSettings.objects.first()
        return context

class FAQView(ContextMixin, TemplateView):
    template_name = os.path.join('website', 'faq.html')

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        print(context)
        context['faqs'] = models.FaqCategory.objects.all()
        return context


class FAQDetailView(ContextMixin, DetailView):
    template_name = os.path.join('website', 'faq_info.html')
    model = models.FaqCategory

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if not self.object:
            self.get_object()

        context['crumbs'] = [
            {
                'label': 'FAQ',
                'link': reverse('website:faq')
            },
        ]

        context['crumb_title'] = self.object.name

        return context


class WishlistView(ContextMixin,TemplateView):
    ctxt = {
        'crumbs': [{'label': 'Wish List', 'link': '#'}]
    }
    template_name = os.path.join('website', 'wishlist.html')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context['items'] = self.request.user.wishlistitem_set.all()

        return context

class OrderView(DetailView):
    model = models.Order
    # template_name = os.path.join ('app', 'invoice.html')

    def get_context_data(self, *args, **kwargs): 
        context = super(OrderView, 
             self).get_context_data(*args, **kwargs) 
        context["settings"] = models.AppSettings.objects.first()        
        return context 




class DiscountView(ContextMixin, ListView):
    ctxt = {
        'image': '/static/website/images/discount.jpg',
        'description': "Listed are the best deals available on Nomie's Collection!"
        " All products are massively discounted."
    }
    template_name = os.path.join('website', 'custom.html')

    def get_queryset(self):
        return models.InventoryItem.objects.filter(discount__gt=0)


class FeaturedView(ContextMixin, ListView):
        template_name = os.path.join('website', 'custom.html')
        ctxt = { 
            'image': '/website/static/website/images/logo3.png',
            'description': 'Ever wanted a personal shopper?'
                            'This collection is made up of specially curated'
                            'products from a wide range of categories'
        }

        def get_queryset(self):
            return models.InventoryItem.objects.filter(featured=True)
        

def search(request):
    #search products
    text = request.GET['text']
    results = []
    for res in models.InventoryItem.objects.filter(Q(
        Q(name__icontains=text) |
        Q(description__icontains=text)
    )):
        results.append({'name': res.name, 'link': reverse(
            'website:inventoryitem', kwargs={'pk': res.pk})})

    #search departments
    for res in models.Department.objects.filter(Q(
        Q(name__icontains=text) |
        Q(description__icontains=text)
    )):
        results.append({'name': "Department: %s" % res.name, 'link': reverse(
            'website:department', kwargs={'pk': res.pk})})

    #search categories
    for res in models.Category.objects.filter(Q(
        Q(name__icontains=text) |
        Q(description__icontains=text)
    )):
        results.append({'name': "Category: %s" % res.name, 'link': reverse(
            'website:category', kwargs={'pk': res.pk})})

    return JsonResponse({'results': results})
