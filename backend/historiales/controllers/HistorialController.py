from historiales.models import Historial
from dispositivos.models import Dispositivo  # Asegúrate de importar el modelo correcto
from historiales.serializers import HistorialSerializer
from utils.network import is_connected
from datetime import datetime
import requests
import os

API = os.getenv("URL")
SISTEMA = os.getenv("SISTEMA")

class HistorialController:
    def __init__(self, id_dispositivo = None):
        self.id_dispositivo = id_dispositivo  # ID del dispositivo en la base de datos

    def set_id_dispositivo(self, id_dispositivo):
        self.id_dispositivo = id_dispositivo

    def get_last(self):
        """
        Obtiene el último valor del historial del dispositivo.
        """
        if (self.id_dispositivo is None):
            return None
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
        Crea un nuevo registro en la base de datos y lo envía a la API remota.
        """
        if (self.id_dispositivo is None):
            return False
        try:
            dispositivo = Dispositivo.objects.get(id_dispositivo=self.id_dispositivo)
            registro = Historial.objects.create(
                id_dispositivo=dispositivo,
                valor=valor,
                sync=0,
                fecha_ingreso=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            data = HistorialSerializer(registro).data
            sync = self.sync_to_remote_api("api/historial/sync", data)
            if sync:
                self.update_sync(registro.id_historial)
            return True
        except Exception as e:
            print(f"Error al guardar el historial de pH: {e}")
            return False

    def sync_pending_historial(self, batch_size=100):
        """
        Sincroniza los registros pendientes en lotes.
        """
        if not is_connected():
            print("Sin conexión, no se puede sincronizar.")
            return

        pendientes = Historial.objects.filter(sync=False)
        total = pendientes.count()
        if (total == 0):
            print("No hay registros pendientes para sincronizar.")
            return
        print(f"Sincronizando {total} registros pendientes en lotes de {batch_size}...")

        # Procesar en lotes
        for i in range(0, total, batch_size):
            batch = pendientes[i:i + batch_size]
            data_batch = []
            ids_batch = []
            for registro in batch:
                data = {
                    "id_empresa": SISTEMA,
                    "id_dispositivo": registro.id_dispositivo.id_dispositivo,
                    "valor": float(registro.valor),
                    "fecha_ingreso": registro.fecha_ingreso.isoformat(),
                }
                data_batch.append(data)
                ids_batch.append(registro.id_historial)

            # Enviar el lote a la API
            success = self.sync_to_remote_api("api/historial/sync", data_batch)  # Ajusta si tu método es async o no
            if success:
                Historial.objects.filter(id_historial__in=ids_batch).update(sync=True)
            else:
                print(f"Error al sincronizar lote {i // batch_size + 1}")
                break  # Si falla un lote, detén para evitar problemas de datos

    def sync_to_remote_api(self, endpoint: str, data):
        """
        Envía datos a la API remota. Compatible con envío de un solo registro (dict) o de varios (list).
        """
        url = f"{API}/{endpoint}"

        # Agregar 'sistema' a cada registro
        if isinstance(data, dict):
            data["id_empresa"] = SISTEMA
            payload = data
        elif isinstance(data, list):
            for d in data:
                d["id_empresa"] = SISTEMA
            payload = data
        else:
            print("Formato de datos no soportado para sincronización remota.")
            return False

        try:
            print(url)
            print(API)
            response = requests.post(url, json=payload, timeout=30)
            print(response.json())
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error enviando a API remota: {e}")
            return False

    def update_sync(self, id_historial: int):
        try:
            registro = Historial.objects.get(id_historial=id_historial)
            registro.sync = 1
            registro.save()
            return True
        except Historial.DoesNotExist:
            return False

