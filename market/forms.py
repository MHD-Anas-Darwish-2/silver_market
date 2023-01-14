from django import forms
from .models import Category, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['slug']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category 
        fields = '__all__'
