from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('',                    views.lista_productos,   name='lista'),
    path('crear/',              views.crear_producto,    name='crear'),
    path('<int:pk>/editar/',    views.editar_producto,   name='editar'),
    path('<int:pk>/eliminar/',  views.eliminar_producto, name='eliminar'),
]
