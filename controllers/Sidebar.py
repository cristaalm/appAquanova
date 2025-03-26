from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QColor, QIcon
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QHBoxLayout


class Sidebar(QWidget):
    def __init__(self, content_container):
        super().__init__()
        self.content_container = content_container

        # Configurar el fondo claro
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)  # Aumentar márgenes
        self.sidebar_layout.setSpacing(8)
        self.setLayout(self.sidebar_layout)

        # Logo y nombre de la compañía - Sección ampliada
        self.logo_container = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_container)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(10)

        # Logo más grande (64x64)
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap("media/logo.png").scaled(
            80,
            80,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Nombre de la compañía con estilo mejorado
        self.company_name_label = QLabel("AQUA NOVA")
        self.company_name_label.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #4da5a6; margin-top: 5px;"
        )
        self.company_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_layout.addWidget(self.logo_label)
        self.logo_layout.addWidget(self.company_name_label)

        # Añadir espacio después del logo
        self.logo_layout.addSpacing(15)

        # Añadir el contenedor del logo al layout principal
        self.sidebar_layout.addWidget(self.logo_container)

        # Categoría: Agua
        self.add_category_separator("AGUA")
        self.add_button("Nivel del Agua", "subida-de-agua", 1)
        self.add_button("pH del agua", "humedad", 2)
        self.add_button("Temperatura agua", "calor", 3)
        self.add_button("Conductividad", "tapon-de-agua-circular", 4)

        # Categoría: Ambiente
        self.add_category_separator("AMBIENTE")
        self.add_button("Temperatura", "temperatura-baja", 5)
        self.add_button("Humedad", "humedad1", 6)

        # Categoría: Configuración
        self.add_category_separator("CONFIGURACIÓN")
        self.add_button("Contenedores", "botella-de-agua", 7)
        self.add_button("Configuración", "engranajes", 8)

        # Espaciador final
        self.sidebar_layout.addItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

    def add_category_separator(self, title):
        """Añade un separador de categoría con título"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("color: #d0d0d0; margin: 15px 0 8px 0;")

        label = QLabel(title)
        label.setStyleSheet(
            """
            color: #666666;
            font-size: 12px;
            font-weight: bold;
            margin-top: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        """
        )

        self.sidebar_layout.addWidget(label)
        self.sidebar_layout.addWidget(separator)

    def add_button(self, text, icon_name, state):
        """Añade un botón con ícono al sidebar con espacio justificado entre icono y texto"""
        button = QPushButton()
        button.setMinimumHeight(45)

        # Crear un widget contenedor para el layout personalizado
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(
            15, 0, 15, 0
        )  # Márgenes izquierdo y derecho
        container_layout.setSpacing(15)  # Espacio entre icono y texto

        # Cargar ícono (si existe)
        icon_label = QLabel()
        try:
            icon = QPixmap(f"icons/{icon_name}.png").scaled(
                24,
                24,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            icon_label.setPixmap(icon)
        except:
            icon_label.setFixedWidth(0)  # Si no hay icono, ocultar espacio

        # Texto del botón
        text_label = QLabel(text)
        text_label.setStyleSheet("font-size: 14px; color: #333333;")

        # Espaciador para empujar el texto hacia la izquierda
        spacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        # Añadir elementos al layout
        container_layout.addWidget(text_label, 0, Qt.AlignmentFlag.AlignLeft)
        container_layout.addSpacerItem(spacer)
        container_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignLeft)

        # Configurar el widget contenedor como el widget del botón
        button.setLayout(container_layout)

        # Estilo del botón
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                margin: 4px 0;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #e8e8e8;
            }
            QPushButton:focus {
                border: 1px solid #2c7be5;
            }
            """
        )

        button.clicked.connect(lambda: self.content_container.set_content_state(state))
        self.sidebar_layout.addWidget(button)
