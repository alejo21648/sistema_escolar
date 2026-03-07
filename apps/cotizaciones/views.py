from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cotizacion
from .forms import CotizacionForm, ItemFormSet


@login_required
def lista_cotizaciones(request):
    user = request.user
    if user.es_acudiente:
        cotizaciones = Cotizacion.objects.filter(acudiente=user)
    elif user.es_admin:
        cotizaciones = Cotizacion.objects.all().select_related('acudiente')
    else:
        return redirect('dashboard:home')
    return render(request, 'cotizaciones/lista.html', {'cotizaciones': cotizaciones})


@login_required
def crear_cotizacion(request):
    if not request.user.es_acudiente:
        return redirect('dashboard:home')
    form    = CotizacionForm(request.POST or None)
    formset = ItemFormSet(request.POST or None)
    if form.is_valid() and formset.is_valid():
        cotizacion = form.save(commit=False)
        cotizacion.acudiente = request.user
        cotizacion.save()
        formset.instance = cotizacion
        formset.save()
        cotizacion.calcular_total()
        messages.success(request, 'Cotización enviada correctamente.')
        return redirect('cotizaciones:lista')
    return render(request, 'cotizaciones/form.html', {
        'form': form, 'formset': formset, 'titulo': 'Nueva Cotización'
    })


@login_required
def detalle_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    if request.user.es_acudiente and cotizacion.acudiente != request.user:
        return redirect('cotizaciones:lista')
    return render(request, 'cotizaciones/detalle.html', {'cotizacion': cotizacion})


@login_required
def cambiar_estado(request, pk):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    nuevo_estado = request.POST.get('estado')
    if nuevo_estado in dict(Cotizacion.ESTADOS):
        cotizacion.estado = nuevo_estado
        cotizacion.save()
        messages.success(request, f'Estado actualizado a {cotizacion.get_estado_display()}.')
    return redirect('cotizaciones:detalle', pk=pk)
