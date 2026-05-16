# Importaciones:
from django.urls import path
from libros.views import LibrosLista
from libros.views import LibroDetalle

urlpatterns = [
    path("libros", LibrosLista.as_view()),
    path("libros/<int:id>", LibroDetalle.as_view()),
]