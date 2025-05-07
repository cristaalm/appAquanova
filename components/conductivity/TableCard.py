from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QGraphicsDropShadowEffect,
    QLineEdit, QTableWidgetItem
)
from random import randint
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap
import os 

class TableCard(QWidget):
    def __init__(self, max, min, parent=None):
        super().__init__(parent)
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.table_height = 400
        self.table_data = []  # Lista para almacenar datos de la tabla
        self.all_data = []    # Lista para datos originales completos

        self.rango_max = max
        self.rango_min = min

        self.current_filter = "Todo" 

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 5, 5) 
        
        self.history_panel = self.create_history_panel()
        self.layout.addWidget(self.history_panel)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        self.populate_table()

    def load(self, path, icon_name, size):
        icon_path = os.path.join(
        self.base_dir,  
        "..",        
        "..",   
        "resources",    
        path,       
        icon_name
        )
        if os.path.exists(icon_path):
            return QPixmap(icon_path).scaled(
                size, 
                size, 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
        )
        else:
            print(f"Error: No se encontró el ícono en {icon_path}")
            return None
        
    def create_history_panel(self):
        """Crea el panel de historial con el filtro."""
        history_panel = QFrame()
        history_panel.setFrameShape(QFrame.Shape.StyledPanel)
        history_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)

        # Sombra
        history_shadow = QGraphicsDropShadowEffect()
        history_shadow.setBlurRadius(15)
        history_shadow.setColor(QColor(197, 239, 236))
        history_shadow.setOffset(0, 3)
        history_panel.setGraphicsEffect(history_shadow)
        
        history_layout = QVBoxLayout(history_panel)
        history_layout.setSpacing(10)
        
        # Encabezado de historial
        history_header = QHBoxLayout()
        history_label = QLabel("Lecturas")
        history_label.setStyleSheet("""
            font-size: 18px;
            color: #074e52;
            font-weight: bold;
        """)
        history_header.addWidget(history_label)
        history_header.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        filter_label = QLabel("Filtrar por:")
        filter_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
        """)
        history_header.addWidget(filter_label)
        
        self.search_filter = QLineEdit()
        self.search_filter.setPlaceholderText("Filtrar por fecha, valor o condición...")
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

        history_header.addWidget(self.search_filter)
        history_layout.addLayout(history_header)
        
        # Tabla de historial
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Conductividad µS/cm", "Condición"])
        
        # Asegurar que la tabla ocupe todo el ancho disponible
        self.history_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.history_table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Configurar el estiramiento de columnas para ocupar todo el ancho
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
                padding-bottom: 50px;
                margin: 0px; 
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
                padding: 5px;
                border-bottom: 1px solid #c5efec;
                border-top: 1px;
            }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 10px;
                border-radius: 10px;
                margin-left: 5px;
                margin-bottom: 50px;
            }
            QScrollBar::handle:vertical {
                background: #4CA4A5;
                min-height: 30px;
                border-radius: 10px;
            }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                height: 0;
                background: none;
                border-radius: 10px;
            }
        """)

        self.history_table.verticalHeader().setDefaultSectionSize(25)  
        self.history_table.verticalHeader().setMinimumSectionSize(25)
        self.history_table.setMinimumHeight(self.table_height)
        self.history_table.setMaximumHeight(600)
        history_layout.addWidget(self.history_table)
        
        return history_panel
    
    def populate_table(self):
        self.all_data = [
            {"fecha": "10/04/2025 09:00am", "valor": randint(25, 35)},
            {"fecha": "10/04/2025 12:00pm", "valor": randint(25, 35)},
            {"fecha": "10/04/2025 03:00pm", "valor": randint(25, 35)},
            {"fecha": "10/04/2025 06:00pm", "valor": randint(25, 35)},
            {"fecha": "11/04/2025 09:00am", "valor": randint(25, 35)},
            {"fecha": "11/04/2025 12:00pm", "valor": randint(25, 35)},
            {"fecha": "11/04/2025 03:00pm", "valor": randint(25, 35)},
            {"fecha": "11/04/2025 06:00pm", "valor": randint(25, 35)},
            {"fecha": "12/04/2025 09:00am", "valor": randint(25, 35)},
            {"fecha": "12/04/2025 12:00pm", "valor": randint(25, 35)},
            {"fecha": "12/04/2025 03:00pm", "valor": randint(25, 35)},
            {"fecha": "12/04/2025 06:00pm", "valor": randint(25, 35)},
        ]
        self.history_table.setRowCount(len(self.all_data))

        for row, item in enumerate(self.all_data):
            # Columna de fecha
            fecha_item = QTableWidgetItem(item["fecha"])
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            self.history_table.setItem(row, 0, fecha_item)

            container = QWidget()
            container.setStyleSheet("background-color: transparent;")

            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(5)
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft) 

            icon_temp = QLabel()
            valor_pixmap = self.load("icons", "verdeElecricity.png", 12)
            if valor_pixmap:
                icon_temp.setPixmap(valor_pixmap)
            layout.addWidget(icon_temp)
            
            # Columna de valor
            value_label = QLabel(f"{item['valor']}")
            value_label.setStyleSheet("color: #4CA4A5; font-size: 14px;")
            layout.addWidget(value_label)
            
            self.history_table.setCellWidget(row, 1, container)

            # Determinar estado basado en el valor de temperatura
            temp_value = float(item["valor"])
            if temp_value < self.rango_min:
                estado = "Bajo"
                icon_name = "rojoElecricity.png"
                color_style = "color: #D9534F; font-size: 14px;"
            elif temp_value > self.rango_max:
                estado = "Alto"
                icon_name = "amarilloElecricity.png"
                color_style = "color:#F4B400; font-size: 14px;"
            else:
                estado = "Óptimo"
                icon_name = "verdeElecricity.png"
                color_style = "color: #2ECC71; font-size: 14px;"

            # Crear widget contenedor
            container = QWidget()
            container.setStyleSheet("background-color: transparent;")
            
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(5)
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  

            # Añadir icono
            icon_label = QLabel()
            estado_pixmap = self.load("icons", icon_name, 10)
            if estado_pixmap:
                icon_label.setPixmap(estado_pixmap)
            layout.addWidget(icon_label)

            text_label = QLabel(estado)
            text_label.setStyleSheet(color_style)
            layout.addWidget(text_label)
            self.history_table.setCellWidget(row, 2, container)
            self.history_table.setRowHeight(row, 28)

    def filter_data(self, text):
        """Filtra los datos de la tabla según el texto ingresado en el campo de búsqueda"""
        search_text = text.lower()
        
        # Ocultar todas las filas
        for row in range(self.history_table.rowCount()):
            self.history_table.hideRow(row)
        
        for row in range(self.history_table.rowCount()):
            show_row = False
            
            for col in range(self.history_table.columnCount()):
                item = self.history_table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
                
                if col == 2:
                    cell_widget = self.history_table.cellWidget(row, col)
                    if cell_widget:
                        for child in cell_widget.findChildren(QLabel):
                            if child.text() and search_text in child.text().lower():
                                show_row = True
                                break
            
            if show_row or search_text == "":
                self.history_table.showRow(row)
    
    def reset_filter(self):
        """Restablece el filtro para mostrar todos los datos"""
        self.search_filter.clear()
        
        for row in range(self.history_table.rowCount()):
            self.history_table.showRow(row)
        
    def set_table_height(self, height):
        self.table_height = height
        self.history_table.setMinimumHeight(height)
        
    def sizeHint(self):
        size = super().sizeHint()
        size.setWidth(800) 
        return size