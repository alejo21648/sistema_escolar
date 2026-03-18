from django import forms
from django.forms import inlineformset_factory
from .models import Cotizacion, ItemCotizacion


class CotizacionForm(forms.ModelForm):
    class Meta:
        model  = Cotizacion
        fields = ['observacion']
        widgets = {
            'observacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe aquí alguna observación o nota adicional (opcional)...'
            }),
        }


class ItemCotizacionForm(forms.ModelForm):
    class Meta:
        model  = ItemCotizacion
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto':        forms.Select(attrs={'class': 'form-select producto-select'}),
            'cantidad':        forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El precio se asigna desde el servidor; no lo validamos en el form
        self.fields['precio_unitario'].required = False


ItemFormSet = inlineformset_factory(
    Cotizacion, ItemCotizacion,
    form=ItemCotizacionForm,
    extra=1, can_delete=True
)