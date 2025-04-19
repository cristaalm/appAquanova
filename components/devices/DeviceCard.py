from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGraphicsDropShadowEffect,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QColor
from .DeviceOptions import DeviceOptions
import utils.LabelMove as MarqueeLabel
from components.ImageViewer import ImageViewer

import os
from dotenv import load_dotenv

load_dotenv()
MEDIA = os.getenv("MEDIA")


class DeviceCard(QFrame):
    def __init__(self, notification, device_data, parent=None):
        super().__init__(parent)
        self.device_data = device_data
        self.notification = notification
        self._setup_frame()
        self._setup_layout()

    def _setup_frame(self):
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(
            """
            QFrame {
                background-color: #f8fafc;
                border-radius: 12px;
                border: none;
            }

            QLabel {
                color: #1e293b;
                font-size: 14px;
            }

            QSpinBox, QDoubleSpinBox {
                background-color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 14px;
                color: #0f172a;
            }

            QSpinBox::up-button,
            QSpinBox::down-button,
            QDoubleSpinBox::up-button,
            QDoubleSpinBox::down-button {
                width: 0;
                height: 0;
                border: none;
            }

            QSpinBox::up-arrow,
            QSpinBox::down-arrow,
            QDoubleSpinBox::up-arrow,
            QDoubleSpinBox::down-arrow {
                width: 0;
                height: 0;
            }

            QSpinBox QLineEdit, QDoubleSpinBox QLineEdit {
                padding: 4px;
                border: none;
                background: transparent;
            }
            """
        )
        self.setFixedWidth(300)
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding
        )

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(3, 3)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

    def _setup_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSpacing(10)

        self._add_header()
        self._add_status()
        self._add_toggle_button()
        self._add_options_panel()

    def _add_header(self):
        header_layout = QHBoxLayout()

        # Icono
        icon_path = f"{MEDIA}sensores/{self.device_data['icon']}"
        icon_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(
            40,
            40,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        icon_label.setPixmap(pixmap)
        icon_label.setCursor(Qt.CursorShape.PointingHandCursor)
        icon_label.mousePressEvent = lambda event: self._show_image_viewer(icon_path)
        header_layout.addWidget(icon_label)

        # Nombre y modelo
        name_layout = QVBoxLayout()
        name_label = MarqueeLabel.MarqueeLabel(self.device_data["name"])
        name_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #1e293b;")
        name_label.setMaximumWidth(180)
        name_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        model_label = QLabel(f"Modelo: {self.device_data['model']}")
        model_label.setStyleSheet("font-size: 12px; color: #64748b;")

        name_layout.addWidget(name_label)
        name_layout.addWidget(model_label)
        header_layout.addLayout(name_layout)

        # Botón de ayuda
        help_button = QPushButton("?")
        help_button.setFixedSize(24, 24)
        help_button.setStyleSheet(
            """
            QPushButton {
                background-color: #e2e8f0;
                border-radius: 12px;
                color: #000;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cbd5e1;
            }
        """
        )
        help_button.setToolTip(self.device_data["description"])
        help_button.setCursor(Qt.CursorShape.PointingHandCursor)
        header_layout.addWidget(help_button)

        self.main_layout.addLayout(header_layout)

    def _add_status(self):
        status_layout = QHBoxLayout()
        status_label = QLabel("Estado:")
        status_label.setStyleSheet("font-weight: bold; color: #475569;")

        status_value = QLabel(self.device_data["status"])
        status_value.setStyleSheet(
            f"""
            color: {'#16a34a' if self.device_data['status'] == 'Activo' else '#dc2626'};
            font-weight: bold;
        """
        )

        status_layout.addWidget(status_label)
        status_layout.addWidget(status_value)
        status_layout.addStretch()
        self.main_layout.addLayout(status_layout)

    def _add_toggle_button(self):
        self.toggle_button = QPushButton("Mostrar Opciones ▼")
        self.toggle_button.setStyleSheet(
            """
            QPushButton {
                background-color: #f1f5f9;
                border-radius: 6px;
                padding: 6px;
                color: #334155;
                border: 1px solid #e2e8f0;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """
        )
        self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_button.clicked.connect(self._toggle_options)
        self.main_layout.addWidget(self.toggle_button)

    def _add_options_panel(self):
        self.options_panel = DeviceOptions(self.notification, self.device_data["type"])
        self.options_panel.setVisible(False)
        self.main_layout.addWidget(self.options_panel)

    def _toggle_options(self):
        is_visible = self.options_panel.isVisible()
        self.options_panel.setVisible(not is_visible)
        self.toggle_button.setText(
            "Ocultar Opciones ▲" if not is_visible else "Mostrar Opciones ▼"
        )

    def _show_image_viewer(self, path):
        self.viewer = ImageViewer(path, self.window())
        self.viewer.show()
