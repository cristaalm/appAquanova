from django.db import models


class Planta(models.Model):
    id_planta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    nivel = models.PositiveSmallIntegerField(null=True, blank=True)
    imagen = models.CharField(max_length=100, null=True, blank=True)
    fecha_ingreso = models.DateTimeField()

    class Meta:
        db_table = "plantas"
