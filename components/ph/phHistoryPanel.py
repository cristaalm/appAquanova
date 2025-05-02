from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView, QSpacerItem, QSizePolicy,
    QGraphicsDropShadowEffect, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QBrush
from .phConstants import *

class PhHistoryPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_height = 400
        self.all_data = []
        self.setup_ui()
        self.populate_table()
    
    def setup_ui(self):
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")

        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(SHADOW_COLOR)
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Encabezado con título y búsqueda
        header = QHBoxLayout()
        
        history_label = QLabel("Lecturas")
        history_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #074e52;")
        header.addWidget(history_label)
        
        header.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        filter_label = QLabel("Filtrar por:")
        filter_label.setStyleSheet("font-size: 14px; color: #64748b;")
        header.addWidget(filter_label)
        
        self.search_filter = QLineEdit()
        self.search_filter.setPlaceholderText("Fecha, valor o estado...")
        self.search_filter.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #4CA4A5;
                color: #333;
                padding: 5px 10px;
                border-radius: 6px;
                font-size: 14px;
                max-width: 250px;
            }
            QLineEdit:focus {
                border: 2px solid #4CA4A5;
            }
        """)
        
        self.search_filter.textChanged.connect(self.filter_data)
        header.addWidget(self.search_filter)
        layout.addLayout(header)

        # Tabla
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Potencial de hidrógeno (ph)", "Estado"])
        
        self.history_table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.verticalHeader().setVisible(False)

        self.history_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #c5efec;
                border: none;
                border-radius: 6px;
                selection-background-color: #d4f1f0;
                selection-color: black;
                alternate-background-color: #f8fafc;
                color: #4CA4A5;
                font-size: 14px;
                padding-bottom: 0px;
                margin-right: 5px;
            }
            QHeaderView::section {
                background-color: #4CA4A5;
                padding: 8px;
                border: none;
                font-weight: bold;
                color: white;
                font-size: 15px;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #c5efec;
            }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 10px;
                border-radius: 5px;
                margin-left: 5px;
            }
            QScrollBar::handle:vertical {
                background: #4CA4A5;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                height: 0;
                background: none;
            }
        """)

        self.history_table.verticalHeader().setDefaultSectionSize(0)  
        self.history_table.verticalHeader().setMinimumSectionSize(0)
        self.history_table.setMinimumHeight(self.table_height)
        self.history_table.setMaximumHeight(600)
        layout.addWidget(self.history_table)
    
    def populate_table(self):
        # Datos históricos para la tabla
        self.all_data = [
            ("15/04/2024 08:30", "6.8", self.get_ph_state(6.8)),
            ("15/04/2024 10:15", "7.1", self.get_ph_state(7.1)),
            ("14/04/2024 09:00", "6.9", self.get_ph_state(6.9)),
            ("14/04/2024 14:20", "7.2", self.get_ph_state(7.2)),
            ("13/04/2024 11:45", "6.7", self.get_ph_state(6.7)),
            ("12/04/2024 08:30", "5.8", self.get_ph_state(5.8)),
            ("11/04/2024 10:15", "8.1", self.get_ph_state(8.1)),
            ("10/04/2024 09:00", "6.9", self.get_ph_state(6.9)),
            ("09/04/2024 13:30", "7.0", self.get_ph_state(7.0)),
            ("08/04/2024 15:45", "6.6", self.get_ph_state(6.6)),
            ("07/04/2024 09:15", "7.3", self.get_ph_state(7.3)),
            ("06/04/2024 10:30", "6.5", self.get_ph_state(6.5)),
            ("05/04/2024 13:45", "7.0", self.get_ph_state(7.0)),
            ("04/04/2024 11:20", "6.4", self.get_ph_state(6.4)),
            ("03/04/2024 16:10", "7.8", self.get_ph_state(7.8)),
            ("02/04/2024 08:50", "7.2", self.get_ph_state(7.2)),
            ("01/04/2024 14:35", "6.9", self.get_ph_state(6.9))

        ]
        
        # Iconos para estados
        icono_acido = QIcon("./resources/icons/acido.png")
        icono_neutro = QIcon("./resources/icons/neutro.png")
        icono_alcalino = QIcon("./resources/icons/alcalino.png")
        
        # Un solo icono para valores
        icono_valor = QIcon("./resources/icons/ph_icon.png")  # O cualquier otro icono que prefieras
        
        self.history_table.setRowCount(len(self.all_data))
        for row, (fecha, valor, estado) in enumerate(self.all_data):
            fecha_item = QTableWidgetItem(fecha)
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            
            # Celda de valor con un único icono
            valor_item = QTableWidgetItem(valor)
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            valor_item.setIcon(icono_valor)  # Siempre el mismo icono
            
            # Color según el valor de pH
            ph_value = float(valor)
            if ph_value < PH_MIN_NEUTRAL:
                valor_item.setForeground(QBrush(QColor("#b91c1c")))  # Rojo para bajo
            elif ph_value > PH_MAX_NEUTRAL:
                valor_item.setForeground(QBrush(QColor("#92400e")))  # Naranja para alto
            else:
                valor_item.setForeground(QBrush(QColor("#166534")))  # Verde para normal
            
            estado_item = QTableWidgetItem(estado)
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            
            if estado == "Ácido":
                estado_item.setBackground(QBrush(QColor("#fee2e2")))
                estado_item.setForeground(QBrush(QColor("#b91c1c")))
                estado_item.setIcon(icono_acido)
            elif estado == "Alcalino":
                estado_item.setBackground(QBrush(QColor("#fef3c7")))
                estado_item.setForeground(QBrush(QColor("#92400e")))
                estado_item.setIcon(icono_alcalino)
            else:  # NEUTRO
                estado_item.setBackground(QBrush(QColor("#dcfce7")))
                estado_item.setForeground(QBrush(QColor("#166534")))
                estado_item.setIcon(icono_neutro)
            
            self.history_table.setItem(row, 0, fecha_item)
            self.history_table.setItem(row, 1, valor_item)
            self.history_table.setItem(row, 2, estado_item)
            self.history_table.setRowHeight(row, 31)
    
    def filter_data(self, text):
        search_text = text.lower()
        
        # Ocultar todas las filas
        for row in range(self.history_table.rowCount()):
            self.history_table.hideRow(row)
        
        # Mostrar filas que coincidan
        for row in range(self.history_table.rowCount()):
            show_row = False
            
            for col in range(self.history_table.columnCount()):
                item = self.history_table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            
            if show_row or search_text == "":
                self.history_table.showRow(row)
    
    def get_ph_state(self, ph_value):
        ph_value = float(ph_value)
        if ph_value < PH_MIN_NEUTRAL:
            return "Ácido"
        elif ph_value > PH_MAX_NEUTRAL:
            return "Alcalino"
        else:
            return "Neutro"