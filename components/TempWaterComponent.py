from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QApplication, 
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QComboBox, QGraphicsDropShadowEffect, QGraphicsOpacityEffect
)
from random import randint
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QColor, QPixmap
from components.TempWaterGraph import TempGraph
import os 

class tempWaterComponent(QWidget):
    QApplication.setStyle("Fusion")
    def __init__(self, graph_widget, parent=None):
        super().__init__(parent)
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.graph_widget = TempGraph()  
        self.value = randint(25, 35)  #Valor inicial simmulado
        self.table_height = 320  
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #f5f7fa;")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.create_summary_panel())
        top_layout.addWidget(self.create_emotion_panel(), 1)
        top_layout.addWidget(self.create_graph_panel(), 2)
        main_layout.addLayout(top_layout)
        
        # Sección de historial
        main_layout.addWidget(self.create_history_panel())
        
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
        summary_panel.setMinimumWidth(220)
        summary_panel.setMaximumWidth(280)
        summary_panel.setMaximumHeight(240)
        summary_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 3)
        summary_panel.setGraphicsEffect(shadow)
        
        summary_layout = QVBoxLayout(summary_panel)
        summary_layout.setContentsMargins(15, 10, 15, 10)
        summary_layout.setSpacing(5)
        
        title_layout = QHBoxLayout()
        
        # Título
        self.title_text = "Condición actual     "
        self.title_index = 0
        title_label = QLabel(self.title_text)
        title_label.setStyleSheet("""
            font-size: 22px;
            color: #074e52;
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

        # Sección del termómetro y temperatura
        value_layout = QHBoxLayout()
        
        # Ícono del termómetro
        thermometer_icon_label = QLabel()
        thermometer_pixmap = self.load("icons","temperature.png", 60)
        if thermometer_pixmap:
            thermometer_icon_label.setPixmap(thermometer_pixmap)
        value_layout.addWidget(thermometer_icon_label)
        
        # Valor de la temperatura
        self.value_label = QLabel(f"{self.value}°C")
        self.value_label.setStyleSheet("""
            font-size: 65px;
            font-weight: bold;
            margin: 15px 0;
            color: #074e52;
        """)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_layout.addWidget(self.value_label)
        
        summary_layout.addLayout(value_layout)
        
        # Fecha y hora de la última lectura (sin icono)
        placeholder = "11/02/2025 09:00am"
        status_label = QLabel(f"{placeholder}")
        status_label.setStyleSheet("""
            font-style: italic;
            color: #64748b;
            font-size: 15px;
            text-align: center;
        """)
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(status_label)
        
        # Añadir rango recomendado
        range_label = QLabel("Rango óptimo: 28°C - 32°C")
        range_label.setStyleSheet("""
            font-size: 13px;
            color: #475569;
            margin-top: 5px;
        """)
        range_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(range_label)
        
        summary_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        return summary_panel

    def create_emotion_panel(self):
        emotion_panel = QFrame()
        emotion_panel.setFrameShape(QFrame.Shape.StyledPanel)
        emotion_panel.setMinimumWidth(60)
        emotion_panel.setMaximumWidth(120)
        emotion_panel.setMaximumHeight(240)
        emotion_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        emotion_shadow = QGraphicsDropShadowEffect()
        emotion_shadow.setBlurRadius(15)
        emotion_shadow.setColor(QColor(0, 0, 0, 40))
        emotion_shadow.setOffset(0, 3)
        emotion_panel.setGraphicsEffect(emotion_shadow)

        emotion_layout = QVBoxLayout(emotion_panel)
        emotion_layout.setContentsMargins(5, 5, 5, 5)
        emotion_layout.setSpacing(5)

        emotion_title = QLabel("Estado")
        emotion_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #074e52;
            text-align: center;
        """)

        self.status_indicator = QLabel()
        self.update_status(self.value)  
        self.status_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(self.status_indicator)

        if self.value < 28:
            estado = "frio"
        elif self.value > 33:
            estado = "caluroso"
        else:
            estado = "ambiente"

        # Diccionario con íconos activos y desactivados
        estados = {
            "caluroso": {
                "activo": "caluroso.png",
                "inactivo": "des_caluroso.png"
            },
            "ambiente": {
                "activo": "ambiente.png",
                "inactivo": "des_ambiente.png"
            },
            "frio": {
                "activo": "frio.png",
                "inactivo": "des_frío.png"
            }
        }

        # Mostrar caritas correspondientes
        for key in ["caluroso", "ambiente", "frio"]:
            label = QLabel()
            media_path = estados[key]["activo"] if key == estado else estados[key]["inactivo"]
            pixmap = self.load("media",media_path, 50)
            
            if pixmap:
                label.setPixmap(pixmap)
            
            if key != estado:
                opacity_effect = QGraphicsOpacityEffect()
                opacity_effect.setOpacity(0.3)
                label.setGraphicsEffect(opacity_effect)

            label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
            emotion_layout.addWidget(label)

        return emotion_panel
    
    def create_graph_panel(self):
        graph_panel = QFrame()
        graph_panel.setMaximumHeight(240)
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
        graph_layout.setContentsMargins(10, 10, 15, 5)
        """        graph_title = QLabel("Tendencia de la tempertarua del agua")
        graph_title.setStyleSheet(
            font-size: 18px;
            color: #074e52;
            margin-bottom: 5px;
        )
        graph_layout.addWidget(graph_title)"""
        
        self.graph_widget.setMinimumHeight(200)
        self.graph_widget.setMinimumWidth(400)
        graph_layout.addWidget(self.graph_widget)
        
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
        history_label = QLabel("Historial de registro")
        history_label.setStyleSheet("""
            font-size: 18px;
            color: #074e52;
        """)
        history_header.addWidget(history_label)
        history_header.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        filter_label = QLabel("Filtrar por:")
        filter_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
        """)
        history_header.addWidget(filter_label)
        
        filter_combo = QComboBox()
        filter_combo.addItems(["Todo", "Ambiente", "Caliente", "Frío"])
        filter_combo.setStyleSheet("""
            QComboBox {
                background-color: #074e52;  
                color: white;
                padding: 5px 10px;
                border-radius: 6px;
                min-width: 100px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #ddd;
                selection-background-color: #074e52;
                selection-color: white;
            }
        """)
        history_header.addWidget(filter_combo)
        history_layout.addLayout(history_header)
        
        # Tabla de historial
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Temperatura", "Condición"])
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setStyleSheet("""
            QTableView {
                background-color: white;
                gridline-color: #e2e8f0;
                border: none;
                border-radius: 6px;
                selection-background-color: #e2e8f0;
                selection-color: black;
                alternate-background-color: #f8fafc;
                color: #1e293b;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #074e52;
                padding: 8px;
                border: none;
                color: white;
                font-size: 15px;
            }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 6px;
                border-radius: 3px;
                margin: 0;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #21797a;
                border-radius: 3px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {
                width: 0px;
                height: 0px;
                background: none;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        scrollbar = self.history_table.verticalScrollBar()
        scrollbar.setStyleSheet("""
            QTableView {
                background-color: white;
                gridline-color: #e2e8f0;
                border: none;
                border-radius: 6px;
                selection-background-color: #e2e8f0;
                selection-color: black;
                alternate-background-color: #f8fafc;
                color: #1e293b;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #074e52;
                padding: 8px;
                border: none;
                color: white;
                font-size: 15px;
            }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 6px;
                border-radius: 3px;
                margin: 0;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #21797a;
                border-radius: 3px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
        """)

        # Después de establecer el estilo
        self.history_table.setStyleSheet(...)
        self.history_table.repaint()  # Fuerza un repintado completo
        QApplication.processEvents()  # Procesa todos los eventos pendientes

        self.history_table.setMinimumHeight(self.table_height)
        self.history_table.setMaximumHeight(self.table_height)
        self.populate_table()
        history_layout.addWidget(self.history_table)
        
        return history_panel
    
    def populate_table(self):
        data = [
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
        self.history_table.setRowCount(len(data))
    
        # Configurar el color de fondo base para toda la tabla
        background_color = "#ffffff"  # Fondo blanco
        alternate_color = "#f8fafc"   # Color alternativo para filas pares/impares
        
        for row, item in enumerate(data):
            # Determinar el color de fondo para esta fila
            row_bg_color = alternate_color if row % 2 else background_color
            cell_style = f"background-color: {row_bg_color}; border: none;"
            
            # Columna de fecha con ícono
            fecha_cell = QWidget()
            fecha_cell.setStyleSheet(cell_style)
            fecha_layout = QHBoxLayout(fecha_cell)
            fecha_layout.setContentsMargins(10, 0, 0, 0)
            fecha_layout.setSpacing(8)
            
            
            fecha_text = QLabel(item["fecha"])
            fecha_text.setStyleSheet(f"background-color: {row_bg_color};")
            
            fecha_layout.addWidget(fecha_text)
            fecha_layout.addStretch()
            
            self.history_table.setCellWidget(row, 0, fecha_cell)
            
            # Columna de valor con ícono de temperatura
            valor_cell = QWidget()
            valor_cell.setStyleSheet(cell_style)
            valor_layout = QHBoxLayout(valor_cell)
            valor_layout.setContentsMargins(0, 0, 0, 0)
            valor_layout.setSpacing(8)
            valor_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Ícono de temperatura de agua
            temp_icon = QLabel()
            temp_pixmap = self.load("icons","temperature.png", 16)
            if temp_pixmap:
                temp_icon.setPixmap(temp_pixmap)
            temp_icon.setStyleSheet(f"background-color: {row_bg_color};")
            
            valor_text = QLabel(f"{item['valor']} °C")
            valor_text.setStyleSheet(f"background-color: {row_bg_color};")
            valor_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            valor_layout.addWidget(temp_icon)
            valor_layout.addWidget(valor_text)
            
            self.history_table.setCellWidget(row, 1, valor_cell)
            
            # Columna de estado con ícono
            valor = float(item["valor"])
            if valor < 28:
                estado = "Frío"
                icon_name = "cold.png"
                estado_color = "#1e40af"
            elif valor > 32:
                estado = "Caliente"
                icon_name = "hot.png"
                estado_color = "#b91c1c"
            else:
                estado = "Ambiente"
                icon_name = "good.png"
                estado_color = "#15803d"
            
            estado_cell = QWidget()
            estado_cell.setStyleSheet(cell_style)
            estado_layout = QHBoxLayout(estado_cell)
            estado_layout.setContentsMargins(10, 0, 0, 0)
            estado_layout.setSpacing(8)
            
            estado_icon = QLabel()
            estado_pixmap = self.load("icons",icon_name, 16)
            if estado_pixmap:
                estado_icon.setPixmap(estado_pixmap)
            estado_icon.setStyleSheet(f"background-color: {row_bg_color};")
            
            estado_text = QLabel(estado)
            estado_text.setStyleSheet(f"color: {estado_color}; background-color: {row_bg_color};")
            
            estado_layout.addWidget(estado_icon)
            estado_layout.addWidget(estado_text)
            estado_layout.addStretch()
            
            self.history_table.setCellWidget(row, 2, estado_cell)
            
            # Altura de fila uniforme
            self.history_table.setRowHeight(row, 35)

    def update_status(self, value):
        self.value = float(value)
        if self.value < 28:  
            status_text = "Frío"
            status_style = """
                background-color: #c7f3fd;
                color: #1e40af;
                font-weight: bold;
                font-size: 16px;
                border-radius: 4px;
                padding: 5px;
                margin-top: 10px;
                text-align: center;
            """
        elif self.value > 32:  
            status_text = "Caliente"
            status_style = """
                background-color: #fee2e2;
                color: #b91c1c;
                font-weight: bold;
                font-size: 16px;
                border-radius: 4px;
                padding: 5px;
                margin-top: 10px;
                text-align: center;
            """
        else: 
            status_text = "Ambiente"
            status_style = """
                background-color: #dcfce7;
                color: #166534;
                font-weight: bold;
                font-size: 16px;
                border-radius: 4px;
                padding: 5px;
                margin-top: 10px;
                text-align: center;
            """
        self.status_indicator.setText(status_text)
        self.status_indicator.setStyleSheet(status_style)

    def set_value(self, new_value):
        self.value = float(new_value)
        self.value_label.setText(str(self.value))
        self.update_status(self.value)
        
    def set_table_height(self, height):
        self.table_height = height
        self.history_table.setMinimumHeight(height)
        self.history_table.setMaximumHeight(height)

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
        history_shadow = QGraphicsDropShadowEffect()
        history_shadow.setBlurRadius(15)
        history_shadow.setColor(QColor(0, 0, 0, 40))
        history_shadow.setOffset(0, 3)
        history_panel.setGraphicsEffect(history_shadow)

        history_layout = QVBoxLayout(history_panel)
        history_layout.setContentsMargins(15, 15, 15, 15)
        history_layout.setSpacing(10)

        history_header = QHBoxLayout()
        history_label = QLabel("Historial térmico")
        history_label.setStyleSheet("""
            font-size: 18px;
            color: #074E52;
            font-weight: bold;
        """)
        history_header.addWidget(history_label)
        history_header.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        filter_label = QLabel("Filtrar por:")
        filter_label.setStyleSheet("""
            font-size: 14px;
            color: black;
        """)
        history_header.addWidget(filter_label)

        filter_combo = QComboBox()
        filter_combo.addItems(["Todo", "Frío", "Ambiente", "Caliente"])
        filter_combo.setStyleSheet("""
            QComboBox {
                background-color: #21797a;  
                color: white;  /* Change text color to white */
                padding: 5px 10px;
                border-radius: 6px;
                min-width: 100px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #ddd;
                selection-background-color: #21797a;
                selection-color: white;
            }
            QComboBox::item {
                color: black;
            }
            QComboBox::item:selected {
                color: white;
            }
            QComboBox::item:hover {
                color: white;
            }
        """)
        filter_combo.currentIndexChanged.connect(self.filter_table)  # Connect filter change to filtering function
        history_header.addWidget(filter_combo)
        history_layout.addLayout(history_header)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Temperatura", "Condición"])
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setStyleSheet("""
            QTableView {
                background-color: white;
                gridline-color: #e2e8f0;
                border: none;
                border-radius: 6px;
                selection-background-color: #97DFDB;
                selection-color: black;
                alternate-background-color: #f8fafc;
                color: #1e293b;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #21797a;
                padding: 8px;
                border: none;
                color: white;
                font-size: 15px;
            }
        """)
        self.history_table.setMinimumHeight(self.table_height)
        self.history_table.setMaximumHeight(self.table_height)
        self.populate_table()
        history_layout.addWidget(self.history_table)

        self.filter_combo = filter_combo  # Store the filter combo for later use
        return history_panel

    def filter_table(self):
        filter_text = self.filter_combo.currentText()
        for row in range(self.history_table.rowCount()):
            state_item = self.history_table.item(row, 2)
            if filter_text == "Todo" or state_item.text() == filter_text:
                self.history_table.setRowHidden(row, False)
            else:
                self.history_table.setRowHidden(row, True)
    
    def set_value(self, new_value):
        self.value = float(new_value)
        self.value_label.setText(f"{self.value}°C")
        self.update_status(self.value)
