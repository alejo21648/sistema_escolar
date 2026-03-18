from django.contrib import admin
from .models import Producto, CategoriaProducto


@admin.register(CategoriaProducto)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'categoria', 'precio', 'stock', 'activo')
    list_filter   = ('categoria', 'activo')
    search_fields = ('nombre',)
