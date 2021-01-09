from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import AccountSignupView, AccountDetailView, AccountUpdateView

app_name = "accounts"

urlpatterns = [
    path('signup/', AccountSignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('detail/<int:pk>', AccountDetailView.as_view(), name='detail'),
    path('update/<int:pk>', AccountUpdateView.as_view(), name='update'),

]