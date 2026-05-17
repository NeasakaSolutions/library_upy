# Importaciones:
import os
from dotenv import load_dotenv
from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.utils.text import slugify
from django.utils.dateformat import DateFormat
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
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
    
    # Agregar registro:
    def post(self, request):

        # Variables:
        nombre = request.data.get("nombre", "").strip()
        autor = request.data.get("autor", "").strip()
        descripcion = request.data.get("descripcion", "").strip()
        categoria_id = request.data.get("categoria_id")
        foto_file = request.FILES.get("foto")
        libro_file = request.FILES.get("libro")
        fs = FileSystemStorage()

        # Validaciones:
        if not nombre:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo nombre es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)
        
        if not autor:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo autor es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)
        
        if not descripcion:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo descripcion es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)
        
        if not categoria_id:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo categoria es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)
        
        if not foto_file:
            return JsonResponse({
                "estado": "error",
                "mensaje": "La foto es obligatoria"
            }, status=HTTPStatus.BAD_REQUEST)
        
        if not libro_file:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El libro PDF es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)
        
        # Validar que exista la categoría:
        try:
            categoria = Categoria.objects.get(id = categoria_id)

        except Categoria.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "La categoría no existe"
            }, status=HTTPStatus.BAD_REQUEST)
        
        # Validar mime de la foto:
        if foto_file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Formato de imagen no valido"
            }, status = HTTPStatus.BAD_REQUEST)
        
        # Validar mime del libro:
        if libro_file.content_type != "application/pdf":
            return JsonResponse({
                "estado": "error",
                "mensaje": "El archivo del libro debe ser PDF"
            }, status=HTTPStatus.BAD_REQUEST)
        
        # Subir foto
        try:
            ext = os.path.splitext(foto_file.name)[1]
            foto = f"{timezone.now().timestamp()}{ext}"
            fs.save(f"fotos/{foto}", foto_file)

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Error al subir la imagen"
            }, status=HTTPStatus.BAD_REQUEST)
        
        # Subir libro
        try:
            ext = os.path.splitext(libro_file.name)[1]
            libro = f"{timezone.now().timestamp()}{ext}"
            fs.save(f"libros/{libro}", libro_file)

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Error al subir el libro"
            }, status=HTTPStatus.BAD_REQUEST)
        
        # Crear registro:
        try:
            Libro.objects.create(
                nombre = nombre,
                autor = autor,
                descripcion = descripcion,
                categoria = categoria,
                fecha = timezone.now(),
                foto = foto,
                libro = libro
            )

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se creo el registro"
            }, status = HTTPStatus.CREATED)

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Error al guardar en la base de datos"
            }, status=HTTPStatus.INTERNAL_SERVER_ERROR)

# Metodos con argumento:
class LibroDetalle(APIView):
    
    # Consultar un libro:
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
                    "imagen": f"{os.getenv("BASE_URL")}uploads/fotos/{libro.foto}",
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
    
    # Modificar libro:
    def put(self, request, id):
        
        # Validar que el libro a modificar exista:
        try:
            libro = Libro.objects.get(id = id)

        except Libro.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error"
            }, status = HTTPStatus.NOT_FOUND)
        
        # Variables:
        nombre = request.data.get("nombre", "").strip()
        autor = request.data.get("autor", "").strip()
        descripcion = request.data.get("descripcion", "").strip()
        categoria_id = request.data.get("categoria_id")

        # Validaciones:
        if not nombre:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo nombre es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)
        
        if not autor:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo autor es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)
        
        if not descripcion:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo descripcion es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)
        
        if not categoria_id:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo categoria es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)
        
        # Validar que exista la categoría:
        try:
            categoria = Categoria.objects.get(id = categoria_id)

        except Categoria.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "La categoría no existe"
            }, status=HTTPStatus.BAD_REQUEST)
        
        # Editar registro:
        try:
            libro.nombre = nombre
            libro.autor = autor
            libro.descripcion = descripcion
            libro.categoria = categoria

            libro.save()

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se modifico el registro"
            }, status = HTTPStatus.OK)

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Error al guardar en la base de datos"
            }, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        
    # Eliminar libro:
    def delete(self, request, id):

        try:
            libro = Libro.objects.get(id = id)
        except Libro.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Registro no encontrado"
            }, status=HTTPStatus.NOT_FOUND)

        # Variables:
        base_path_book = "./uploads/libros/"
        base_path_picture = "./uploads/fotos/"

        # Eliminar foto
        path_foto = base_path_picture + str(libro.foto)
        if os.path.exists(path_foto):
            os.remove(path_foto)

        # Eliminar libro:
        path_libro = base_path_book + str(libro.libro)
        if os.path.exists(path_libro):
            os.remove(path_libro)

        # eliminar registro
        libro.delete()

        return JsonResponse({
            "estado": "ok",
            "mensaje": "Registro eliminado correctamente"
        }, status=HTTPStatus.OK)

