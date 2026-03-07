from django import forms
from .models import Actividad, EntregaActividad
from apps.academico.models import AsignacionProfesorMateria


class ActividadForm(forms.ModelForm):
    class Meta:
        model  = Actividad
        fields = ['asignacion', 'titulo', 'descripcion', 'fecha_entrega', 'valor_maximo']
        widgets = {
            'asignacion':    forms.Select(attrs={'class': 'form-select'}),
            'titulo':        forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion':   forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'fecha_entrega': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'valor_maximo':  forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
        }

    def __init__(self, *args, profesor=None, **kwargs):
        super().__init__(*args, **kwargs)
        if profesor:
            self.fields['asignacion'].queryset = AsignacionProfesorMateria.objects.filter(
                profesor=profesor, activa=True
            ).select_related('materia', 'curso')


class EntregaForm(forms.ModelForm):
    class Meta:
        model  = EntregaActividad
        fields = ['archivo', 'comentario']
        widgets = {
            'archivo':    forms.FileInput(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CalificacionEntregaForm(forms.ModelForm):
    class Meta:
        model  = EntregaActividad
        fields = ['calificacion', 'retroalimentacion']
        widgets = {
            'calificacion':       forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'retroalimentacion':  forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
