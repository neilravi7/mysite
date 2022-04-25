from distutils.command.clean import clean
from django import forms
from .models import Recipe, RecipeIngredients
from django.utils.text import slugify


class RecipeModelForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']
    
    def clean(self):
        cleaned_data = self.cleaned_data
        name_slug = slugify(cleaned_data.get("name"))
        if Recipe.objects.filter(slug=name_slug).exists():
            self.add_error("name", "try diffrent name")
        return cleaned_data
    

class RecipeForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    directions = forms.CharField(widget=forms.Textarea)

class RecipeIngredientsModelForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ['name', 'description', 'directions', 'quantity', 'unit']
    
    def clean(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data['name']
        if RecipeIngredients.objects.filter(name__icontains=name).exists():
            self.add_error("name", "Ingredients already exists.")
        return cleaned_data