from operator import imod
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from recipes.forms import RecipeForm, RecipeModelForm, RecipeIngredientsModelForm
from recipes.models import Recipe
from mysite.utils import url_encode_utils
from django.urls import reverse
# Create your views here.

# class RecipeListView(ListView):
#     model = Recipe

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['recipe_list'] = Recipe.objects.filter()
#         return context

def recipe_list_view(request):
    recipes = Recipe.objects.filter()
    context = {
        "recipes" : recipes
    }
    return render(request, 'recipes/list.html', context)

def recipe_detail_view(request, number, enc_string):
    slug = url_encode_utils(enc_string, "decode")
    print("slug :: ", slug)
    
    recipe = Recipe.objects.get(slug=slug)
    
    print(recipe.name)

    context = {
        'recipe':recipe
    }
    
    return render(
        request,
        'recipes/detail.html',
        context=context
    )

def recipe_create_view(request):
    form = RecipeModelForm()
    
    context = {
        'form':form,
        'created':False
    }
    
    if request.method == 'POST':
        form =  RecipeModelForm(request.POST, None)
        context['form'] = form
        if form.is_valid():
            recipe_obj = form.save(commit=False)
            recipe_obj.user = request.user
            recipe_obj.save()
            context['object'] = recipe_obj
            context['created'] = True

    return render(request, 'recipes/create.html', context=context)

def recipe_ingredients_create_view(request):
    form = RecipeIngredientsModelForm()
    
    context = {
        'form':form,
        'created':False
    }
    
    if request.method == 'POST':
        form =  RecipeIngredientsModelForm(request.POST, None)
        context['form'] = form
        if form.is_valid():
            recipe_ing_obj = form.save()
            if recipe_ing_obj.pk:
                print("object created")
                context['object'] = recipe_ing_obj
                context['created'] = True
            else:
                print("Got some error.")

    return render(request, 'recipes/create.html', context=context)