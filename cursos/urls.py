from django.urls import path

from . import views

app_name = "cursos"

urlpatterns = [
    path("", views.lista_cursos, name="lista"),
    path("cursos/crear/", views.crear_curso, name="crear"),
    path("cursos/<int:pk>/editar/", views.editar_curso, name="editar"),
    path("cursos/<int:pk>/eliminar/", views.eliminar_curso, name="eliminar"),
]
