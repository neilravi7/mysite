# from multiprocessing import context
import os
import json
# from turtle import tilt
from django.contrib.auth.decorators import login_required
from cryptography.fernet import Fernet
from django.urls import reverse 
from django.shortcuts import render
from django.http import HttpResponseRedirect
from random import randint
from .models import Article
from .forms import ArticleForm

# Create your views here.

def article_home_view(request):
    articles = Article.objects.all()
    # list compression 
    # article_list = (
    #     {
    #         "id":article.id, 
    #         "slug":url_encode_utils(str(article.slug), 'encode').decode(), 
    #         "title":article.title,
    #         "number":randint(1, 12345)
            
    #     } 
    #     for article in articles
    # )
    return render(request, 'article/list.html',  {'articles':articles})


def article_detail_view(request, number, url_string):
    try:
        print("number", number)
        # print("URL STRING", url_string)
        url_string = url_encode_utils(url_string, 'decode')
        article = Article.objects.get(slug=url_string)
        return render(
            request,
            'article/detail.html',
            {
                "article":article
            }
        )
    except Article.DoesNotExist:
        return render(
            request, 
            'article/article_detail.html', 
            {
                "message":"No article found"
            }
        )

def article_search_view(request):
    query = request.GET.get('query')
    """Use if one specific fields start with an word"""
    # articles = Article.objects.filter(title__startswith=query_dict.get('query'))
    """Use to match pattern of word if contains word in sentences."""
    # using list compression 
    # Article.objects.search(query)

    article_list = (
        {
            "id":article.id, 
            "slug":article.get_absolute_url(), 
            "title":article.title
        }
        for article in Article.objects.search(query)
    )

    return render(
        request, 
        'article/search.html', 
        {
            'articles':article_list, 
            'query':query
            # "total":len(article_list)
        }
    )

# User should be authenticated
@login_required(login_url='/accounts/login')
def article_create_view(request):
    # It will return default empty forms in context
    form = ArticleForm()
    # print('Printing form related attributes:', dir(form))
    context = {
        "form":form
    }
    print("Before Deciding context :", context)
    if request.method == 'POST':
        form = ArticleForm(request.POST or None)
        context['form'] = form

        """Request handled by basic html forms"""

        # params = request.POST.dict()
        # print("params", params)

        # article_obj = Article.objects.create(
        #     user=request.user
        #     title = params.get('title'),
        #     content = params.get('content')
        # )
        # if article_obj.pk:    
        #     context['created'] = True
        #     context['object'] = article_obj

        """Return to created article details page."""
        
        # fernet_string = url_encode_utils(str(article.pk),'encode')
        # return HttpResponseRedirect(reverse('article_detail', args=[fernet_string.decode()]))

        """Request handled by django form system"""
        
        # if form.is_valid():
        #     print("Django Form Used")
        #     from_title_field = form.cleaned_data.get('title')
        #     form_content_field = form.cleaned_data.get('content')
        #     print("form :", form.cleaned_data)
        #     article_obj = Article.objects.create(
        #         user=request.user,
        #         title=from_title_field,
        #         content=form_content_field
        #     )
        #     context['created'] = True
        #     context['object'] = article_obj

        """Request handled by django model form system"""
        if form.is_valid():
            print("The form is valid")
            # print("Django Model Form Used")
            
            """Provide parameter commit=False to saving addition values
            before it's save instance"""
            
            article_obj = form.save(commit=False)
            """Saving user instance"""
            article_obj.user = request.user
            article_obj.save()
            context['created'] = True
            context['object'] = article_obj
            

            # print("Context in valid form    :", context)
            if article_obj.pk:
                # print(f"{article_obj.title} objects created.")
                fernet_string = url_encode_utils(str(article_obj.slug),'encode')
                return HttpResponseRedirect(
                    reverse(
                        'article_detail',
                        args=[randint(1, 12345), fernet_string.decode()
                    ]
                )
            )
    else:
        """Return Default Response """
        """Template context change accordingly [ModelForm, DjangoForm, HtmlBasicForm]"""
        return render(request, 'article/create.html', context=context)


# Url encoding decoding to hide parameters.
def url_encode_utils(target_data, target_action):
    # print("Target data", target_data)
    key = bytes(os.environ.get('ENC_SECRET'), 'utf-8')
    f = Fernet(key)
    if target_action == "encode":
        target_data = bytes(target_data, 'utf-8')
        return f.encrypt(target_data)
    elif target_action == "decode":
        # print("target_data :", target_data)
        target_data = target_data.encode()
        return f.decrypt(target_data).decode()