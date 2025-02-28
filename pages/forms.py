from django import forms
from .models import Product  # Asegúrate de que el modelo Product exista en models.py

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # O especifica los campos que necesitas
