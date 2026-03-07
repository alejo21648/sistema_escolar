from django.db import models
from apps.usuarios.models import Usuario


class Curso(models.Model):
    """Representa un grado/grupo escolar. Ej: '10A', '11B'."""
    nombre      = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    año_lectivo = models.IntegerField(default=2025)
    activo      = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering            = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.año_lectivo})'


class EstudianteCurso(models.Model):
    """
    Tabla intermedia: relaciona un Estudiante con un Curso.
    Permite saber en qué curso está cada estudiante.
    """
    estudiante    = models.ForeignKey(
        Usuario, on_delete=models.CASCADE,
        related_name='inscripciones',
        limit_choices_to={'rol': Usuario.ROL_ESTUDIANTE}
    )
    curso         = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_ingreso = models.DateField(auto_now_add=True)
    activo        = models.BooleanField(default=True)

    class Meta:
        unique_together     = ('estudiante', 'curso')
        verbose_name        = 'Estudiante en Curso'
        verbose_name_plural = 'Estudiantes en Cursos'

    def __str__(self):
        return f'{self.estudiante} → {self.curso}'


class Materia(models.Model):
    """
    Materia académica. Ej: Matemáticas, Español.
    Una materia puede dictarse en múltiples cursos.
    """
    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activa      = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Materia'
        verbose_name_plural = 'Materias'
        ordering            = ['nombre']

    def __str__(self):
        return self.nombre


class AsignacionProfesorMateria(models.Model):
    """
    Tabla clave: conecta Profesor + Materia + Curso.
    Un profesor puede dictar la misma materia en distintos cursos.
    Una materia puede tener hasta 2 profesores por curso.
    """
    profesor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE,
        related_name='asignaciones',
        limit_choices_to={'rol': Usuario.ROL_PROFESOR}
    )
    materia  = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='asignaciones')
    curso    = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='asignaciones')
    activa   = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Asignación Profesor-Materia'
        verbose_name_plural = 'Asignaciones Profesor-Materia'
        # Evita duplicar la misma asignación exacta
        unique_together = ('profesor', 'materia', 'curso')

    def __str__(self):
        return f'{self.profesor.get_full_name()} → {self.materia} en {self.curso}'
