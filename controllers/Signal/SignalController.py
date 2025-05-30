# signal_controller.py

from PyQt6.QtCore import QObject, QTimer, pyqtSlot
from dispositivos.controllers.deviceController import DispositivoController
from historiales.controllers.HistorialController import HistorialController
from actuadores.models import Actuadores
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import localtime
from django.utils.timezone import is_aware
import threading
import time
import json


class SignalController(QObject):
    def __init__(self, serial_worker, notification):
        super().__init__()
        self.serial_worker = serial_worker
        self.device_controller = DispositivoController()
        self.notification = notification

        # Conecta a la señal
        self.serial_worker.data_received.connect(self.evaluate_data)

    @pyqtSlot(dict)
    def evaluate_data(self, data):
        """
        Slot que se ejecuta cada vez que se recibe una nueva lectura.
        `data` es un dict con al menos:
        {
            "id_dispositivo": 1,
            "valor": 500.0
        }
        """
        id_dispositivo = data["id_dispositivo"]
        valor = data["valor"]

        # id dispositivo debe estar dentro del ranto de 1 o 2
        if id_dispositivo < 1 or id_dispositivo > 2:
            return

        dispositivo = self.device_controller.get_dispositivo(id_dispositivo)
        if not dispositivo:
            print(f"[SignalController] Dispositivo {id_dispositivo} no encontrado.")
            return

        min_val = dispositivo["valor_minimo"]
        max_val = dispositivo["valor_maximo"]
        tiempo_batido = dispositivo["tiempo_batido"] or 0
        nombre = dispositivo["nombre"].lower()
        nombre_message = ""

        if "ph" in nombre:
            nombre_message = "del pH"
        elif "tds" in nombre:
            nombre_message = "de la conductividad"
            

        # Comparar el valor recibido contra el rango permitido  
        if valor < min_val:
            accion = "subir"
            self.notification.show_message(f"El valor {nombre_message} está por debajo del minimo permitido.", "warning")
        elif valor > max_val and id_dispositivo == 2:
            accion = "bajar"
            self.notification.show_message(f"El valor del PH está por encima del maximo permitido.", "warning")
        elif valor > max_val and id_dispositivo == 1:
            self.notification.show_message(f"El valor de la Conductividad está por encima del maximo permitido.", "warning")
            return
        else:
            # Dentro del rango, no hay que hacer nada
            print(f"[SignalController] {nombre} dentro del rango.")
            return

        print(f"[SignalController] {nombre} fuera de rango: {valor}. Acción: {accion}")

        # Buscar actuadores relacionados
        self.activar_actuadores(id_dispositivo, nombre, accion, tiempo_batido)

    def activar_actuadores(self, id_dispositivo, nombre_sensor, accion, tiempo_batido):
        """
        Activa el mezclador correspondiente, espera `tiempo_batido`, luego activa la bomba.
        """
        actuadores = Actuadores.objects.filter(id_dispositivo=id_dispositivo)

        # Mapear acciones a nombres de actuadores
        for actuador in actuadores:
            nombre_act = actuador.nombre.lower()

            if accion in nombre_act and "mezclador" in nombre_act:
                if not self._reciente(actuador):
                    print(f"→ Activando mezclador: {actuador.nombre}")
                    self._activar_actuador(actuador)

                    # Después del batido, activar la bomba en un hilo separado
                    threading.Thread(
                        target=self._activar_bomba_despues,
                        args=(id_dispositivo, accion, tiempo_batido),
                        daemon=True
                    ).start()

            elif accion in nombre_act and "bomba" in nombre_act:
                # bomba será activada después del batido, ignorar por ahora
                continue

    def _activar_bomba_despues(self, id_dispositivo, accion, delay):
        """
        Espera el tiempo de batido y luego activa la bomba.
        """
        time.sleep(delay)  # segundos
        actuadores = Actuadores.objects.filter(id_dispositivo=id_dispositivo)
        for actuador in actuadores:
            if accion in actuador.nombre.lower() and "bomba" in actuador.nombre.lower():
                if not self._reciente(actuador):
                    print(f"→ Activando bomba: {actuador.nombre}")
                    self._activar_actuador(actuador)

    def _activar_actuador(self, actuador):
        """
        Envía una señal al microcontrolador para activar el actuador (simulado aquí).
        """
        actuador.activado = timezone.now()
        actuador.save()
        # Envía el diccionario como JSON y salto de línea para el Arduino
        json_data = json.dumps({"actuador": actuador.id_actuador}) + "\n"
        print('\n')
        print('------------------------------------------------------')
        print(f"[SignalController] Activando actuador: {json_data}")
        print(f"[SignalController] is_aware: {is_aware(actuador.activado)}")
        print(f"[SignalController] local time: {localtime(actuador.activado)}")
        print('------------------------------------------------------')
        print('\n')
        self.serial_worker.send_data(json_data)

    def _reciente(self, actuador, minutos=20):
        """
        Verifica si el actuador fue activado recientemente.
        """
        if not actuador.activado:
            return False
        
        # imprimimos el tiempo actual y el tiempo de activacion
        print(f"[SignalController] Tiempo actual: {timezone.now()}")
        print(f"[SignalController] Tiempo de activacion: {actuador.activado}")
        print(f"[SignalController] Diferencia: {timezone.now() - actuador.activado}")
        print(f"[SignalController] Minutos: {minutos}")
        print(f"[SignalController] Diferencia en minutos: {(timezone.now() - actuador.activado).total_seconds() / 60}")
        print('------------------------------------------------------')
        print('\n')
        return timezone.now() - actuador.activado < timedelta(minutes=minutos)
