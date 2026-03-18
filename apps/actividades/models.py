from django.db import models
from apps.usuarios.models import Usuario
from apps.academico.models import AsignacionProfesorMateria


class Actividad(models.Model):
    """
    Tarea, taller o proyecto creado por un profesor para una materia/curso.
    """
    asignacion   = models.ForeignKey(
        AsignacionProfesorMateria, on_delete=models.CASCADE, related_name='actividades'
    )
    titulo       = models.CharField(max_length=200)
    descripcion  = models.TextField()
    fecha_entrega = models.DateTimeField()
    valor_maximo = models.DecimalField(max_digits=4, decimal_places=2, default=10)
    creada_en    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering            = ['fecha_entrega']

    def __str__(self):
        return f'{self.titulo} | {self.asignacion.materia} | {self.asignacion.curso}'


class EntregaActividad(models.Model):
    """
    Entrega de un estudiante para una actividad específica.
    Incluye archivo adjunto y calificación del profesor.
    """
    actividad   = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='entregas')
    estudiante  = models.ForeignKey(
        Usuario, on_delete=models.CASCADE,
        related_name='entregas',
        limit_choices_to={'rol': Usuario.ROL_ESTUDIANTE}
    )
    archivo     = models.FileField(upload_to='entregas/', null=True, blank=True)
    comentario  = models.TextField(blank=True)
    calificacion = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    retroalimentacion = models.TextField(blank=True)
    entregado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Entrega de Actividad'
        verbose_name_plural = 'Entregas de Actividades'
        unique_together     = ('actividad', 'estudiante')

    def __str__(self):
        return f'{self.estudiante.get_full_name()} → {self.actividad.titulo}'
