from django import forms
from django.forms import inlineformset_factory
from .models import Cotizacion, ItemCotizacion


class CotizacionForm(forms.ModelForm):
    class Meta:
        model  = Cotizacion
        fields = ['observacion']
        widgets = {
<<<<<<< HEAD
            'observacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe aquí alguna observación o nota adicional (opcional)...'
            }),
=======
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
>>>>>>> 19d2c3af1c98f2eda2fa8b1aec62310d8c577731
        }


class ItemCotizacionForm(forms.ModelForm):
    class Meta:
        model  = ItemCotizacion
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
<<<<<<< HEAD
            'producto':        forms.Select(attrs={'class': 'form-select producto-select'}),
            'cantidad':        forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El precio se asigna desde el servidor; no lo validamos en el form
        self.fields['precio_unitario'].required = False

=======
            'producto':        forms.Select(attrs={'class': 'form-select'}),
            'cantidad':        forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

>>>>>>> 19d2c3af1c98f2eda2fa8b1aec62310d8c577731

ItemFormSet = inlineformset_factory(
    Cotizacion, ItemCotizacion,
    form=ItemCotizacionForm,
    extra=1, can_delete=True
)
