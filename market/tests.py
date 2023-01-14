from django.test import TestCase
from .models import *

# Create your tests here.

class CategoryTestCase(TestCase):
    def setup(self):
        Category.objects.create('sports')
        Category.objects.create('shirts')
        sports = Category.objects.get(name='sports')
        shirts = Category.objects.get(name='shirts')
        self.assertEqual(sports, 'sports')
        self.assertEqual(shirts, 'shirts')
        sports.delete()
        shirts.delete()
