from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

from apps.usuarios.models import Usuario
from apps.academico.models import Curso, Materia, AsignacionProfesorMateria, EstudianteCurso
from apps.notas.models import Nota
from apps.asistencia.models import Asistencia
from apps.actividades.models import Actividad, EntregaActividad
from apps.cotizaciones.models import Cotizacion
from apps.inventario.models import Producto


# ─── REPORTES ADMIN ──────────────────────────────────────────────────────────

@login_required
def reporte_admin_usuarios(request):
    """Reporte de usuarios: distribución por rol, recientes, acudientes sin hijo."""
    if not request.user.es_admin:
        return redirect('dashboard:home')

    por_rol = {
        rol: Usuario.objects.filter(rol=rol).count()
        for rol, _ in Usuario.ROLES
    }

    # Últimos 30 días
    hace_30 = timezone.now() - timedelta(days=30)
    nuevos  = Usuario.objects.filter(date_joined__gte=hace_30).order_by('-date_joined')

    # Acudientes sin hijo vinculado (código inválido o vacío)
    acudientes_sin_hijo = [
        u for u in Usuario.objects.filter(rol=Usuario.ROL_ACUDIENTE)
        if not u.hijo
    ]

    # Estudiantes sin curso
    con_curso = EstudianteCurso.objects.filter(activo=True).values_list('estudiante_id', flat=True)
    sin_curso = Usuario.objects.filter(rol=Usuario.ROL_ESTUDIANTE).exclude(pk__in=con_curso)

    return render(request, 'reportes/admin_usuarios.html', {
        'nuevos':                nuevos,
        'acudientes_sin_hijo':   acudientes_sin_hijo,
        'sin_curso':             sin_curso,
        'total_usuarios':        sum(por_rol.values()),
        'total_administradores': por_rol.get(Usuario.ROL_ADMIN, 0),
        'total_profesores':      por_rol.get(Usuario.ROL_PROFESOR, 0),
        'total_estudiantes':     por_rol.get(Usuario.ROL_ESTUDIANTE, 0),
        'total_acudientes':      por_rol.get(Usuario.ROL_ACUDIENTE, 0),
    })


@login_required
def reporte_admin_academico(request):
    """Reporte académico: cursos, promedios por materia y por período."""
    if not request.user.es_admin:
        return redirect('dashboard:home')

    # Promedios por materia
    promedios_materia = Nota.objects.values(
        'asignacion__materia__nombre'
    ).annotate(
        promedio=Avg('valor'),
        total_notas=Count('id'),
    ).order_by('asignacion__materia__nombre')

    # Promedios por período
    promedios_periodo = Nota.objects.values('periodo').annotate(
        promedio=Avg('valor'),
        total_notas=Count('id'),
    ).order_by('periodo')

    # Actividad por curso
    cursos_stats = Curso.objects.filter(activo=True).annotate(
        num_estudiantes=Count('inscripciones', filter=Q(inscripciones__activo=True)),
        num_asignaciones=Count('asignaciones', filter=Q(asignaciones__activa=True)),
    )

    # Top 10 mejores y peores promedios de estudiantes
    promedios_estudiante = Nota.objects.values(
        'estudiante__id', 'estudiante__first_name', 'estudiante__last_name'
    ).annotate(promedio=Avg('valor')).order_by('-promedio')

    top_mejores = list(promedios_estudiante[:10])
    top_peores  = list(promedios_estudiante.order_by('promedio')[:10])

    return render(request, 'reportes/admin_academico.html', {
        'promedios_materia':  promedios_materia,
        'promedios_periodo':  promedios_periodo,
        'cursos_stats':       cursos_stats,
        'top_mejores':        top_mejores,
        'top_peores':         top_peores,
        'total_notas':        Nota.objects.count(),
    })


@login_required
def reporte_admin_cotizaciones(request):
    """Reporte de cotizaciones: estados, totales, productos más solicitados."""
    if not request.user.es_admin:
        return redirect('dashboard:home')

    por_estado = {
        estado: Cotizacion.objects.filter(estado=estado).count()
        for estado, _ in Cotizacion.ESTADOS
    }

    # Totales monetarios
    total_aprobado = Cotizacion.objects.filter(
        estado=Cotizacion.ESTADO_APROBADA
    ).aggregate(t=Sum('total'))['t'] or 0

    total_pendiente = Cotizacion.objects.filter(
        estado=Cotizacion.ESTADO_PENDIENTE
    ).aggregate(t=Sum('total'))['t'] or 0

    # Últimas 20 cotizaciones
    recientes = Cotizacion.objects.select_related('acudiente').order_by('-creada_en')[:20]

    # Productos más solicitados
    from apps.cotizaciones.models import ItemCotizacion
    productos_top = ItemCotizacion.objects.values(
        'producto__nombre'
    ).annotate(
        veces=Count('id'),
        unidades=Sum('cantidad'),
    ).order_by('-unidades')[:10]

    # Stock bajo (≤5 unidades)
    stock_bajo = Producto.objects.filter(activo=True, stock__lte=5).order_by('stock')

    return render(request, 'reportes/admin_cotizaciones.html', {
        'por_estado':     por_estado,
        'total_aprobado': total_aprobado,
        'total_pendiente': total_pendiente,
        'recientes':      recientes,
        'productos_top':  productos_top,
        'stock_bajo':     stock_bajo,
        'total_cotizaciones': sum(por_estado.values()),
    })


@login_required
def reporte_admin_trabajo(request):
    """Reporte de carga de trabajo: asignaciones por profesor, actividades abiertas."""
    if not request.user.es_admin:
        return redirect('dashboard:home')

    # Carga por profesor: número de asignaciones activas
    profesores = Usuario.objects.filter(rol=Usuario.ROL_PROFESOR).annotate(
        num_asignaciones=Count('asignaciones', filter=Q(asignaciones__activa=True)),
        num_actividades=Count('asignaciones__actividades', distinct=True),
    ).order_by('-num_asignaciones')

    # Actividades sin calificar por asignación
    actividades_pendientes = Actividad.objects.annotate(
        pendientes=Count('entregas', filter=Q(entregas__calificacion__isnull=True))
    ).filter(pendientes__gt=0).select_related(
        'asignacion__profesor', 'asignacion__materia', 'asignacion__curso'
    ).order_by('-pendientes')[:20]

    # Resumen global
    total_asignaciones = AsignacionProfesorMateria.objects.filter(activa=True).count()
    total_actividades  = Actividad.objects.count()
    total_entregas_pen = EntregaActividad.objects.filter(calificacion__isnull=True).count()

    return render(request, 'reportes/admin_trabajo.html', {
        'profesores':            profesores,
        'actividades_pendientes': actividades_pendientes,
        'total_asignaciones':    total_asignaciones,
        'total_actividades':     total_actividades,
        'total_entregas_pen':    total_entregas_pen,
    })


# ─── REPORTES PROFESOR ────────────────────────────────────────────────────────

@login_required
def reporte_profesor_notas(request):
    """Reporte de notas del profesor: promedios por materia, curso y período."""
    if not request.user.es_profesor:
        return redirect('dashboard:home')

    # Asignaciones del profesor
    asignaciones = AsignacionProfesorMateria.objects.filter(
        profesor=request.user, activa=True
    ).select_related('materia', 'curso')

    # Período seleccionado (filtro)
    periodo_sel = request.GET.get('periodo', '')

    # Promedios por asignación
    stats_asig = []
    for asig in asignaciones:
        qs = Nota.objects.filter(asignacion=asig)
        if periodo_sel:
            qs = qs.filter(periodo=periodo_sel)

        promedio = qs.aggregate(p=Avg('valor'))['p'] or 0
        aprobados  = qs.filter(valor__gte=6).count()
        reprobados = qs.filter(valor__lt=6).count()
        total      = qs.count()

        # Desglose por estudiante
        por_estudiante = qs.values(
            'estudiante__first_name', 'estudiante__last_name'
        ).annotate(
            promedio=Avg('valor'),
            num_notas=Count('id'),
        ).order_by('estudiante__last_name')

        stats_asig.append({
            'asig':          asig,
            'promedio':      round(promedio, 2),
            'aprobados':     aprobados,
            'reprobados':    reprobados,
            'total':         total,
            'por_estudiante': list(por_estudiante),
        })

    periodo_choices = Nota.PERIODO_CHOICES

    return render(request, 'reportes/profesor_notas.html', {
        'stats_asig':      stats_asig,
        'periodo_sel':     periodo_sel,
        'periodo_choices': periodo_choices,
    })


@login_required
def reporte_profesor_asistencia(request):
    """Reporte de asistencia del profesor: porcentajes por asignación y por estudiante."""
    if not request.user.es_profesor:
        return redirect('dashboard:home')

    asignaciones = AsignacionProfesorMateria.objects.filter(
        profesor=request.user, activa=True
    ).select_related('materia', 'curso')

    stats_asig = []
    for asig in asignaciones:
        registros = Asistencia.objects.filter(asignacion=asig)
        total = registros.count()

        if total == 0:
            continue

        presentes  = registros.filter(estado=Asistencia.ESTADO_PRESENTE).count()
        ausentes   = registros.filter(estado=Asistencia.ESTADO_AUSENTE).count()
        tardanzas  = registros.filter(estado=Asistencia.ESTADO_TARDANZA).count()
        excusados  = registros.filter(estado=Asistencia.ESTADO_EXCUSADO).count()

        # Por estudiante
        por_est = []
        estudiantes = registros.values('estudiante').distinct()
        for e in estudiantes:
            est_id   = e['estudiante']
            est_reg  = registros.filter(estudiante_id=est_id)
            est_tot  = est_reg.count()
            est_pres = est_reg.filter(estado=Asistencia.ESTADO_PRESENTE).count()
            pct      = round(est_pres / est_tot * 100, 1) if est_tot else 0
            try:
                est_obj = Usuario.objects.get(pk=est_id)
            except Usuario.DoesNotExist:
                continue
            por_est.append({
                'nombre':    est_obj.get_full_name(),
                'total':     est_tot,
                'presentes': est_pres,
                'pct':       pct,
                'ausentes':  est_reg.filter(estado=Asistencia.ESTADO_AUSENTE).count(),
                'alerta':    pct < 75,
            })
        por_est.sort(key=lambda x: x['pct'])

        stats_asig.append({
            'asig':      asig,
            'total':     total,
            'presentes': presentes,
            'ausentes':  ausentes,
            'tardanzas': tardanzas,
            'excusados': excusados,
            'pct_asist': round(presentes / total * 100, 1),
            'por_est':   por_est,
        })

    return render(request, 'reportes/profesor_asistencia.html', {
        'stats_asig': stats_asig,
    })
