from cgitb import lookup
import os
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from random import randint
from cryptography.fernet import Fernet
from django.db.models import Q


# Create your models here.

class ActiveBlogs(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class ArticleManager(models.Manager):
    def search(self, query):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        return Article.objects.filter(lookup)


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(
        auto_now=False, auto_now_add=False, default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        key = bytes(os.environ.get('ENC_SECRET'), 'utf-8')
        f = Fernet(key)
        fernet_string = bytes(self.slug, 'utf-8')
        encoded_string = f.encrypt(fernet_string)
        return f'{randint(567, 8750432)}/{encoded_string.decode()}'

    def save(self, *args, **kwargs):
        # Check how the current values differ from ._loaded_values. For example,
        # prevent changing the creator_id of the model. (This example doesn't
        # support cases where 'creator_id' is deferred).
        # if not self._state.adding and (
        #         self.creator_id != self._loaded_values['creator_id']):
        #     raise ValueError("Updating the value of creator isn't allowed")
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    '''Article default model managers'''
    # objects = models.Manager()
    objects = ArticleManager()

    '''Active Article models managers'''
    active_blogs = ActiveBlogs()


def article_pre_save(*args, **kwargs):
    print("article signal called")
    pass


pre_save.connect(article_pre_save, sender=Article)


def article_post_save(*args, **kwargs):
    print("article post save signal called")
    pass


post_save.connect(article_post_save, sender=Article)