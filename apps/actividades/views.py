from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Actividad, EntregaActividad
from .forms import ActividadForm, EntregaForm, CalificacionEntregaForm


@login_required
def lista_actividades(request):
    user = request.user
    if user.es_profesor:
        actividades = Actividad.objects.filter(
            asignacion__profesor=user
        ).select_related('asignacion__materia', 'asignacion__curso')
    elif user.es_estudiante:
        # Actividades de las asignaciones del curso del estudiante
        from apps.academico.models import AsignacionProfesorMateria, EstudianteCurso
        cursos = EstudianteCurso.objects.filter(estudiante=user, activo=True).values_list('curso_id', flat=True)
        actividades = Actividad.objects.filter(
            asignacion__curso__in=cursos
        ).select_related('asignacion__materia', 'asignacion__curso')
    else:
        actividades = Actividad.objects.all().select_related('asignacion__materia', 'asignacion__curso')
    return render(request, 'actividades/lista.html', {'actividades': actividades})


@login_required
def crear_actividad(request):
    if not request.user.es_profesor:
        return redirect('dashboard:home')
    form = ActividadForm(request.POST or None, profesor=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Actividad creada.')
        return redirect('actividades:lista')
    return render(request, 'actividades/form.html', {'form': form, 'titulo': 'Crear Actividad'})


@login_required
def detalle_actividad(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk)
    entregas  = EntregaActividad.objects.filter(actividad=actividad).select_related('estudiante')
    return render(request, 'actividades/detalle.html', {
        'actividad': actividad, 'entregas': entregas
    })


@login_required
def entregar_actividad(request, pk):
    if not request.user.es_estudiante:
        return redirect('dashboard:home')

    actividad = get_object_or_404(Actividad, pk=pk)

    # ── Verificar si el plazo sigue abierto ──────────────────
    from django.utils import timezone
    ahora          = timezone.now()
    plazo_abierto  = ahora <= actividad.fecha_entrega

    # ── Buscar si ya existe una entrega previa ───────────────
    entrega_existente = EntregaActividad.objects.filter(
        actividad=actividad,
        estudiante=request.user
    ).first()

    # Caso 1: Ya entregó y el plazo cerró → solo lectura
    if entrega_existente and not plazo_abierto:
        messages.warning(request, 'El plazo de entrega ha cerrado. Ya no puedes modificar tu entrega.')
        return render(request, 'actividades/entregar.html', {
            'actividad'        : actividad,
            'entrega_existente': entrega_existente,
            'plazo_abierto'    : False,
            'form'             : None,
        })

    # Caso 2: No entregó y el plazo cerró → sin acceso
    if not entrega_existente and not plazo_abierto:
        messages.error(request, 'El plazo de entrega ha cerrado. No puedes entregar esta actividad.')
        return redirect('actividades:lista')

    # Caso 3: Plazo abierto → puede entregar o actualizar su entrega
    # get_or_create: si ya existe la reutiliza, si no, la crea
    entrega, creada = EntregaActividad.objects.get_or_create(
        actividad=actividad,
        estudiante=request.user
    )

    form = EntregaForm(request.POST or None, request.FILES or None, instance=entrega)

    if form.is_valid():
        form.save()
        if creada:
            messages.success(request, '✅ Actividad entregada correctamente.')
        else:
            messages.success(request, '✅ Tu entrega fue actualizada correctamente.')
        return redirect('actividades:lista')

    return render(request, 'actividades/entregar.html', {
        'form'             : form,
        'actividad'        : actividad,
        'entrega_existente': entrega_existente,
        'plazo_abierto'    : plazo_abierto,
        'es_reentrega'     : not creada,   # True si está actualizando
    })


@login_required
def calificar_entrega(request, pk):
    if not request.user.es_profesor:
        return redirect('dashboard:home')
    entrega = get_object_or_404(EntregaActividad, pk=pk)
    form    = CalificacionEntregaForm(request.POST or None, instance=entrega)
    if form.is_valid():
        form.save()
        messages.success(request, 'Entrega calificada.')
        return redirect('actividades:detalle', pk=entrega.actividad.pk)
    return render(request, 'actividades/calificar.html', {
        'form': form, 'entrega': entrega
    })
