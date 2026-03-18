# comercial/forms.py

from django import forms
from .models import Producto, Cotizacion, DetalleCotizacion
from apps.usuarios.models import Usuario


class ProductoForm(forms.ModelForm):
    class Meta:
        model  = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'stock', 'activo']
        widgets = {
            'nombre':       forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio':       forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria':    forms.Select(attrs={'class': 'form-select'}),
            'stock':        forms.NumberInput(attrs={'class': 'form-control'}),
            'activo':       forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CotizacionAcudienteForm(forms.ModelForm):
    """
    Formulario para el acudiente.
    Solo puede escribir observaciones — NO puede elegir estado.
    El estado siempre será 'pendiente' automáticamente.
    """
    class Meta:
        model  = Cotizacion
        fields = ['observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Escribe alguna observación o nota (opcional)...'
            }),
        }


class CotizacionCoordinadorForm(forms.ModelForm):
    """
    Formulario para el coordinador/admin.
    Puede cambiar el estado y ver todas las opciones.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['acudiente'].queryset = Usuario.objects.filter(
            rol=Usuario.ROL_ACUDIENTE
        )

    class Meta:
        model  = Cotizacion
        fields = ['acudiente', 'estado', 'observaciones']
        widgets = {
            'acudiente':     forms.Select(attrs={'class': 'form-select'}),
            'estado':        forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DetalleCotizacionForm(forms.ModelForm):
    class Meta:
        model  = DetalleCotizacion
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto':        forms.Select(attrs={'class': 'form-select'}),
            'cantidad':        forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }