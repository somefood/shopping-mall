from django.shortcuts import get_list_or_404
from django.urls import path
from django.views.generic import TemplateView

from myproject.urls import HomeView
from . import views
from .models import Product, Category

app_name = 'products'

urlpatterns = [
    path('category/', views.ProductListView.as_view(), name='all_list'),
    path('category/<int:pk>/', views.ProductListView.as_view(), name='category'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
]