from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('category/', views.ProductListView.as_view(), name='all_list'),
    path('category/<int:pk>/', views.ProductListView.as_view(), name='category'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
]