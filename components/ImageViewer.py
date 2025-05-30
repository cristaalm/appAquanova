from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGraphicsDropShadowEffect,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtGui import QPixmap, QColor, QIcon
from PyQt6.QtCore import Qt, QRect

import os


class ImageViewer(QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)

        # Hacer que cubra toda la ventana principal
        if parent:
            self.setGeometry(parent.rect())
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Capa de fondo semitransparente
        self.background = QWidget(self)
        self.background.setStyleSheet("background-color: rgba(0, 0, 0, 140);")
        self.background.setGeometry(self.rect())

        # Cerrar al dar clic fuera de la imagen
        self.background.mousePressEvent = self.close_on_click_outside

        # Contenedor de la imagen
        self.image_container = QWidget(self)
        self.image_container.setStyleSheet(
            """
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """
        )
        self.image_container.setFixedSize(420, 420)
        self.image_container.move(
            (self.width() - self.image_container.width()) // 2,
            (self.height() - self.image_container.height()) // 2,
        )

        # Sombra
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.image_container.setGraphicsEffect(shadow)

        # Layout de imagen + botón
        layout = QVBoxLayout(self.image_container)
        layout.setContentsMargins(10, 10, 10, 10)

        # Botón X para cerrar
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        close_btn = QPushButton("✖")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                font-size: 16px;
                color: #1e293b;
                border: none;
            }
            QPushButton:hover {
                color: #ef4444;
            }
        """
        )
        close_btn.clicked.connect(self.close)
        top_bar.addWidget(close_btn)
        layout.addLayout(top_bar)

        # Imagen
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(
            pixmap.scaled(
                380,
                380,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        layout.addWidget(self.image_label)

    def close_on_click_outside(self, event):
        # Cierra el visor si se da clic fuera del contenedor de imagen
        cursor_pos = event.globalPosition().toPoint()
        if not self.image_container.geometry().contains(cursor_pos - self.pos()):
            self.close()
