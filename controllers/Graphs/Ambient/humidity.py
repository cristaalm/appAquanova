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
    def __init__(self):
        super().__init__(
            x_label="Tiempo (horas)",
            y_label="% Humedad",
            line_color=HUMIDITY_COLOR,  # Color para humedad
            data_range=(30.0, 90.0),
            initial_data_length=24,  # Mostrar 24 puntos
        )
        # Ajustar los valores del eje X para que comiencen desde 1
        self.data_x = list(range(1, 25))  # De 1 a 24
        self.curve.setData(self.data_x, self.data_y)

    def custom_config(self):
        """Configuración adicional específica para humedad"""
        # Configuración de rango de humedad
        self.set_data_range(0, 100)  # Rango razonable para humedad relativa
        
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

    def updateHumidity(self, new_value: float):
        """Alias para mantener compatibilidad con código existente"""
        self.update_data(new_value)

    def create_graph_panel(self):
        graph_panel = QFrame()
        self.setMinimumHeight(0)
        # No se fija altura máxima, se adapta al contenedor
        graph_panel.setFrameShape(QFrame.Shape.StyledPanel)
        graph_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        r, g, b = map(int, SHADOW.split(","))
        shadow_color = QColor(r, g, b)
        shadow.setColor(shadow_color)
        shadow.setOffset(0, 3)
        graph_panel.setGraphicsEffect(shadow)
        
        graph_layout = QVBoxLayout(graph_panel)
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        graph_layout.addWidget(self, 1)  # Añadir el widget de gráfica directamente
        return graph_panel