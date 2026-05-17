# Importaciones:
from django.urls import path
from libros import views
from libros.views import LibrosLista
from libros.views import LibroDetalle

urlpatterns = [
    path("libros", LibrosLista.as_view()),
    path("libros/<int:id>/<slug:slug>", views.LibroDetalle.as_view())
]