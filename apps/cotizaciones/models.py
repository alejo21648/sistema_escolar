from django.db import models
from apps.usuarios.models import Usuario
from apps.inventario.models import Producto


class Cotizacion(models.Model):
    """Cotización de productos realizada por un acudiente."""
    ESTADO_PENDIENTE  = 'PENDIENTE'
    ESTADO_APROBADA   = 'APROBADA'
    ESTADO_RECHAZADA  = 'RECHAZADA'

    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_APROBADA,  'Aprobada'),
        (ESTADO_RECHAZADA, 'Rechazada'),
    ]

    acudiente  = models.ForeignKey(
        Usuario, on_delete=models.CASCADE,
        related_name='cotizaciones',
        limit_choices_to={'rol': Usuario.ROL_ACUDIENTE}
    )
    estado     = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    total      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observacion = models.TextField(blank=True)
    creada_en  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
        ordering            = ['-creada_en']

    def __str__(self):
        return f'Cotización #{self.pk} | {self.acudiente.get_full_name()} | {self.estado}'

    def calcular_total(self):
        self.total = sum(item.subtotal() for item in self.items.all())
        self.save()


class ItemCotizacion(models.Model):
    """Producto individual dentro de una cotización."""
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='items')
    producto   = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad   = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f'{self.producto} x{self.cantidad}'
