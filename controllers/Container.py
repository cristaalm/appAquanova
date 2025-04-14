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

# controladores Django
from historiales.controllers.PHController import PHController
from historiales.controllers.TempWaterController import TempWaterController
from historiales.controllers.TempAmbientController import TempAmbientController
from historiales.controllers.CEController import CEController
from historiales.controllers.DistanceController import DistanceController
from historiales.controllers.HUAmbientController import HUAmbientController
from views.systems import Systems


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
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.layout.addWidget(self.content_container)

        # Espaciador inferior
        self.spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.layout.addItem(self.spacer)

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

        # Valores ambientales simulados
        self.temp_value = 20.3
        self.hum_value = 58

        company_list = [
            {
                "company_name": "Empresa 1",
                "trade_name": "Comercial Uno",
                "legal_name": "S.A. de C.V. Uno",
                "logo": "logo_text.png"
            },
            {
                "company_name": "Empresa 2",
                "trade_name": "Comercial Dos",
                "legal_name": "S.A. de C.V. Dos",
                "logo": "logo_text.png"
            },{
                "company_name": "Empresa 1",
                "trade_name": "Comercial Uno",
                "legal_name": "S.A. de C.V. Uno",
                "logo": "logo_text.png"
            },
            {
                "company_name": "Empresa 2",
                "trade_name": "Comercial Dos",
                "legal_name": "S.A. de C.V. Dos",
                "logo": "logo_text.png"
            },{
                "company_name": "Empresa 1",
                "trade_name": "Comercial Uno",
                "legal_name": "S.A. de C.V. Uno",
                "logo": "logo_text.png"
            },
            {
                "company_name": "Empresa 2",
                "trade_name": "Comercial Dos",
                "legal_name": "S.A. de C.V. Dos",
                "logo": "logo_text.png"
            }
        ]
        # Inicialización de gráficas
        self.graph_ph_water = GraphHpWater()
        self.graph_temp_water = GraphTempWater()
        self.graph_lvl_water = GraphLvlWater()
        self.graph_ce_water = GraphCEWater()
        self.graph_temp_ambient = GraphTempAmbient()
        self.graph_humidity_ambient = GraphHumidityAmbient()

        # Componentes
        self.ph_component = phComponent(self.graph_ph_water)
        self.ambient = Ambient(
            self.graph_temp_ambient,
            self.temp_value,
            self.hum_value,
            self.graph_humidity_ambient,
        )
        self.systems = Systems(company_list)
        # Estado inicial
        self.content_state = 0

        # Serial
        self.serial_worker = SerialWorker()
        self.serial_worker.data_received.connect(self.handle_serial_data)
        self.serial_worker.error_occurred.connect(self.handle_serial_error)
        self.serial_worker.status_changed.connect(self.handle_serial_status)
        self.serial_worker.start()

        # Mostrar contenido inicial
        self.update_content()

    def handle_serial_data(self, data):
        print("Datos recibidos:", data)
        try:
            if "ph" in data:
                self.graph_ph_water.updateHp(float(data["ph"]))
                self.ph_controller.set_history(float(data["ph"]))
            if "temp" in data:
                self.graph_temp_water.updateTemp(float(data["temp"]))
                self.temp_water_controller.set_history(float(data["temp"]))
            if "dist" in data:
                self.graph_lvl_water.updateLvlWater(float(data["dist"]))
                self.distance_controller.set_history(float(data["dist"]))
            if "ec" in data:
                self.graph_ce_water.updateCE(float(data["ec"]))
                self.ce_controller.set_history(float(data["ec"]))
            if "humidity" in data and data["humidity"] is not None:
                self.graph_humidity_ambient.updateHU(float(data["humidity"]))
                self.humidity_controller.set_history(float(data["humidity"]))
            if "dht_temp" in data and data["dht_temp"] is not None:
                self.graph_temp_ambient.updateTemp(float(data["dht_temp"]))
                self.temp_ambient_controller.set_history(float(data["dht_temp"]))
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
        super().closeEvent(event)

    def update_content(self):
        # Limpiar contenido actual
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Mostrar contenido según estado
        if self.content_state == 0:
            self.title_label.setText("Bienvenido a el monitor de AquaNova")
            welcome_label = QLabel(
                "¡Explora los datos de tus sensores en tiempo real!<br><br>"
                "Este sistema te permite monitorear parámetros vitales del agua y del entorno, como el nivel, pH, temperatura, conductividad y condiciones ambientales. "
                "Utiliza el menú lateral para comenzar.<br><br>"
                "<i>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus luctus urna sed urna ultricies ac tempor dui sagittis.</i>"
            )
            welcome_label.setStyleSheet("color: #4CA4A5; font-size: 14px;")
            welcome_label.setWordWrap(True)
            welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.content_layout.addWidget(welcome_label)
        elif self.content_state == 1:
            self.title_label.setText("Gráfica de Nivel de Agua")
            self.content_layout.addWidget(self.graph_lvl_water)
        elif self.content_state == 2:
            self.title_label.setText("Nivel de pH")
            self.content_layout.addWidget(self.ph_component)
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
            self.title_label.setText("Dispositivos")
        elif self.content_state == 7:
            self.title_label.setText("Sistemas")
            self.content_layout.addWidget(self.systems)
        else:
            self.title_label.setText("Estado Desconocido")
            error_msg = QLabel("Estado no válido")
            error_msg.setStyleSheet("color: #cc0000; font-size: 16px;")
            error_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.content_layout.addWidget(error_msg)

    def set_content_state(self, state):
        self.content_state = state
        self.update_content()

    def get_container(self):
        return self
