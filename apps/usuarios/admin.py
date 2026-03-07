from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display   = ('username', 'email', 'get_full_name_display', 'rol', 'get_codigo_display', 'is_active')
    list_filter    = ('rol', 'is_active', 'fecha_nacimiento')
    search_fields  = ('username', 'email', 'first_name', 'last_name', 'codigo_estudiante', 'codigo_hijo')
    readonly_fields = ('get_relacion_info',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('rol', 'telefono', 'foto', 'fecha_nacimiento')
        }),
        ('Código de Estudiante', {
            'fields': ('codigo_estudiante',),
            'description': 'Código único para identificar estudiantes. Los acudientes usarán este código para relacionarse.',
        }),
        ('Código de Acudiente', {
            'fields': ('codigo_hijo', 'get_relacion_info'),
            'description': 'Campo para acudientes. Ingresa el código del estudiante (hijo) para relacionarlos.',
        }),
    )
    
    def get_full_name_display(self, obj):
        return obj.get_full_name() or 'Sin nombre'
    get_full_name_display.short_description = 'Nombre Completo'
    
    def get_codigo_display(self, obj):
        if obj.rol == Usuario.ROL_ESTUDIANTE and obj.codigo_estudiante:
            return f'Estudiante: {obj.codigo_estudiante}'
        elif obj.rol == Usuario.ROL_ACUDIENTE and obj.codigo_hijo:
            return f'Hijo: {obj.codigo_hijo}'
        elif obj.rol == Usuario.ROL_ACUDIENTE:
            return 'Acudiente: Sin relación'
        return '—'
    get_codigo_display.short_description = 'Código/Relación'
    
    def get_relacion_info(self, obj):
        if obj.rol == Usuario.ROL_ACUDIENTE and obj.codigo_hijo:
            try:
                hijo = Usuario.objects.get(codigo_estudiante=obj.codigo_hijo, rol=Usuario.ROL_ESTUDIANTE)
                return f'✓ Relacionado con: {hijo.get_full_name()}'
            except Usuario.DoesNotExist:
                return f'✗ Código inválido: {obj.codigo_hijo}'
        elif obj.rol == Usuario.ROL_ACUDIENTE:
            return 'Sin hijo relacionado'
        return '—'
    get_relacion_info.short_description = 'Información de Relación'
