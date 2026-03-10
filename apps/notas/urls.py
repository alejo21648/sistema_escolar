from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('',                    views.lista_notas,         name='lista'),
    path('agregar/',            views.agregar_nota,        name='agregar'),
    path('<int:pk>/editar/',    views.editar_nota,         name='editar'),
    path('<int:pk>/eliminar/',  views.eliminar_nota,       name='eliminar'),
    path('promedios/',          views.promedios_estudiante, name='promedios'),
]
