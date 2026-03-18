from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirigir raíz al dashboard
    path('', lambda req: redirect('dashboard:home'), name='root'),
    path('usuarios/',     include('apps.usuarios.urls',     namespace='usuarios')),
    path('dashboard/',    include('apps.dashboard.urls',    namespace='dashboard')),
    path('academico/',    include('apps.academico.urls',    namespace='academico')),
    path('notas/',        include('apps.notas.urls',        namespace='notas')),
    path('asistencia/',   include('apps.asistencia.urls',   namespace='asistencia')),
    path('actividades/',  include('apps.actividades.urls',  namespace='actividades')),
    path('inventario/',   include('apps.inventario.urls',   namespace='inventario')),
    path('cotizaciones/', include('apps.cotizaciones.urls', namespace='cotizaciones')),
    path('blog/',         include('apps.blog.urls',         namespace='blog')),
    path('reportes/',     include('apps.reportes.urls',     namespace='reportes')),
    path('comercial/',    include('apps.comercial.urls',    namespace='comercial')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
