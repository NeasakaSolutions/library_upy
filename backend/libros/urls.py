# Importaciones:
from django.urls import path
from libros import views
from libros.views import LibrosLista, LibroDetalle, LeerLibroPDF

urlpatterns = [
    path("libros", LibrosLista.as_view()),

    path(
        "libros/<int:id>/<slug:slug>",
        LibroDetalle.as_view()
    ),

    path(
        "libros/<int:id>/<slug:slug>/pdf/",
        LeerLibroPDF.as_view(),
        name="leer-libro-pdf"
    ),
]