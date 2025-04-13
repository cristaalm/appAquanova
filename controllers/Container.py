from .Graphs.Water.pH import GraphHp as GraphHpWater
from .Graphs.Water.Temp import GraphTemp as GraphTempWater
from .Graphs.Water.LvlWater import GraphLvlWater
from .Graphs.Water.CE import GraphCE as GraphCEWater
from .Graphs.Ambient.Temp import GraphTemp as GraphTempAmbient
from .Graphs.Ambient.humidity import GraphHU as GraphHumidityAmbient
from .Serial.AsyncSerialWorker import SerialWorker
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from .Notification.NotificationWidget import NotificationWidget
from components.pHComponent import phComponent
from views.ambient import Ambient


class ContentContainer(QWidget):
    def __init__(self):
        super().__init__()
        # Layout principal (vertical)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Parte superior: Título
        self.title_label = QLabel("Bienvenido a el monitor de AquaNova")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar el texto
        self.title_label.setStyleSheet(
            """
            font-size: 20px; 
            font-weight: bold; 
            color: #333333;
            padding: 10px;
            border-bottom: 2px solid #e0e0e0;
        """
        )  # Estilo del título con tema claro
        self.layout.addWidget(self.title_label)

        # Parte central: Contenedor para la gráfica o componente (ocupará solo la parte superior)
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Centrar el contenido
        self.content_layout.setContentsMargins(10, 10, 10, 10)  # Márgenes internos

        # Añadir el contenedor de contenido al layout principal
        self.layout.addWidget(self.content_container)

        # Añadir un espaciador que empujará todo hacia arriba
        self.spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.layout.addItem(self.spacer)

        # Parte inferior derecha: Notificación (hacer que se sobreponga a la gráfica y al contenedor)
        self.notification = NotificationWidget(self)
        self.notification.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
        self.notification.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.notification.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )

        # Configurar tema claro
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(
            QPalette.ColorRole.Window, QColor(240, 255, 254)
        )  # Fondo claro
        palette.setColor(
            QPalette.ColorRole.WindowText, QColor(51, 51, 51)
        )  # Texto oscuro
        palette.setColor(
            QPalette.ColorRole.Base, QColor(255, 255, 255)
        )  # Fondo de widgets
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))  # Texto en widgets
        self.setPalette(palette)

        # values 
        self.temp_value = 20.3
        self.hum_value = 58
        
        # Initialize graphs
        self.graph_ph_water = GraphHpWater()
        self.graph_temp_water = GraphTempWater()
        self.graph_lvl_water = GraphLvlWater()
        self.graph_ce_water = GraphCEWater()
        self.graph_temp_ambient = GraphTempAmbient()
        self.graph_humidity_ambient = GraphHumidityAmbient()

        # Initialize components
        self.ph_component = phComponent(self.graph_ph_water)
        self.ambient = Ambient(self.graph_temp_ambient, 
                            self.temp_value,
                            self.hum_value, 
                            self.graph_humidity_ambient)

        # Instance variable to track content state
        self.content_state = 0

        # Configuración del serial
        self.serial_worker = SerialWorker()
        self.serial_worker.data_received.connect(self.handle_serial_data)
        self.serial_worker.error_occurred.connect(self.handle_serial_error)
        self.serial_worker.status_changed.connect(self.handle_serial_status)
        self.serial_worker.start()

    def handle_serial_data(self, data):
        """Actualiza todas las gráficas con los datos recibidos"""
        print("Datos recibidos:", data)  # Debug

        try:
            if "ph" in data:
                self.graph_ph_water.updateHp(float(data["ph"]))
            if "temp" in data:
                self.graph_temp_water.updateTemp(float(data["temp"]))
            if "dist" in data:
                self.graph_lvl_water.updateLvlWater(float(data["dist"]))
            if "ec" in data:
                self.graph_ce_water.updateCE(float(data["ec"]))
            if "humidity" in data and data["humidity"] is not None:
                self.graph_humidity_ambient.updateHU(float(data["humidity"]))
            if "dht_temp" in data and data["dht_temp"] is not None:
                self.graph_temp_ambient.updateTemp(float(data["dht_temp"]))
        except (ValueError, TypeError) as e:
            print(f"Error procesando datos: {e}")

    def handle_serial_error(self, error_msg):
        print(f"ERROR SERIAL: {error_msg}")
        # Puedes mostrar esto en la UI
        self.notification.show_message(error_msg, "error")

    def handle_serial_status(self, status_msg):
        print(f"ESTADO SERIAL: {status_msg}")
        # Puedes mostrar esto en la UI
        self.notification.show_message(status_msg, "success")

    def closeEvent(self, event):
        """Cierre seguro de todos los recursos"""
        if self.serial_worker.isRunning():
            self.serial_worker.stop()
        super().closeEvent(event)

    def update_content(self):
        # Limpiar el contenedor de contenido
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Actualizar el contenido basado en el estado
        if self.content_state == 0:
            self.title_label.setText("Contenido Principal")
            default_msg = QLabel("Seleccione una gráfica")
            default_msg.setStyleSheet("color: #666666; font-size: 16px;")
            self.content_layout.addWidget(default_msg)
        elif self.content_state == 1:
            self.title_label.setText("Gráfica de Nivel de Agua")
            self.content_layout.addWidget(self.graph_lvl_water)
        elif self.content_state == 2:
            self.title_label.setText("Nivel de pH")
            self.content_layout.addWidget(
                self.ph_component
            )  # Usar el componente completo
        elif self.content_state == 3:
            self.title_label.setText("Gráfica de Temperatura")
            self.content_layout.addWidget(self.graph_temp_water)
        elif self.content_state == 4:
            self.title_label.setText("Gráfica de Conductividad")
            self.content_layout.addWidget(self.graph_ce_water)
        elif self.content_state == 5:
            self.title_label.setText("Supervisión medioambiental")
            self.content_layout.addWidget(self.ambient)
        elif self.content_state == 6:
            self.title_label.setText("Gráfica de Humedad Ambiente")
            self.content_layout.addWidget(self.graph_humidity_ambient)
        else:
            self.title_label.setText("Estado Desconocido")
            error_msg = QLabel("Estado no válido")
            error_msg.setStyleSheet("color: #cc0000; font-size: 16px;")
            self.content_layout.addWidget(error_msg)

    def set_content_state(self, state):
        self.content_state = state
        self.update_content()

    def get_container(self):
        return self
