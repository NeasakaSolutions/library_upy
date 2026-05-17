# Importaciones:
from django.urls import path

from seguridad.views import Login

urlpatterns = [
    path("seguridad/login", Login.as_view()),
]

