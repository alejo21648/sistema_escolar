from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Nota
from .forms import NotaForm
from apps.academico.models import AsignacionProfesorMateria
from apps.usuarios.models import Usuario
from apps.actividades.models import EntregaActividad


@login_required
def lista_notas(request):
    user = request.user

    if user.es_profesor:
        notas = Nota.objects.filter(
            asignacion__profesor=user
        ).select_related('estudiante', 'asignacion__materia', 'asignacion__curso')
        # El profesor ve sus notas normales (las de actividades se ven en actividades/detalle)
        notas_actividades = []

    elif user.es_estudiante:
        # Notas normales del estudiante
        notas = Nota.objects.filter(
            estudiante=user
        ).select_related('asignacion__materia', 'asignacion__curso', 'asignacion__profesor')

        # Notas de actividades YA CALIFICADAS por el profesor
        # Solo se muestran si tienen calificacion asignada (no null)
        notas_actividades = EntregaActividad.objects.filter(
            estudiante=user,
            calificacion__isnull=False          # Solo las calificadas
        ).select_related(
            'actividad__asignacion__materia',
            'actividad__asignacion__curso',
            'actividad__asignacion__profesor'
        ).order_by('-actividad__fecha_entrega')

    elif user.es_admin:
        notas = Nota.objects.all().select_related(
            'estudiante', 'asignacion__materia', 'asignacion__curso'
        )
        notas_actividades = []
    else:
        return redirect('dashboard:home')

    return render(request, 'notas/lista.html', {
        'notas'            : notas,
        'notas_actividades': notas_actividades,  # ← nuevo contexto
    })


@login_required
def agregar_nota(request):
    if not (request.user.es_profesor or request.user.es_admin):
        return redirect('dashboard:home')
    form = NotaForm(request.POST or None, profesor=request.user if request.user.es_profesor else None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Nota registrada correctamente.')
        return redirect('notas:lista')
    return render(request, 'notas/form.html', {'form': form, 'titulo': 'Agregar Nota'})


@login_required
def editar_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    if request.user.es_profesor and nota.asignacion.profesor != request.user:
        messages.error(request, 'No puedes editar esta nota.')
        return redirect('notas:lista')
    form = NotaForm(request.POST or None, instance=nota,
                    profesor=request.user if request.user.es_profesor else None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Nota actualizada.')
        return redirect('notas:lista')
    return render(request, 'notas/form.html', {'form': form, 'titulo': 'Editar Nota'})


@login_required
def eliminar_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    if request.method == 'POST':
        nota.delete()
        messages.success(request, 'Nota eliminada.')
        return redirect('notas:lista')
    return render(request, 'notas/confirmar_eliminar.html', {'nota': nota})


@login_required
def promedios_estudiante(request):
    """Vista de promedios por materia para el estudiante autenticado."""
    user = request.user
    if user.es_acudiente:
        # Acudiente ve las notas de sus hijos (relación futura)
        return redirect('dashboard:home')
    if user.es_estudiante:
        target = user
    else:
        # Admin o profesor pueden ver el perfil de un estudiante
        pk     = request.GET.get('estudiante')
        target = get_object_or_404(Usuario, pk=pk) if pk else None
        if not target:
            return redirect('dashboard:home')

    notas = Nota.objects.filter(estudiante=target).values(
        'asignacion__materia__nombre', 'periodo'
    ).annotate(promedio=Avg('valor')).order_by('asignacion__materia__nombre', 'periodo')

    return render(request, 'notas/promedios.html', {
        'target': target, 'notas': notas
    })
