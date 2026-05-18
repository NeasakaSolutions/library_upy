# Importaciones
from django.core.paginator import Paginator

# Dividir la informacion:
def paginar(request, queryset, limite=9):

    page = request.GET.get("page", 1)

    paginator = Paginator(queryset, limite)

    registros = paginator.get_page(page)

    return {
        "data": registros,
        "pagina_actual": registros.number,
        "total_paginas": paginator.num_pages,
        "total_registros": paginator.count,
        "hay_siguiente": registros.has_next(),
        "hay_anterior": registros.has_previous()
    }