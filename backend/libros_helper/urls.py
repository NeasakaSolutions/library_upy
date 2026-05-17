# Importaciones:
from django.urls import path
from libros_helper.views import LibroHelperLista
from libros_helper.views import LibroHelperEditarFoto
from libros_helper.views import LibroHelperEditarLibro
from libros_helper.views import LibroHelperSlug
from libros_helper.views import LibroHelperHome
from libros_helper.views import LibroHelperBuscador

urlpatterns = [
    path("libros/editar/foto", LibroHelperEditarFoto.as_view()),
    path("libros/editar/documento", LibroHelperEditarLibro.as_view()),
    path("libros/slug/<int:id>/<str:slug>", LibroHelperSlug.as_view()),
    path("libros-home", LibroHelperHome.as_view()),
    path("libros-buscador", LibroHelperBuscador.as_view()),
    path("libros-panel/<int:id>", LibroHelperLista.as_view()),
]