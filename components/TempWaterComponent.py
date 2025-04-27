from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QApplication, 
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QComboBox, QGraphicsDropShadowEffect,
    QProgressBar, QLineEdit, QTableWidgetItem
)
from random import randint
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPixmap, QBrush
import os 

class tempWaterComponent(QWidget):
    QApplication.setStyle("Fusion")
    def __init__(self, graph_widget, parent=None):
        super().__init__(parent)
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.graph_widget = graph_widget 
        self.value = randint(25, 35)  # Valor inicial simulado
        self.table_height = 400
        self.table_data = []  # Lista para almacenar datos de la tabla
        self.all_data = []  # Lista para datos originales completos

        # Rangos de temperatura
        self.temp_max = 32
        self.temp_min = 28

        # Estado del filtro
        self.current_filter = "Todo"  # Valor por defecto

        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #f5f7fa;")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)
        top_layout.addWidget(self.create_summary_panel(), 1)
        top_layout.addWidget(self.create_graph_panel(), 4)

        main_layout.addLayout(top_layout, 1)
        main_layout.addWidget(self.create_history_panel(), 10)
        main_layout.setContentsMargins(20, 20, 20, 10)
        
        self.setLayout(main_layout)

    # Función para cargar íconos
    def load(self, path, icon_name, size):
        icon_path = os.path.join(
        self.base_dir,  # Ruta del script actual (components/)
        "..",           # Subir a la carpeta padre (vscode/)
        "resources",    # Entrar a resources/
        path,        # Entrar a icons/
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
        
    def scroll_title_text(self, label):
        scrolled = self.title_text[self.title_index:] + self.title_text[:self.title_index]
        label.setText(scrolled)
        self.title_index = (self.title_index + 1) % len(self.title_text)

    def create_summary_panel(self):
        summary_panel = QFrame()
        summary_panel.setFrameShape(QFrame.Shape.StyledPanel)
        summary_panel.setMinimumWidth(200)
        summary_panel.setMaximumWidth(280)
        summary_panel.setMinimumHeight(280)
        summary_panel.setFixedHeight(280)
        summary_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        summary_panel.setGraphicsEffect(shadow)
        
        summary_layout = QVBoxLayout(summary_panel)
        summary_layout.setContentsMargins(15, 15, 15, 15)
        summary_layout.setSpacing(10)
        
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        
        # Título
        self.title_text = "Temperatura actual     "
        self.title_index = 0
        title_label = QLabel(self.title_text)
        title_label.setStyleSheet("""
            font-size: 22px;
            color: #045859;
            font-weight: bold;                                
        """)
        title_label.setMinimumWidth(150)
        title_label.setMaximumWidth(200)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.title_timer = QTimer()
        self.title_timer.timeout.connect(lambda: self.scroll_title_text(title_label))
        self.title_timer.start(150)

        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        temp_icon_label = QLabel()
        temp_pixmap = self.load("icons","water_temp.png", 24)
        if temp_pixmap:
            temp_icon_label.setPixmap(temp_pixmap)
        
        title_layout.addWidget(temp_icon_label)
        summary_layout.addLayout(title_layout)  
        
        # Subtítulo
        subtitle = QLabel("Último registro del sensor")
        subtitle.setStyleSheet("""
            font-size: 12px;
            font-style: italic;
            color: #6b7280;
        """)
        summary_layout.addWidget(subtitle)
        summary_layout.addSpacing(2)

        # Sección del termómetro y temperatura
        value_layout = QHBoxLayout()
        
        # Ícono del termómetro
        thermometer_icon_label = QLabel()
        thermometer_pixmap = self.load("icons","temperature.png", 60)
        if thermometer_pixmap:
            thermometer_icon_label.setPixmap(thermometer_pixmap)
        value_layout.addWidget(thermometer_icon_label)
        
        # Valor de la temperatura
        self.value_label = QLabel(f"{self.value}")
        self.value_label.setStyleSheet("""
            font-size: 56px;
            font-weight: bold;
            color: #045859;
            text-align: center;
        """)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_layout.addWidget(self.value_label)

        self.value_unit_lable = QLabel("°C")
        self.value_unit_lable.setStyleSheet("""
            font-size: 40px;
            color: #045859;
            margin-left: 2px;
            margin-top: 20px;
            font-weight: bold;
        """)
        value_layout.addWidget(self.value_unit_lable)
        summary_layout.addLayout(value_layout)

        summary_layout.addSpacing(5)

        labels_layout = QHBoxLayout()
        labels_layout.setContentsMargins(0, 0, 0, 0)  

        min_label = QLabel("Min.")
        min_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        min_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        labels_layout.addWidget(min_label)

        labels_layout.addStretch()

        max_label = QLabel("Max.")
        max_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        max_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        labels_layout.addWidget(max_label)

        summary_layout.addLayout(labels_layout)

        progress_bar = QProgressBar()
        progress_bar.setFixedHeight(12)
        progress_bar.setTextVisible(False)

        # Calcular el porcentaje de temperatura
        temp_porcentage = (self.value - self.temp_min) * 100 / (self.temp_max - self.temp_min)
        # Limitar el valor entre 0 y 100
        temp_porcentage = max(0, min(100, temp_porcentage))  
        progress_bar.setValue(int(temp_porcentage))
        progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #e2e8f0;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background-color: #4CA4A5;
                border-radius: 6px;
            }
        """)

        summary_layout.addWidget(progress_bar)
        summary_layout.addSpacing(20)

        self.status = QLabel(self.get_status())
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("""
            background-color: #c5efeb; 
            color: #2b6363;
            border-radius: 15px;
            padding: 6px;
            font-size: 18px;
            font-weight: bold;
        """)

        summary_layout.addWidget(self.status)
        summary_layout.addStretch()

        return summary_panel
    
    def get_status(self):
        if self.value < self.temp_min:  
            return "Frío"
        elif self.value > self.temp_max:  
            return "Caliente"
        else: 
            return "Ambiente"
    
    def create_graph_panel(self):
        graph_panel = QFrame()
        graph_panel.setMaximumHeight(280)
        graph_panel.setFixedHeight(280)
        graph_panel.setFrameShape(QFrame.Shape.StyledPanel)
        graph_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        graph_shadow = QGraphicsDropShadowEffect()
        graph_shadow.setBlurRadius(15)
        graph_shadow.setColor(QColor(0, 0, 0, 40))
        graph_shadow.setOffset(0, 3)
        graph_panel.setGraphicsEffect(graph_shadow)
        
        graph_layout = QVBoxLayout(graph_panel)
        graph_layout.setContentsMargins(15, 0, 15, 15)
        graph_layout.setSpacing(10)
        
        # Encabezado de la gráfica
        header_layout = QHBoxLayout()
        
        header_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        graph_layout.addLayout(header_layout)
        self.graph_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        graph_layout.addWidget(self.graph_widget, 1)
        
        return graph_panel

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
        # Aplicar efecto de sombra para el panel de historial
        history_shadow = QGraphicsDropShadowEffect()
        history_shadow.setBlurRadius(15)
        history_shadow.setColor(QColor(0, 0, 0, 40))
        history_shadow.setOffset(0, 3)
        history_panel.setGraphicsEffect(history_shadow)
        
        history_layout = QVBoxLayout(history_panel)
        history_layout.setContentsMargins(15, 15, 15, 15)
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
        self.search_filter.setPlaceholderText("Filtrar por fecha, valor o estado...")
        self.search_filter.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #4CA4A5;
                color: #333;
                padding: 5px 10px;
                border-radius: 6px;
                font-size: 14px;
                max-width: 200px;  
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
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Temperatura", "Condición"])
        
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
                padding-bottom: 20px;
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

        self.history_table.verticalHeader().setDefaultSectionSize(40)  
        self.history_table.verticalHeader().setMinimumSectionSize(40)
        self.history_table.setMinimumHeight(self.table_height)
        self.history_table.setMaximumHeight(600)
        history_layout.addWidget(self.history_table)
        
        # Población de datos de ejemplo
        self.populate_table()
        
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
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 0, fecha_item)
            
            # Columna de valor
            valor_item = QTableWidgetItem(f"{item['valor']} °C")
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 1, valor_item)
            
            # Determinar estado basado en el valor de temperatura
            estado = self.get_temp_state(item["valor"])
            
            # Columna de estado con color de fondo según temperatura
            estado_item = QTableWidgetItem(estado)
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            
            if estado == "Frío":
                estado_item.setBackground(QBrush(QColor("#e0f2fe")))
                estado_item.setForeground(QBrush(QColor("#0369a1")))
                icon_name = "cold.png"
            elif estado == "Caliente":
                estado_item.setBackground(QBrush(QColor("#fee2e2")))
                estado_item.setForeground(QBrush(QColor("#b91c1c")))
                icon_name = "hot.png"
            else:  # Ambiente
                estado_item.setBackground(QBrush(QColor("#dcfce7")))
                estado_item.setForeground(QBrush(QColor("#166534")))
                icon_name = "good.png"
            
            # Agregar el ícono correspondiente
            estado_pixmap = self.load("icons", icon_name, 16)
            if estado_pixmap:
                # Convertir QPixmap a QIcon antes de asignarlo
                from PyQt6.QtGui import QIcon
                estado_icon = QIcon(estado_pixmap)
                estado_item.setIcon(estado_icon)
            
            self.history_table.setItem(row, 2, estado_item)
            
            # Altura de fila uniforme
            self.history_table.setRowHeight(row, 35)

    def get_temp_state(self, temp_value):
        """Determina el estado de temperatura para la tabla de historial"""
        temp_value = float(temp_value)
        if temp_value < self.temp_min:
            return "Frío"
        elif temp_value > self.temp_max:
            return "Caliente"
        else:
            return "Ambiente"

    def filter_data(self, text):
        """Filtra los datos de la tabla según el texto ingresado en el campo de búsqueda"""
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
    
    def reset_filter(self):
        """Restablece el filtro para mostrar todos los datos"""
        # Limpiar el campo de búsqueda
        self.search_filter.clear()
        
        # Mostrar todas las filas
        for row in range(self.history_table.rowCount()):
            self.history_table.showRow(row)
    
    def set_value(self, new_value):
        self.value = float(new_value)
        self.value_label.setText(str(self.value))
        
        # Actualizar la barra de progreso
        temp_porcentage = (self.value - self.temp_min) * 100 / (self.temp_max - self.temp_min)
        temp_porcentage = max(0, min(100, temp_porcentage))  # Asegurar que esté entre 0 y 100
        
        # Actualizar el estado
        self.status.setText(self.get_status())
        
    def set_table_height(self, height):
        self.table_height = height
        self.history_table.setMinimumHeight(height)
        self.history_table.setMaximumHeight(height)

    def resizeEvent(self, event):
        """Manejar cambios de tamaño de la ventana"""
        super().resizeEvent(event)
        
        card_width = self.width()
        
        if card_width < 800:
            # Modo compacto
            self.value_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #045859;")
        else:
            # Modo normal
            self.value_label.setStyleSheet("font-size: 56px; font-weight: bold; color: #045859;")