from django.urls import path
from . import views

app_name = 'cotizaciones'

urlpatterns = [
    path('',                       views.lista_cotizaciones, name='lista'),
    path('crear/',                 views.crear_cotizacion,   name='crear'),
    path('<int:pk>/',              views.detalle_cotizacion, name='detalle'),
    path('<int:pk>/estado/',       views.cambiar_estado,     name='cambiar_estado'),

    # ──────────────────────────────────────────────────────────────────────
    # NUEVO: Endpoint AJAX que devuelve el precio oficial de un producto.
    # El JavaScript del formulario lo consulta cada vez que el acudiente
    # selecciona un producto, de modo que el campo "Precio Unitario" se
    # rellena automáticamente con el valor correcto desde la base de datos.
    # ──────────────────────────────────────────────────────────────────────
    path('api/precio/<int:producto_id>/', views.precio_producto, name='precio_producto'),
]
