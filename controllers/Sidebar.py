from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QLabel,
    QFrame,
    QHBoxLayout,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QPalette, QColor, QIcon
import os
from dotenv import load_dotenv

from PyQt6.QtCore import pyqtSignal


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


load_dotenv()
SHADOW = os.getenv("SHADOW")


class Sidebar(QWidget):
    def __init__(self, content_container):
        super().__init__()
        self.content_container = content_container
        self.buttons = []


        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(228, 250, 249))
        self.setPalette(palette)

        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(20, 10, 20, 10)
        self.sidebar_layout.setSpacing(8)
        self.setLayout(self.sidebar_layout)

        # Logo de la compañía
        self.logo_container = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_container)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)

        # Logo clickeable usando ClickableLabel
        self.logo_label = ClickableLabel()
        pixmap = QPixmap("resources/media/logo_text.png")
        if not pixmap.isNull():
            scaled = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(scaled)
        else:
            print("No se pudo cargar el logo")

        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logo_label.clicked.connect(lambda: self.handle_logo_click())

        self.logo_layout.addWidget(self.logo_label)
        self.logo_layout.addSpacing(15)
        self.sidebar_layout.addWidget(self.logo_container)

        # Categoría: Supervisión
        self.add_category_separator("SUPERVISIÓN")
        self.add_button("Nivel del Agua", "subida-de-agua", "subida-de-agua_w", 1)
        self.add_button("pH del agua", "humedad", "humedad_w", 2)
        self.add_button("Temperatura agua", "calor", "calor_w", 3)
        self.add_button("Conductividad", "tapon-de-agua-circular", "tapon-de-agua-circular_w", 4)
        self.add_button("Ambiente", "temperatura-baja", "temperatura-baja_w", 5)

        # Categoría: Configuración
        self.add_category_separator("CONFIGURACIÓN")
        self.add_button("Contenedores", "botella-de-agua", "botella-de-agua_w", 7)
        self.add_button("Configuración", "engranajes", "engranajes_w", 8)

        # Espaciador final
        self.sidebar_layout.addItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # Al inicio, asegurarse que nada esté seleccionado
        self.clear_button_selection()

    def add_category_separator(self, title):
        separator = QFrame()

        label = QLabel(title)
        label.setStyleSheet(
            """
            color: #666666;
            font-size: 12px;
            font-weight: bold;
            margin-top: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        """
        )

        self.sidebar_layout.addWidget(label)
        self.sidebar_layout.addWidget(separator)

    def add_button(self, text, icon_name, white_icon_name, index):
        button = QPushButton(text)
        button.setIcon(QIcon(f"resources/icons/{icon_name}.png"))
        button.setIconSize(QSize(24, 24))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setCheckable(True)

        button.setStyleSheet("""
            QPushButton {
                background-color: #fff;
                border: none;
                font-size: 14px;
                border-radius: 8px;
                color: #4CA4A5;
                font-weight: 500;  
                padding: 10px 15px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #E4FFF3;
            }
            QPushButton:checked {
                background-color: #4CA4A5;
                color: white;
                font-weight: 600;
            }
            QPushButton {
                padding-right: 15px;
            }
            QPushButton::icon {
                padding-left: 20px;
            }
        """)

        button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 3)
        r, g, b = map(int, SHADOW.split(","))
        shadow.setColor(QColor(r, g, b))
        button.setGraphicsEffect(shadow)

        def on_click():
            self.clear_button_selection()
            button.setChecked(True)
            button.setIcon(QIcon(f"resources/icons/{white_icon_name}.png"))
            self.change_content(index)

        button.clicked.connect(on_click)
        button.icon_default = icon_name
        button.white_icon_name = white_icon_name

        self.sidebar_layout.addWidget(button)
        self.buttons.append(button)

    def clear_button_selection(self):
        for b in self.buttons:
            b.setChecked(False)
            b.setIcon(QIcon(f"resources/icons/{b.icon_default}.png"))

    def handle_logo_click(self):
        self.clear_button_selection()
        self.change_content(0)

    def change_content(self, state_id):
        print(f"Cambiar contenido a estado: {state_id}")
        if hasattr(self.content_container, "set_content_state"):
            self.content_container.set_content_state(state_id)
