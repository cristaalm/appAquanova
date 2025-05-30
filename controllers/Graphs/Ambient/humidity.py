from utils.BaseGraph import BaseGraph
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QApplication, 
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QComboBox, QGraphicsDropShadowEffect,
    QProgressBar, QLineEdit, QTableWidgetItem
)
from random import randint
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPixmap, QBrush
import os 
from dotenv import load_dotenv
import pyqtgraph as pg

load_dotenv()
SHADOW = os.getenv("SHADOW")
HUMIDITY_COLOR = os.getenv("HUMIDITY_COLOR")
GRAPH_POINT_SIZE = int(os.getenv("GRAPH_POINT_SIZE"))
COLOR_LEYEND = os.getenv("COLOR_LEYEND")


class GraphHumidity(BaseGraph):
    def __init__(self, parent=None, hum_value=None, hum_min=None, hum_max=None):
        # Valores por defecto para evitar None
        if hum_min is None:
            hum_min = 30
        if hum_max is None:
            hum_max = 90
        self.hum_min = hum_min   # Guarda como atributo
        self.hum_max = hum_max   # Guarda como atributo
        super().__init__(
            x_label="Tiempo (horas)",
            y_label="% Humedad",
            line_color=HUMIDITY_COLOR,  # Color para humedad
            data_range=(hum_min, hum_max),
            initial_data_length=24,  # Mostrar 24 puntos
        )
        # Ajustar los valores del eje X para que comiencen desde 1
        self.data_x = list(range(1, 25))  # De 1 a 24
        self.curve.setData(self.data_x, self.data_y)

    def custom_config(self):
        """Configuración adicional específica para humedad"""
        # Configuración de rango de humedad
        self.set_data_range(self.hum_min, self.hum_max)  # Rango razonable para humedad relativa
        
        style = {"color": COLOR_LEYEND, "font-size": "11px"}
        
        # Establecer fondo blanco
        self.setBackground("white")
        
        # Configurar etiquetas con el estilo deseado
        self.getPlotItem().setLabel("left", "% Humedad", **style)
        self.getPlotItem().setLabel("bottom", "Tiempo (horas)", **style)
        
        # Añadir leyenda
        self.getPlotItem().addLegend()
        
        # Mostrar cuadrícula
        self.getPlotItem().showGrid(x=True, y=True, alpha=0.3)
        
        # Modificar el estilo de la línea para añadir símbolos
        pen = pg.mkPen(color=HUMIDITY_COLOR)
        self.curve.setPen(pen)
        self.curve.setSymbol('o')
        self.curve.setSymbolSize(GRAPH_POINT_SIZE)
        self.curve.setSymbolBrush(HUMIDITY_COLOR)

    def updateHumidity(self, hum_value: float):
        """Alias para mantener compatibilidad con código existente"""
        self.update_data(hum_value)

    def create_graph_panel(self):
        graph_panel = QFrame()
        # graph_panel.setFixedHeight(150) 
        # No se fija altura máxima, se adapta al contenedor
        graph_panel.setFrameShape(QFrame.Shape.StyledPanel)
        graph_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        return graph_panel