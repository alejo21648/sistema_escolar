from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# NUEVO: JsonResponse para responder las peticiones AJAX del formulario
from django.http import JsonResponse
from .models import Cotizacion
from .forms import CotizacionForm, ItemFormSet
# NUEVO: importamos Producto para consultar el precio real en la API y en la vista
from apps.inventario.models import Producto


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


# ──────────────────────────────────────────────────────────────────────────────
# NUEVO: Vista API que el JavaScript del formulario consulta con fetch().
# Recibe el ID del producto y devuelve su precio oficial en JSON.
# Esto evita que el cliente necesite conocer los precios de antemano; los pide
# al servidor en tiempo real al seleccionar cada producto.
# ──────────────────────────────────────────────────────────────────────────────
@login_required
def precio_producto(request, producto_id):
    """Devuelve el precio oficial de un producto en formato JSON."""
    try:
        # Solo productos activos son válidos para cotizar
        producto = Producto.objects.get(pk=producto_id, activo=True)
        return JsonResponse({'precio': str(producto.precio)})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)


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

        # ──────────────────────────────────────────────────────────────────
        # MODIFICADO: guardamos los ítems con commit=False para poder
        # sobrescribir precio_unitario ANTES de persistir en la base de datos.
        # Aunque el campo es readonly en el HTML, aquí lo forzamos al precio
        # real del producto, lo que protege el sistema incluso si alguien
        # manipula la petición HTTP manualmente (p. ej. con DevTools o curl).
        # ──────────────────────────────────────────────────────────────────
        items = formset.save(commit=False)
        for item in items:
            # Forzamos siempre el precio oficial del producto
            item.precio_unitario = item.producto.precio
            item.save()

        # Guardar también las posibles eliminaciones del formset
        for obj in formset.deleted_objects:
            obj.delete()

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
