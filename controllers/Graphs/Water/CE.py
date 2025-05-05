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


class GraphCE(BaseGraph):
    def __init__(self):
        super().__init__(
            x_label="Tiempo (minutos)",
            y_label="°C Temperatura",
            line_color="#1E89CF",  # Color azul similar a TempGraph
            data_range=(20.0, 25.0),  # Rango inicial
        )

    def custom_config(self):
        """Configuración adicional específica para temperatura"""
        # Configuración de rango de temperatura
        self.set_data_range(10, 40)  # Rango razonable para temperatura ambiente
        
        # Aplicar estilos de TempGraph
        style = {"color": "#045859", "font-size": "11px"}
        
        # Establecer fondo blanco
        self.setBackground("white")
        
        # Configurar etiquetas con el estilo deseado
        self.getPlotItem().setLabel("left", "Conductividad (S/m)", **style)
        self.getPlotItem().setLabel("bottom", "Tiempo (horas)", **style)
        
        # Añadir leyenda
        self.getPlotItem().addLegend()
        
        # Mostrar cuadrícula
        self.getPlotItem().showGrid(x=True, y=True, alpha=0.3)
        
        # Modificar el estilo de la línea para añadir símbolos
        pen = pg.mkPen(color="#2ECC71")
        self.curve.setPen(pen)
        self.curve.setSymbol('o')
        self.curve.setSymbolSize(7)
        self.curve.setSymbolBrush("#2ECC71")
        
        # Habilitar auto-rango
        self.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=True)
        self.getViewBox().autoRange()

    def updateCE(self, new_value: float):
        """Alias para mantener compatibilidad con código existente"""
        self.update_data(new_value)

    def create_graph_panel(self):
        graph_panel = QFrame()
        graph_panel.setMaximumHeight(280)
        graph_panel.setFixedHeight(280)
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
        graph_layout.setContentsMargins(15, 15, 15, 15)
        graph_layout.setSpacing(10)
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        graph_layout.addWidget(self, 1)  # Añadir el widget de gráfica directamente
        
        return graph_panel