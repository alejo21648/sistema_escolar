from django.db import models
from apps.usuarios.models import Usuario
from apps.academico.models import AsignacionProfesorMateria


class Asistencia(models.Model):
    """
    Registra si un estudiante asistió o no a una clase específica
    (materia + curso + profesor + fecha).
    """
    ESTADO_PRESENTE  = 'P'
    ESTADO_AUSENTE   = 'A'
    ESTADO_TARDANZA  = 'T'
    ESTADO_EXCUSADO  = 'E'

    ESTADOS = [
        (ESTADO_PRESENTE, 'Presente'),
        (ESTADO_AUSENTE,  'Ausente'),
        (ESTADO_TARDANZA, 'Tardanza'),
        (ESTADO_EXCUSADO, 'Excusado'),
    ]

    estudiante = models.ForeignKey(
        Usuario, on_delete=models.CASCADE,
        related_name='asistencias',
        limit_choices_to={'rol': Usuario.ROL_ESTUDIANTE}
    )
    asignacion = models.ForeignKey(
        AsignacionProfesorMateria, on_delete=models.CASCADE,
        related_name='asistencias'
    )
    fecha      = models.DateField()
    estado     = models.CharField(max_length=1, choices=ESTADOS, default=ESTADO_PRESENTE)
    observacion = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name        = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        unique_together     = ('estudiante', 'asignacion', 'fecha')
        ordering            = ['-fecha']

    def __str__(self):
        return (f'{self.estudiante.get_full_name()} | '
                f'{self.asignacion.materia} | '
                f'{self.fecha} | {self.get_estado_display()}')
