from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import ProfileForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            return self.render_to_response(self.get_context_data(form=form, profile_form=form2))