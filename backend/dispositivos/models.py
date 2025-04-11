from django.db import models


class Dispositivo(models.Model):
    id_dispositivo = models.AutoField(
        primary_key=True
    )  # Primary key with auto-increment
    nombre = models.CharField(max_length=100)
    requiere_contenedor = models.BooleanField(null=True, blank=True)
    tiempo_batido = models.PositiveSmallIntegerField(null=True, blank=True)
    estado = models.PositiveSmallIntegerField()
    sync = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "dispositivos"
