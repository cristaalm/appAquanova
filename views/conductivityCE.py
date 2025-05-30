from components.conductivity.TableCard import TableCard
from components.conductivity.InfoCard import CurrentCe

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, 
    QSizePolicy, QFrame, QGraphicsDropShadowEffect, QSpacerItem
)
from PyQt6.QtCore import Qt,QTimer
from PyQt6.QtGui import QColor
from historiales.controllers.HistorialController import HistorialController
from dispositivos.controllers.deviceController import DispositivoController

class conductivityComponent(QWidget):
    def __init__(self, GraphCE, parent=None):
        super().__init__(parent)
        self.value = 0
        self.disp = 1
        self.graph = GraphCE
        self.ce_max = 0
        self.ce_min = 9999
        self.rango_min = 0
        self.rango_max = 0
        self.historial_controller = HistorialController(self.disp)
        self.device_controller = DispositivoController()

        self.load()
        self.load_data()

        self.current_ce = CurrentCe(self.value, self.ce_min, self.ce_max, self.rango_max, self.rango_min)
        self.table_card = TableCard(self.historial, self.rango_max, self.rango_min)

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
            print(f"Error al cargar configuración de conductividad: {e}")
            return None
        
    def load_data(self):
        self.value = self.historial_controller.get_last()
        self.historial = [
            {
                "fecha_ingreso": registro.fecha_ingreso.strftime("%Y-%m-%d %H:%M:%S"),
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
        if self.current_ce:
            self.current_ce.update_value(self.value)
            self.current_ce.rango_min = self.rango_min
            self.current_ce.rango_max = self.rango_max
        if self.table_card:
            self.table_card.clear_and_update_table(self.historial)
            self.table_card.rango_min = self.rango_min
            self.table_card.rango_max = self.rango_max

    def setup_ui(self):
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #f5f7fa;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 0, 20, 0)  
        main_layout.setSpacing(15)  
        
        infoCard = self.current_ce
        panel = infoCard.panel
        graph = self.graph
        graph_panel = graph.create_graph_panel()
        
        table_widget = QWidget()
        table_container = QFrame()
        table_container.setFrameShape(QFrame.Shape.NoFrame)
        table_container.setStyleSheet("background: transparent;")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 5) 
        table_layout.setSpacing(0)
        table_layout.addWidget(table_widget)
        
        # Create the table card
        table_card = self.table_card
        table_layout.addWidget(table_card)
        
        top_layout = QHBoxLayout() 
        top_layout.setSpacing(15)
        
        top_layout.addWidget(panel, 1)
        top_layout.addWidget(graph_panel, 4)

        main_layout.addLayout(top_layout, 1)
        main_layout.addWidget(table_container, 10)  

    def start_timer(self, milliseconds=5000):
        """Start or restart the timer with the given interval"""
        if self.timer.isActive():
            self.timer.stop()
        self.timer.start(milliseconds)
    
    def stop_timer(self):
        """Stop the refresh timer"""
        if self.timer.isActive():
            self.timer.stop()