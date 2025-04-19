from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QFrame,
    QLabel,
    QSizePolicy,
)
from .DeviceCard import DeviceCard
from .FlowLayout import FlowLayout


class DevicesView(QWidget):
    def __init__(self, notification, parent=None):
        super().__init__(parent)
        self.notification = notification
        self.setup_ui()
        self.load_devices()

    def setup_ui(self):
        self.setStyleSheet("background-color: #f0fffe;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # self.setMinimumHeight(0)  # Altura mínima de 600 píxeles

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Título
        title = QLabel("Dispositivos Conectados")
        title.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            color: #1e293b;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0fffe;
            """
        )
        main_layout.addWidget(title)

        # Contenedor del layout dinámico (sin scroll)
        content_widget = QWidget()
        self.flow_layout = FlowLayout(content_widget, spacing=20)
        content_widget.setLayout(self.flow_layout)
        content_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum
        )
        main_layout.addWidget(content_widget)
        main_layout.addStretch()  # Esto empujará el contenido hacia arriba

    def load_devices(self):
        devices_data = [
            {
                "name": "Sensor de Conductividad",
                "model": "TDS",
                "status": "Activo",
                "type": "sensor_tds",
                "icon": "conductivity.jpg",
                "description": "Sensor TDS para medir la conductividad del agua, útil para calidad del agua.",
            },
            {
                "name": "Sensor de pH",
                "model": "PH-4502C + E201-BNC",
                "status": "Activo",
                "type": "sensor_ph",
                "icon": "ph.jpg",
                "description": "Sensor de pH para monitorear la acidez o alcalinidad del agua.",
            },
            {
                "name": "Sensor de Temperatura y Humedad",
                "model": "DHT11",
                "status": "Activo",
                "type": "sensor_dht11",
                "icon": "dht11.jpg",
                "description": "Sensor DHT11 para monitoreo básico de temperatura y humedad ambiental.",
            },
            {
                "name": "Sensor de Temperatura Sumergible",
                "model": "DS18B20",
                "status": "Activo",
                "type": "sensor_ds18b20",
                "icon": "sub_temp.jpg",
                "description": "Sensor DS18B20 sumergible ideal para líquidos, con alta precisión.",
            },
            {
                "name": "Sensor Ultrasónico",
                "model": "JSN-SR04T",
                "status": "Activo",
                "type": "sensor_ultrasonico",
                "icon": "ultrasonic.jpg",
                "description": "Sensor ultrasónico impermeable para medir distancia o nivel de agua.",
            },
        ]

        for device_data in devices_data:
            card = DeviceCard(self.notification, device_data)
            self.flow_layout.addWidget(card)
