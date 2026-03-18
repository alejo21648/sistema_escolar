from django.db import models
from apps.usuarios.models import Usuario


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name        = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering            = ['nombre']

    def __str__(self):
        return self.nombre


class Publicacion(models.Model):
    ESTADO_BORRADOR  = 'BORRADOR'
    ESTADO_PUBLICADO = 'PUBLICADO'
    ESTADO_ARCHIVADO = 'ARCHIVADO'

    ESTADOS = [
        (ESTADO_BORRADOR,  'Borrador'),
        (ESTADO_PUBLICADO, 'Publicado'),
        (ESTADO_ARCHIVADO, 'Archivado'),
    ]

    autor       = models.ForeignKey(
        Usuario, on_delete=models.CASCADE,
        related_name='publicaciones',
        limit_choices_to={'rol__in': [Usuario.ROL_ADMIN, Usuario.ROL_PROFESOR]}
    )
    categoria   = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='publicaciones'
    )
    titulo      = models.CharField(max_length=250)
    resumen     = models.TextField(max_length=500, blank=True, help_text='Breve descripción visible en el listado.')
    contenido   = models.TextField()
    imagen      = models.ImageField(upload_to='blog/', null=True, blank=True)
    estado      = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_BORRADOR)
    destacada   = models.BooleanField(default=False, help_text='Aparece fija al inicio del blog.')
    creada_en   = models.DateTimeField(auto_now_add=True)
    actualizada = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Publicación'
        verbose_name_plural = 'Publicaciones'
        ordering            = ['-creada_en']

    def __str__(self):
        return f'{self.titulo} ({self.get_estado_display()})'


class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')
    autor       = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios_blog')
    texto       = models.TextField(max_length=1000)
    creado_en   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering            = ['creado_en']

    def __str__(self):
        return f'Comentario de {self.autor.get_full_name()} en "{self.publicacion.titulo}"'
