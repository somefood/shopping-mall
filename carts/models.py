from django.db import models
from products.models import Product


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    class Meta:
        ordering = ['created_at']


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='장바구니 ID')
    quantity = models.PositiveIntegerField(default=0, verbose_name='수량')
    active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)