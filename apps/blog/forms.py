from django import forms
from .models import Publicacion, Comentario, Categoria


class PublicacionForm(forms.ModelForm):
    class Meta:
        model  = Publicacion
        fields = ['titulo', 'categoria', 'resumen', 'contenido', 'imagen', 'estado', 'destacada']
        widgets = {
            'titulo':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la publicación'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'resumen':   forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Breve descripción…'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'imagen':    forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'estado':    forms.Select(attrs={'class': 'form-select'}),
            'destacada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model  = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu comentario…'
            }),
        }
        labels = {'texto': ''}


class CategoriaForm(forms.ModelForm):
    class Meta:
        model  = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
