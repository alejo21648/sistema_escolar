from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, Materia, AsignacionProfesorMateria, EstudianteCurso
from .forms import CursoForm, MateriaForm, AsignacionForm, EstudianteCursoForm


# ─── CURSOS ───────────────────────────────────────────────────────────────────
@login_required
def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'academico/cursos/lista.html', {'cursos': cursos})

@login_required
def crear_curso(request):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    form = CursoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Curso creado.')
        return redirect('academico:lista_cursos')
    return render(request, 'academico/cursos/form.html', {'form': form, 'titulo': 'Crear Curso'})

@login_required
def editar_curso(request, pk):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    curso = get_object_or_404(Curso, pk=pk)
    form  = CursoForm(request.POST or None, instance=curso)
    if form.is_valid():
        form.save()
        messages.success(request, 'Curso actualizado.')
        return redirect('academico:lista_cursos')
    return render(request, 'academico/cursos/form.html', {'form': form, 'titulo': 'Editar Curso'})

@login_required
def eliminar_curso(request, pk):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso eliminado.')
        return redirect('academico:lista_cursos')
    return render(request, 'academico/cursos/confirmar_eliminar.html', {'objeto': curso, 'nombre': str(curso)})

@login_required
def detalle_curso(request, pk):
    curso       = get_object_or_404(Curso, pk=pk)
    estudiantes = EstudianteCurso.objects.filter(curso=curso, activo=True).select_related('estudiante')
    asignaciones = AsignacionProfesorMateria.objects.filter(curso=curso, activa=True).select_related('profesor', 'materia')
    return render(request, 'academico/cursos/detalle.html', {
        'curso': curso, 'estudiantes': estudiantes, 'asignaciones': asignaciones
    })


# ─── MATERIAS ─────────────────────────────────────────────────────────────────
@login_required
def lista_materias(request):
    materias = Materia.objects.all()
    return render(request, 'academico/materias/lista.html', {'materias': materias})

@login_required
def crear_materia(request):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    form = MateriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Materia creada.')
        return redirect('academico:lista_materias')
    return render(request, 'academico/materias/form.html', {'form': form, 'titulo': 'Crear Materia'})

@login_required
def editar_materia(request, pk):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    materia = get_object_or_404(Materia, pk=pk)
    form    = MateriaForm(request.POST or None, instance=materia)
    if form.is_valid():
        form.save()
        messages.success(request, 'Materia actualizada.')
        return redirect('academico:lista_materias')
    return render(request, 'academico/materias/form.html', {'form': form, 'titulo': 'Editar Materia'})


# ─── ASIGNACIONES ─────────────────────────────────────────────────────────────
@login_required
def lista_asignaciones(request):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    asignaciones = AsignacionProfesorMateria.objects.select_related('profesor', 'materia', 'curso').all()
    return render(request, 'academico/asignaciones/lista.html', {'asignaciones': asignaciones})

@login_required
def crear_asignacion(request):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    form = AsignacionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Asignación creada.')
        return redirect('academico:lista_asignaciones')
    return render(request, 'academico/asignaciones/form.html', {'form': form, 'titulo': 'Asignar Profesor'})

@login_required
def eliminar_asignacion(request, pk):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    asig = get_object_or_404(AsignacionProfesorMateria, pk=pk)
    if request.method == 'POST':
        asig.delete()
        messages.success(request, 'Asignación eliminada.')
        return redirect('academico:lista_asignaciones')
    return render(request, 'academico/asignaciones/confirmar_eliminar.html', {'objeto': asig, 'nombre': str(asig)})


# ─── INSCRIBIR ESTUDIANTE ─────────────────────────────────────────────────────
@login_required
def inscribir_estudiante(request):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    form = EstudianteCursoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Estudiante inscrito al curso.')
        return redirect('academico:lista_cursos')
    return render(request, 'academico/cursos/inscribir.html', {'form': form, 'titulo': 'Inscribir Estudiante'})
