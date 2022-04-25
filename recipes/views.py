from operator import imod
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from recipes.forms import RecipeForm, RecipeModelForm, RecipeIngredientsModelForm
from recipes.models import Recipe, RecipeIngredients
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
        'created':False,
        'action':'create_recipe'
    }
    
    if request.method == 'POST':
        form =  RecipeModelForm(request.POST, None)
        context['form'] = form
        context['action'] = 'create_recipe'

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
        'created':False,
        'action':'create_recipe_ingredient'
    }
    
    if request.method == 'POST':
        form =  RecipeIngredientsModelForm(request.POST, None)
        context['form'] = form
        context['action'] = 'create_recipe_ingredient'

        if form.is_valid():
            recipe_ing_obj = form.save()
            if recipe_ing_obj.pk:
                # print("object created")
                context['object'] = recipe_ing_obj
                context['created'] = True
            else:
                print("Got some error.")

    return render(request, 'recipes/create.html', context=context)

def recipe_ingredients_update_view(request, id):
    instance = RecipeIngredients.objects.get(id=id)
    form = RecipeIngredientsModelForm(instance = instance)
    context = {
        'form':form,
        'created':False,
        'action':'update_recipe_ingredient'
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


def base_template_view(request):
    context = {
        "text":"test view of base template."
    }
    return render(request, 'article/main_list_article.html', context=context)
    # return render(request, 'test_htmx.html', context=context)

def recipe_and_ingredients_view(request):
    context = {
        'recipe_form':RecipeModelForm(),
        'recipe_ingredient_from':RecipeIngredientsModelForm()
    }
    if request.method == 'POST':
        recipe_form = RecipeModelForm(request.POST or None)
        recipe_ingredient_from = RecipeIngredientsModelForm(request.POST or None)
        context['recipe_form'] = recipe_form
        context['recipe_ingredient_from'] = recipe_ingredient_from
        for rec in Recipe.objects.all():
            print("-> ", rec.name)

        if all([recipe_form.is_valid(), recipe_ingredient_from.is_valid()]):
            print("Cleaned Data: ", recipe_form.cleaned_data)
            
            recipe_obj = recipe_form.save(commit=False)
            # print("name : ", recipe_obj.name)
            ingredient_obj = recipe_ingredient_from.save(commit=False)
            recipe_obj.user_id = request.user.id
            # print("Who :", request.user)
            recipe_obj.save()
            
            if recipe_obj.pk:
                print("recipe created")    
                ingredient_obj.recipe_id = recipe_obj.pk
                ingredient_obj.save()
                if ingredient_obj.pk:
                    print("Ingredients created")

    return render(request, 'recipes/create_both.html', context=context)