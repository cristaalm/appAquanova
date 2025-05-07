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
from dispositivos.controllers.deviceController import DispositivoController

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
            scaled = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(scaled)
        else:
            print("No se pudo cargar el logo")

        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logo_label.clicked.connect(lambda: self.handle_logo_click())

        self.logo_layout.addWidget(self.logo_label)
        self.logo_layout.addSpacing(5)
        self.sidebar_layout.addWidget(self.logo_container)

        # Categoría: Supervisión
        self.add_category_separator("SUPERVISIÓN")
        # Mapeo de id a seccion, nombre, iconos
        secciones = {
            5: ("Nivel del agua", "subida-de-agua", "subida-de-agua_w", 1),
            2: ("pH del agua", "humedad", "humedad_w", 2),
            4: ("Temperatura del agua", "calor", "calor_w", 3),
            1: ("Conductividad eléctrica", "tapon-de-agua-circular", "tapon-de-agua-circular_w", 4),
            3: ("Ambiente", "temperatura-baja", "temperatura-baja_w", 5),
        }
        # Instancia el controlador y consulta dispositivos activos
        try:
            from dispositivos.models import Dispositivo
            dispositivos_activos = Dispositivo.objects.filter(estado=1)
        except Exception as e:
            print(f"Error al consultar dispositivos activos: {e}")
            dispositivos_activos = []
        # Solo agrega botones de dispositivos activos, respetando el orden de 'secciones'
        ids_dispositivos_activos = set(d.id_dispositivo for d in dispositivos_activos)
        for id_disp, (nombre, icono, icono_w, id_seccion) in secciones.items():
            if id_disp in ids_dispositivos_activos:
                self.add_button(nombre, icono, icono_w, id_seccion)
        # Categoría: Configuración
        self.add_category_separator("CONFIGURACIÓN")
        self.add_button("Dispositivos", "engranajes", "engranajes_w", 6)

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
                border-radius: 8px;
                border: none;
                color: #4CA4A5;
                font-size: 14px;
                font-weight: 500;  
                padding-left: 15px;
                padding: 10px 15px;
                text-align: left;
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
        if hasattr(self.content_container, "set_content_state"):
            self.content_container.set_content_state(state_id)
