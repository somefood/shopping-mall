from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='이름')

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('products:category', args=[self.id])

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, verbose_name='이름')
    description = models.TextField(verbose_name='설명')
    price = models.PositiveIntegerField(default=0, verbose_name='가격')

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.id])

    class Meta:
        verbose_name = '상품'
        verbose_name_plural = '상품'


