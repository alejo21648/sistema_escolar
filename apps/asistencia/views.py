from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Asistencia
from .forms import AsistenciaForm


@login_required
def lista_asistencia(request):
    user = request.user
    if user.es_profesor:
        registros = Asistencia.objects.filter(
            asignacion__profesor=user
        ).select_related('estudiante', 'asignacion__materia', 'asignacion__curso')
    elif user.es_estudiante:
        registros = Asistencia.objects.filter(
            estudiante=user
        ).select_related('asignacion__materia', 'asignacion__curso')
    elif user.es_admin:
        registros = Asistencia.objects.all().select_related(
            'estudiante', 'asignacion__materia', 'asignacion__curso'
        )
    else:
        return redirect('dashboard:home')
    return render(request, 'asistencia/lista.html', {'registros': registros})


@login_required
def registrar_asistencia(request):
    if not (request.user.es_profesor or request.user.es_admin):
        return redirect('dashboard:home')
    form = AsistenciaForm(
        request.POST or None,
        profesor=request.user if request.user.es_profesor else None
    )
    if form.is_valid():
        form.save()
        messages.success(request, 'Asistencia registrada.')
        return redirect('asistencia:lista')
    return render(request, 'asistencia/form.html', {'form': form, 'titulo': 'Registrar Asistencia'})


@login_required
def editar_asistencia(request, pk):
    reg  = get_object_or_404(Asistencia, pk=pk)
    form = AsistenciaForm(
        request.POST or None, instance=reg,
        profesor=request.user if request.user.es_profesor else None
    )
    if form.is_valid():
        form.save()
        messages.success(request, 'Asistencia actualizada.')
        return redirect('asistencia:lista')
    return render(request, 'asistencia/form.html', {'form': form, 'titulo': 'Editar Asistencia'})
