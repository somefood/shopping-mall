from django.contrib import admin
from .models import Order, OrderItem, OrderTransaction


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'address']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderTransaction)
class OrderTransactionAdmin(admin.ModelAdmin):
    pass