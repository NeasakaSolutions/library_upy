# Importaciones:
import os
from rest_framework import serializers
from libros.models import Libro
from dotenv import load_dotenv

class LibroSerializer(serializers.ModelSerializer):

    # Formatear datos:
    categoria = serializers.ReadOnlyField(source = "categoria.nombre")
    autor = serializers.ReadOnlyField(source = "autor.nombre")
    fecha = serializers.DateTimeField(format = "%d/%m/%Y")
    imagen = serializers.SerializerMethodField()
    libro = serializers.SerializerMethodField()
    #user = serializers.ReadOnlyField(source = "user.first_name")

    class Meta:
        model = Libro
        fields = ("id", "nombre", "slug", "descripcion", "fecha", "categoria_id", "categoria", 
                   "autor", "imagen", "libro")

    # Formateo de la imagen:
    def get_imagen(self, obj):
        return f"{os.getenv('BASE_URL')}uploads/fotos/{obj.foto}"

    # Formateo de la cancion:
    def get_libro(self, obj):
        return f"{os.getenv('BASE_URL')}uploads/libros/{obj.libro}"
    


