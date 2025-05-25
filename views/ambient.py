# componentes
from components.ambient.currentAmbient import CurrentAmbient
from components.ambient.graphicsAmbient import GraphicsAmbient
from components.ambient.history import TableCard

# widgets
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QGridLayout,
    QHeaderView, QSpacerItem, QScrollArea, QFrame, QComboBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize,QTimer
from PyQt6.QtGui import QFont, QColor

from historiales.controllers.HistorialController import HistorialController
from dispositivos.controllers.deviceController import DispositivoController

import os
from dotenv import load_dotenv
load_dotenv()
SHADOW = os.getenv("SHADOW")

class Ambient(QWidget):
    def __init__(self, temperature_graphic, humidity_graphic, parent=None):
        super().__init__(parent)
        self.disp = 3
        self.temp_value = 22
        self.temp_min = 0
        self.temp_max = 50
        self.hum_value = 50
        self.hum_min = 0
        self.hum_max = 100
        self.rango_min = 0
        self.rango_max = 0
        self.temp_historial = []
        self.hum_historial = []

        self.temperature_graphic = temperature_graphic  # recibe gráfica
        self.humidity_graphic = humidity_graphic        # recibe gráfica

        self.historial_controller = HistorialController(self.disp)
        self.device_controller = DispositivoController()

        self.load()
        self.load_data()

        self.setup_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(10000)

    def load(self):
        if not self.device_controller:
            return None
        try:
            config = self.device_controller.get_dispositivo(self.disp) or {}
            self.rango_min = int(config.get("valor_minimo"))
            self.rango_max = int(config.get("valor_maximo"))
            return {
                "rango_min": self.rango_min,
                "rango_max": self.rango_max
            }
        except Exception as e:
            print(f"Error al cargar configuración de temperatura: {e}")
            return None
        
    def load_data(self):
        self.temp_value = self.historial_controller.get_last()
        self.temp_historial = [
            {
                "fecha_ingreso": registro.fecha_ingreso.strftime("%d/%m/%Y %I:%M %p"),
                "valor": registro.valor,
            }
            for registro in self.historial_controller.get_historial()
        ]
        self.hum_value = self.historial_controller.get_last()
        self.hum_historial = [
            {
                "fecha_ingreso": registro.fecha_ingreso.strftime("%d/%m/%Y %I:%M %p"),
                "valor": registro.valor,
            }
            for registro in self.historial_controller.get_historial()
        ]

    def refresh_data(self): 
        try:
            self.load()
            self.load_data()
            self.update_ui() 
        except Exception as e:
            print(f"No se pudo refrescar los datos: {e}") 

    def update_ui(self): 
        if self.current_temp:
            self.current_temp.update_value(self.temp_value)
            self.current_temp.rango_min = self.rango_min
            self.current_temp.rango_max = self.rango_max
        if self.table_card:
            self.table_card.clear_and_update_table(self.temp_historial)
            self.table_card.rango_min = self.rango_min
            self.table_card.rango_max = self.rango_max
        if self.current_hum:
            self.current_hum.update_value(self.hum_value)
            self.current_hum.rango_min = self.rango_min
            self.current_hum.rango_max = self.rango_max
        if self.table_card:
            self.table_card.clear_and_update_table(self.hum_historial)
            self.table_card.rango_min = self.rango_min
            self.table_card.rango_max = self.rango_max
    
    def start_timer(self, milliseconds=5000):
        """Start or restart the timer with the given interval"""
        if self.timer.isActive():
            self.timer.stop()
        self.timer.start(milliseconds)
    
    def stop_timer(self):
        """Stop the refresh timer"""
        if self.timer.isActive():
            self.timer.stop()

    def setup_ui(self):
        # Configuración principal del formulario
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) #quitar espacios del layout 
        main_layout.setSpacing(0)  # Sin espacio entre secciones principales

        # infoCardTemp = CurrentTemp(self.temp_value, self.temp_min, self.temp_max, self.rango_max, self.rango_min)
        # infoCardHum = CurrentHum(self.hum_value, self.hum_min, self.hum_max, self.rango_max, self.rango_min)
        
        # Panel de ambiente actual
        ambient_panel = CurrentAmbient(self.temp_value, self.hum_value)
        temp_card = ambient_panel.temperature_card
        humidity_card = ambient_panel.humidity_card

        # Layout izquierdo para las tarjetas
        left_cards_layout = QVBoxLayout()
        # margen blanco de las cards, es como el fondo
        left_cards_layout.setContentsMargins(0, 0, 5, 5)
        left_cards_layout.addWidget(temp_card)
        left_cards_layout.addWidget(humidity_card)
        left_cards_widget = QWidget()
        left_cards_widget.setLayout(left_cards_layout)
        left_cards_widget.setStyleSheet("background-color: #F0FFFE;")

        # Panel de gráfica
        graph_panel = GraphicsAmbient(self.temperature_graphic, self.humidity_graphic)
        graph_panel.setStyleSheet("margin:0;padding:0;margin-bottom:10px;border-radius: 12px;")
        graph_panel.setContentsMargins(0, 0, 0, 15)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(1, 4)
        r, g, b = map(int, SHADOW.split(","))
        shadow.setColor(QColor(r, g, b))
        graph_panel.setGraphicsEffect(shadow)

        # Layout superior (tarjetas + gráfica)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 0, 20, 0)  # Quita margen inferior
        top_layout.setSpacing(10)  # Sin espacio entre cards y gráfica
        top_layout.addWidget(left_cards_widget, 1)
        top_layout.addWidget(graph_panel, 4)

        # Widget historial
        history_widget = TableCard(self.temp_historial, self.rango_max, self.rango_min)
        history_shadow = QGraphicsDropShadowEffect()
        history_shadow.setBlurRadius(10)
        history_shadow.setOffset(1, 4)
        history_shadow.setColor(QColor(r, g, b))
        history_widget.setGraphicsEffect(history_shadow)
        # Si quieres margen externo para separar del borde, usa un widget contenedor:
        history_container = QWidget()
        history_layout = QVBoxLayout(history_container)
        history_layout.setContentsMargins(15, 0, 15, 0)
        history_layout.setSpacing(0)  # Sin espacio extra en historial
        history_container.setStyleSheet("background-color: #F0FFFE;")
        history_layout.addWidget(history_widget)

        # Añadir layouts al principal
        main_layout.addLayout(top_layout, 1)
        main_layout.addWidget(history_container, 10)

        self.setLayout(main_layout)

