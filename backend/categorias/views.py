# Importaciones:
from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.utils.text import slugify
from http import HTTPStatus
from categorias.models import Categoria
from categorias.serializers import CategoriaSerializer

# Clases sin argumentos:
class CategoriasLista(APIView):

    # Listar categorias:
    def get(self, request):
        data = Categoria.objects.order_by('-id').all()
        datos_json = CategoriaSerializer(data, many = True)

        return JsonResponse({
            "data": datos_json.data
        }, status = HTTPStatus.OK)

    # Crear categorias:
    def post(self, request):

        # Variables:
        nombre = request.data.get("nombre", "").strip()
        
        # Validaciones:
        if not nombre:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo nombre es obligatorio"
            }, status = HTTPStatus.BAD_REQUEST)
        
        # Crear categoria:
        try:
            Categoria.objects.create(nombre  = nombre)

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se creo el registro exitosamente"
            }, status = HTTPStatus.CREATED)

        except Exception as e:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error"
            }, status = HTTPStatus.BAD_REQUEST)

# Clase con argumentos:
class CategoriaDetalle(APIView):

    # Consultar categoria
    def get(self, request, id):
        
        try:
            data = Categoria.objects.filter(id = id).get()

            return JsonResponse({"data": {
                "id": data.id,
                "nombre": data.nombre,
                "slug": data.slug
                }}, status = HTTPStatus.OK)
        
        except Categoria.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error"
            }, status = HTTPStatus.BAD_REQUEST)
        
    # Editar categoria:    
    def put(self, request, id):

        # Variables:
        nombre = request.data.get("nombre", "").strip()
        
        # Validaciones:
        if not nombre:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo nombre es obligatorio"
            }, status = HTTPStatus.BAD_REQUEST)

        # Modificar registro:
        try:
            # Consulta:
            categoria = Categoria.objects.get(id = id)

            # Modificar datos:
            categoria.nombre = nombre
            categoria.slug = slugify(nombre)

            # Guardar cambios:
            categoria.save()
            
            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se modifico el registro exitosamente"
            }, status = HTTPStatus.OK)

        except Categoria.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error"
            }, status = HTTPStatus.NOT_FOUND)

    # Eliminar categoria:
    def delete(self, request, id):

        # Eliminar registro:
        try:
            # Consulta:
            categoria = Categoria.objects.get(id = id)

            # Eliminar regsitro:
            categoria.delete()

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se elimino el registro"
            }, status = HTTPStatus.OK)
        
        except Categoria.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error"
            }, status = HTTPStatus.NOT_FOUND)

