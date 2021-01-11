from django.contrib import admin
from .models import Category, Product, Photo


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

# Photo 클래스를 inline
class PhotoInline(admin.TabularInline):
    model = Photo

# Product 클래스는 해당하는 Photo 객체를 리스트로 관리한다.
#@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]

# Register your models here.
admin.site.register(Product, ProductAdmin)