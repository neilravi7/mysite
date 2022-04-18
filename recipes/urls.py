from django.urls import path
from . import views 

urlpatterns=[
    # path('list', RecipeListView.as_view(), 'recipe_view'),
    path('list', views.recipe_list_view, name='recipe_list'),
    path('<int:number>/<str:enc_string>', views.recipe_detail_view, name='recipe_detail'),
    path('create', views.recipe_create_view, name='recipe_create'),
    path('create/ingredients', views.recipe_ingredients_create_view, name='recipe_ingredients_create'),
]