from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy,
    QProgressBar, QGraphicsDropShadowEffect, QWidget
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QPixmap, QColor
from .phConstants import *
import os

class PhSummaryPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ph_value = 6.5
        self.title_text = "Potencial de hidrógeno (pH)   "
        self.title_index = 0
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.setup_ui()
        
    def setup_ui(self):
        # Configuración básica del panel
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumWidth(200)
        self.setMaximumWidth(280)
        self.setMinimumHeight(280)
        self.setFixedHeight(280)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        
        # Aplicar efecto de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(SHADOW_COLOR)
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Título con carrusel
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        # Texto del título con carrusel
        self.title_label = QLabel(self.title_text)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #045859;")
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
        icon_label = QLabel()
        icon_pixmap = QPixmap("./resources/icons/ph_icon.png")
        if not icon_pixmap.isNull():
            icon_label.setPixmap(icon_pixmap.scaled(QSize(30, 30), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            icon_label.setText("○")
            icon_label.setStyleSheet("font-size: 20px; color: #045859;")
        
        header_layout.addWidget(icon_label)
        layout.addLayout(header_layout)
        
        # Descripción
        description_label = QLabel("Monitoreo del nivel de ph del agua")
        description_label.setStyleSheet("font-size: 12px; font-style: italic; color: #6b7280;")
        layout.addWidget(description_label)
        layout.addSpacing(2)
        
        # Valor de pH
        value_container = QHBoxLayout()
        value_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icono antes del valor
        ph_icon_label = QLabel()
        ph_icon_pixmap = QPixmap("./resources/icons/ph_icon.png")
        if not ph_icon_pixmap.isNull():
            ph_icon_label.setPixmap(ph_icon_pixmap.scaled(QSize(55, 55), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            ph_icon_label.setText("○")
            ph_icon_label.setStyleSheet("font-size: 24px; color: #045859;")
        
        value_container.addWidget(ph_icon_label)
        
        # Valor de pH grande
        self.ph_value_label = QLabel(str(self.ph_value))
        self.ph_value_label.setStyleSheet("font-size: 56px; font-weight: bold; color: #045859; text-align: center;")
        value_container.addWidget(self.ph_value_label)

        ph_unit_label = QLabel("ph")
        ph_unit_label.setStyleSheet("font-size: 24px; color: #045859; margin-left: 0px; margin-top: 20px; font-weight: bold;")
        value_container.addWidget(ph_unit_label)
        
        layout.addLayout(value_container)
        layout.addSpacing(5)
        
        # Etiquetas MIN y MAX
        self.add_min_max_labels(layout)
        
        # Barra de progreso
        self.add_progress_bar(layout)
        layout.addSpacing(20)
        
        # Panel de estado con icono y texto
        self.status_container = QWidget()
        self.status_container.setStyleSheet("""
            background-color: #c5efeb; 
            border-radius: 15px;
        """)
        self.status_layout = QHBoxLayout(self.status_container)
        self.status_layout.setContentsMargins(10, 6, 10, 6)
        self.status_layout.setSpacing(5)
        self.status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icono de estado (se actualizará en update_status_chip)
        self.status_icon_label = QLabel()
        self.status_layout.addWidget(self.status_icon_label)
        
        # Texto de estado
        self.status_text_label = QLabel(self.get_ph_status_text())
        self.status_text_label.setStyleSheet("""
            color: #2b6363;
            font-size: 18px;
            font-weight: bold;
            background-color: transparent;
        """)
        self.status_layout.addWidget(self.status_text_label)
        
        # Inicializar el estado
        self.update_status_chip()
        
        layout.addWidget(self.status_container)
        layout.addStretch()
    
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
        min_label = QLabel("MÍN 0")
        min_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        min_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        labels_layout.addWidget(min_label)
        
        # Espaciador
        labels_layout.addStretch()
        
        # Etiqueta MAX
        max_label = QLabel("MÁX 14")
        max_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        max_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        labels_layout.addWidget(max_label)
        
        layout.addLayout(labels_layout)
    
    def add_progress_bar(self, layout):
        progress_bar = QProgressBar()
        progress_bar.setFixedHeight(12)
        progress_bar.setTextVisible(False)
        
        # Calcular el valor en porcentaje (0-100) basado en el rango pH (0-14)
        ph_percent = min(max(self.ph_value / 14.0, 0), 1) * 100
        progress_bar.setValue(int(ph_percent))
        
        progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #e2e8f0;
                border-radius: 6px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #4CA4A5;
                border-radius: 6px;
            }
        """)
        
        layout.addWidget(progress_bar)
    
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
        self.update_status_chip()
    
    def update_status_chip(self):
        status = self.get_ph_status_text()
        self.status_text_label.setText(status)
        container_style = """
            background-color: #c5efeb; 
            border-radius: 15px;
        """
        
        if status == "Bajo":
            icon_name = "acido_status.png"  # Nombre del icono para pH bajo
            text_style = """
                color: #045859;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            """
        elif status == "Alto":
            icon_name = "alcalino_status.png"  # Nombre del icono para pH alto
            text_style = """
                color: #045859;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            """
        else:  # Óptimo
            icon_name = "neutro_status.png"  # Nombre del icono para pH óptimo
            text_style = """
                color: #045859;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            """
        
        # Cargar el icono correspondiente
        status_pixmap = self.load_icon(icon_name, 20)
        if status_pixmap:
            self.status_icon_label.setPixmap(status_pixmap)
        else:
            # Si no se encuentra el icono, usar un respaldo genérico
            # Puedes adaptar esto para usar iconos que sepas que existen
            if status == "Bajo":
                fallback_icon = "warning_icon.png"
            elif status == "Alto":
                fallback_icon = "alert_icon.png"
            else:
                fallback_icon = "check_icon.png"
            
            fallback_pixmap = self.load_icon(fallback_icon, 20)
            if fallback_pixmap:
                self.status_icon_label.setPixmap(fallback_pixmap)
            else:
                # Si aún no hay iconos disponibles, mostrar un texto como respaldo
                self.status_icon_label.setText("●")
                if status == "Bajo":
                    self.status_icon_label.setStyleSheet("color: #92400e; font-size: 16px;")
                elif status == "Alto":
                    self.status_icon_label.setStyleSheet("color: #b91c1c; font-size: 16px;")
                else:
                    self.status_icon_label.setStyleSheet("color: #166534; font-size: 16px;")
        
        # Aplicar estilos
        self.status_container.setStyleSheet(container_style)
        self.status_text_label.setStyleSheet(text_style)