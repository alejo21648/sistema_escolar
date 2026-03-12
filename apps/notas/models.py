from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.usuarios.models import Usuario
from apps.academico.models import Materia, Curso, AsignacionProfesorMateria


class Nota(models.Model):
    """
    Nota de un estudiante en una materia específica de un curso,
    registrada por un profesor.
    """
    PERIODO_CHOICES = [
        (1, 'Primer Período'),
        (2, 'Segundo Período'),
        (3, 'Tercer Período'),
        (4, 'Cuarto Período'),
    ]

    estudiante   = models.ForeignKey(
        Usuario, on_delete=models.CASCADE,
        related_name='notas',
        limit_choices_to={'rol': Usuario.ROL_ESTUDIANTE}
    )
    asignacion   = models.ForeignKey(
        AsignacionProfesorMateria, on_delete=models.CASCADE,
        related_name='notas',
        help_text='Relaciona al profesor, materia y curso al mismo tiempo.'
    )
    periodo      = models.IntegerField(choices=PERIODO_CHOICES)
    valor        = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    descripcion  = models.CharField(max_length=200, blank=True, help_text='Ej: Parcial 1, Taller 2')
    fecha        = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Nota'
        verbose_name_plural = 'Notas'
        ordering            = ['-fecha']

    def __str__(self):
        return (f'{self.estudiante.get_full_name()} | '
                f'{self.asignacion.materia} | '
                f'P{self.periodo} | {self.valor}')
