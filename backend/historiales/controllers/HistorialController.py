from historiales.models import Historial
from dispositivos.models import Dispositivo  # Asegúrate de importar el modelo correcto
from datetime import datetime


class HistorialController:
    def __init__(self, id_dispositivo):
        self.id_dispositivo = id_dispositivo  # ID del dispositivo en la base de datos

    def get_last(self):
        """
        Obtiene el último valor del historial del dispositivo.
        """
        try:
            dispositivo = Dispositivo.objects.get(id_dispositivo=self.id_dispositivo)
            registro = Historial.objects.filter(id_dispositivo=dispositivo).order_by(
                "-fecha_ingreso"
            )[0]
            return registro.valor
        except (IndexError, Dispositivo.DoesNotExist):
            return None

    def set_history(self, valor):
        """
        Establece un nuevo valor en el historial del dispositivo.
        """
        try:
            dispositivo = Dispositivo.objects.get(id_dispositivo=self.id_dispositivo)
            registro = Historial.objects.create(
                id_dispositivo=dispositivo,
                valor=valor,
                sync=0,
                fecha_ingreso=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            registro.save()
        except Exception as e:
            print(f"Error al guardar el historial de pH: {e}")
            return False
        return True
