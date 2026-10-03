from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CursoForm
from .models import Curso


def _reportar_errores(request, form):
    """Convierte los errores del formulario en mensajes para el usuario."""
    for campo, errores in form.errors.items():
        etiqueta = form.fields[campo].label if campo in form.fields else "Error"
        for error in errores:
            messages.error(request, f"{etiqueta}: {error}")


# READ ---------------------------------------------------------------
def lista_cursos(request):
    # Si no hay otro mensaje pendiente, mostramos el aviso de la imagen.
    if len(messages.get_messages(request)) == 0:
        messages.success(request, "¡Cursos listados!")
    contexto = {"cursos": Curso.objects.all(), "form": CursoForm()}
    return render(request, "cursos/lista.html", contexto)


# CREATE -------------------------------------------------------------
@require_POST
def crear_curso(request):
    form = CursoForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "¡Curso creado correctamente!")
    else:
        _reportar_errores(request, form)
    return redirect("cursos:lista")


# UPDATE -------------------------------------------------------------
@require_POST
def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    form = CursoForm(request.POST, instance=curso)
    if form.is_valid():
        form.save()
        messages.success(request, "¡Curso actualizado correctamente!")
    else:
        _reportar_errores(request, form)
    return redirect("cursos:lista")


# DELETE -------------------------------------------------------------
@require_POST
def eliminar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    curso.delete()
    messages.success(request, "¡Curso eliminado correctamente!")
    return redirect("cursos:lista")
