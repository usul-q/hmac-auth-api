from django.urls import path
from .models import CustomUser
from . import views

urlpatterns = [
    path('users/', views.get_users),
    path('register/', views.create_user),
    path('user/<int:id>/', views.get_user),
    path('login/', views.view_details),
    path('user/secret/', views.reveal_secret),
]