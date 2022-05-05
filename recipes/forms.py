import json
from distutils.command.clean import clean
from django import forms
from .models import Recipe, RecipeIngredients
from django.utils.text import slugify


class RecipeModelForm(forms.ModelForm):
    error_css_class = 'invalid-feedback'
    # fields_class = "form-inline my-2 my-lg-0"
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


'''
    Django model form.
'''


class IngredientsBaseFormset(forms.BaseFormSet):

    def __init__(self, *args, **kwargs):
        super(IngredientsBaseFormset, self).__init__(*args, **kwargs)
        self.queryset = RecipeIngredients.objects.none()

class RecipeIngredientsModelForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ['name', 'quantity', 'unit']

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     name = cleaned_data['name']
    #     if RecipeIngredients.objects.filter(name__icontains=name).exists():
    #         self.add_error("name", "Ingredients already exists.")
    #     return cleaned_data


# models formset for ingredients
IngredientsFormset = forms.modelformset_factory(
    RecipeIngredients,
    form=RecipeIngredientsModelForm,
    formset=IngredientsBaseFormset,
    extra=5
)

"""Django Simple forms"""


class IngredientsForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    directions = forms.CharField(widget=forms.Textarea)
    quantity = forms.CharField()
    unit = forms.CharField()


IngredientsFormset_2 = forms.formset_factory(form=IngredientsForm, extra=5)
