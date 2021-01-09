from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator

from .forms import ProfileForm
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView


class AccountSignupView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in kwargs:
            context['profile_form'] = ProfileForm
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        self.object2 = None
        form = self.get_form()
        form2 = ProfileForm(request.POST)
        if form.is_valid() and form2.is_valid():
            self.object = form.save()
            self.object2 = form2.save(commit=False)
            self.object2.user = self.object
            self.object2.save()
            return super().form_valid(form)
        else:
            print(form2.errors)
            return self.render_to_response(self.get_context_data(form=form, profile_form=form2))



class AccountDetailView(DetailView):
    model = User
    context_object_name = 'join_user'
    template_name = 'accounts/detail.html'


@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class AccountUpdateView(UpdateView):
    model = User
    form_class = UserCreationForm
    context_object_name = 'join_user'
    success_url = reverse_lazy('accounts:update')
    template_name = 'accounts/update.html'