"""
Script para cargar datos de prueba en el sistema escolar.
Ejecutar con: python cargar_datos.py
(debe ejecutarse desde la raíz del proyecto con el entorno virtual activo)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.usuarios.models import Usuario
from apps.academico.models import Curso, Materia, AsignacionProfesorMateria, EstudianteCurso
from apps.inventario.models import CategoriaProducto, Producto

print("🚀 Cargando datos de prueba...\n")

"""
Script para cargar datos de prueba en el sistema escolar.
Ejecutar con: python cargar_datos.py
(debe ejecutarse desde la raíz del proyecto con el entorno virtual activo)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.usuarios.models import Usuario
from apps.academico.models import Curso, Materia, AsignacionProfesorMateria, EstudianteCurso
from apps.inventario.models import CategoriaProducto, Producto

print("🚀 Cargando datos de prueba...\n")

# ─── 1. Usuarios ──────────────────────────────────────────────────────────────

# Admin (verificar si existe)
try:
    admin = Usuario.objects.get(username='admin')
    print(f"  ✅ Admin ya existe: {admin.username}")
except Usuario.DoesNotExist:
    admin = Usuario.objects.create_superuser(
        username='admin', password='admin123',
        first_name='Carlos', last_name='García',
        email='admin@escuela.com', rol=Usuario.ROL_ADMIN
    )
    print(f"  ✅ Admin creado: {admin.username} / admin123")

# Profesores
try:
    prof1 = Usuario.objects.get(username='prof_maria')
    print(f"  ✅ Profesor ya existe: {prof1.username}")
except Usuario.DoesNotExist:
    prof1 = Usuario.objects.create_user(
        username='prof_maria', password='prof123',
        first_name='María', last_name='López',
        email='maria@escuela.com', rol=Usuario.ROL_PROFESOR
    )
    print(f"  ✅ Profesor creado: {prof1.username} / prof123")

try:
    prof2 = Usuario.objects.get(username='prof_juan')
    print(f"  ✅ Profesor ya existe: {prof2.username}")
except Usuario.DoesNotExist:
    prof2 = Usuario.objects.create_user(
        username='prof_juan', password='prof123',
        first_name='Juan', last_name='Martínez',
        email='juan@escuela.com', rol=Usuario.ROL_PROFESOR
    )
    print(f"  ✅ Profesor creado: {prof2.username} / prof123")

# Estudiantes
try:
    est1 = Usuario.objects.get(username='est_ana')
    print(f"  ✅ Estudiante ya existe: {est1.username}")
except Usuario.DoesNotExist:
    est1 = Usuario.objects.create_user(
        username='est_ana', password='est123',
        first_name='Ana', last_name='Rodríguez',
        email='ana@escuela.com', rol=Usuario.ROL_ESTUDIANTE,
        codigo_estudiante='EST001'
    )
    print(f"  ✅ Estudiante creado: {est1.username} / est123 (Código: EST001)")

try:
    est2 = Usuario.objects.get(username='est_pedro')
    print(f"  ✅ Estudiante ya existe: {est2.username}")
except Usuario.DoesNotExist:
    est2 = Usuario.objects.create_user(
        username='est_pedro', password='est123',
        first_name='Pedro', last_name='Sánchez',
        email='pedro@escuela.com', rol=Usuario.ROL_ESTUDIANTE,
        codigo_estudiante='EST002'
    )
    print(f"  ✅ Estudiante creado: {est2.username} / est123 (Código: EST002)")

# Acudiente
try:
    acud1 = Usuario.objects.get(username='acud_rosa')
    print(f"  ✅ Acudiente ya existe: {acud1.username}")
except Usuario.DoesNotExist:
    acud1 = Usuario.objects.create_user(
        username='acud_rosa', password='acud123',
        first_name='Rosa', last_name='Ramírez',
        email='rosa@escuela.com', rol=Usuario.ROL_ACUDIENTE,
        codigo_hijo='EST001'
    )
    print(f"  ✅ Acudiente creado: {acud1.username} / acud123 (Hijo: EST001)")

print(f"  ✅ Usuarios verificados/creados\n")

# ─── 2. Cursos ────────────────────────────────────────────────────────────────
curso10a = Curso.objects.create(nombre='10A', descripcion='Décimo grado grupo A', año_lectivo=2025)
curso11b = Curso.objects.create(nombre='11B', descripcion='Undécimo grado grupo B', año_lectivo=2025)
print(f"  ✅ Cursos: 10A, 11B")

# ─── 3. Inscripciones ─────────────────────────────────────────────────────────
EstudianteCurso.objects.create(estudiante=est1, curso=curso10a)
EstudianteCurso.objects.create(estudiante=est2, curso=curso10a)
print(f"  ✅ Estudiantes inscritos en 10A")

# ─── 4. Materias ──────────────────────────────────────────────────────────────
matematicas = Materia.objects.create(nombre='Matemáticas', descripcion='Álgebra y cálculo')
español     = Materia.objects.create(nombre='Español', descripcion='Lengua castellana')
ciencias    = Materia.objects.create(nombre='Ciencias Naturales')
historia    = Materia.objects.create(nombre='Historia')
print(f"  ✅ Materias creadas")

# ─── 5. Asignaciones ──────────────────────────────────────────────────────────
AsignacionProfesorMateria.objects.create(profesor=prof1, materia=matematicas, curso=curso10a)
AsignacionProfesorMateria.objects.create(profesor=prof1, materia=matematicas, curso=curso11b)
AsignacionProfesorMateria.objects.create(profesor=prof2, materia=español,     curso=curso10a)
AsignacionProfesorMateria.objects.create(profesor=prof2, materia=ciencias,    curso=curso11b)
print(f"  ✅ Asignaciones creadas")

# ─── 6. Inventario ────────────────────────────────────────────────────────────
cat_libros    = CategoriaProducto.objects.create(nombre='Libros')
cat_uniformes = CategoriaProducto.objects.create(nombre='Uniformes')

Producto.objects.create(categoria=cat_libros,    nombre='Libro de Matemáticas 10°', precio=45000, stock=50)
Producto.objects.create(categoria=cat_libros,    nombre='Libro de Español 10°',     precio=38000, stock=40)
Producto.objects.create(categoria=cat_uniformes, nombre='Camisa Blanca Talla M',    precio=32000, stock=100)
Producto.objects.create(categoria=cat_uniformes, nombre='Pantalón Azul Talla 30',   precio=55000, stock=80)
print(f"  ✅ Productos de inventario creados\n")

print("=" * 50)
print("✅ Datos cargados exitosamente.")
print()
print("👤 USUARIOS DE PRUEBA:")
print("  Admin:      admin / admin123")
print("  Profesor:   prof_maria / prof123")
print("  Profesor:   prof_juan  / prof123")
print("  Estudiante: est_ana    / est123")
print("  Acudiente:  acud_rosa  / acud123")
print()
print("🌐 Accede en: http://127.0.0.1:8000")
