from django.db import models


class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name        = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Producto del inventario escolar (libros, uniformes, etc.)."""
    categoria   = models.ForeignKey(CategoriaProducto, on_delete=models.SET_NULL,
                                    null=True, related_name='productos')
    nombre      = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio      = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField(default=0)
    imagen      = models.ImageField(upload_to='productos/', null=True, blank=True)
    activo      = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Producto'
        verbose_name_plural = 'Productos'
        ordering            = ['nombre']

    def __str__(self):
<<<<<<< HEAD
        return f'{self.nombre} (${self.precio})'
=======
        return f'{self.nombre} (${self.precio})'
>>>>>>> 19d2c3af1c98f2eda2fa8b1aec62310d8c577731
