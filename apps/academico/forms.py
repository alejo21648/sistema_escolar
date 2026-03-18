from django import forms
from .models import Curso, Materia, AsignacionProfesorMateria, EstudianteCurso
from apps.usuarios.models import Usuario


class CursoForm(forms.ModelForm):
    class Meta:
        model  = Curso
        fields = ['nombre', 'descripcion', 'año_lectivo', 'activo']
        widgets = {
            'nombre':      forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'año_lectivo': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo':      forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MateriaForm(forms.ModelForm):
    class Meta:
        model  = Materia
        fields = ['nombre', 'descripcion', 'activa']
        widgets = {
            'nombre':      forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activa':      forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AsignacionForm(forms.ModelForm):
    class Meta:
        model  = AsignacionProfesorMateria
        fields = ['profesor', 'materia', 'curso', 'activa']
        widgets = {
            'profesor': forms.Select(attrs={'class': 'form-select'}),
            'materia':  forms.Select(attrs={'class': 'form-select'}),
            'curso':    forms.Select(attrs={'class': 'form-select'}),
            'activa':   forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profesor'].queryset = Usuario.objects.filter(
            rol=Usuario.ROL_PROFESOR, is_active=True
        )


class EstudianteCursoForm(forms.ModelForm):
    class Meta:
        model  = EstudianteCurso
        fields = ['estudiante', 'curso', 'activo']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-select'}),
            'curso':      forms.Select(attrs={'class': 'form-select'}),
            'activo':     forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estudiante'].queryset = Usuario.objects.filter(
            rol=Usuario.ROL_ESTUDIANTE, is_active=True
        )
