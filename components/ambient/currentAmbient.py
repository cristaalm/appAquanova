from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QGraphicsDropShadowEffect,
    QProgressBar,
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


class MarqueeLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.full_text = text + "     "  # Espacio extra para que el texto dé la vuelta
        self.index = 0

        self.setText(self.full_text)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_text)
        self.timer.start(150)  # Menor valor = más rápido

    def scroll_text(self):
        scrolled = self.full_text[self.index:] + self.full_text[:self.index]
        self.setText(scrolled)
        self.index = (self.index + 1) % len(self.full_text)


class CurrentAmbient(QWidget):
    def __init__(self, temperature_value, humidity_value, parent=None):
        super().__init__(parent)

        self.temperature_value = temperature_value
        self.humidity_value = humidity_value

        # Diseño principal vertical
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)

        # Tarjeta de temperatura
        self.temperature_card = self.create_card(
            title="Temperatura actual",
            subtitle="Nivel de calor ambiental.",
            value=f"{self.temperature_value} °C",
            is_temperature=True,
        )
        main_layout.addWidget(self.temperature_card)

        # Tarjeta de humedad
        self.humidity_card = self.create_card(
            title="Humedad actual",
            subtitle="Cantidad de vapor en el aire.",
            value=f"{self.humidity_value} %",
            is_temperature=False,
        )
        main_layout.addWidget(self.humidity_card)

    def create_card(self, title, subtitle, value, is_temperature=False):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setMinimumWidth(220)
        frame.setMaximumWidth(280)
        frame.setMinimumHeight(155)
        frame.setMaximumHeight(155)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """
        )

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

        # Título con ícono
        title_layout = QHBoxLayout()
        title_label = MarqueeLabel(title)
        title_label.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            color: #074e52;
        """
        )
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
            22,
            22,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        corner_icon.setPixmap(corner_pixmap)

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(corner_icon)
        layout.addLayout(title_layout)

        # Subtítulo y valor
        bottom_layout = QHBoxLayout()

        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(
            """
            font-size: 12px;
            font-style: italic;
            color: #6b7280;
        """
        )
        subtitle_label.setWordWrap(True)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        bottom_layout.addWidget(subtitle_label, 1)

        value_container = QHBoxLayout()
        image_label = QLabel()
        image_label.setFixedSize(30, 30)
        image_path = f"{ICONS}thermometer.png" if is_temperature else f"{ICONS}nube.png"
        pixmap = QPixmap(image_path).scaled(
            30,
            30,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        image_label.setPixmap(pixmap)

        value_label = QLabel(value)
        value_label.setStyleSheet(
            """
            font-size: 28px;
            font-weight: bold;
            color: #074e52;
        """
        )
        value_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        value_container.addWidget(image_label)
        value_container.addSpacing(5)
        value_container.addWidget(value_label)
        bottom_layout.addLayout(value_container, 0)

        layout.addLayout(bottom_layout)

        # Etiquetas MÍN y MAX dinámicas según el tipo de card
        if is_temperature:
            min_label_text = "MÍN 0°C"
            max_label_text = "MÁX 50°C"
        else:
            min_label_text = "MÍN 0%"
            max_label_text = "MÁX 100%"

        labels_layout = QHBoxLayout()
        labels_layout.setContentsMargins(0, 0, 0, 0)
        min_label = QLabel(min_label_text)
        min_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        min_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        labels_layout.addWidget(min_label)
        labels_layout.addStretch()
        max_label = QLabel(max_label_text)
        max_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        max_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        labels_layout.addWidget(max_label)
        layout.addLayout(labels_layout)

        # Barra de progreso
        progress_bar = QProgressBar()
        progress_bar.setFixedHeight(12)
        progress_bar.setTextVisible(False)

        num_value = float(value.split()[0])
        if is_temperature:
            percentage = min(max(num_value / 50.0, 0), 1) * 100  # supongamos máximo 50°C
        else:
            percentage = min(max(num_value / 100.0, 0), 1) * 100  # humedad sobre 100%

        progress_bar.setValue(int(percentage))

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

        # Panel de estado dinámico
        status = self.get_status(num_value, is_temperature)

        self.status_chip = QLabel(status)
        self.status_chip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_chip.setStyleSheet("""
            background-color: #c5efeb;
            color: #2b6363;
            border-radius: 15px;
            padding: 6px;
            font-size: 18px;
            font-weight: bold;
        """)
        
        layout.addWidget(self.status_chip)
        layout.addStretch()
        return frame

    def get_status(self, value, is_temperature):
        if is_temperature:
            if value > 30:
                return "ALERTA: Temperatura Alta"
            elif value < 10:
                return "ALERTA: Temperatura Baja"
            else:
                return "Óptima Temperatura"
        else:
            if value > 80:
                return "ALERTA: Humedad Alta"
            elif value < 30:
                return "ALERTA: Humedad Baja"
            else:
                return "Óptima Humedad"
