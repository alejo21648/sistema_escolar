from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Usuario
from .forms import LoginForm, UsuarioForm, UsuarioEditForm, RegistroEstudianteForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    form = LoginForm(data=request.POST or None, request=request)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, f'Bienvenido, {form.get_user().get_full_name()}')
        return redirect('dashboard:home')
    return render(request, 'usuarios/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('usuarios:login')


@login_required
def lista_usuarios(request):
    if not request.user.es_admin:
        messages.error(request, 'Acceso no autorizado.')
        return redirect('dashboard:home')
    rol = request.GET.get('rol', '')
    qs  = Usuario.objects.all()
    if rol:
        qs = qs.filter(rol=rol)
    paginator = Paginator(qs.order_by('last_name', 'first_name'), 20)
    page_obj  = paginator.get_page(request.GET.get('page'))
    return render(request, 'usuarios/lista.html', {
        'usuarios':    page_obj,
        'rol_filtro':  rol,
        'roles':       Usuario.ROLES,
    })


@login_required
def crear_usuario(request):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    form = UsuarioForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuario creado correctamente.')
        return redirect('usuarios:lista')
    return render(request, 'usuarios/form.html', {
        'form': form, 'titulo': 'Crear Usuario'
    })


@login_required
def editar_usuario(request, pk):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    usuario = get_object_or_404(Usuario, pk=pk)
    form    = UsuarioEditForm(request.POST or None, request.FILES or None, instance=usuario)
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuario actualizado.')
        return redirect('usuarios:lista')
    return render(request, 'usuarios/form.html', {
        'form': form, 'titulo': f'Editar: {usuario.get_full_name()}'
    })


@login_required
def eliminar_usuario(request, pk):
    if not request.user.es_admin:
        return redirect('dashboard:home')
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado.')
        return redirect('usuarios:lista')
    return render(request, 'usuarios/confirmar_eliminar.html', {'usuario': usuario})


@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})


def registro_estudiante(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    form = RegistroEstudianteForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Bienvenido, {user.get_full_name()}')
        return redirect('dashboard:home')
    return render(request, 'usuarios/registro.html', {'form': form})
