# componentes
from components.systems.card import Card

# widgets
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QScrollArea, QFrame, QPushButton
)
from PyQt6.QtCore import Qt

import os
from dotenv import load_dotenv
load_dotenv()
SHADOW = os.getenv("SHADOW")

class Systems(QWidget):
    def __init__(self, company_data, parent=None):
        super().__init__(parent)
        self.company_data = company_data
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: transparent;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 12px;
                background: transparent;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #4CA4A5;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::up-button, QScrollBar::down-button,
            QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {
                background: transparent;
                border: none;
            }
        """)

        # Widget de contenido (para scroll)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 10, 20, 10)
        content_layout.setSpacing(10)

        # Botón para añadir nueva empresa (primero)
        add_button = QPushButton("Añadir nueva empresa")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CA4A5;
                color: white;
                font-size:12px;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3B8E8F;
            }
        """)
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        content_layout.addWidget(add_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Grid de tarjetas
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(12)
        grid_layout.setVerticalSpacing(6)

        # Agregar tarjetas al grid 3 por fila, derecha a izquierda
        for index, data in enumerate(self.company_data):
            row = index // 3
            col = 2 - (index % 3)
            card = Card(
                company_name=data["company_name"],
                trade_name=data["trade_name"],
                legal_name=data["legal_name"],
                logo_path=data["logo"]
            )
            grid_layout.addWidget(card, row, col)

        content_layout.addLayout(grid_layout)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area, stretch=1)
