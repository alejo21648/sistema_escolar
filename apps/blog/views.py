from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Publicacion, Comentario, Categoria
from .forms import PublicacionForm, ComentarioForm, CategoriaForm


@login_required
def lista_blog(request):
    """Vista principal del blog — todos los usuarios autenticados pueden leer."""
    categoria_id = request.GET.get('categoria')
    qs = Publicacion.objects.filter(estado=Publicacion.ESTADO_PUBLICADO)\
                            .select_related('autor', 'categoria')\
                            .prefetch_related('comentarios')

    if categoria_id:
        qs = qs.filter(categoria_id=categoria_id)

    # Destacadas al tope
    destacadas  = qs.filter(destacada=True)[:3]
    normales    = qs.filter(destacada=False)

    paginator = Paginator(normales, 9)
    page_obj  = paginator.get_page(request.GET.get('page'))

    categorias = Categoria.objects.all()

    # Admin y Profesor ven sus borradores también
    mis_borradores = []
    if request.user.es_admin or request.user.es_profesor:
        mis_borradores = Publicacion.objects.filter(
            autor=request.user,
            estado=Publicacion.ESTADO_BORRADOR
        ).order_by('-creada_en')[:5]

    return render(request, 'blog/lista.html', {
        'destacadas':     destacadas,
        'page_obj':       page_obj,
        'categorias':     categorias,
        'categoria_id':   categoria_id,
        'mis_borradores': mis_borradores,
    })


@login_required
def detalle_publicacion(request, pk):
    """Detalle de una publicación con comentarios."""
    pub = get_object_or_404(Publicacion, pk=pk)

    # Solo publicadas son visibles para estudiantes y acudientes
    if pub.estado != Publicacion.ESTADO_PUBLICADO:
        if not (request.user.es_admin or request.user.es_profesor):
            messages.error(request, 'Esta publicación no está disponible.')
            return redirect('blog:lista')
        if pub.estado == Publicacion.ESTADO_BORRADOR and pub.autor != request.user and not request.user.es_admin:
            messages.error(request, 'No tienes permiso para ver este borrador.')
            return redirect('blog:lista')

    comentarios  = pub.comentarios.select_related('autor').all()
    form_comment = ComentarioForm(request.POST or None)

    if request.method == 'POST' and form_comment.is_valid():
        c = form_comment.save(commit=False)
        c.publicacion = pub
        c.autor       = request.user
        c.save()
        messages.success(request, 'Comentario agregado.')
        return redirect('blog:detalle', pk=pk)

    return render(request, 'blog/detalle.html', {
        'pub':         pub,
        'comentarios': comentarios,
        'form':        form_comment,
    })


@login_required
def crear_publicacion(request):
    """Solo Admin y Profesor pueden crear publicaciones."""
    if not (request.user.es_admin or request.user.es_profesor):
        messages.error(request, 'No tienes permiso para crear publicaciones.')
        return redirect('blog:lista')

    form = PublicacionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        pub = form.save(commit=False)
        pub.autor = request.user
        pub.save()
        messages.success(request, 'Publicación guardada correctamente.')
        return redirect('blog:detalle', pk=pub.pk)

    return render(request, 'blog/form.html', {
        'form':   form,
        'titulo': 'Nueva Publicación',
    })


@login_required
def editar_publicacion(request, pk):
    """Admin puede editar cualquiera; Profesor solo las propias."""
    pub = get_object_or_404(Publicacion, pk=pk)

    if request.user.es_profesor and pub.autor != request.user:
        messages.error(request, 'Solo puedes editar tus propias publicaciones.')
        return redirect('blog:lista')
    if not (request.user.es_admin or request.user.es_profesor):
        return redirect('blog:lista')

    form = PublicacionForm(request.POST or None, request.FILES or None, instance=pub)
    if form.is_valid():
        form.save()
        messages.success(request, 'Publicación actualizada.')
        return redirect('blog:detalle', pk=pub.pk)

    return render(request, 'blog/form.html', {
        'form':   form,
        'titulo': 'Editar Publicación',
        'pub':    pub,
    })


@login_required
def eliminar_publicacion(request, pk):
    """Admin puede eliminar cualquiera; Profesor solo las propias."""
    pub = get_object_or_404(Publicacion, pk=pk)

    if request.user.es_profesor and pub.autor != request.user:
        messages.error(request, 'No puedes eliminar esta publicación.')
        return redirect('blog:lista')
    if not (request.user.es_admin or request.user.es_profesor):
        return redirect('blog:lista')

    if request.method == 'POST':
        pub.delete()
        messages.success(request, 'Publicación eliminada.')
        return redirect('blog:lista')

    return render(request, 'blog/confirmar_eliminar.html', {'pub': pub})


@login_required
def eliminar_comentario(request, pk):
    """Elimina un comentario propio o cualquiera si es admin."""
    comentario = get_object_or_404(Comentario, pk=pk)
    pub_pk = comentario.publicacion.pk

    if request.user != comentario.autor and not request.user.es_admin:
        messages.error(request, 'No puedes eliminar este comentario.')
        return redirect('blog:detalle', pk=pub_pk)

    if request.method == 'POST':
        comentario.delete()
        messages.success(request, 'Comentario eliminado.')
    return redirect('blog:detalle', pk=pub_pk)


# ─── Gestión de categorías (solo Admin) ──────────────────────────────────────

@login_required
def lista_categorias(request):
    if not request.user.es_admin:
        return redirect('blog:lista')
    categorias = Categoria.objects.all()
    return render(request, 'blog/categorias.html', {'categorias': categorias})


@login_required
def crear_categoria(request):
    if not request.user.es_admin:
        return redirect('blog:lista')
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría creada.')
        return redirect('blog:categorias')
    return render(request, 'blog/categoria_form.html', {'form': form, 'titulo': 'Nueva Categoría'})


@login_required
def editar_categoria(request, pk):
    if not request.user.es_admin:
        return redirect('blog:lista')
    cat  = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=cat)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría actualizada.')
        return redirect('blog:categorias')
    return render(request, 'blog/categoria_form.html', {'form': form, 'titulo': 'Editar Categoría', 'cat': cat})


@login_required
def eliminar_categoria(request, pk):
    if not request.user.es_admin:
        return redirect('blog:lista')
    cat = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Categoría eliminada.')
        return redirect('blog:categorias')
    return render(request, 'blog/categoria_confirmar_eliminar.html', {'cat': cat})
