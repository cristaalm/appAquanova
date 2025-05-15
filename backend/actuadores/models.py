from django.db import models
from dispositivos.models import Dispositivo


class Actuadores(models.Model):
    id_actuador = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255)
    activado = models.DateTimeField(null=True, blank=True)
    id_dispositivo = models.ForeignKey(
        Dispositivo, on_delete=models.DO_NOTHING, db_column="id_dispositivo"
    )

    class Meta:
        db_table = "actuadores"
        
