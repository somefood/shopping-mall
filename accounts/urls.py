from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import index, AccountSignupView

app_name = "accounts"

urlpatterns = [
    path('index/', index, name='index'),
    path('signup/', AccountSignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]