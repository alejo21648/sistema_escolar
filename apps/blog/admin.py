from django.contrib import admin
from .models import Categoria, Publicacion, Comentario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display  = ['titulo', 'autor', 'categoria', 'estado', 'destacada', 'creada_en']
    list_filter   = ['estado', 'destacada', 'categoria']
    search_fields = ['titulo', 'contenido']
    date_hierarchy = 'creada_en'


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display  = ['autor', 'publicacion', 'creado_en']
    search_fields = ['texto', 'autor__username']
