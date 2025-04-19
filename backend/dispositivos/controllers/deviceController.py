from dispositivos.models import Dispositivo
from django.core.exceptions import ObjectDoesNotExist


class DispositivoController:
    def __init__(self):
        pass

    def get_dispositivo(self, id_dispositivo):
        """
        Obtiene un dispositivo por su ID.
        """
        try:
            dispositivo = Dispositivo.objects.get(id_dispositivo=id_dispositivo)
            return self._to_dict(dispositivo)
        except Dispositivo.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error al obtener el dispositivo: {e}")
            return None

    def update_dispositivo(self, id_dispositivo, data):
        """
        Actualiza un dispositivo con los datos proporcionados.
        data debe ser un diccionario con los campos a actualizar.
        """
        try:
            dispositivo = Dispositivo.objects.get(id_dispositivo=id_dispositivo)

            for field, value in data.items():
                if hasattr(dispositivo, field):
                    setattr(dispositivo, field, value)

            dispositivo.save()
            return True
        except Dispositivo.DoesNotExist:
            return False
        except Exception as e:
            print(f"Error al actualizar el dispositivo: {e}")
            return False

    def _to_dict(self, dispositivo):
        """
        Convierte un objeto Dispositivo en un diccionario.
        """
        return {
            "id_dispositivo": dispositivo.id_dispositivo,
            "nombre": dispositivo.nombre,
            "requiere_contenedor": dispositivo.requiere_contenedor,
            "tiempo_batido": dispositivo.tiempo_batido,
            "valor_maximo": (
                float(dispositivo.valor_maximo)
                if dispositivo.valor_maximo is not None
                else None
            ),
            "valor_minimo": (
                float(dispositivo.valor_minimo)
                if dispositivo.valor_minimo is not None
                else None
            ),
            "estado": dispositivo.estado,
            "sync": dispositivo.sync,
            "type": self._map_sensor_type(
                dispositivo.nombre
            ),  # si necesitas esto para DeviceOptions
        }

    def _map_sensor_type(self, nombre):
        """
        Mapea el nombre del sensor a un tipo reconocible por DeviceOptions.
        """
        nombre = nombre.lower()
        if "tds" in nombre:
            return "tds"
        if "ph" in nombre:
            return "ph"
        if "temperatura" in nombre:
            return "temp"
        if "humedad" in nombre:
            return "hum"
        if "ultrasonico" in nombre or "nivel" in nombre:
            return "ultrasonico"
        return "otro"
