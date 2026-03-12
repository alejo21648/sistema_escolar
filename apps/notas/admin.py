from django.contrib import admin
from .models import Nota


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display  = ('estudiante', 'asignacion', 'periodo', 'valor', 'fecha')
    list_filter   = ('periodo', 'asignacion__materia', 'asignacion__curso')
    search_fields = ('estudiante__first_name', 'estudiante__last_name')
