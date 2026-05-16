# Importaciones:
from django.urls import path
from categorias.views import CategoriasLista
from categorias.views import CategoriaDetalle

urlpatterns = [
    path('categorias', CategoriasLista.as_view()),
    path("categorias/<int:id>", CategoriaDetalle.as_view()),
]


