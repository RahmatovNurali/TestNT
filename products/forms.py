from django import forms
from products import models


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ('title','price','category')