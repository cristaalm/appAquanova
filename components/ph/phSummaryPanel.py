from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy,
    QProgressBar, QGraphicsDropShadowEffect, QWidget
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QPixmap, QColor
from .phConstants import *
from utils.theme_manager import theme_manager  # Importar el theme manager
import os

class PhSummaryPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ph_value = 6.5
        self.title_text = "Potencial de hidrógeno (pH)   "
        self.title_index = 0
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Conectar al cambio de tema
        theme_manager.theme_changed.connect(self.update_theme)
        
        self.setup_ui()
        self.update_theme()  # Aplicar tema inicial
        
    def setup_ui(self):
        # Configuración básica del panel
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumWidth(200)
        self.setMaximumWidth(280)
        self.setMinimumHeight(280)
        self.setFixedHeight(280)
        
        # Aplicar efecto de sombra
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setOffset(0, 3)
        self.setGraphicsEffect(self.shadow)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Título con carrusel
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        # Texto del título con carrusel
        self.title_label = QLabel(self.title_text)
        self.title_label.setMinimumWidth(150)
        self.title_label.setMaximumWidth(200)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Iniciar el temporizador para el efecto de carrusel
        self.title_timer = QTimer()
        self.title_timer.timeout.connect(lambda: self.scroll_title_text())
        self.title_timer.start(150)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        # Icono al lado del título
        self.icon_label = QLabel()
        icon_pixmap = QPixmap("./resources/icons/ph-metro.png")
        if not icon_pixmap.isNull():
            self.icon_label.setPixmap(icon_pixmap.scaled(QSize(28, 28), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.icon_label.setText("○")
        
        header_layout.addWidget(self.icon_label)
        layout.addLayout(header_layout)
        
        # Descripción
        self.description_label = QLabel("Monitoreo del nivel de ph del agua")
        layout.addWidget(self.description_label)
        layout.addSpacing(2)
        
        # Valor de pH
        value_container = QHBoxLayout()
        value_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icono antes del valor
        self.ph_icon_label = QLabel()
        ph_icon_pixmap = QPixmap("./resources/icons/ph_icon.png")
        if not ph_icon_pixmap.isNull():
            self.ph_icon_label.setPixmap(ph_icon_pixmap.scaled(QSize(55, 55), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.ph_icon_label.setText("○")
        
        value_container.addWidget(self.ph_icon_label)
        
        # Valor de pH grande
        self.ph_value_label = QLabel(str(self.ph_value))
        value_container.addWidget(self.ph_value_label)

        self.ph_unit_label = QLabel("ph")
        value_container.addWidget(self.ph_unit_label)
        
        layout.addLayout(value_container)
        layout.addSpacing(5)
        
        # Etiquetas MIN y MAX
        self.add_min_max_labels(layout)
        
        # Barra de progreso
        self.add_progress_bar(layout)
        layout.addSpacing(20)
        
        # Panel de estado con icono y texto
        self.status_container = QWidget()
        self.status_layout = QHBoxLayout(self.status_container)
        self.status_layout.setContentsMargins(10, 6, 10, 6)
        self.status_layout.setSpacing(5)
        self.status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icono de estado (se actualizará en update_status_chip)
        self.status_icon_label = QLabel()
        self.status_layout.addWidget(self.status_icon_label)
        
        # Texto de estado
        self.status_text_label = QLabel(self.get_ph_status_text())
        self.status_layout.addWidget(self.status_text_label)
        
        # Inicializar el estado
        self.update_status_chip()
        
        layout.addWidget(self.status_container)
        layout.addStretch()
    
    def update_theme(self):
        """Actualiza los estilos según el tema actual"""
        if theme_manager.is_dark_mode():
            # Solo aplicar cambios en modo oscuro
            colors = theme_manager.get_theme_colors()
            
            # Estilo del panel principal para modo oscuro
            panel_style = f"""
                QFrame {{
                    background-color: {colors['panel_bg']};
                    border-radius: 12px;
                    border: none;
                }}
            """
            self.setStyleSheet(panel_style)
            
            # Sombra más intensa para modo oscuro
            shadow_color = QColor(0, 0, 0, 80)
            self.shadow.setColor(shadow_color)
            
            # Estilos para modo oscuro
            title_style = f"font-size: 22px; font-weight: bold; color: #FFFFFF;"
            self.title_label.setStyleSheet(title_style)
            
            icon_style = f"font-size: 20px; color: {colors['accent']};"
            if self.icon_label.pixmap() is None:
                self.icon_label.setStyleSheet(icon_style)
            
            description_style = f"font-size: 12px; font-style: italic; color: {colors['text_secondary']};"
            self.description_label.setStyleSheet(description_style)
            
            ph_icon_style = f"font-size: 24px; color: {colors['accent']};"
            if self.ph_icon_label.pixmap() is None:
                self.ph_icon_label.setStyleSheet(ph_icon_style)
            
            ph_value_style = f"font-size: 56px; font-weight: bold; color: {colors['text_primary']}; text-align: center;"
            self.ph_value_label.setStyleSheet(ph_value_style)
            
            ph_unit_style = f"font-size: 24px; color: {colors['text_primary']}; margin-left: 0px; margin-top: 20px; font-weight: bold;"
            self.ph_unit_label.setStyleSheet(ph_unit_style)
            
            # Actualizar estilos de MIN/MAX labels para modo oscuro
            self.update_min_max_styles(colors)
            
            # Actualizar la barra de progreso para modo oscuro
            self.update_progress_bar_style(colors)
        else:
            # Modo claro: usar estilos originales
            panel_style = """
                QFrame {
                    background-color: white;
                    border-radius: 12px;
                    border: none;
                }
            """
            self.setStyleSheet(panel_style)
            
            # Sombra suave para modo claro (original)
            shadow_color = SHADOW_COLOR if 'SHADOW_COLOR' in globals() else QColor(0, 0, 0, 30)
            self.shadow.setColor(shadow_color)
            
            # Estilos originales del modo claro
            self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #045859;")
            
            if self.icon_label.pixmap() is None:
                self.icon_label.setStyleSheet("font-size: 20px; color: #045859;")
            
            self.description_label.setStyleSheet("font-size: 12px; font-style: italic; color: #6b7280;")
            
            if self.ph_icon_label.pixmap() is None:
                self.ph_icon_label.setStyleSheet("font-size: 24px; color: #045859;")
            
            self.ph_value_label.setStyleSheet("font-size: 56px; font-weight: bold; color: #045859; text-align: center;")
            self.ph_unit_label.setStyleSheet("font-size: 24px; color: #045859; margin-left: 0px; margin-top: 20px; font-weight: bold;")
            
            # Estilos originales MIN/MAX
            for child in self.findChildren(QLabel):
                if child.text() == "MÍN 0" or child.text() == "MÁX 14":
                    child.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
            
            # Estilo original de la barra de progreso
            progress_bar = self.findChild(QProgressBar)
            if progress_bar:
                progress_style = """
                    QProgressBar {
                        background-color: #e2e8f0;
                        border-radius: 6px;
                        border: none;
                    }
                    QProgressBar::chunk {
                        background-color: #4CA4A5;
                        border-radius: 6px;
                    }
                """
                progress_bar.setStyleSheet(progress_style)
        
        # Actualizar el chip de estado
        self.update_status_chip()
    
    def update_min_max_styles(self, colors):
        """Actualiza los estilos de las etiquetas MIN y MAX"""
        min_max_style = f"font-size: 14px; color: {colors['text_primary']}; font-weight: bold;"
        
        # Encontrar y actualizar las etiquetas MIN y MAX
        for child in self.findChildren(QLabel):
            if child.text() == "MÍN 0" or child.text() == "MÁX 14":
                child.setStyleSheet(min_max_style)
    
    def update_progress_bar_style(self, colors):
        """Actualiza el estilo de la barra de progreso"""
        # Encontrar la barra de progreso
        progress_bar = self.findChild(QProgressBar)
        if progress_bar:
            # Color de fondo de la barra según el tema
            bg_color = colors['surface'] if theme_manager.is_dark_mode() else "#e2e8f0"
            
            progress_style = f"""
                QProgressBar {{
                    background-color: {bg_color};
                    border-radius: 6px;
                    border: none;
                }}
                QProgressBar::chunk {{
                    background-color: {colors['accent']};
                    border-radius: 6px;
                }}
            """
            progress_bar.setStyleSheet(progress_style)
    
    def load_icon(self, icon_name, size):
        """Función para cargar iconos desde la carpeta de recursos"""
        icon_path = f"./resources/icons/{icon_name}"
        if os.path.exists(icon_path):
            return QPixmap(icon_path).scaled(
                size, 
                size, 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        else:
            print(f"Error: No se encontró el ícono en {icon_path}")
            return None
    
    def scroll_title_text(self):
        scrolled = self.title_text[self.title_index:] + self.title_text[:self.title_index]
        self.title_label.setText(scrolled)
        self.title_index = (self.title_index + 1) % len(self.title_text)
    
    def add_min_max_labels(self, layout):
        labels_layout = QHBoxLayout()
        
        # Etiqueta MIN
        self.min_label = QLabel("MÍN 0")
        self.min_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        labels_layout.addWidget(self.min_label)
        
        # Espaciador
        labels_layout.addStretch()
        
        # Etiqueta MAX
        self.max_label = QLabel("MÁX 14")
        self.max_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        labels_layout.addWidget(self.max_label)
        
        layout.addLayout(labels_layout)
    
    def add_progress_bar(self, layout):
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setTextVisible(False)
        
        # Calcular el valor en porcentaje (0-100) basado en el rango pH (0-14)
        ph_percent = min(max(self.ph_value / 14.0, 0), 1) * 100
        self.progress_bar.setValue(int(ph_percent))
        
        layout.addWidget(self.progress_bar)
    
    def get_ph_status_text(self):
        ph_value = float(self.ph_value)
        if ph_value < PH_MIN_OPTIMAL_INDICATOR:
            return "Ácido"
        elif ph_value > PH_MAX_OPTIMAL_INDICATOR:
            return "Alcalino"
        else:
            return "Óptimo"
    
    def set_ph_value(self, new_value):
        self.ph_value = float(new_value)
        self.ph_value_label.setText(str(self.ph_value))
        
        # Actualizar la barra de progreso
        ph_percent = min(max(self.ph_value / 14.0, 0), 1) * 100
        self.progress_bar.setValue(int(ph_percent))
        
        self.update_status_chip()
    
    def update_status_chip(self):
        """Actualiza el chip de estado con colores apropiados para el tema"""
        status = self.get_ph_status_text()
        self.status_text_label.setText(status)
        
        # Colores del chip según el tema
        if theme_manager.is_dark_mode():
            # Modo oscuro
            chip_bg = "#c5efeb"  # Color claro 
            text_color = "#2b6363"  # Texto blanco
        else:
            # Modo claro: colores originales
            chip_bg = "#c5efeb"
            text_color = "#2b6363"
        
        # Iconos según el estado
        if status == "Ácido":
            icon_name = "acido_status.png"
        elif status == "Alcalino":
            icon_name = "alcalino_status.png"
        else:  # Óptimo
            icon_name = "neutro_status.png"
        
        # Aplicar estilos al contenedor
        container_style = f"""
            background-color: {chip_bg}; 
            border-radius: 15px;
        """
        
        # Aplicar estilos al texto
        text_style = f"""
            color: {text_color};
            font-size: 18px;
            font-weight: bold;
            background-color: transparent;
        """
        
        # Cargar el icono correspondiente
        status_pixmap = self.load_icon(icon_name, 20)
        if status_pixmap:
            self.status_icon_label.setPixmap(status_pixmap)
        else:
            # Respaldo con texto coloreado
            self.status_icon_label.setText("●")
            self.status_icon_label.setStyleSheet(f"color: {text_color}; font-size: 16px; background-color: transparent;")
        
        # Aplicar estilos
        self.status_container.setStyleSheet(container_style)
        self.status_text_label.setStyleSheet(text_style)