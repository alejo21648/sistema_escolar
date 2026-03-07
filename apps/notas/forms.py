from django import forms
from .models import Nota
from apps.academico.models import AsignacionProfesorMateria


class NotaForm(forms.ModelForm):
    class Meta:
        model  = Nota
        fields = ['estudiante', 'asignacion', 'periodo', 'valor', 'descripcion']
        widgets = {
            'estudiante':  forms.Select(attrs={'class': 'form-select'}),
            'asignacion':  forms.Select(attrs={'class': 'form-select'}),
            'periodo':     forms.Select(attrs={'class': 'form-select'}),
            'valor':       forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '10'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, profesor=None, **kwargs):
        super().__init__(*args, **kwargs)
        if profesor:
            # Mostrar solo las asignaciones del profesor que registra
            self.fields['asignacion'].queryset = AsignacionProfesorMateria.objects.filter(
                profesor=profesor, activa=True
            ).select_related('materia', 'curso')
