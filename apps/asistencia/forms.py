from django import forms
from .models import Asistencia
from apps.academico.models import AsignacionProfesorMateria


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model  = Asistencia
        fields = ['estudiante', 'asignacion', 'fecha', 'estado', 'observacion']
        widgets = {
            'estudiante':   forms.Select(attrs={'class': 'form-select'}),
            'asignacion':   forms.Select(attrs={'class': 'form-select'}),
            'fecha':        forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado':       forms.Select(attrs={'class': 'form-select'}),
            'observacion':  forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, profesor=None, **kwargs):
        super().__init__(*args, **kwargs)
        if profesor:
            self.fields['asignacion'].queryset = AsignacionProfesorMateria.objects.filter(
                profesor=profesor, activa=True
            ).select_related('materia', 'curso')
