from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    # Admin
    path('admin/usuarios/',     views.reporte_admin_usuarios,     name='admin_usuarios'),
    path('admin/academico/',    views.reporte_admin_academico,    name='admin_academico'),
    path('admin/cotizaciones/', views.reporte_admin_cotizaciones, name='admin_cotizaciones'),
    path('admin/trabajo/',      views.reporte_admin_trabajo,      name='admin_trabajo'),
    # Profesor
    path('profesor/notas/',      views.reporte_profesor_notas,      name='profesor_notas'),
    path('profesor/asistencia/', views.reporte_profesor_asistencia, name='profesor_asistencia'),
]
