from .models import Profile
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nickname', 'phone_number', 'birth_day')
        widgets = {
            'nickname': forms.TextInput(attrs={'placeholder': '닉네임을 입력해주세요.'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '전화번호를 입력해주세요.'}),
            'birth_day': forms.TextInput(attrs={'placeholder': '생년월일을 입력해주세요.'}),
        }