from django.db import models
from dispositivos.models import Dispositivo


class Historial(models.Model):
    id_historial = models.AutoField(primary_key=True)  # Primary key and auto-increment
    id_dispositivo = models.ForeignKey(
        Dispositivo, on_delete=models.CASCADE, db_column="id_dispositivo"
    )  # Corrected field name
    valor = models.DecimalField(max_digits=12, decimal_places=10)  # Adjusted precision
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    sync = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "historiales"
