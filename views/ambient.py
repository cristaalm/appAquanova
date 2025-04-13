# componentes
from components.currentAmbient import CurrentAmbient
from components.graphicsAmbient import GraphicsAmbient
from components.historyAmbient import HistoryAmbient

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
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        # Panel de ambiente actual
        ambient_panel = CurrentAmbient(self.temperature_value, self.humidity_value)
        
        # Extraer los widgets de temperatura y humedad para colocarlos por separado
        temp_card = ambient_panel.temperature_card
        humidity_card = ambient_panel.humidity_card

        # Agregar tarjetas en la columna izquierda (fila 0 y 1)
        grid_layout.addWidget(temp_card, 0, 0)
        grid_layout.addWidget(humidity_card, 1, 0)

        # Agregar gráfica que ocupará las filas 0 y 1 de la segunda columna
        graph_panel = GraphicsAmbient(self.temperature_graphic, self.humidity_graphic)
        graph_panel.setStyleSheet("margin:0;padding:0;border-radius: 12px;")
        
        # Efecto de sombra para la gráfica
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(5, 5)
        r, g, b = map(int, SHADOW.split(","))
        shadow.setColor(QColor(r, g, b))
        graph_panel.setGraphicsEffect(shadow)
        
        # Limitar la altura máxima del panel de gráficos
        graph_panel.setMaximumHeight(300)

        # Agregar el panel de gráficos al layout
        grid_layout.addWidget(graph_panel, 0, 1, 2, 1)  # fila 0, col 1, rowspan 2, colspan 1

        main_layout.addLayout(grid_layout)
        
        # Estilo para los widgets en el layout
        temp_card.setStyleSheet("margin: 0; padding: 0; border-radius: 12px;")
        humidity_card.setStyleSheet("margin: 0; padding: 0; border-radius: 12px;")
        
        # Historial con scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Crear widget de historial
        history_widget = HistoryAmbient()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(5, 5)
        r, g, b = map(int, SHADOW.split(","))
        shadow.setColor(QColor(r, g, b))
        scroll_area.setGraphicsEffect(shadow)
        scroll_area.setWidget(history_widget)
        
        # Estilo del scroll
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                border-radius: 12px;
            }
            QScrollBar:vertical {
                width: 12px;
                background: transparent;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #4CA4A5;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::up-button, QScrollBar::down-button {
                background: transparent;
                border: none;
            }
            QScrollBar::up-button:hover, QScrollBar::down-button:hover {
                background: transparent;
            }
            QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {
                background: transparent;
            }
        """)

        # Agregar la área de scroll al layout principal
        main_layout.addWidget(scroll_area)
        
        # Establecer el layout del widget principal
        self.setLayout(main_layout)
