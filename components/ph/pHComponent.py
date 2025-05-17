from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from controllers.Graphs.Water.pH import GraphHp
from .phSummaryPanel import PhSummaryPanel
from .phHistoryPanel import PhHistoryPanel
from historiales.controllers.HistorialController import HistorialController
from dispositivos.controllers.deviceController import DispositivoController

class phComponent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Configuración inicial
        self.disp = 2  # ID del dispositivo de pH
        self.ph_value = 0
        self.rango_min = 0
        self.rango_max = 14
        
        # Controladores
        self.historial_controller = HistorialController(self.disp)
        self.device_controller = DispositivoController()
        self.graph_widget = GraphHp()
        
        # Cargar datos iniciales
        self.load_config()
        self.load_data()
        
        # Configurar UI
        self.setup_ui()
        
        # Configurar timer para actualización automática
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(10000)  # Actualizar cada 10 segundos
    
    def load_config(self):
        """Carga la configuración del dispositivo"""
        try:
            config = self.device_controller.get_dispositivo(self.disp) or {}
            self.rango_min = float(config.get("valor_minimo", 0))
            self.rango_max = float(config.get("valor_maximo", 14))
        except Exception as e:
            print(f"Error al cargar configuración de pH: {e}")
    
    def load_data(self):
        """Carga los datos del historial desde la base de datos"""
        try:
            self.ph_value = self.historial_controller.get_last() or 0
            registros = self.historial_controller.get_historial()
            if registros:
                self.historial = [
                    {
                        "fecha_ingreso": registro.fecha_ingreso.strftime("%Y-%m-%d %H:%M:%S"),
                        "valor": registro.valor,
                    }
                    for registro in registros
                ]
            else:
                self.historial = []
        except Exception as e:
            print(f"Error al cargar datos de pH: {e}")
            self.historial = []

    def refresh_data(self):
        """Actualiza los datos y la interfaz"""
        try:
            self.load_config()
            self.load_data()
            self.update_ui()
        except Exception as e:
            print(f"Error al actualizar datos de pH: {e}")

    def update_ui(self):
        """Actualiza todos los componentes de la UI con nuevos datos"""
        if self.summary_panel:
            self.summary_panel.set_ph_value(self.ph_value)
        if self.history_panel:
            self.history_panel.clear_and_update_table(self.historial)
    
    def setup_ui(self):
        # Layout principal
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #f5f7fa;")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 0, 20, 0)
        main_layout.setSpacing(15)
        
        # Dos paneles superiores en fila con alturas iguales
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)
        
        # Panel de resumen
        self.summary_panel = PhSummaryPanel()
        self.summary_panel.set_ph_value(self.ph_value)
        top_layout.addWidget(self.summary_panel, 1)
        
        # Panel de gráfico
        top_layout.addWidget(self.create_graph_panel(), 4)
        
        main_layout.addLayout(top_layout, 1)
        
        # Panel de historial con datos reales
        self.history_panel = PhHistoryPanel(historial=self.historial)
        main_layout.addWidget(self.history_panel, 10)
        
        self.setLayout(main_layout)
    
    def create_graph_panel(self):
        # Panel para gráfica de tendencia
        graph_panel = QFrame()
        graph_panel.setFrameShape(QFrame.Shape.StyledPanel)
        graph_panel.setMinimumHeight(280)
        graph_panel.setFixedHeight(280)
        graph_panel.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")
        
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
    
    def stop_timer(self):
        """Detiene el timer de actualización"""
        if self.timer.isActive():
            self.timer.stop()