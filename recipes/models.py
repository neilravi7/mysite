import os
import pint
from django.db import models
from django.conf import settings
from .validators import validate_unit_of_measure
from .utils import number_str_to_float
from random import randint
from cryptography.fernet import Fernet
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Create your models here.

"""
- Global
    - Ingredients
    - Recipes
- User
    - Ingredients
    - Recipes
        - Ingredients
        - Directions for Ingredients
"""

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField()
    name = models.CharField(max_length=220)
    description = models.TextField()
    directions = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def get_hidden_url(self):
        key = bytes(os.environ.get('ENC_SECRET'), 'utf-8')
        f = Fernet(key)
        fernet_string = bytes(self.slug, 'utf-8')
        encoded_string = f.encrypt(fernet_string)
        return f'{randint(567, 8750432)}/{encoded_string.decode()}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField()
    quantity = models.CharField(max_length=50)
    quantity_as_float = models.FloatField(blank=True, null=True)
    # pounds, lbs, oz, gram, etc
    unit = models.CharField(max_length=50, validators=[validate_unit_of_measure], blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        # Use as system
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit]
        return measurement

    def as_mks(self): 
        """Metric units are the SI(The International System of Units) or MKS(Meter-Kilogram-Second) system.
        Units:Metric system Vs. Imperial system
        Meter
        Litre
        Gram"""
        measurement = self.convert_to_system(system="mks")
        return measurement

    def as_imperial(self):
        '''Imperial units are the FPS(Foot Pound Second) System.
        Units:Metric system Vs. Imperial system
        Inch, Foot, Yard, Mile
        Pound
        Pint, Gallon'''
        
        measurement = self.convert_to_system(system="imperial")
        return measurement
        
    def save(self, *args, **kwargs) -> None:
        str_to_number , success = number_str_to_float(self.quantity)
        '''If success true'''
        if success:
           self.quantity_as_float = str_to_number
           
        return super().save(*args, kwargs)