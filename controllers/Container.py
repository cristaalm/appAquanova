from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import QThread
from .Notification.NotificationWidget import NotificationWidget
from .Graphs.Ambient.Humidity import GraphHumidity as GraphHumidityAmbient
from .Graphs.Ambient.Temp import GraphTemp as GraphTempAmbient
from .Graphs.Water.Temp import GraphTemp as GraphTempWater
from .Graphs.Water.CE import GraphCE as GraphCEWater
from .Graphs.Water.pH import GraphHp as GraphHpWater
from .Graphs.Water.LvlWater import GraphLvlWater
from components.lvlWater.WaterComponent import WaterComponent
from .Serial.AsyncSerialWorker import SerialWorker
from .Signal.SignalController import SignalController
from components.ph.pHComponent import phComponent
from views.waterTemp import tempWaterComponent
from views.DevicesView import DevicesView
from views.conductivityE import conductivityComponent
from PyQt6.QtGui import QPalette, QColor
from views.ambient import Ambient
from PyQt6.QtCore import Qt
from random import randint
import threading
from concurrent.futures import ThreadPoolExecutor
from historiales.controllers.TempAmbientController import TempAmbientController
from historiales.controllers.TempWaterController import TempWaterController
from historiales.controllers.HUAmbientController import HUAmbientController
from historiales.controllers.HistorialController import HistorialController
from historiales.controllers.DistanceController import DistanceController
from historiales.controllers.PHController import PHController
from historiales.controllers.CEController import CEController
from components.cardDashboard import CardDashboard
from utils.backgroundSync import background_sync

class ContentContainer(QWidget):
    def __init__(self):
        super().__init__()
        # Layout principal (vertical)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Parte superior: Título
        self.title_label = QLabel("Bienvenido a el monitor de AquaNova")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(
            """
            font-size: 20px; 
            font-weight: bold; 
            color: #333333;
            padding: 10px;
            border-bottom: 2px solid #B6F1ED;
        """
        )
        self.layout.addWidget(self.title_label)

        # Parte central: Contenedor para la gráfica o componente
        self.content_container = QWidget()
        self.content_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.layout.addWidget(self.content_container, stretch=1)

        # Espaciador inferior
        self.spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.layout.addItem(self.spacer)
        self.spacer_active = True

        # Notificaciones
        self.notification = NotificationWidget(self)
        self.notification.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
        self.notification.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.notification.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )

        # Tema claro
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 255, 254))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(51, 51, 51))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        self.setPalette(palette)

        # inicialización de controladores
        self.ph_controller = PHController()
        self.temp_water_controller = TempWaterController()
        self.temp_ambient_controller = TempAmbientController()
        self.ce_controller = CEController()
        self.distance_controller = DistanceController()
        self.humidity_controller = HUAmbientController()
        self.historial_controller = HistorialController()

        # iniciar thread para sincronización del historial
        sync_thread = threading.Thread(target=background_sync, args=(self.historial_controller,), daemon=True)
        sync_thread.start()

        # Pool de hilos para registro de datos
        self.executor = ThreadPoolExecutor(max_workers=5)  # Puedes ajustar el número

        # Inicialización de gráficas
        self.graph_ph_water = GraphHpWater()
        self.graph_temp_water = GraphTempWater()
        self.graph_lvl_water = GraphLvlWater()
        self.graph_ce_water = GraphCEWater()
        self.graph_temp_ambient = GraphTempAmbient()
        self.graph_humidity_ambient = GraphHumidityAmbient()

        ce_value = randint(1000, 1500)        # Componentes
        self.water_component = WaterComponent(self.graph_lvl_water)
        self.ph_component = phComponent(self.graph_ph_water)
        self.temp_water_component = tempWaterComponent(self.graph_temp_water)
        self.ce_component = conductivityComponent(self.graph_ce_water,ce_value)  # Nuevo componente
        self.ambient = Ambient(
            self.graph_temp_ambient,
            self.graph_humidity_ambient,
        )

        self.devices_view = DevicesView(self.notification)
        self.card_dashboard = CardDashboard()
        # Estado inicial
        self.content_state = 0

        # Serial
        self.serial_worker = SerialWorker()
        self.serial_worker.data_received.connect(self.handle_serial_data)
        self.serial_worker.error_occurred.connect(self.handle_serial_error)
        self.serial_worker.status_changed.connect(self.handle_serial_status)
        self.serial_worker.start()

        # Inicialización del controlador de señales
        self.signal_thread = QThread()
        self.signal_controller = SignalController(self.serial_worker, self.notification)
        self.signal_controller.moveToThread(self.signal_thread)
        self.signal_thread.start()

        # Mostrar contenido inicial
        self.update_content()

    def handle_serial_data(self, data):
        """
        Ejemplo de como se resiven los datos desde el serial:
        {"sensor":"temp","valor":27.2}
        {"sensor":"dist","valor":54.4}
        {"sensor":"ec","valor":2623}
        {"sensor":"humedad_dht","valor":50.9}
        {"sensor":"temp_dht","valor":20}
        {"sensor":"ph","valor":20}
        """
        print(data)
        try:
            sensor = data["sensor"]
            valor = data["valor"]
            if sensor == "ph":
                self.graph_ph_water.updateHp(float(valor))
                self.executor.submit(self.ph_controller.set_history, float(valor))

                self.ph_component.set_ph_value(valor)  # Actualizar componente pH
            elif sensor == "temp":
                self.graph_temp_water.updateTemp(float(valor))
                self.executor.submit(self.temp_water_controller.set_history, float(valor))

            elif sensor == "dist":
                self.graph_lvl_water.updateLvlWater(float(valor))
                self.executor.submit(self.distance_controller.set_history, float(valor))

            elif sensor == "ec":
                self.graph_ce_water.updateCE(float(valor))
                self.executor.submit(self.ce_controller.set_history, float(valor))

            elif sensor == "humedad_dht":
                self.graph_humidity_ambient.updateHU(float(valor))
                self.executor.submit(self.humidity_controller.set_history, float(valor))

            elif sensor == "temp_dht":
                self.graph_temp_ambient.updateTemp(float(valor))
                self.executor.submit(self.temp_ambient_controller.set_history, float(valor))

        except (ValueError, TypeError) as e:
            print(f"Error procesando datos: {e}")

    def handle_serial_error(self, error_msg):
        print(f"ERROR SERIAL: {error_msg}")
        self.notification.show_message(error_msg, "error")

    def handle_serial_status(self, status_msg):
        print(f"ESTADO SERIAL: {status_msg}")
        self.notification.show_message(status_msg, "success")

    def closeEvent(self, event):
        if self.serial_worker.isRunning():
            self.serial_worker.stop()
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)
        super().closeEvent(event)

    def update_content(self):
        # Limpiar contenido actual
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Quitar espaciador si estamos en Dispositivos
        if self.content_state == 6:
            if self.spacer is not None and self.spacer_active:
                self.layout.removeItem(self.spacer)
                self.spacer_active = False
            self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.content_layout.setContentsMargins(0, 0, 0, 0)
        else:
            if self.spacer is not None and not self.spacer_active:
                self.layout.addItem(self.spacer)
                self.spacer_active = True
            self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.content_layout.setContentsMargins(10, 10, 10, 10)

        # Mostrar contenido según estado
        if self.content_state == 0:
            self.title_label.setText("Bienvenido a el monitor de AquaNova")
            self.content_layout.addWidget(self.card_dashboard)
        elif self.content_state == 1:
            self.title_label.setText("Gestión de niveles de agua")
            self.content_layout.addWidget(self.water_component)
        elif self.content_state == 2:
            self.title_label.setText("Nivel de pH del agua")
            self.content_layout.addWidget(self.ph_component)
        elif self.content_state == 3:
            self.title_label.setText("Temperatura del Agua")
            self.content_layout.addWidget(self.temp_water_component)
        elif self.content_state == 4:
            self.title_label.setText("Conductividad eléctrica")
            self.content_layout.addWidget(self.ce_component) 
        elif self.content_state == 5:
            self.title_label.setText("Supervisión medioambiental")
            self.content_layout.addWidget(self.ambient)
        elif self.content_state == 6:
            self.title_label.setText("Dispositivos")
            self.content_layout.addWidget(self.devices_view)
        else:
            self.title_label.setText("Estado Desconocido")
            error_msg = QLabel("Estado no válido")
            error_msg.setStyleSheet("color: #cc0000; font-size: 16px;")
            error_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.content_layout.addWidget(error_msg)

    def set_content_state(self, state):
        self.content_state = state
        self.update_content()

    def get_container(self):        return self