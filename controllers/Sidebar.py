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

# Importar el theme manager
from utils.theme_manager import theme_manager


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

        # Conectar al sistema de temas
        theme_manager.theme_changed.connect(self.apply_theme)

        self.setAutoFillBackground(True)
        
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

        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logo_label.clicked.connect(lambda: self.handle_logo_click())

        self.logo_layout.addWidget(self.logo_label)
        self.logo_layout.addSpacing(5)
        self.sidebar_layout.addWidget(self.logo_container)

        # Categoría: Supervisión
        self.supervision_label = self.add_category_separator("SUPERVISIÓN")
        
        # Mapeo de id a seccion, nombre, iconos
        secciones = {
            4: ("Temperatura del agua", "calor", "calor_w", 1),
            5: ("Nivel del agua", "subida-de-agua", "subida-de-agua_w", 3),
            2: ("pH del agua", "humedad", "humedad_w", 2),
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
        self.config_label = self.add_category_separator("CONFIGURACIÓN")
        self.add_button("Dispositivos", "engranajes", "engranajes_w", 6)

        # Espaciador final
        self.sidebar_layout.addItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # Al inicio, asegurarse que nada esté seleccionado
        self.clear_button_selection()
        
        # Aplicar tema inicial
        self.apply_theme(theme_manager.current_theme)

    def create_theme_toggle(self):
        """Crea el botón de alternancia de tema"""
        # Container para el botón de tema
        theme_container = QWidget()
        theme_layout = QHBoxLayout(theme_container)
        theme_layout.setContentsMargins(0, 10, 0, 15)
        
        # Botón de alternancia
        self.theme_toggle_btn = QPushButton()
        self.theme_toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        
        # Configurar texto inicial
        self.update_theme_button_text()
        
        theme_layout.addStretch()
        theme_layout.addWidget(self.theme_toggle_btn)
        theme_layout.addStretch()

    def update_theme_button_text(self):
        """Actualiza el texto del botón de tema"""
        if theme_manager.is_dark_mode():
            self.theme_toggle_btn.setText("☀️ CLARO")
        else:
            self.theme_toggle_btn.setText("🌙 OSCURO")

    def toggle_theme(self):
        """Alterna entre modo claro y oscuro"""
        theme_manager.toggle_theme()
        self.update_theme_button_text()

    def apply_theme(self, theme_name):
        """Aplica el tema actual a todos los elementos"""
        colors = theme_manager.get_theme_colors()
        
        # Aplicar color de fondo al sidebar
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(colors['sidebar_bg']))
        self.setPalette(palette)
        
        # Aplicar estilos a las etiquetas de categoría
        if hasattr(self, 'supervision_label'):
            self.supervision_label.setStyleSheet(theme_manager.get_category_label_stylesheet())
        if hasattr(self, 'config_label'):
            self.config_label.setStyleSheet(theme_manager.get_category_label_stylesheet())
        
        # Aplicar estilos al botón de tema
        if hasattr(self, 'theme_toggle_btn'):
            self.theme_toggle_btn.setStyleSheet(theme_manager.get_theme_toggle_stylesheet())
        
        # Aplicar estilos a todos los botones
        for button in self.buttons:
            button.setStyleSheet(theme_manager.get_button_stylesheet())
            
        # Actualizar iconos según el estado de selección
        self.update_button_icons()

    def add_category_separator(self, title):
        separator = QFrame()

        label = QLabel(title)
        # El estilo se aplicará en apply_theme()
        
        self.sidebar_layout.addWidget(label)
        self.sidebar_layout.addWidget(separator)
        
        return label  # Retornar la etiqueta para poder aplicar estilos después

    def add_button(self, text, icon_name, white_icon_name, index):
        button = QPushButton(text)
        button.setIcon(QIcon(f"resources/icons/{icon_name}.png"))
        button.setIconSize(QSize(24, 24))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setCheckable(True)

        # El estilo se aplicará en apply_theme()
        button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Sombra (solo en modo claro)
        self.update_button_shadow(button)

        def on_click():
            self.clear_button_selection()
            button.setChecked(True)
            self.update_button_icons()
            self.change_content(index)

        button.clicked.connect(on_click)
        button.icon_default = icon_name
        button.white_icon_name = white_icon_name

        self.sidebar_layout.addWidget(button)
        self.buttons.append(button)

    def update_button_shadow(self, button):
        """Actualiza la sombra del botón según el tema"""
        if not theme_manager.is_dark_mode() and SHADOW:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setOffset(0, 3)
            r, g, b = map(int, SHADOW.split(","))
            shadow.setColor(QColor(r, g, b))
            button.setGraphicsEffect(shadow)
        else:
            button.setGraphicsEffect(None)

    def update_button_icons(self):
        """Actualiza los iconos de todos los botones según su estado"""
        for button in self.buttons:
            if button.isChecked():
                button.setIcon(QIcon(f"resources/icons/{button.white_icon_name}.png"))
            else:
                button.setIcon(QIcon(f"resources/icons/{button.icon_default}.png"))

    def clear_button_selection(self):
        for b in self.buttons:
            b.setChecked(False)
        self.update_button_icons()

    def handle_logo_click(self):
        self.clear_button_selection()
        if (self.get_content_state() != 1):
            self.change_content(1)

    def change_content(self, state_id):
        if hasattr(self.content_container, "set_content_state"):
            self.content_container.set_content_state(state_id)

    def get_content_state(self):
        return self.content_container.content_state