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
    def __init__(self, graph_widget=None, parent=None, theme_manager=None):
        super().__init__(parent)
        
        # Configurar theme_manager
        if theme_manager is None:
            from utils.theme_manager import theme_manager as tm
            self.theme_manager = tm
        else:
            self.theme_manager = theme_manager
            
        # Configuración inicial
        self.disp = 2  # ID del dispositivo de pH
        self.ph_value = 0
        self.rango_min = 0
        self.rango_max = 14
        
        # Controladores
        self.historial_controller = HistorialController(self.disp)
        self.device_controller = DispositivoController()
        # Pasar el theme_manager a la gráfica
        self.graph_widget = graph_widget if graph_widget else GraphHp(self.theme_manager)
        
        # Cargar datos iniciales
        self.load_config()
        self.load_data()
        
        # Conectar al cambio de tema
        self.theme_manager.theme_changed.connect(self.apply_theme)
        
        # Configurar UI
        self.setup_ui()
        
        # Aplicar tema inicial
        self.apply_theme()
          
        # Configurar timer para actualización automática
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(5000)  # Actualizar cada 5 segundos

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
            last_value = self.historial_controller.get_last()
            if last_value is not None:
                self.ph_value = float(last_value)
            else:
                self.ph_value = 7.0  # Valor neutral por defecto

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
        if hasattr(self, 'summary_panel'):
            self.summary_panel.set_ph_value(self.ph_value)
        if hasattr(self, 'history_panel'):
            self.history_panel.clear_and_update_table(self.historial)
        if self.graph_widget and hasattr(self.graph_widget, 'updateHp'):
            self.graph_widget.updateHp(float(self.ph_value))

    def apply_theme(self):
        """Aplica el tema actual a todos los componentes"""
        colors = self.theme_manager.get_theme_colors()
        
        # Aplicar tema al fondo principal
        main_bg = colors['panel_bg'] if self.theme_manager.is_dark_mode() else "#f5f7fa"
        self.setStyleSheet(f"background-color: {main_bg};")
        
        # Actualizar el panel de la gráfica si ya existe
        if hasattr(self, 'graph_panel'):
            self.update_graph_panel_theme()
    
    def update_graph_panel_theme(self):
        """Actualiza el tema del panel de la gráfica"""
        colors = self.theme_manager.get_theme_colors()
        
        # Aplicar nuevo estilo al panel de la gráfica
        panel_bg = colors['panel_bg']
        self.graph_panel.setStyleSheet(
            f"QFrame {{ background-color: {panel_bg}; border-radius: 12px; border: none; }}"
        )
        
        # Actualizar el color de la sombra según el tema
        if self.theme_manager.is_dark_mode():
            # Sombra más sutil para modo oscuro
            shadow_color = QColor(0, 0, 0, 100)  # Negro semi-transparente
        else:
            # Sombra original para modo claro
            shadow_color = QColor(197, 239, 236)
        
        # Crear nueva sombra con el color apropiado
        graph_shadow = QGraphicsDropShadowEffect()
        graph_shadow.setBlurRadius(15)
        graph_shadow.setColor(shadow_color)
        graph_shadow.setOffset(0, 3)
        self.graph_panel.setGraphicsEffect(graph_shadow)
    
    def setup_ui(self):
        # Layout principal
        self.setMinimumSize(700, 500)
        
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
        self.graph_panel = QFrame()  # Guardar referencia como atributo de instancia
        self.graph_panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph_panel.setMinimumHeight(280)
        self.graph_panel.setFixedHeight(280)
        
        # El estilo se aplicará en apply_theme(), no aquí
        
        graph_layout = QVBoxLayout(self.graph_panel)
        graph_layout.setContentsMargins(15, 15, 15, 15)
        graph_layout.setSpacing(10)
        
        # Configurar la gráfica
        self.graph_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        graph_layout.addWidget(self.graph_widget, 1)
        
        return self.graph_panel
    
    def stop_timer(self):
        """Detiene el timer de actualización"""
        if self.timer.isActive():
            self.timer.stop()    

    def set_ph_value(self, new_value):
        """Actualiza el valor de pH y todos los componentes relacionados"""
        try:
            self.ph_value = float(new_value)
            
            # Actualizar los componentes
            if hasattr(self, 'summary_panel'):
                self.summary_panel.set_ph_value(self.ph_value)
            
            if hasattr(self, 'history_panel'):
                # Agregar el nuevo valor al inicio del historial
                from datetime import datetime
                new_entry = {
                    "fecha_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "valor": self.ph_value
                }
                
                self.historial.insert(0, new_entry)
                if len(self.historial) > 100:
                    self.historial = self.historial[:100]
                self.history_panel.clear_and_update_table(self.historial)
              # No necesitamos actualizar la gráfica aquí ya que se hace en Container.py
                
        except Exception as e:
            print(f"Error al establecer valor de pH: {e}")