from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPixmap
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()
ICONS = os.getenv("ICONS")
SHADOW = os.getenv("SHADOW")

class CurrentAmbient(QWidget):
    def __init__(self, temperature_value, humidity_value, parent=None):
        super().__init__(parent)

        self.temperature_value = temperature_value
        self.humidity_value = humidity_value

        # Cambiar a diseño vertical
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 20, 0, 20)
        main_layout.setSpacing(20)

        # Card de temperatura (arriba)
        self.temperature_card = self.create_card(
            title="Temperatura actual",
            subtitle="Control de la temperatura en tiempo real",
            value=f"{self.temperature_value} °C",
            is_temperature=True
        )
        main_layout.addWidget(self.temperature_card)

        # Card de humedad (debajo)
        self.humidity_card = self.create_card(
            title="Humedad actual",
            subtitle="Control de la humedad en tiempo real",
            value=f"{self.humidity_value} %",
            is_temperature=False
        )
        main_layout.addWidget(self.humidity_card)


    def create_card(self, title, subtitle, value, is_temperature=False):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setMinimumWidth(220)
        frame.setMaximumWidth(280)
        frame.setStyleSheet("""
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
        frame.setGraphicsEffect(shadow)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Fila: Título + ícono en la esquina
        title_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #074e52;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        corner_icon = QLabel()
        corner_icon.setFixedSize(22, 22)
        if is_temperature:
            timezone = pytz.timezone("America/Mexico_City")
            current_hour = datetime.now(timezone).hour
            icon_path = f"{ICONS}sol.png" if 6 <= current_hour < 19 else f"{ICONS}luna.png"
        else:
            icon_path = f"{ICONS}gota.png"
        corner_pixmap = QPixmap(icon_path).scaled(
            22, 22, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        corner_icon.setPixmap(corner_pixmap)

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(corner_icon)
        layout.addLayout(title_layout)

        # Fila: Descripción (izquierda) y valor con imagen (derecha)
        bottom_layout = QHBoxLayout()

        # Subtítulo (izquierda)
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("""
            font-size: 12px;
            font-style: italic;
            color: #6b7280;
        """)
        subtitle_label.setWordWrap(True)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        bottom_layout.addWidget(subtitle_label, 1)

        # Valor con imagen (derecha)
        value_container = QHBoxLayout()
        image_label = QLabel()
        image_label.setFixedSize(32, 32)
        image_path = f"{ICONS}thermometer.png" if is_temperature else f"{ICONS}nube.png"
        pixmap = QPixmap(image_path).scaled(
            32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        image_label.setPixmap(pixmap)

        value_label = QLabel(value)
        value_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #074e52;
        """)
        value_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        value_container.addWidget(image_label)
        value_container.addSpacing(5)
        value_container.addWidget(value_label)
        bottom_layout.addLayout(value_container, 0)

        layout.addLayout(bottom_layout)

        return frame
