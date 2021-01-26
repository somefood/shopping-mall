from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path("create_ajax/", views.OrderCreateAjaxView.as_view(), name="order_create_ajax"),
    path("checkout/", views.OrderCheckoutAjaxView.as_view(), name="order_checkout"),
    path("validation/", views.OrderImpAjaxView.as_view(), name="order_validation"),
    path("complete/", views.order_complete, name="order_complete"),
]