from django.urls import path
from . import views

app_name = 'academico'

urlpatterns = [
    # Cursos
    path('cursos/',                   views.lista_cursos,       name='lista_cursos'),
    path('cursos/crear/',             views.crear_curso,        name='crear_curso'),
    path('cursos/<int:pk>/',          views.detalle_curso,      name='detalle_curso'),
    path('cursos/<int:pk>/editar/',   views.editar_curso,       name='editar_curso'),
    path('cursos/<int:pk>/eliminar/', views.eliminar_curso,     name='eliminar_curso'),
    path('cursos/inscribir/',         views.inscribir_estudiante, name='inscribir_estudiante'),
    # Materias
    path('materias/',                 views.lista_materias,     name='lista_materias'),
    path('materias/crear/',           views.crear_materia,      name='crear_materia'),
    path('materias/<int:pk>/editar/', views.editar_materia,     name='editar_materia'),
    # Asignaciones
<<<<<<< HEAD
    path('mis-clases/',                     views.mis_clases,           name='mis_clases'),
=======
>>>>>>> 19d2c3af1c98f2eda2fa8b1aec62310d8c577731
    path('asignaciones/',                   views.lista_asignaciones,   name='lista_asignaciones'),
    path('asignaciones/crear/',             views.crear_asignacion,     name='crear_asignacion'),
    path('asignaciones/<int:pk>/eliminar/', views.eliminar_asignacion,  name='eliminar_asignacion'),
]
