from django.db import models
from dispositivos.models import Dispositivo


class Contenedor(models.Model):
    id_contenedor = models.AutoField(primary_key=True)  # Primary key and auto-increment
    id_dispositivo = models.ForeignKey(
        Dispositivo, on_delete=models.DO_NOTHING, db_column="id_dispositivo"
    )  # Foreign key with no action on delete
    nombre = models.CharField(max_length=255)  # Name field with max length 255

    class Meta:
        db_table = "contenedores"  # Table name
        indexes = [
            models.Index(fields=["id_dispositivo"], name="fk_dispositivo_idx")
        ]  # Index for id_dispositivo
