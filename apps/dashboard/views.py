from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from apps.usuarios.models import Usuario
from apps.academico.models import Curso, Materia, AsignacionProfesorMateria, EstudianteCurso
from apps.notas.models import Nota
from apps.asistencia.models import Asistencia
from apps.actividades.models import Actividad, EntregaActividad
from apps.cotizaciones.models import Cotizacion


@login_required
def home(request):
    user = request.user

    if user.es_admin:
        return _dashboard_admin(request)
    elif user.es_profesor:
        return _dashboard_profesor(request)
    elif user.es_estudiante:
        return _dashboard_estudiante(request)
    elif user.es_acudiente:
        return _dashboard_acudiente(request)
    else:
        return redirect('usuarios:login')


def _dashboard_admin(request):
    """Dashboard con estadísticas generales del sistema."""
    total_estudiantes = Usuario.objects.filter(rol=Usuario.ROL_ESTUDIANTE).count()
    total_profesores  = Usuario.objects.filter(rol=Usuario.ROL_PROFESOR).count()
    total_cursos      = Curso.objects.filter(activo=True).count()
    total_materias    = Materia.objects.filter(activa=True).count()

    # Promedio académico general
    promedio_general = Nota.objects.aggregate(p=Avg('valor'))['p'] or 0

    # Asistencia general (% presentes)
    total_asistencias  = Asistencia.objects.count()
    presentes          = Asistencia.objects.filter(estado=Asistencia.ESTADO_PRESENTE).count()
    porcentaje_asist   = round((presentes / total_asistencias * 100), 1) if total_asistencias else 0

    # Cotizaciones recientes
    cotizaciones_recientes = Cotizacion.objects.select_related('acudiente').order_by('-creada_en')[:5]

    context = {
        'total_estudiantes':     total_estudiantes,
        'total_profesores':      total_profesores,
        'total_cursos':          total_cursos,
        'total_materias':        total_materias,
        'promedio_general':      round(promedio_general, 2),
        'porcentaje_asistencia': porcentaje_asist,
        'cotizaciones_recientes': cotizaciones_recientes,
    }
    return render(request, 'dashboard/admin.html', context)


def _dashboard_profesor(request):
    """Dashboard para el profesor con estadísticas de sus materias."""
    asignaciones = AsignacionProfesorMateria.objects.filter(
        profesor=request.user, activa=True
    ).select_related('materia', 'curso').annotate(
        total_estudiantes=Count('curso__inscripciones', distinct=True),
        promedio=Avg('notas__valor'),
    )

    # Actividades pendientes de calificar
    pendientes = EntregaActividad.objects.filter(
        actividad__asignacion__profesor=request.user,
        calificacion__isnull=True
    ).count()

    context = {
        'asignaciones': asignaciones,
        'pendientes':   pendientes,
    }
    return render(request, 'dashboard/profesor.html', context)


def _dashboard_estudiante(request):
    """Dashboard del estudiante: notas y actividades."""
    notas = Nota.objects.filter(
        estudiante=request.user
    ).values('asignacion__materia__nombre').annotate(
        promedio=Avg('valor')
    )

    actividades_pendientes = Actividad.objects.filter(
        asignacion__curso__inscripciones__estudiante=request.user,
        asignacion__curso__inscripciones__activo=True,
    ).exclude(
        entregas__estudiante=request.user
    ).count()

    context = {
        'notas':                  notas,
        'actividades_pendientes': actividades_pendientes,
    }
    return render(request, 'dashboard/estudiante.html', context)


def _dashboard_acudiente(request):
    """Dashboard del acudiente: información de sus hijos."""
    user = request.user
    hijo = user.hijo  # Obtiene el estudiante relacionado
    
    context = {
        'hijo': hijo,
        'cotizaciones': [],
        'notas': [],
        'asistencia': None,
        'actividades_pendientes': 0,
    }
    
    # Si existe el hijo, obtener información relevante
    if hijo:
        # Cotizaciones del acudiente
        cotizaciones = Cotizacion.objects.filter(acudiente=user).order_by('-creada_en')[:10]
        context['cotizaciones'] = cotizaciones
        
        # Notas del hijo
        notas = Nota.objects.filter(
            estudiante=hijo
        ).values('asignacion__materia__nombre').annotate(
            promedio=Avg('valor'),
            num_notas=Count('id')
        ).order_by('asignacion__materia__nombre')
        context['notas'] = notas
        
        # Asistencia del hijo
        if Asistencia.objects.filter(estudiante=hijo).exists():
            total = Asistencia.objects.filter(estudiante=hijo).count()
            presentes = Asistencia.objects.filter(
                estudiante=hijo,
                estado=Asistencia.ESTADO_PRESENTE
            ).count()
            porcentaje = round((presentes / total * 100), 1) if total else 0
            context['asistencia'] = {
                'total': total,
                'presentes': presentes,
                'porcentaje': porcentaje,
            }
        
        # Actividades pendientes del hijo
        actividades_pendientes = Actividad.objects.filter(
            asignacion__curso__inscripciones__estudiante=hijo,
            asignacion__curso__inscripciones__activo=True,
        ).exclude(
            entregas__estudiante=hijo
        ).count()
        context['actividades_pendientes'] = actividades_pendientes
    
    return render(request, 'dashboard/acudiente.html', context)
