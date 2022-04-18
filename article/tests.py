from django.test import TestCase
from django.utils.text import slugify

# Create your tests here.
from .models import Article

class ArticleTestCase(TestCase):
    def setUp(self):
        self.number_of_article = 100
        for obj in range(0, self.number_of_article):
            Article.objects.create(
                user_id=3,
                title="How to say no",
                content="An stumble art of don't give a fuck"
            )

    def test_queryset_exist(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.number_of_article)
    
    def test_slug(self):
        obj = Article.objects.filter().first()
        title = obj.title
        slug =  obj.slug
        slugify_title = slugify(obj.title)
        self.assertEqual(slugify_title, slug)

    def test_slug_unified(self):
        qs = Article.objects.filter()
        for obj in qs:
            slug = obj.slug
            title = obj.title
            slugify_title = slugify(title)
            self.assertNotEqual(slug, slugify_title)
