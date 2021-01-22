from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('form_test/', views.OrderFormView.as_view(), name='test'),
]