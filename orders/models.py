from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='OrderDetail')
    address = models.CharField(max_length=100, verbose_name='주소')
    phone_number = models.CharField(max_length=11, verbose_name='연락처')
    quantity = models.PositiveIntegerField(default=0)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = '주문'
        verbose_name_plural = '주문'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order} - {self.product}"

    class Meta:
        verbose_name = '주문_상세'
        verbose_name_plural = '주문_상세'
