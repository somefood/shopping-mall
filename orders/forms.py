from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['postal_code',
                  'address',
                  'detail_address',
                  'extra_address',
                  'phone_number',
                  ]
