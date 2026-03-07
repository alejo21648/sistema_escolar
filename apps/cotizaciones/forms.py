from django import forms
from django.forms import inlineformset_factory
from .models import Cotizacion, ItemCotizacion


class CotizacionForm(forms.ModelForm):
    class Meta:
        model  = Cotizacion
        fields = ['observacion']
        widgets = {
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ItemCotizacionForm(forms.ModelForm):
    class Meta:
        model  = ItemCotizacion
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto':        forms.Select(attrs={'class': 'form-select'}),
            'cantidad':        forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


ItemFormSet = inlineformset_factory(
    Cotizacion, ItemCotizacion,
    form=ItemCotizacionForm,
    extra=1, can_delete=True
)
