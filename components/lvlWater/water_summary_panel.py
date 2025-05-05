from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QProgressBar, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QColor, QPixmap
import os


class WaterSummaryPanel(QFrame):
    def __init__(self, water_value=35, water_min=0, water_max=50, parent=None):
        super().__init__(parent)
        self.water_value = water_value
        self.water_min = water_min
        self.water_max = water_max
        self.setup_ui()

    def setup_ui(self):
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
        
        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(197, 239, 236))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Título carrusel
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        self.title_text = "Capacidad disponible de agua      "
        self.title_index = 0

        self.title_label = QLabel(self.title_text)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #045859;")
        self.title_label.setMinimumWidth(150)
        self.title_label.setMaximumWidth(200)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.title_timer = QTimer()
        self.title_timer.timeout.connect(self.scroll_title_text)
        self.title_timer.start(150)

        header_layout.addWidget(self.title_label)

        header_icon = QLabel()
        pixmap = QPixmap("./resources/icons/botella-de-agua.png")
        if not pixmap.isNull():
            header_icon.setPixmap(pixmap.scaled(QSize(28, 28), Qt.AspectRatioMode.KeepAspectRatio))
        header_layout.addWidget(header_icon)

        layout.addLayout(header_layout)

        # Descripción
        description_label = QLabel("Estado de almacenamiento")
        description_label.setStyleSheet("font-size: 12px; font-style: italic; color: #6b7280;")
        layout.addWidget(description_label)

        # Contenedor horizontal para íconos y valores
        value_container = QHBoxLayout()
        value_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_container.setSpacing(4)  # Espacio entre elementos
        value_container.setContentsMargins(0, 0, 0, 0)

        # Ruta correcta a la imagen de gota rellena
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../resources/icons/icon_water.png")

        # Icono de gota rellena
        water_icon_label = QLabel()
        water_icon_pixmap = QPixmap(icon_path)

        if not water_icon_pixmap.isNull():
            water_icon_label.setPixmap(
                water_icon_pixmap.scaled(QSize(60, 60), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            )
        else:
            water_icon_label.setText("○")
            water_icon_label.setStyleSheet("font-size: 24px; color: #045859;")

        # Lo bajamos un poco para alinearlo mejor con el número
        water_icon_label.setContentsMargins(0, 6, 0, 0)
        value_container.addWidget(water_icon_label)

        # Icono de estado
        self.state_icon_label = QLabel()
        self.state_icon_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.state_icon_label.setContentsMargins(0, 8, 0, 0)  # Lo bajamos un poco
        value_container.addWidget(self.state_icon_label)

        # Valor numérico
        self.water_value_label = QLabel(str(self.water_value))
        self.water_value_label.setStyleSheet("font-size: 56px; font-weight: bold; color: #045859; text-align: center;")
        self.water_value_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.water_value_label.setContentsMargins(0, 0, 0, 0)
        value_container.addWidget(self.water_value_label)

        # Unidad (cm)
        unit_label = QLabel("cm")
        unit_label.setStyleSheet("font-size: 24px; color: #045859; margin-left: 0px; margin-top: 20px; font-weight: bold;")
        unit_label.setContentsMargins(0, 6, 0, 0)  # Lo bajamos un poco
        unit_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        value_container.addWidget(unit_label)

        # Agregar al layout principal
        layout.addLayout(value_container)

        # Etiquetas MIN y MAX
        labels_layout = QHBoxLayout()
        min_label = QLabel("MÍN 0 CM")
        min_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        min_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        labels_layout.addWidget(min_label)
        labels_layout.addStretch()
        max_label = QLabel("MÁX 50 CM")
        max_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        max_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        labels_layout.addWidget(max_label)
        layout.addLayout(labels_layout)

        # Barra con ícono dinámico encima
        percent = min(max(self.water_value / self.water_max, self.water_min), 1) * 100

        progress_container = QWidget()
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(0)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(int(percent))
        self.progress_bar.setStyleSheet("""
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
        progress_layout.addWidget(self.progress_bar)

        layout.addWidget(progress_container)
        layout.addSpacing(20)

        # Chip de estado
        self.status_chip_container = QWidget()
        self.status_chip_container.setStyleSheet("""
            background-color: #c5efeb; 
            border-radius: 15px;
        """)
        chip_layout = QHBoxLayout(self.status_chip_container)
        chip_layout.setContentsMargins(10, 6, 10, 6)
        chip_layout.setSpacing(5)
        chip_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_icon = QLabel()
        self.status_icon.setFixedSize(24, 24)
        chip_layout.addWidget(self.status_icon)

        self.status_text = QLabel("")
        self.status_text.setStyleSheet("""
            color: #2b6363;
            font-size: 18px;
            font-weight: bold;
            background-color: transparent;
        """)
        chip_layout.addWidget(self.status_text)

        layout.addWidget(self.status_chip_container)

        # Actualiza íconos y estado textual al iniciar
        self.update_status_chip()
        self.update_state_icon(self.get_water_status())

    def scroll_title_text(self):
        scrolled = self.title_text[self.title_index:] + self.title_text[:self.title_index]
        self.title_label.setText(scrolled)
        self.title_index = (self.title_index + 1) % len(self.title_text)

    def set_water_value(self, new_value):
        self.water_value = float(new_value)
        self.water_value_label.setText(str(self.water_value))
        self.progress_bar.setValue(min(max(self.water_value / self.water_max, self.water_min), 1) * 100)
        estado = self.get_water_status()
        self.status_text.setText(estado)

        self.status_chip_container.setStyleSheet(f"""
            background-color: {self.get_status_bg_color(estado)};
            border-radius: 15px;
        """)

        self.status_text.setStyleSheet(f"""
            color: {self.get_status_fg_color(estado)};
            font-size: 18px;
            font-weight: bold;
        """)

        self.status_icon.setPixmap(QPixmap(self.get_status_icon_path(estado)).scaled(
            24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))

        self.update_state_icon(self.get_water_status())

    def get_water_status(self):
        if self.water_value < 20:
            return "Bajo"
        elif self.water_value > 40:
            return "Alto"
        else:
            return "Óptimo"

    def update_status_chip(self):
        status = self.get_water_status()
        self.status_text.setText(status)

        if status == "Bajo":
            icon_name = "low-water.png"
            text_style = """
                color: #045859;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            """
        elif status == "Alto":
            icon_name = "overflow-water.png"
            text_style = """
                color: #045859;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            """
        else:
            icon_name = "optimal-water.png"
            text_style = """
                color: #045859;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            """

        icon_path = f"./resources/icons/{icon_name}"
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path).scaled(QSize(24, 24), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.status_icon.setPixmap(pixmap)
        else:
            self.status_icon.setText("●")

        self.status_text.setStyleSheet(text_style)

    def get_status_icon_path(self, estado):
        if estado == "Bajo":
            return "./resources/icons/low-water.png"
        elif estado == "Óptimo":
            return "./resources/icons/optimal-water.png"
        elif estado == "Alto":
            return "./resources/icons/overflow-water.png"
        return ""

    def get_status_bg_color(self, estado):
        if estado == "Bajo":
            return "#fef3c7"
        elif estado == "Óptimo":
            return "#dcfce7"
        elif estado == "Alto":
            return "#fee2e2"
        return "#c5efeb"

    def get_status_fg_color(self, estado):
        if estado == "Bajo":
            return "#92400e"
        elif estado == "Óptimo":
            return "#166534"
        elif estado == "Alto":
            return "#b91c1c"
        return "#2b6363"

    def update_state_icon(self, estado):
        if estado == "Bajo":
            pixmap = QPixmap("./resources/icons/low-water.png")
        elif estado == "Óptimo":
            pixmap = QPixmap("./resources/icons/optimal-water.png")
        elif estado == "Alto":
            pixmap = QPixmap("./resources/icons/overflow-water.png")
        else:
            pixmap = QPixmap()

        self.state_icon_label.setPixmap(pixmap.scaled(55, 55, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def get_status_style(self):
        status = self.get_water_status()
        if status == "Bajo":
            return "background-color: #fef3c7; color: #92400e; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"
        elif status == "Alto":
            return "background-color: #fee2e2; color: #b91c1c; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"
        else:  # Óptimo
            return "background-color: #dcfce7; color: #166534; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"