from operator import imod
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from recipes.forms import RecipeForm, RecipeModelForm, RecipeIngredientsModelForm, IngredientsFormset
from recipes.models import Recipe, RecipeIngredients
from mysite.utils import url_encode_utils
from django.urls import reverse
from django import forms 
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
    return render(request, 'recipes/main_list_article.html', context)
    # return render(request, 'recipes/list.html', context)

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
    return render(request, 'base.html', context=context)
    # return render(request, 'test_htmx.html', context=context)

def recipe_and_ingredients_view(request):
    """Save both recipes and it's ingredients togeather.

    Args:
        request (post): ?

    Returns:
        _type_: success and failers 
    """    
    context = {
        'recipe_form':RecipeModelForm(),
        # 'recipe_ingredient_form':RecipeIngredientsModelForm(),
        'ingredient_formset':IngredientsFormset()
    }
    if request.method == 'POST':
        recipe_form = RecipeModelForm(request.POST or None)

        ingredient_formset = IngredientsFormset(request.POST or None)
        context['ingredient_formset'] = ingredient_formset
        context['recipe_form'] = recipe_form

        if all([recipe_form.is_valid()]):
            recipe_obj = recipe_form.save(commit=False)
            recipe_obj.user_id = request.user.id
            recipe_obj.save()

            print("recipe obj saved")
            for ri_form in ingredient_formset:
                if ri_form.is_valid():
                    ingredient_obj = ri_form.save(commit=False)
                    print("ingredient_obj", ingredient_obj)
                    ingredient_obj.recipe = recipe_obj
                    ingredient_obj.save()
                    print("ingredient_obj saved")

    return render(request, 'recipes/create_both.html', context=context)

def recipe_ingredients_update_view(request, id):
    """
        Update recipe object and it's ingredients together.
        all ingredients objects saved together.
        set_all() : all ingredients objects.

    Args:
        request (Update): _description_
        id (_type_): instance id (recipe ID)

    Returns:
        _type_: success massage (HTTPS 200) at success 
    """    
    recipe_obj = Recipe.objects.get(id=id)
    recipe_form = RecipeModelForm(request.POST or None, instance=recipe_obj)
    # ingredient_form = RecipeIngredientsModelForm(request.POST or None)
    qs = recipe_obj.recipeingredients_set.all()
    RecipeIngredientsFormset = forms.modelformset_factory(RecipeIngredients, form=RecipeIngredientsModelForm, extra=0)
    ingredient_formset = RecipeIngredientsFormset(request.POST or None, queryset=qs)
    
    context = {
        'recipe_form':recipe_form,
        'ingredient_formset': ingredient_formset
    }
    if all([recipe_form.is_valid(), ingredient_formset.is_valid()]):
        recipe_obj = recipe_form.save(commit=False)
        recipe_obj.save() 
        for ingredient in ingredient_formset:
            print("ingredients updated")
            ingredient_obj = ingredient.save(commit=False)
            ingredient_obj.recipe = recipe_obj
            ingredient_obj.save()
    
    return render(request, 'recipes/dynamic_formset.html', context=context)  