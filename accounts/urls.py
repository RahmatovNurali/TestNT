from django.contrib.auth.views import LoginView
from django.urls import path

from accounts.views import register

urlpatterns = [
    path('register', register, name='register'),
    path('login', LoginView.as_view(
        next_page='product_list',
        template_name='auth/login.html',
    ), name='login_page'),
]
