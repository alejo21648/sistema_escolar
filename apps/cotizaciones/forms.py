from django import forms
from django.forms import inlineformset_factory
from decimal import Decimal
from .models import Cotizacion, ItemCotizacion


class CotizacionForm(forms.ModelForm):
    class Meta:
        model  = Cotizacion
        fields = ['observacion']
        widgets = {
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                 'placeholder': 'Observaciones opcionales...'}),
        }


class ItemCotizacionForm(forms.ModelForm):
    class Meta:
        model  = ItemCotizacion
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-select item-producto',
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control item-cantidad',
                'min': 1,
                'step': 1,
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control item-precio',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00',
            }),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 1:
            raise forms.ValidationError('La cantidad debe ser al menos 1.')
        return cantidad

    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')
        if precio is not None:
            if precio <= Decimal('0'):
                raise forms.ValidationError('El precio unitario debe ser mayor a cero ($0.00).')
            if precio > Decimal('9999999.99'):
                raise forms.ValidationError('El precio unitario no puede superar $9,999,999.99.')
        return precio

ItemFormSet = inlineformset_factory(
    Cotizacion, ItemCotizacion,
    form=ItemCotizacionForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)