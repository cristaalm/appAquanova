from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from controllers.Graphs.Water.pH import GraphHp
from .phSummaryPanel import PhSummaryPanel
from .phHistoryPanel import PhHistoryPanel

class phComponent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph_widget = GraphHp()
        self.ph_value = 6.5
        self.setup_ui()
    
    def setup_ui(self):
        # Layout principal
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #f5f7fa;")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Dos paneles superiores en fila con alturas iguales
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)
        
        # Panel de resumen
        self.summary_panel = PhSummaryPanel()
        top_layout.addWidget(self.summary_panel, 1)
        
        # Panel de gráfico
        top_layout.addWidget(self.create_graph_panel(), 4)
        
        main_layout.addLayout(top_layout, 1)
        
        # Panel de historial
        self.history_panel = PhHistoryPanel()
        main_layout.addWidget(self.history_panel, 10)
        
        self.setLayout(main_layout)
    
    def create_graph_panel(self):
        # Panel para gráfica de tendencia
        graph_panel = QFrame()
        graph_panel.setFrameShape(QFrame.Shape.StyledPanel)
        graph_panel.setMinimumHeight(280)
        graph_panel.setFixedHeight(280)
        graph_panel.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")
        
        from PyQt6.QtGui import QColor
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QSizePolicy, QVBoxLayout
        
        # Sombra
        graph_shadow = QGraphicsDropShadowEffect()
        graph_shadow.setBlurRadius(15)
        graph_shadow.setColor(QColor(197, 239, 236))
        graph_shadow.setOffset(0, 3)
        graph_panel.setGraphicsEffect(graph_shadow)
        
        graph_layout = QVBoxLayout(graph_panel)
        graph_layout.setContentsMargins(15, 15, 15, 15)
        graph_layout.setSpacing(10)
        
        # Configurar la gráfica
        self.graph_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        graph_layout.addWidget(self.graph_widget, 1)
        
        return graph_panel
    
    def set_ph_value(self, new_value):
        self.ph_value = float(new_value)
        self.summary_panel.set_ph_value(new_value)