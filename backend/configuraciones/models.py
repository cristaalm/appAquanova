from django.db import models
from dispositivos.models import Dispositivo


class configuraciones(models.Model):
    id_configuracion = models.AutoField(
        primary_key=True
    )  # Primary key and auto-increment
    name = models.CharField(
        max_length=50, db_column="nombre", default="Default Name"
    )  # Unique name for each configuration
    id_dispositivo = models.ForeignKey(
        Dispositivo,
        on_delete=models.PROTECT,  # Matches "ON DELETE NO ACTION"
        db_column="id_dispositvo",
    )
    valor = models.DecimalField(
        max_digits=10, decimal_places=0
    )  # Adjusted to match SQL definition

    class Meta:
        db_table = "configuraciones"
