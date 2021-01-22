from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .forms import AddProductForm
from .cart import Cart


@require_POST # 어노테이션(데코레이터)
def add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = AddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        print(cd['is_update'])
        cart.add(product=product, quantity=cd['quantity'],
                 is_update=cd['is_update'])

        return redirect('carts:detail')


def remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('carts:detail')


def detail(request):
    cart = Cart(request)
    for product in cart:
        # 디테일란에서 수량 변경 시
        product['quantity_form'] = AddProductForm(initial={
            'quantity': product['quantity'], 'is_update': True
        })

    return render(request, 'carts/detail.html', {
        'carts': cart,
    })