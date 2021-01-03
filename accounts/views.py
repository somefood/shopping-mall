from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView


def index(request):
    return render(request, 'accounts/index.html')


class AccountSignupView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:index')
    template_name = 'accounts/signup.html'