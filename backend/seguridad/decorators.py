import time
from functools import wraps
from http import HTTPStatus

from django.conf import settings
from django.http import JsonResponse
from jose import jwt, JWTError


def logueado():
    def metodo(func):
        @wraps(func)
        def _decorator(self, request, *args, **kwargs):

            # Obtener el encabezado de autorización
            authorization = request.headers.get("Authorization", "")

            if not authorization:
                return JsonResponse(
                    {
                        "estado": "error",
                        "mensaje": "Sin autorización"
                    },
                    status=HTTPStatus.UNAUTHORIZED
                )

            # Validar el formato Bearer <token>
            partes = authorization.split()

            if len(partes) != 2 or partes[0].lower() != "bearer":
                return JsonResponse(
                    {
                        "estado": "error",
                        "mensaje": "Token de autorización inválido"
                    },
                    status=HTTPStatus.UNAUTHORIZED
                )

            token = partes[1]

            try:
                resuelto = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS512"]
                )

                # Verificar explícitamente que exista la expiración
                expiracion = resuelto.get("exp")

                if expiracion is None or int(expiracion) <= int(time.time()):
                    raise JWTError("Token expirado o sin expiración")

            except (JWTError, ValueError, TypeError):
                return JsonResponse(
                    {
                        "estado": "error",
                        "mensaje": "Token inválido o expirado"
                    },
                    status=HTTPStatus.UNAUTHORIZED
                )

            return func(self, request, *args, **kwargs)

        return _decorator
    return metodo