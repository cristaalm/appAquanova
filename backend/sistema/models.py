from django.db import models


class Sistema(models.Model):
    id_sistema = models.PositiveIntegerField(primary_key=True)
    id_remoto = models.PositiveIntegerField(null=True, blank=True, unique=True)
    razon_social = models.CharField(max_length=100)
    nombre_comercial = models.CharField(max_length=100)
    rfc = models.CharField(max_length=20, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    logotipo = models.CharField(max_length=255, null=True, blank=True)
    fecha_ingreso = models.DateTimeField()

    class Meta:
        db_table = "sistema"
