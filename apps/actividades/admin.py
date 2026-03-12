from django.contrib import admin
from .models import Actividad, EntregaActividad


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display  = ('titulo', 'asignacion', 'fecha_entrega', 'valor_maximo')
    list_filter   = ('asignacion__materia', 'asignacion__curso')
    search_fields = ('titulo',)


@admin.register(EntregaActividad)
class EntregaAdmin(admin.ModelAdmin):
    list_display  = ('estudiante', 'actividad', 'calificacion', 'entregado_en')
    list_filter   = ('actividad__asignacion__materia',)
    search_fields = ('estudiante__first_name', 'estudiante__last_name')
