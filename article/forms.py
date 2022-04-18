import imp
from tkinter.tix import Form
from turtle import tilt
from django import forms
from .models import Article
from django.forms import ModelForm

class ArticleFormOld(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

    # def cleaned_title(self):
    #     if Article.objects.filter(title__iexact=self.title).exits():
    #         raise forms.ValidationError("this title is taken")
    #     return self.title

    def clean(self):
        cleaned_data = self.cleaned_data
        if Article.objects.filter(title__iexact=cleaned_data.get("title")).exists():
            # print("Title Validations errors")
            self.add_error('title', 'This title already taken')
            # raise forms.ValidationError("this title is taken")
        # if cleaned_data.get('title') == "The Toaster Project":
        #     print("Validations Errors")
        #     raise forms.ValidationError("this title is taken")
        return cleaned_data

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        print("Data :", data)
        if Article.objects.filter(title__iexact=data.get('title')).exists():
            print("Adding errors")
            self.add_error('title', f'Title {data.get("title")} is already taken')
        return data
