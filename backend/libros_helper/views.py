# Importaciones:
import os
from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from dotenv import load_dotenv
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.core.files.storage import FileSystemStorage
from seguridad.decorators import logueado
from utilidades.utilidades import paginar
from django.db.models import Q
from django.contrib.auth.models import User
from libros.serializers import LibroSerializer
from libros.models import Libro

# Editar fotos:
class LibroHelperEditarFoto(APIView):

    @logueado()
    def post(self, request):
        
        # Variables:
        id = request.data.get("id")
        fs = FileSystemStorage()
        foto_file  = request.FILES.get("foto")

        # Validaciones:
        if not id:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo id es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)
        
        if not foto_file:
            return JsonResponse({
                "estado": "error",
                "mensaje": "La foto es obligatoria"
            }, status=HTTPStatus.BAD_REQUEST)
        
        try:
            libro = Libro.objects.get(id = id)
            anterior = libro.foto

        except Libro.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El libro seleccionado no existe"
            }, status=HTTPStatus.BAD_REQUEST)
        
        # Validacion MIME:
        if foto_file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Formato de imagen no valido"
            }, status=HTTPStatus.BAD_REQUEST)
        
        # Guardar foto
        try:
            ext = os.path.splitext(foto_file.name)[1]
            foto = f"{datetime.timestamp(datetime.now())}{ext}"
            fs.save(f"fotos/{foto}", foto_file)

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Error al subir la imagen"
            }, status=HTTPStatus.BAD_REQUEST)
        
        # Actualizar registro:
        try:
            libro.foto = foto
            libro.save()

            # Eliminar archivo anterior:
            path = f"./uploads/fotos/{anterior}"

            if os.path.exists(path):
                os.remove(path)

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se actualizo correctamente"
            }, status=HTTPStatus.OK)

        except Exception as e:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error inesperado"
            }, status=HTTPStatus.BAD_REQUEST)

# Editar PDF:
class LibroHelperEditarLibro(APIView):

    @logueado()
    def post(self, request):

        # Variables:
        id = request.data.get("id")
        libro_file = request.FILES.get("libro")

        fs = FileSystemStorage()

        # Validaciones:
        if not id:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo id es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        if not libro_file:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El archivo PDF es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        # Validar existencia:
        try:
            libro = Libro.objects.get(id=id)

            anterior = libro.libro

        except Libro.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El libro seleccionado no existe"
            }, status=HTTPStatus.BAD_REQUEST)

        # Validar MIME:
        if libro_file.content_type != "application/pdf":
            return JsonResponse({
                "estado": "error",
                "mensaje": "El archivo debe ser PDF"
            }, status=HTTPStatus.BAD_REQUEST)

        # Guardar PDF:
        try:
            ext = os.path.splitext(libro_file.name)[1]

            archivo = f"{datetime.timestamp(datetime.now())}{ext}"

            fs.save(f"libros/{archivo}", libro_file)

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Error al subir el PDF"
            }, status=HTTPStatus.BAD_REQUEST)

        # Actualizar registro:
        try:
            libro.libro = archivo

            libro.save()

            # Eliminar archivo anterior:
            path = f"./uploads/libros/{anterior}"

            if os.path.exists(path):
                os.remove(path)

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se actualizo correctamente"
            }, status=HTTPStatus.OK)

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error inesperado"
            }, status=HTTPStatus.BAD_REQUEST)

# Buscador:
class LibroHelperSlug(APIView):

    # Consultar un registro:
    def get(self, request, id, slug):

        try:
            libro = Libro.objects.get(id=id)

            return JsonResponse({
                "data": {
                    "id": libro.id,
                    "nombre": libro.nombre,
                    "slug": libro.slug,
                    "autor": libro.autor,
                    "descripcion": libro.descripcion,
                    "fecha": DateFormat(libro.fecha).format("d/m/Y"),
                    "categoria_id": libro.categoria_id,
                    "categoria": libro.categoria.nombre,
                    "imagen": f"{os.getenv('BASE_URL')}uploads/fotos/{libro.foto}",
                    "libro": f"{os.getenv('BASE_URL')}uploads/libros/{libro.libro}",
                    "user_id": libro.user_id,
                    "user": libro.user.first_name
                }
            }, status=HTTPStatus.OK)

        except Libro.DoesNotExist:
            raise Http404

# Libros aleatorios:
class LibroHelperHome(APIView):

    def get(self, request):
        libro = Libro.objects.order_by("?").all()[:6] # SELECT * FROM libros ORDER BY rand()  LIMIT 3
        datos_json = LibroSerializer(libro, many = True)
        return JsonResponse({
            "data": datos_json.data
        }, status = HTTPStatus.OK)

# Buscador individual:
class LibroHelperBuscador(APIView):

    def get(self, request):

        categoria_id = request.GET.get("categoria_id")
        search = request.GET.get("search", "").strip()

        #if not categoria_id:
        #    return JsonResponse({
        #        "estado": "error",
        #        "mensaje": "Categoria no valida"
        #    }, status = HTTPStatus.BAD_REQUEST)

        libro = Libro.objects.all()

        if categoria_id and categoria_id != "0":
            libro = libro.filter(categoria_id=categoria_id)

        libro = libro.filter(
            Q(slug__icontains=search) |
            Q(nombre__icontains=search)
        )

        #libro = Libro.objects.filter(
         #   categoria_id = categoria_id,
          #  slug__icontains = search
        #).order_by("?")[:3]

        datos_json = LibroSerializer(libro, many = True)

        return JsonResponse({
            "data": datos_json.data
        }, status = HTTPStatus.OK)

# Libros asociados al usuario:
class LibroHelperLista(APIView):
    
    @logueado()
    def get(self, request, id):

        try:
            User.objects.get(id=id)

        except User.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error"
            }, status=HTTPStatus.BAD_REQUEST)

        libro = Libro.objects.filter(
            user_id=id
        ).order_by('-id')

        paginado = paginar(request, libro, 10)

        datos_json = LibroSerializer(
            paginado["data"],
            many=True
        )

        return JsonResponse({
            "data": datos_json.data,
            "pagina_actual": paginado["pagina_actual"],
            "total_paginas": paginado["total_paginas"],
            "total_registros": paginado["total_registros"],
            "hay_siguiente": paginado["hay_siguiente"],
            "hay_anterior": paginado["hay_anterior"]
        }, status=HTTPStatus.OK)



