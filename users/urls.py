"""this module handles the user app urls"""

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# API endpoints
urlpatterns = format_suffix_patterns([
    path('', views.HelloView().as_view(), name="hello"),
    path('users/register/', views.CreateUserView().as_view(), name="register"),
    path('users/login/', views.LoginView().as_view(), name="login"),
])