# Importaciones
import time
import os
from datetime import datetime, timedelta
from http import HTTPStatus
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework.views import APIView
from jose import jwt

# Login
class Login(APIView):

    def post(self, request):

        # Variables:
        correo = request.data.get("correo", "").strip()
        password = request.data.get("password", "").strip()

        # Validaciones:
        if not correo:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo correo es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        if not password:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo password es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        # Autenticación:
        auth = authenticate(request, username = correo, password = password)

        # Validar credenciales:
        if auth is None:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Las credenciales ingresadas no son válidas"
            }, status=HTTPStatus.BAD_REQUEST)

        # Configuración del token:
        fecha = datetime.now()
        despues = fecha + timedelta(days=1)

        payload = {
            "id": auth.id,
            "iss": os.getenv("BASE_URL"),
            "iat": int(time.time()),
            "exp": int(datetime.timestamp(despues))
        }

        # Crear token:
        try:
            token = jwt.encode(
                payload,
                settings.SECRET_KEY,
                algorithm="HS512"
            )

            return JsonResponse({
                "estado": "ok",
                "id": auth.id,
                "nombre": auth.first_name,
                "token": token
            })

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrió un error inesperado"
            }, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        
        



