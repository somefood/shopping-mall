from django.contrib import admin
from .models import Order, OrderDetail


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'address']


@admin.register(OrderDetail)
class OrderAdmin(admin.ModelAdmin):
    pass