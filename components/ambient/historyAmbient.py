from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
    QSpacerItem, QSizePolicy, QFrame, QDateEdit, QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QIcon, QPixmap,QBrush

import os
from dotenv import load_dotenv

load_dotenv()
SHADOW = os.getenv("SHADOW")

class HistoryAmbient(QWidget):
    def __init__(self, table_height=300):
        super().__init__()
        self.table_height = table_height
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.create_history_panel())

        self.add_example_data()

    def create_history_panel(self):
        history_panel = QFrame()
        history_panel.setFrameShape(QFrame.Shape.StyledPanel)
        history_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)

        history_layout = QVBoxLayout(history_panel)
        history_layout.setSpacing(10)

        # Encabezado con filtro
        history_header = QHBoxLayout()
        history_label = QLabel("Lecturas detalladas")
        history_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #074e52;
        """)
        history_header.addWidget(history_label)
        history_header.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        filter_label = QLabel("Filtrar por fecha:")
        filter_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
        """)
        history_header.addWidget(filter_label)

        self.date_filter = QDateEdit()
        self.date_filter.setDisplayFormat("dd/MM/yyyy")
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setStyleSheet("""
            QDateEdit {
                background-color: #4CA4A5;
                color: white;
                padding: 5px 10px;
                border-radius: 6px;
                font-size: 14px;
            }
            QDateEdit::drop-down {
                border: none;
            }
            QCalendarWidget QToolButton {
                background-color: #4CA4A5;
                color: white;
                border-radius: 4px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #4CA4A5;
            }
            QCalendarWidget QMenu {
                background-color: white;
                color: #4CA4A5;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: black;
                selection-background-color: #4CA4A5;
                selection-color: white;
            }
        """)
        history_header.addWidget(self.date_filter)
        history_layout.addLayout(history_header)

        # Tabla
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Temperatura (°C)", "Humedad", "Condición"])        
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setStyleSheet("""
        QTableView {
            background-color: white;
            gridline-color: #c5efec;
            border: none;
            border-radius: 6px;
            selection-background-color: #d4f1f0;
            selection-color: black;
            alternate-background-color: #f8fafc;
            color: #4CA4A5;
            font-size: 14px;
        }
        QHeaderView::section {
            background-color: #4CA4A5;
            padding: 8px;
            border: none;
            font-weight: bold;
            color: white;
            font-size: 15px;
        }
        QTableView::item {
            padding: 6px;
            border-bottom: 1px solid #c5efec;
            border-top: none;
            border-left: none;
            border-right: none;
        }
        QTableView::item:selected {
            border: none;
            background-color: #d4f1f0;
            color: black;
        }
        QScrollBar:vertical {
            background: #f1f5f9;
            width: 10px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background: #4CA4A5;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0;
        }
    """)

        self.history_table.setMinimumHeight(self.table_height)
        self.history_table.setMaximumHeight(600)  # Ajuste si deseas un tamaño máximo
        history_layout.addWidget(self.history_table)

        return history_panel

    def add_example_data(self):
        datos = [
            ("12/04/2025 08:30", "26.5", "65%", "Moderado"),
            ("12/04/2025 14:20", "30.1", "72%", "Moderado"),
            ("12/04/2025 19:15", "28.3", "70%", "Frío"),
            ("12/04/2025 13:00", "32.0", "80%", "Caliente"),
            ("12/04/2025 07:45", "25.0", "60%", "Frío"),
            ("11/04/2025 10:15", "27.0", "64%", "Caliente"),
            ("10/04/2025 09:00", "26.8", "67%", "Moderado"),
            ("09/04/2025 15:00", "31.2", "75%", "Caliente"),
        ]

        # Asegúrate que las rutas sean correctas
        thermometer_icon = QIcon(QPixmap("resources/icons/thermometer.png").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        drop_icon = QIcon(QPixmap("resources/icons/gota.png").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        sun_icon = QIcon(QPixmap("resources/icons/amarillo_sol.png").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        snowflake_icon = QIcon(QPixmap("resources/icons/azul_viento.png").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        cloud_icon = QIcon(QPixmap("resources/icons/verde_nube.png").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        self.history_table.setRowCount(len(datos))
        for i, fila in enumerate(datos):
            for j, dato in enumerate(fila):
                item = QTableWidgetItem(dato)
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

                if j == 1:
                    item.setIcon(thermometer_icon)
                elif j == 2:
                    item.setIcon(drop_icon)
                elif j == 3:
                    # Condiciones con color de fondo, texto e ícono
                    if dato == "Caliente":
                        item.setForeground(QBrush(QColor("#f4b400")))
                        item.setIcon(sun_icon)
                    elif dato == "Moderado":
                        item.setForeground(QBrush(QColor("#27b061")))
                        item.setIcon(cloud_icon)
                    elif dato == "Frío":
                        item.setForeground(QBrush(QColor("#1E89CF")))
                        item.setIcon(snowflake_icon)

                self.history_table.setItem(i, j, item)