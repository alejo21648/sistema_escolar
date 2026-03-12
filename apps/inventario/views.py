from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm


@login_required
def lista_productos(request):
    productos = Producto.objects.select_related('categoria').all()
    return render(request, 'inventario/lista.html', {'productos': productos})


@login_required
def crear_producto(request):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    form = ProductoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Producto creado.')
        return redirect('inventario:lista')
    return render(request, 'inventario/form.html', {'form': form, 'titulo': 'Crear Producto'})


@login_required
def editar_producto(request, pk):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    producto = get_object_or_404(Producto, pk=pk)
    form     = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if form.is_valid():
        form.save()
        messages.success(request, 'Producto actualizado.')
        return redirect('inventario:lista')
    return render(request, 'inventario/form.html', {'form': form, 'titulo': 'Editar Producto'})


@login_required
def eliminar_producto(request, pk):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado.')
        return redirect('inventario:lista')
    return render(request, 'inventario/confirmar_eliminar.html', {'producto': producto})
