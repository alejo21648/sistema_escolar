from django import forms
from .models import Producto, CategoriaProducto


class ProductoForm(forms.ModelForm):
    class Meta:
        model  = Producto
        fields = ['categoria', 'nombre', 'descripcion', 'precio', 'stock', 'imagen', 'activo']
        widgets = {
            'categoria':   forms.Select(attrs={'class': 'form-select'}),
            'nombre':      forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio':      forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock':       forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen':      forms.FileInput(attrs={'class': 'form-control'}),
            'activo':      forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
