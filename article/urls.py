from django.urls import path

from . import views

urlpatterns = [
    path('',views.article_home_view, name='article_list'),
    path('<int:number>/<str:url_string>', views.article_detail_view, name='article_detail'),
    path('search/', views.article_search_view, name='article_search'),
    path('create/new', views.article_create_view, name='article_create'),
    
]