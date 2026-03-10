from django.contrib import admin
from .models import Curso, EstudianteCurso, Materia, AsignacionProfesorMateria


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'año_lectivo', 'activo')
    list_filter   = ('año_lectivo', 'activo')
    search_fields = ('nombre',)


@admin.register(EstudianteCurso)
class EstudianteCursoAdmin(admin.ModelAdmin):
    list_display  = ('estudiante', 'curso', 'fecha_ingreso', 'activo')
    list_filter   = ('activo', 'curso')
    search_fields = ('estudiante__first_name', 'estudiante__last_name')


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'activa')
    list_filter   = ('activa',)
    search_fields = ('nombre',)


@admin.register(AsignacionProfesorMateria)
class AsignacionAdmin(admin.ModelAdmin):
    list_display  = ('profesor', 'materia', 'curso', 'activa')
    list_filter   = ('activa', 'curso', 'materia')
    search_fields = ('profesor__first_name', 'profesor__last_name', 'materia__nombre')
