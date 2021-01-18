from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Category, Product, Photo


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

# Photo 클래스를 inline
class PhotoInline(admin.TabularInline):
    model = Photo

# Product 클래스는 해당하는 Photo 객체를 리스트로 관리한다.
#@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    inlines = [PhotoInline, ]
    # 특정 필드를 summer-note로 쓰려면 이렇게 사용.
    summernote_fields = ('description',)
    # 모든 필드를 summer-note로 쓰려면 이렇게 사용.
    # summernote_fields = '__all__'

# Register your models here.
admin.site.register(Product, ProductAdmin)