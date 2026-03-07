from django.contrib import admin
from .models import Cotizacion, ItemCotizacion


class ItemInline(admin.TabularInline):
    model  = ItemCotizacion
    extra  = 1


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'acudiente', 'estado', 'total', 'creada_en')
    list_filter   = ('estado',)
    inlines       = [ItemInline]
