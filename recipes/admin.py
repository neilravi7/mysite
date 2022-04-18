from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Recipe, RecipeIngredients

# Register your models here.
# getting user model
user = get_user_model()

class RecipeIngredientInline(admin.ModelAdmin):
    readonly_fields = ['quantity_as_float', 'as_mks', 'as_imperial']
    raw_fields = ['user']

class RecipeAdmin(admin.ModelAdmin):
    inline = "RecipeIngredientInline"
    list_display = ['name', 'user']
    readonly_fields = ['created', 'updated']
    raw_id_fields = ['user']

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientInline)