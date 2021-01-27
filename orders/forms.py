from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'name',
            'phone_number',
            'email',
            'postal_code',
            'address',
            'detail_address',
            'extra_address',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '이름'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '연락처'}),
            'email': forms.EmailInput(attrs={'placeholder': '이메일'}),
            'postal_code': forms.TextInput(attrs={'id': 'postcode', 'placeholder': '우편번호'}),
            'address': forms.TextInput(attrs={'id': 'address', 'placeholder': '주소'}),
            'detail_address': forms.TextInput(attrs={'id': 'detailAddress', 'placeholder': '상세 주소'}),
            'extra_address': forms.TextInput(attrs={'id': 'extraAddress', 'placeholder': '추가 주소'}),
        }
