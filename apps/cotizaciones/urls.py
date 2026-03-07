from django.urls import path
from . import views

app_name = 'cotizaciones'

urlpatterns = [
    path('',                       views.lista_cotizaciones, name='lista'),
    path('crear/',                 views.crear_cotizacion,   name='crear'),
    path('<int:pk>/',              views.detalle_cotizacion, name='detalle'),
    path('<int:pk>/estado/',       views.cambiar_estado,     name='cambiar_estado'),
]
