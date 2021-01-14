from django.shortcuts import render
from django.shortcuts import get_list_or_404
from .models import Category, Product
from django.views.generic import ListView, DetailView


class ProductListView(ListView):
    model = Product
    context_object_name = 'product_list'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = get_list_or_404(Category)
        context['selected_category'] = self.selected_category
        return context

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            self.selected_category = Category.objects.get(pk=kwargs['pk'])
            self.queryset = Product.objects.filter(category=kwargs['pk'])
        return super().get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product_detail'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = get_list_or_404(Category)
        return context