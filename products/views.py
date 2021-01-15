from django.shortcuts import render
from django.shortcuts import get_list_or_404
from .models import Category, Product
from django.views.generic import ListView, DetailView


class ProductListView(ListView):
    # 어떤 테이블에서 객체 리스트를 가져올 것인지 지정해주기
    model = Product
    # 템플릿 파일로 넘겨주는 객체 리스트의 이름 지정
    context_object_name = 'product_list'
    # 템플릿 파일 위치 지정
    template_name = 'products/product_list.html'
    # 한 페이지에서 보여주는 페이지 갯수 지정 (페이징)
    # paginate_by = 1

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
    context_object_name = 'product'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = get_list_or_404(Category)
        return context