# componentes
from components.ambient.currentAmbient import CurrentAmbient
from components.ambient.graphicsAmbient import GraphicsAmbient
from components.ambient.historyAmbient import HistoryAmbient

# widgets
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QGridLayout,
    QHeaderView, QSpacerItem, QScrollArea, QFrame, QComboBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor

import os
from dotenv import load_dotenv
load_dotenv()
SHADOW = os.getenv("SHADOW")

class Ambient(QWidget):
    def __init__(self, temperature_graphic, 
                 temperature_value, humidity_value, 
                 humidity_graphic, parent=None):
        super().__init__(parent)
        self.temperature_value = temperature_value      # valor de temperatura
        self.temperature_graphic = temperature_graphic  # recibe gráfica
        self.humidity_value = humidity_value            # valor de humedada
        self.humidity_graphic = humidity_graphic        # recibe gráfica
        self.setup_ui()

    def setup_ui(self):
        # Configuración principal del formulario
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) #quitar espacios del layout 
        main_layout.setSpacing(0)  # Sin espacio entre secciones principales

        # Panel de ambiente actual
        ambient_panel = CurrentAmbient(self.temperature_value, self.humidity_value)
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
        graph_panel.setContentsMargins(0, 0, 0, 10)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(1, 4)
        r, g, b = map(int, SHADOW.split(","))
        shadow.setColor(QColor(r, g, b))
        graph_panel.setGraphicsEffect(shadow)
        graph_panel.setMaximumHeight(500)

        # Layout superior (tarjetas + gráfica)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 0, 20, 0)  # Quita margen inferior
        top_layout.setSpacing(10)  # Sin espacio entre cards y gráfica
        top_layout.addWidget(left_cards_widget, 1)
        top_layout.addWidget(graph_panel, 4)

        # Widget historial
        history_widget = HistoryAmbient()
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

