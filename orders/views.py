from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic import FormView
from .forms import OrderCreateForm
from .models import Order, OrderItem, OrderTransaction
from products.models import Product
from django.contrib import messages
from carts.cart import Cart


class OrderCreateView(View):
    def get_cart(self):
        return Cart(self.request)

    def get(self, request, *args, **kwargs):
        cart = self.get_cart()
        form = OrderCreateForm()
        return render(request, "orders/create.html", {'carts': cart, 'form': form})

    def post(self, request, *args, **kwargs):
        cart = self.get_cart()
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
        if cart.coupon:
            order.coupon = cart.coupon
            # order.discount = cart.coupon.amout
            order.discount = cart.get_discount_total()
            order.save()
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()
        return render(request, 'orders/created.html', {'order': order})


# JS 동작하지 않는 환경에서도 주문은 가능해야한다.
def order_complete(request):
    order_id = request.GET.get('order_id')
    # order = Order.objects.get(id=order_id)
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/created.html', {'order': order})


class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)

        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.get_discount_total()
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            data = {
                "order_id": order.id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


# 트랜잭션 생성
# 결제 정보 생성
class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        amount = request.POST.get('amount')

        try:
            merchant_order_id = OrderTransaction.objects.create_new(
                order=order,
                amount=amount
            )
        except Exception as e:
            merchant_order_id = None
            print(e)
        print(merchant_order_id)
        if merchant_order_id is not None:
            data = {
                "works": True,
                "merchant_id": merchant_order_id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'test': 'test'}, status=401)


class OrderImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        try:
            trans = OrderTransaction.objects.get(
                order=order,
                merchant_order_id=merchant_id,
                amount=amount
            )
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            #trans.success = True
            trans.save() # 저장 시, 시그널 함수 작동해서 문제 생기면 예외 발생
            order.paid = True
            order.save()

            data = {
                "works": True
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)
