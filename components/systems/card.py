from PyQt6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt
import os
from dotenv import load_dotenv

load_dotenv()
SHADOW = os.getenv("SHADOW")
MEDIA = os.getenv("MEDIA")

class Card(QWidget):
    def __init__(self, trade_name, legal_name, logo_path, parent=None):
        super().__init__(parent)

        self.setFixedHeight(120)

        # Layout principal
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 20, 10, 20)

        # Frame con sombra
        frame = QFrame()
        frame.setStyleSheet("background-color: white; border-radius: 12px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        r, g, b = map(int, SHADOW.split(","))
        shadow.setColor(QColor(r, g, b))
        shadow.setOffset(4, 4)
        frame.setGraphicsEffect(shadow)

        frame_layout = QHBoxLayout(frame)
        frame_layout.setContentsMargins(15, 5, 15, 5)  # Añadir margen interno horizontal

        # Logo (izquierda)
        logo_label = QLabel()
        logo_label.setFixedSize(80, 80)
        logo = f"{MEDIA}{logo_path}"
        pixmap = QPixmap(logo).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        frame_layout.addWidget(logo_label)

        # Espacio entre logo y texto
        frame_layout.addSpacing(10)

        # Info (centro, alineado verticalmente)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Nombre comercial
        trade_label = QLabel(trade_name)
        trade_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        trade_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info_layout.addWidget(trade_label)

        # Razón social
        legal_label = QLabel(legal_name)
        legal_label.setStyleSheet("font-size: 14px; color: #777; font-style: italic;")
        legal_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info_layout.addWidget(legal_label)

        frame_layout.addLayout(info_layout)

        main_layout.addWidget(frame)
