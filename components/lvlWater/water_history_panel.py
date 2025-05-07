from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QLineEdit, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QPixmap, QIcon, QBrush


class WaterHistoryPanel(QFrame):
    def __init__(self, table_height=400, parent=None):
        super().__init__(parent)
        self.table_height = table_height
        self.setup_ui()
        self.populate_table()

    def setup_ui(self):
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")
        
        # Sombra
        history_shadow = QGraphicsDropShadowEffect()
        history_shadow.setBlurRadius(15)
        history_shadow.setColor(QColor(197, 239, 236))
        history_shadow.setOffset(0, 3)
        self.setGraphicsEffect(history_shadow)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        label = QLabel("Lecturas")
        label.setStyleSheet("font-size: 18px; font-weight: bold; color: #074e52;")
        header_layout.addWidget(label)

        header_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        filter_label = QLabel("Filtrar por:")
        filter_label.setStyleSheet("font-size: 14px; color: #64748b;")
        header_layout.addWidget(filter_label)

        self.search_filter = QLineEdit()
        self.search_filter.setPlaceholderText("Fecha, nivel o estado...")
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

        header_layout.addWidget(self.search_filter)
        layout.addLayout(header_layout)

        # Tabla de registros históricos
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Nivel (cm)", "Estado"])

        # Configuración de scroll y visualización
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
                margin-right: 3px;
<<<<<<< HEAD
=======
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
                margin: 2px 2px 2px 0px;
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
        self.all_data = [
            ("27/04/2025 08:00", "22.0", "Óptimo"),
            ("27/04/2025 08:10", "28.5", "Óptimo"),
            ("27/04/2025 08:20", "12.5", "Bajo"),
            ("27/04/2025 08:30", "19.0", "Bajo"),
            ("27/04/2025 08:40", "36.8", "Alto"),
            ("27/04/2025 08:50", "40.2", "Alto"),
            ("27/04/2025 09:00", "30.0", "Óptimo"),
            ("27/04/2025 09:10", "15.7", "Bajo"),
            ("27/04/2025 09:20", "38.0", "Alto"),
            ("27/04/2025 09:30", "25.0", "Óptimo"),
            ("27/04/2025 09:40", "10.0", "Bajo"),
            ("27/04/2025 09:50", "35.5", "Alto"),
            ("27/04/2025 10:00", "23.4", "Óptimo"),
            ("27/04/2025 10:10", "9.0", "Bajo"),
            ("27/04/2025 10:20", "42.1", "Alto"),
            ("27/04/2025 10:30", "26.7", "Óptimo"),
        ]

        self.history_table.setRowCount(len(self.all_data))
        for row, (fecha, valor, estado) in enumerate(self.all_data):
            # Columna 1: Fecha y hora
            fecha_item = QTableWidgetItem(fecha)
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.history_table.setItem(row, 0, fecha_item)

            # Columna 2: Nivel (cm) con ícono de botella
            valor_item = QTableWidgetItem(valor)
            valor_item.setIcon(QIcon("./resources/icons/botella-de-agua.png"))
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.history_table.setItem(row, 1, valor_item)

            # Columna 3: Estado con íconos por nivel
            estado_item = QTableWidgetItem(estado)
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

            if estado == "Bajo":
                estado_item.setIcon(QIcon("./resources/icons/low-water-red.png"))
                estado_item.setBackground(QBrush(QColor("#fef3c7")))
                estado_item.setForeground(QColor("#92400e"))
            elif estado == "Óptimo":
                estado_item.setIcon(QIcon("./resources/icons/optimal-water-green.png"))
                estado_item.setBackground(QBrush(QColor("#dcfce7")))
                estado_item.setForeground(QColor("#166534"))
            elif estado == "Alto":
                estado_item.setIcon(QIcon("./resources/icons/overflow-water-red.png"))
                estado_item.setBackground(QBrush(QColor("#fee2e2")))
                estado_item.setForeground(QColor("#b91c1c"))

            self.history_table.setItem(row, 2, estado_item)
            self.history_table.setRowHeight(row, 31)

    def filter_data(self, text):
        # Filtra los datos de la tabla según el texto ingresado en el campo de búsqueda
        search_text = text.lower()
        
        # Ocultar todas las filas
        for row in range(self.history_table.rowCount()):
            self.history_table.hideRow(row)
        
        # Mostrar solo las filas que contienen el texto de búsqueda en cualquier columna
        for row in range(self.history_table.rowCount()):
            show_row = False
            
            # Buscar en todas las columnas
            for col in range(self.history_table.columnCount()):
                item = self.history_table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            
            if show_row or search_text == "":
                self.history_table.showRow(row)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QLineEdit, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QPixmap, QIcon, QBrush


class WaterHistoryPanel(QFrame):
    def __init__(self, table_height=400, parent=None):
        super().__init__(parent)
        self.table_height = table_height
        self.setup_ui()
        self.populate_table()

    def setup_ui(self):
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")
        
        # Sombra
        history_shadow = QGraphicsDropShadowEffect()
        history_shadow.setBlurRadius(15)
        history_shadow.setColor(QColor(197, 239, 236))
        history_shadow.setOffset(0, 3)
        self.setGraphicsEffect(history_shadow)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        label = QLabel("Lecturas")
        label.setStyleSheet("font-size: 18px; font-weight: bold; color: #074e52;")
        header_layout.addWidget(label)

        header_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        filter_label = QLabel("Filtrar por:")
        filter_label.setStyleSheet("font-size: 14px; color: #64748b;")
        header_layout.addWidget(filter_label)

        self.search_filter = QLineEdit()
        self.search_filter.setPlaceholderText("Fecha, nivel o estado...")
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

        header_layout.addWidget(self.search_filter)
        layout.addLayout(header_layout)

        # Tabla de registros históricos
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Nivel (cm)", "Estado"])

        # Configuración de scroll y visualización
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
>>>>>>> 157474e8f36019d9e4ccb2ca2e6b9885332b2612
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
                margin: 2px 2px 2px 0px;
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
        self.all_data = [
            ("27/04/2025 08:00", "22.0", "Óptimo"),
            ("27/04/2025 08:10", "28.5", "Óptimo"),
            ("27/04/2025 08:20", "12.5", "Bajo"),
            ("27/04/2025 08:30", "19.0", "Bajo"),
            ("27/04/2025 08:40", "36.8", "Alto"),
            ("27/04/2025 08:50", "40.2", "Alto"),
            ("27/04/2025 09:00", "30.0", "Óptimo"),
            ("27/04/2025 09:10", "15.7", "Bajo"),
            ("27/04/2025 09:20", "38.0", "Alto"),
            ("27/04/2025 09:30", "25.0", "Óptimo"),
            ("27/04/2025 09:40", "10.0", "Bajo"),
            ("27/04/2025 09:50", "35.5", "Alto"),
            ("27/04/2025 10:00", "23.4", "Óptimo"),
            ("27/04/2025 10:10", "9.0", "Bajo"),
            ("27/04/2025 10:20", "42.1", "Alto"),
            ("27/04/2025 10:30", "26.7", "Óptimo"),
        ]

        self.history_table.setRowCount(len(self.all_data))
        for row, (fecha, valor, estado) in enumerate(self.all_data):
            # Columna 1: Fecha y hora
            fecha_item = QTableWidgetItem(fecha)
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.history_table.setItem(row, 0, fecha_item)

            # Columna 2: Nivel (cm) con ícono de botella
            valor_item = QTableWidgetItem(valor)
            valor_item.setIcon(QIcon("./resources/icons/botella-de-agua.png"))
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.history_table.setItem(row, 1, valor_item)

            # Columna 3: Estado con íconos por nivel
            estado_item = QTableWidgetItem(estado)
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

            if estado == "Bajo":
                estado_item.setIcon(QIcon("./resources/icons/low-water-red.png"))
                estado_item.setBackground(QBrush(QColor("#fef3c7")))
                estado_item.setForeground(QColor("#92400e"))
            elif estado == "Óptimo":
                estado_item.setIcon(QIcon("./resources/icons/optimal-water-green.png"))
                estado_item.setBackground(QBrush(QColor("#dcfce7")))
                estado_item.setForeground(QColor("#166534"))
            elif estado == "Alto":
                estado_item.setIcon(QIcon("./resources/icons/overflow-water-red.png"))
                estado_item.setBackground(QBrush(QColor("#fee2e2")))
                estado_item.setForeground(QColor("#b91c1c"))

            self.history_table.setItem(row, 2, estado_item)
            self.history_table.setRowHeight(row, 31)

    def filter_data(self, text):
        # Filtra los datos de la tabla según el texto ingresado en el campo de búsqueda
        search_text = text.lower()
        
        # Ocultar todas las filas
        for row in range(self.history_table.rowCount()):
            self.history_table.hideRow(row)
        
        # Mostrar solo las filas que contienen el texto de búsqueda en cualquier columna
        for row in range(self.history_table.rowCount()):
            show_row = False
            
            # Buscar en todas las columnas
            for col in range(self.history_table.columnCount()):
                item = self.history_table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            
            if show_row or search_text == "":
                self.history_table.showRow(row)
