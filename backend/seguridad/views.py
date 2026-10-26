# Importaciones
import time
import uuid
import os
from seguridad.models import UsersMetadata
from utilidades.utilidades import sendMail
from dotenv import load_dotenv
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework.views import APIView
from jose import jwt
from http import HTTPStatus
from django.http import (
    HttpResponseRedirect,
    Http404
)
from datetime import (
    datetime, 
    timedelta
)

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
        
# Registro:
class Registro(APIView):

    # Mandar datos del formulario de registro:
    def post(self, request):

        # Variables:
        nombre = request.data.get("nombre")
        correo = request.data.get("correo")
        password = request.data.get("password")

        # Validaciones:
        if not nombre or not correo or not password:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Hay campos vacions"
            }, status = HTTPStatus.BAD_REQUEST)

        # Validar que el correo no se repita con uno existente en la bd:
        if User.objects.filter(email = correo).exists():
            return JsonResponse({
                "estado": "error",
                "mensaje": "No se puede usar el correo proporcionado"
            },status = HTTPStatus.BAD_REQUEST)

        token = uuid.uuid4()
        url = f"{os.getenv('BASE_URL')}api/v1/seguridad/verificacion/{token}"

        # Registrar usuario:
        try:

            u = User.objects.create_user(
                username = correo,
                password = password,
                email = correo,
                first_name = nombre,
                last_name = "",
                is_active = 0,
            )

            UsersMetadata.objects.create(token = token, user_id = u.id)

            # Correo de verificación:
            html = f"""
                <div style="
                    background-color: #171725;
                    color: #e8e8f0;
                    padding: 25px;
                    border: 1px solid #6254a6;
                    border-radius: 12px;
                    font-family: Arial, Helvetica, sans-serif;
                ">

                    <h3 style="
                        color: #c9a7ff;
                        text-align: center;
                        padding-bottom: 15px;
                        border-bottom: 2px solid #e5bb4e;
                    ">
                        Autorización de acceso a la biblioteca virtual
                    </h3>

                    <p style="color: #d5d5e8;">
                        El usuario con los siguientes datos:
                    </p>

                    <table style="
                        width: 100%;
                        border-collapse: collapse;
                        background-color: #222338;
                        border: 1px solid #426a91;
                    ">
                        <tr>
                            <th style="
                                padding: 12px;
                                text-align: left;
                                color: #f1cd65;
                                border-bottom: 1px solid #454765;
                            ">Nombre</th>

                            <td style="
                                padding: 12px;
                                color: #a9d9ff;
                                border-bottom: 1px solid #454765;
                            ">{nombre}</td>
                        </tr>

                        <tr>
                            <th style="
                                padding: 12px;
                                text-align: left;
                                color: #f1cd65;
                            ">Correo</th>

                            <td style="
                                padding: 12px;
                                color: #a9d9ff;
                            ">{correo}</td>
                        </tr>
                        <tr>
                            <th style="
                                padding: 12px;
                                text-align: left;
                                color: #f1cd65;
                                ">KeyPass</th>
                        
                                <td style="
                                padding: 12px;
                                color: #a9d9ff;
                                ">{password}</td>
                        </tr>
                    </table>

                    <p style="
                        color: #d5d5e8;
                        line-height: 1.6;
                        margin-top: 20px;
                    ">
                        Solicita tener acceso al contenido de la biblioteca virtual.
                    </p>

                    <p style="
                        background-color: #302a20;
                        color: #ffdc7c;
                        padding: 12px;
                        border-left: 4px solid #e5bb4e;
                        line-height: 1.6;
                    ">
                        <strong>Importante:</strong> para darle acceso, es necesario
                        confirmar la solicitud. SOLO CONFIRME EL ACCESO SI CONOCE
                        A LA PERSONA.
                    </p>

                    <div style="text-align: center; margin-top: 25px;">
                        <a href="{url}" style="
                            display: inline-block;
                            background-color: #51418c;
                            color: #ffffff;
                            text-decoration: none;
                            padding: 14px 25px;
                            border: 1px solid #8ecbff;
                            border-radius: 7px;
                            font-weight: bold;
                            letter-spacing: 0.5px;
                        ">
                            CONFIRMAR ACCESO
                        </a>
                    </div>

                </div>
            """

            # Mandar argumentos a la funcion de mailtrap
            sendMail(html, "Verificacion", correo)

        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}") #DEBUGIN
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error inesperado"
            }, status = HTTPStatus.BAD_REQUEST)

        # Retorno de toda la funcion POST:
        return JsonResponse({
            "estado": "ok",
            "mensaje": "El formulario se mando correctamente"
        }, status = HTTPStatus.CREATED)


# Verificacion del token:
class Verificacion(APIView):

    # Funcion de prueba:
    def get(self, request, token):
        
        # Validacones:
        if token == None or not token:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Recurso no disponible"
            })

        # Activar usuario:
        try:
            data = UsersMetadata.objects.filter(token = token).filter(user__is_active = 0).get()
            UsersMetadata.objects.filter(token = token).update(token = "")
            User.objects.filter(id = data.user_id).update(is_active = 1)

            return HttpResponseRedirect(os.getenv("BASE_URL_FRONTEND"))

        except UsersMetadata.DoesNotExist:
            raise Http404
        


