import json
# componentes
from components.ambient.currentAmbient import CurrentAmbient
from components.ambient.graphicsAmbient import GraphicsAmbient
from components.ambient.historyAmbient import historyAmbient

# widgets
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor

from historiales.controllers.HistorialController import HistorialController
from dispositivos.controllers.deviceController import DispositivoController

import os
from dotenv import load_dotenv
load_dotenv()
SHADOW = os.getenv("SHADOW")

class Ambient(QWidget):
    def __init__(self, temperature_graphic, temp_value, temp_min, temp_max, 
                       humidity_graphic, hum_value, hum_min, hum_max, parent=None):
        super().__init__(parent)

        # IDs de dispositivos
        self.temp_disp = 3
        self.hum_disp = 6
        self.disp = self.temp_disp  # Predeterminado para temperatura

        # Valores actuales
        self.temp_value = temp_value
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.hum_value = hum_value
        self.hum_min = hum_min
        self.hum_max = hum_max

        # Historial
        self.temp_historial = []
        self.hum_historial = []

        # Gráficas
        self.temperature_graphic = temperature_graphic
        self.humidity_graphic = humidity_graphic

        # Controladores
        self.temp_historial_controller = HistorialController(self.temp_disp)
        self.hum_historial_controller = HistorialController(self.hum_disp)
        self.device_controller = DispositivoController()

        # Carga inicial de datos
        self.load()
        self.load_data()

        # Inicializa interfaz
        self.setup_ui()

        # Timer de actualización
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(10000)

        self.print_json()  # Esto imprimirá el JSON en consola al crear el widget


    def load(self):
        """Carga la configuración del dispositivo actual"""
        try:
            config = self.device_controller.get_dispositivo(self.disp) or {}
            self.temp_min = int(config.get("valor_minimo", 0))
            self.temp_max = int(config.get("valor_maximo", 100))
            return {
                "rango_min": self.temp_min,
                "rango_max": self.temp_max
            }
        except Exception as e:
            print(f"Error al cargar configuración de dispositivo: {e}")
            self.temp_min = 0
            self.temp_max = 100
            return None

    def load_data(self):
        """Carga datos de valor actual e historial para temperatura y humedad"""
        self.temp_value = self.temp_historial_controller.get_last()
        self.temp_historial = [
            {
                "fecha_ingreso": registro.fecha_ingreso.strftime("%d/%m/%Y %I:%M %p"),
                "valor": registro.valor,
            }
            for registro in self.temp_historial_controller.get_historial()
        ]
        self.hum_value = self.hum_historial_controller.get_last()
        self.hum_historial = [
            {
                "fecha_ingreso": registro.fecha_ingreso.strftime("%d/%m/%Y %I:%M %p"),
                "valor": registro.valor,
            }
            for registro in self.hum_historial_controller.get_historial()
        ]

    def refresh_data(self): 
        try:
            self.load()
            self.load_data()
            self.update_ui()
        except Exception as e:
            print(f"No se pudo refrescar los datos: {e}")

    def update_ui(self):
        """Actualiza los componentes de la UI con los datos nuevos"""
        # Actualiza las tarjetas de ambiente recreando el widget CurrentAmbient
        ambient_panel = CurrentAmbient(self.temp_value, self.temp_min, self.temp_max,
                                       self.hum_value, self.hum_min, self.hum_max)
        self.temp_card = ambient_panel.temperature_card
        self.hum_card = ambient_panel.humidity_card

        # Si tienes layouts, actualízalos correctamente aquí
        # (puedes agregar lógica para reemplazar widgets en el layout si es necesario)

        # Actualiza la gráfica de temperatura si existe
        if hasattr(self, 'temperature_graphic') and self.temperature_graphic:
            if hasattr(self.temperature_graphic, 'set_data'):
                self.temperature_graphic.set_data(self.temp_value)
            elif hasattr(self.temperature_graphic, 'update'):
                self.temperature_graphic.update()

        # Actualiza la gráfica de humedad si existe
        if hasattr(self, 'humidity_graphic') and self.humidity_graphic:
            if hasattr(self.humidity_graphic, 'set_data'):
                self.humidity_graphic.set_data(self.hum_value)
            elif hasattr(self.humidity_graphic, 'update'):
                self.humidity_graphic.update()

        # Actualiza la tabla del historial
        if self.table_card:
            self.table_card.clear_and_update_table(self.temp_historial)
            # Si tienes historial de humedad separado, puedes combinarlo aquí si es necesario
            self.table_card.temp_min = self.temp_min
            self.table_card.temp_max = self.temp_max
            self.table_card.hum_min = self.hum_min
            self.table_card.hum_max = self.hum_max

        # Imprime el JSON actualizado en consola cada vez que se actualiza la UI
        self.print_json()

    def start_timer(self, milliseconds=5000):
        if self.timer.isActive():
            self.timer.stop()
        self.timer.start(milliseconds)

    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()

    def setup_ui(self):
        """Inicializa y organiza los componentes visuales"""
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Panel ambiente actual
        ambient_panel = CurrentAmbient(self.temp_value, self.temp_min, self.temp_max,
                                       self.hum_value, self.hum_min, self.hum_max)
        self.temp_card = ambient_panel.temperature_card
        self.hum_card = ambient_panel.humidity_card

        left_cards_layout = QVBoxLayout()
        left_cards_layout.setContentsMargins(0, 0, 5, 5)
        left_cards_layout.addWidget(self.temp_card)
        left_cards_layout.addWidget(self.hum_card)

        left_cards_widget = QWidget()
        left_cards_widget.setLayout(left_cards_layout)
        left_cards_widget.setStyleSheet("background-color: #F0FFFE;")

        # Panel de gráfica
        graph_panel = GraphicsAmbient(self.temperature_graphic, self.humidity_graphic,
                                      self.temp_value, self.hum_value)
        graph_panel.setStyleSheet("margin:0;padding:0;margin-bottom:10px;border-radius: 12px;")
        graph_panel.setContentsMargins(0, 0, 0, 15)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(1, 4)
        r, g, b = map(int, SHADOW.split(","))
        shadow.setColor(QColor(r, g, b))
        graph_panel.setGraphicsEffect(shadow)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 0, 20, 0)
        top_layout.setSpacing(10)
        top_layout.addWidget(left_cards_widget, 1)
        top_layout.addWidget(graph_panel, 4)

        # Panel historial
        self.table_card = historyAmbient(self.to_json())

        history_shadow = QGraphicsDropShadowEffect()
        history_shadow.setBlurRadius(10)
        history_shadow.setOffset(1, 4)
        history_shadow.setColor(QColor(r, g, b))
        self.table_card.setGraphicsEffect(history_shadow)

        history_container = QWidget()
        history_layout = QVBoxLayout(history_container)
        history_layout.setContentsMargins(15, 0, 15, 0)
        history_layout.setSpacing(0)
        history_container.setStyleSheet("background-color: #F0FFFE;")
        history_layout.addWidget(self.table_card)

        # Ensamblar UI
        main_layout.addLayout(top_layout, 1)
        main_layout.addWidget(history_container, 10)
        self.setLayout(main_layout)

    def to_json(self):
        return {
            "rango": self.load(),
            "temperatura": {
                "actual": self.temp_value,
                "historial": self.temp_historial
            },
            "humedad": {
                "actual": self.hum_value,
                "historial": self.hum_historial
            }
        }

    def print_json(self):
        import decimal
        def decimal_default(obj):
            if isinstance(obj, decimal.Decimal):
                return float(obj)
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
        print(json.dumps(self.to_json(), indent=4, ensure_ascii=False, default=decimal_default))