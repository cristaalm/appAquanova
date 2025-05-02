from components.WaterTemp.TableCard import TableCard
from components.WaterTemp.InfoCard import CurrentTemp

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, 
    QSizePolicy, QFrame, QGraphicsDropShadowEffect, QSpacerItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class tempWaterComponent(QWidget):
    def __init__(self, GraphTemp, water_temp, parent=None):
        super().__init__(parent)
        self.value = water_temp
        self.graph = GraphTemp
        self.temp_max = 40
        self.temp_min = 10
        self.rango_min = 28
        self.rango_max = 32
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #f5f7fa;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  
        main_layout.setSpacing(15)  
        
        infoCard = CurrentTemp(self.value, self.temp_min, self.temp_max, self.rango_max, self.rango_min)
        panel = infoCard.panel
        graph = self.graph
        graph_panel = graph.create_graph_panel()
        
        table_container = QFrame()
        table_container.setFrameShape(QFrame.Shape.NoFrame)
        table_container.setStyleSheet("background: transparent;")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(15, 0, 15, 5) 
        
        # Create the table card
        table_card = TableCard(self.rango_max, self.rango_min)
        table_layout.addWidget(table_card)
        
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 0, 20, 0)  
        top_layout.setSpacing(15)
        
        top_layout.addWidget(panel, 1)
        top_layout.addWidget(graph_panel, 4)

        main_layout.addLayout(top_layout, 1)
        main_layout.addWidget(table_container, 10)  