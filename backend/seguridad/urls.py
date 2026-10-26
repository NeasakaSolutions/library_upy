# Importaciones:
from django.urls import path
from seguridad.views import (
    Login,
    Registro,
    Verificacion
)

urlpatterns = [
    path("seguridad/registro", Registro.as_view()),
    path("seguridad/verificacion/<str:token>", Verificacion.as_view()),
    path("seguridad/login", Login.as_view()),
]

