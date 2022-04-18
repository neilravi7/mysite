from django.urls import path
from . import views

urlpatterns = [
    path('register', views.view_register, name='register'),
    path('login', views.view_login, name='login'),
    path('logout', views.view_logout, name='logout'),
]