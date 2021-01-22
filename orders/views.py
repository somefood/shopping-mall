from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import FormView
from .forms import OrderForm


class OrderFormView(FormView):
    form_class = OrderForm
    template_name = 'orders/test.html'