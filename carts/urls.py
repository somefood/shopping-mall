from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.detail, name='detail'),
    path('add/<int:product_id>/', views.add, name='product_add'),
    path('remove/<int:product_id>/', views.remove, name='product_remove'),
]