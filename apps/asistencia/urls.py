from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
    path('',                  views.lista_asistencia,     name='lista'),
    path('registrar/',        views.registrar_asistencia, name='registrar'),
    path('<int:pk>/editar/',  views.editar_asistencia,    name='editar'),
]
