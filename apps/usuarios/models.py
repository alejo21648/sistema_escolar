from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado con sistema de roles.
    Hereda todos los campos de Django (username, email, password, etc.)
    y añade: rol, teléfono, foto y fecha de nacimiento.
    """
    ROL_ADMIN      = 'ADMINISTRADOR'
    ROL_PROFESOR   = 'PROFESOR'
    ROL_ESTUDIANTE = 'ESTUDIANTE'
    ROL_ACUDIENTE  = 'ACUDIENTE'

    ROLES = [
        (ROL_ADMIN,      'Administrador'),
        (ROL_PROFESOR,   'Profesor'),
        (ROL_ESTUDIANTE, 'Estudiante'),
        (ROL_ACUDIENTE,  'Acudiente'),
    ]

    rol              = models.CharField(max_length=20, choices=ROLES, default=ROL_ESTUDIANTE)
    telefono         = models.CharField(max_length=20, blank=True)
    foto             = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    codigo_estudiante = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="Código único para estudiantes")
    codigo_hijo      = models.CharField(max_length=20, blank=True, help_text="Código del hijo para acudientes")

    class Meta:
        verbose_name        = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.get_full_name()} ({self.get_rol_display()})'

    @property
    def es_admin(self):
        return self.rol == self.ROL_ADMIN

    @property
    def es_profesor(self):
        return self.rol == self.ROL_PROFESOR

    @property
    def es_estudiante(self):
        return self.rol == self.ROL_ESTUDIANTE

    @property
    def es_acudiente(self):
        return self.rol == self.ROL_ACUDIENTE

    @property
    def hijo(self):
        if self.es_acudiente and self.codigo_hijo:
            try:
                return Usuario.objects.get(codigo_estudiante=self.codigo_hijo, rol=self.ROL_ESTUDIANTE)
            except Usuario.DoesNotExist:
                return None
        return None
