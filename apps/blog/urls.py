from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',                              views.lista_blog,            name='lista'),
    path('nueva/',                        views.crear_publicacion,     name='crear'),
    path('<int:pk>/',                     views.detalle_publicacion,   name='detalle'),
    path('<int:pk>/editar/',              views.editar_publicacion,    name='editar'),
    path('<int:pk>/eliminar/',            views.eliminar_publicacion,  name='eliminar'),
    path('comentario/<int:pk>/eliminar/', views.eliminar_comentario,   name='eliminar_comentario'),
    # Categorías
    path('categorias/',                   views.lista_categorias,      name='categorias'),
    path('categorias/nueva/',             views.crear_categoria,       name='crear_categoria'),
    path('categorias/<int:pk>/editar/',   views.editar_categoria,      name='editar_categoria'),
    path('categorias/<int:pk>/eliminar/', views.eliminar_categoria,    name='eliminar_categoria'),
]
