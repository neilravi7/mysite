"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from recipes import views as views

urlpatterns = [
    path('base/template', views.base_template_view, name = "base_template"),
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('article/', include('article.urls')),
    path('accounts/', include('accounts.urls')),
    path('recipe/', include('recipes.urls')),
]
