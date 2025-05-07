from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, 
    QSizePolicy, QFrame, QGraphicsDropShadowEffect,
    QProgressBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPixmap
from utils.LabelMove import MarqueeLabel
import os 
from dotenv import load_dotenv
load_dotenv()
SHADOW = os.getenv("SHADOW")

class CurrentTemp(QWidget):
    QApplication.setStyle("Fusion")
    def __init__(self, value, CE_min, CE_max, rango_max, rango_min):
        super().__init__()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.value = value
        # Rangos de temperatura
        self.CE_max = CE_max
        self.CE_min = CE_min
        self.rango_max = rango_max
        self.rango_min = rango_min
        self.panel = self.create_summary_panel()

    # Función para cargar íconos
    def load(self, path, icon_name, size):
        icon_path = os.path.join(
        self.base_dir,  
        "..",        
        "..",   
        "resources",    
        path,       
        icon_name
        )
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

    def get_status_widget(self):
        # Determinar el estado y el icono correspondiente
        if self.value < self.rango_min:  
            self.status = "Baja"
            icon_name = "tuerca.png"
        elif self.value > self.rango_max:  
            self.status = "Alta"
            icon_name = "tuerca.png"  #CAMBIARRRRRRRRRRRRRRRRRR
        else: 
            self.status = "Optima"
            icon_name = "tuerca.png"

        status_container = QWidget()
        status_container.setStyleSheet("""
            background-color: #c5efeb; 
            border-radius: 15px;
        """)
        
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(10, 6, 10, 6)
        status_layout.setSpacing(5)  
        
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Añadir icono
        icon_label = QLabel()
        status_pixmap = self.load("icons", icon_name, 20)
        if status_pixmap:
            icon_label.setPixmap(status_pixmap)
        else:
            print(f"ERROR: No se pudo cargar el icono: {icon_name}")
        
        icon_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        status_layout.addWidget(icon_label)
        
        # Añadir texto
        text_label = QLabel(self.status)
        text_label.setStyleSheet("""
            color: #2b6363;
            font-size: 18px;
            font-weight: bold;
            background-color: transparent;
        """)
        text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        status_layout.addWidget(text_label)
        
        return status_container

    def scroll_title_text(self, label):
        scrolled = self.title_text[self.title_index:] + self.title_text[:self.title_index]
        label.setText(scrolled)
        self.title_index = (self.title_index + 1) % len(self.title_text)
        
    def create_summary_panel(self):
        self.summary_panel = QFrame()
        self.summary_panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.summary_panel.setMinimumWidth(200)
        self.summary_panel.setMaximumWidth(280)
        self.summary_panel.setMinimumHeight(280)
        self.summary_panel.setFixedHeight(280)
        self.summary_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(197, 239, 236))
        shadow.setOffset(0, 3)
        self.summary_panel.setGraphicsEffect(shadow)
        
        self.summary_layout = QVBoxLayout(self.summary_panel)
        self.summary_layout.setContentsMargins(15, 15, 15, 15)
        self.summary_layout.setSpacing(10)
        
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)

        
        self.title_text = "Conductividad actual"
        self.title_index = 0
        
        self.title_label = MarqueeLabel(self.title_text)
        self.title_label.setStyleSheet("""
            font-size: 22px;
            color: #045859;
            font-weight: bold;                                
        """)
        self.title_label.setMinimumWidth(150)
        self.title_label.setMaximumWidth(200)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        title_layout.addWidget(self.title_label)
        
        title_layout.addStretch()
        
        temp_icon_label = QLabel()
        temp_pixmap = self.load("icons","verdeElecricity.png", 26)
        if temp_pixmap:
            temp_icon_label.setPixmap(temp_pixmap)
        
        title_layout.addWidget(temp_icon_label)
        self.summary_layout.addLayout(title_layout)  
        
        # Subtítulo
        subtitle = QLabel("Registro actual de conductividad elécrica")
        subtitle.setStyleSheet("""
            font-size: 12px;
            font-style: italic;
            color: #6b7280;
        """)
        self.summary_layout.addWidget(subtitle)
        self.summary_layout.addSpacing(2)

        value_layout = QHBoxLayout()
        
        # Ícono del termómetro
        thermometer_icon_label = QLabel()
        thermometer_pixmap = self.load("icons","elecricity.png", 50)
        if thermometer_pixmap:
            thermometer_icon_label.setPixmap(thermometer_pixmap)
        value_layout.addWidget(thermometer_icon_label)
        
        # Valor de la temperatura
        self.value_label = QLabel(f"{self.value}")
        self.value_label.setStyleSheet("""
            font-size: 56px;
            font-weight: bold;
            color: #045859;
            text-align: center;
            margin-right: -3px;
        """)
        value_layout.addWidget(self.value_label)

        unit_label = QLabel("µS/cm")
        unit_label.setStyleSheet("""
            font-size: 24px;
            color: #045859;
            margin-left: -3px;
            margin-top: 20px;
            font-weight: bold;
        """)
        value_layout.addWidget(unit_label)

        self.summary_layout.addLayout(value_layout)

        self.summary_layout.addSpacing(0)

        labels_layout = QHBoxLayout()
        labels_layout.setContentsMargins(0, 0, 0, 0)  

        min_label = QLabel(f" {self.CE_min}µ")
        min_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        min_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        labels_layout.addWidget(min_label)

        labels_layout.addStretch()

        max_label = QLabel(f" {self.CE_max}µ")
        max_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        max_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        labels_layout.addWidget(max_label)

        self.summary_layout.addLayout(labels_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setTextVisible(False)

        # Calcular el porcentaje de temperatura
        CE_porcentage = (self.value - self.CE_min) * 100 / (self.CE_max - self.CE_min)
        self.progress_bar.setValue(int(CE_porcentage))
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #e2e8f0;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background-color: #4CA4A5;
                border-radius: 6px;
            }
        """)

        self.summary_layout.addWidget(self.progress_bar)
        self.summary_layout.addSpacing(20)
        
        # Crear y añadir el widget de estado
        self.status_widget = self.get_status_widget()
        self.summary_layout.addWidget(self.status_widget)
        self.summary_layout.addStretch()
        
        return self.summary_panel
    
    def update_value(self, new_value):
        self.value = new_value
        self.value_label.setText(f"{new_value}")
        
        CE_porcentage = (self.value - self.CE_min) * 100 / (self.CE_max - self.CE_min)
        self.progress_bar.setValue(int(CE_porcentage))
        
        if hasattr(self, 'status_widget'):
            self.summary_layout.removeWidget(self.status_widget)
            self.status_widget.setParent(None)
        
        self.status_widget = self.get_status_widget()
        self.summary_layout.insertWidget(self.summary_layout.count() - 1, self.status_widget)
    
    def resizeEvent(self, event):
        """Manejar cambios de tamaño de la ventana"""
        super().resizeEvent(event)
        
        card_width = self.width()
        
        if card_width < 800:
            # Modo compacto
            self.value_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #045859;")
        else:
            # Modo normal
            self.value_label.setStyleSheet("font-size: 56px; font-weight: bold; color: #045859;")