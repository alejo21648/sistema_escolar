from django.contrib import admin
from .models import Asistencia


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display  = ('estudiante', 'asignacion', 'fecha', 'estado')
    list_filter   = ('estado', 'fecha', 'asignacion__materia')
    search_fields = ('estudiante__first_name', 'estudiante__last_name')
    date_hierarchy = 'fecha'
