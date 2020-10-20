from django.urls import path
from website import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('category/<int:pk>', views.CategoryView.as_view(), name='category'),
    path('department/<int:pk>', views.DepartmentView.as_view(), name='department'),
    path('category/<int:pk>', views.CategoryView.as_view(), name='category'),
    path('about/<int:pk>', views.AboutView.as_view(), name='about'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('faq-detail/<int:pk>', views.FAQDetailView.as_view(), name='faq-detail'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('featured/', views.FeaturedView.as_view(), name='featured'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('search/', views.search, name='search')





]

