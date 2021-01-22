from django import template
from products.models import Category

register = template.Library()


@register.filter
def is_category(value):
    if isinstance(value, Category):
        return value.name
    else:
        return "전체"