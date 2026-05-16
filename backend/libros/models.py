# Importaciones:
from django.db import models
from autoslug import AutoSlugField
#from django.contrib.auth.models import User
from categorias.models import Categoria


# Create your models here.
class Libro(models.Model):
    #user = models.ForeignKey(User, models.DO_NOTHING, default = 1)
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING)
    nombre = models.CharField(max_length = 100, null = False)
    slug = AutoSlugField(populate_from = "nombre", max_length = 100)
    autor = models.CharField(max_length = 100, null = True)
    foto = models.CharField(max_length = 100, null = True)
    libro = models.CharField(max_length = 100, null = True)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "libros"
        verbose_name = "Libro"
        verbose_name_plural = "Libros"