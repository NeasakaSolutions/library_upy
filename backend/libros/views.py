# Importaciones:
import os
from dotenv import load_dotenv
from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.utils.text import slugify
from django.utils.dateformat import DateFormat
from http import HTTPStatus
from utilidades.utilidades import paginar
from categorias.models import Categoria
from libros.models import Libro
from categorias.serializers import CategoriaSerializer
from libros.serializers import LibroSerializer

# Metodos sin argumento.
class LibrosLista(APIView):

    # Consultar registros:
    def get(self, request):

        data = Libro.objects.order_by("-id")

        paginado = paginar(request, data, 10)

        datos_json = LibroSerializer(
            paginado["data"],
            many = True
        )

        return JsonResponse({
            "data": datos_json.data,
            "pagina_actual": paginado["pagina_actual"],
            "total_paginas": paginado["total_paginas"],
            "total_registros": paginado["total_registros"],
            "hay_siguiente": paginado["hay_siguiente"],
            "hay_anterior": paginado["hay_anterior"]
        })

# Metodos con argumento:
class LibroDetalle(APIView):
    
    # Consultar un registro:
    def get(self, request, id):
        
        try:
            libro = Libro.objects.get(id = id)
            
            return JsonResponse({
                "data": {
                    "id": libro.id,
                    "nombre": libro.nombre,
                    "slug": libro.slug,
                    "descripcion": libro.descripcion,
                    "fecha": DateFormat(libro.fecha).format("d/m/Y"),
                    "categoria_id": libro.categoria_id,
                    "categoria": libro.categoria.nombre,
                    "imagen": f"{os.getenv("BASE_URL")}uploads/libros/{libro.foto}",
                    "libro": f"{os.getenv("BASE_URL")}uploads/libros/{libro.libro}",
                    #"user_id": data.user_id,
                    #"user": data.user.first_name
                    }
            }, status = HTTPStatus.OK)

        except Libro.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error"
            }, status = HTTPStatus.NOT_FOUND)
