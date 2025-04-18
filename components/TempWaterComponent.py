from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QComboBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPixmap
import os 

class tempWaterComponent(QWidget):
    def __init__(self, graph_widget, parent=None):
        super().__init__(parent)
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.graph_widget = graph_widget  
        self.value = 33 #Valor inicial simmulado
        self.table_height = 250  
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #f5f7fa;")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.create_summary_panel())
        top_layout.addWidget(self.create_graph_panel(), 2)
        top_layout.addWidget(self.create_emotion_panel(), 1)
        main_layout.addLayout(top_layout)
        
        # Sección de historial
        main_layout.addWidget(self.create_history_panel())
        
        self.setLayout(main_layout)

    def create_summary_panel(self):
        summary_panel = QFrame()
        summary_panel.setFrameShape(QFrame.Shape.StyledPanel)
        summary_panel.setMinimumWidth(220)
        summary_panel.setMaximumWidth(280)
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
        summary_layout.setContentsMargins(15, 15, 15, 15)
        summary_layout.setSpacing(10)
        
        # Layout horizontal para título + ícono
        title_layout = QHBoxLayout()
        
        # Título
        title_label = QLabel("Temperatura")
        title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #074e52;                                
        """)
        title_layout.addWidget(title_label)
        
        # Espacio elástico para alinear el ícono a la derecha
        title_layout.addStretch()
        
        # Ícono del termómetro
        icon_label = QLabel()
        icon_path = os.path.join(
            self.base_dir,  # Ruta del script actual (components/)
            "..",           # Subir a la carpeta padre (vscode/)
            "resources",    # Entrar a resources/
            "icons",        # Entrar a icons/
            "thermometer.png"
        )
        
        # Cargar y escalar la imagen
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path).scaled(
                24, 
                24, 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            icon_label.setPixmap(pixmap)
        else:
            print(f"Error: No se encontró el ícono en {icon_path}")
        
        title_layout.addWidget(icon_label)
        summary_layout.addLayout(title_layout)  # Añadir el layout horizontal
        
        # Subtítulo
        subtitle = QLabel("Última medición")
        subtitle.setStyleSheet("""
            font-size: 12px;
            font-style: italic;
            color: #6b7280;
        """)
        summary_layout.addWidget(subtitle)
        
        self.value_label = QLabel(f"{self.value}°C")
        self.value_label.setStyleSheet("""
            font-size: 65px;
            font-weight: bold;
            margin: 15px 0;
            color: #074e52;
        """)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.value_label)
        
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
        
        self.status_indicator = QLabel()
        self.update_status(self.value)  
        self.status_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.status_indicator)
        
        summary_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        return summary_panel

    def create_graph_panel(self):
        graph_panel = QFrame()
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
        graph_layout.setContentsMargins(15, 15, 15, 15)
        """        graph_title = QLabel("Tendencia de la tempertarua del agua")
        graph_title.setStyleSheet(
            font-size: 18px;
            font-weight: bold;
            color: #074e52;
            margin-bottom: 5px;
        )
        graph_layout.addWidget(graph_title)"""
        
        self.graph_widget.setMinimumHeight(200)
        self.graph_widget.setMinimumWidth(400)
        graph_layout.addWidget(self.graph_widget)
        
        return graph_panel

    def create_emotion_panel(self):
        emotion_panel = QFrame()
        emotion_panel.setFrameShape(QFrame.Shape.StyledPanel)
        emotion_panel.setMinimumWidth(120)
        emotion_panel.setMaximumWidth(180)
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
        emotion_layout.setContentsMargins(10, 30, 10, 15)
        emotion_layout.setSpacing(15)
        
        # Título del panel de caritas
        emotion_title = QLabel("Estado")
        emotion_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #074e52;
            text-align: center;
        """)
        emotion_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(emotion_title)
        
        # Carita dinámica
        self.emotion_label = QLabel()
        self.emotion_label.setStyleSheet("""
            font-size: 30px;
            border-radius: 5px;
            padding: 5px;
        """)
        self.emotion_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(self.emotion_label)
        
        emotion_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        self.update_emotion(self.value)  # Actualizar la carita según el valor inicial
        
        return emotion_panel

    def update_emotion(self, value):
        if value > 32:
            image_name = "caluroso.png"
        elif value < 28:
            image_name = "frio.png"
        else:
            image_name = "ambiente.png"
        
        # Construir ruta absoluta
        image_path = os.path.join(
            self.base_dir,          # Directorio del componente (components/)
            "..",                   # Subir a la carpeta padre (vscode/)
            "resources",            # Entrar a resources/
            "media",                # Entrar a media/
            image_name              # Nombre del archivo
        )
        
        # Depuración: Verificar ruta
        print(f"Intentando cargar imagen desde: {image_path}")
        
        if not os.path.exists(image_path):
            print(f"Error: La imagen no existe en {image_path}")
            return
        
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: No se pudo cargar la imagen {image_path}")
            return
        
        # Escalar la imagen correctamente
        self.emotion_label.setPixmap(
            pixmap.scaled(
                150, 
                150, 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    def set_value(self, new_value):
        self.value = float(new_value)
        self.value_label.setText(f"{self.value}°C")
        self.update_status(self.value)
        self.update_emotion(self.value)

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
            font-weight: bold;
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
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
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
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Valor", "Estado"])
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
                font-weight: bold;
                color: white;
                font-size: 15px;
            }
            QTableView::item {
                padding: 6px;
                border-bottom: 1px solid #e2e8f0;
            }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 5px;
            }
        """)
        self.history_table.setMinimumHeight(self.table_height)
        self.history_table.setMaximumHeight(self.table_height)
        self.populate_table()
        history_layout.addWidget(self.history_table)
        
        return history_panel

    def populate_table(self):
        data = [
            {"fecha": "10/04/2025 09:00am", "valor": "25"},
            {"fecha": "10/04/2025 12:00pm", "valor": "28"},
            {"fecha": "10/04/2025 03:00pm", "valor": "30"},
            {"fecha": "10/04/2025 06:00pm", "valor": "33"},
        ]
        self.history_table.setRowCount(len(data))
        for row, item in enumerate(data):
            fecha_item = QTableWidgetItem(item["fecha"])
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 0, fecha_item)

            # Añadir "°C" al valor
            valor_item = QTableWidgetItem(f"{item['valor']} °C")
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            valor_font = QFont()
            valor_font.setBold(True)
            valor_item.setFont(valor_font)
            self.history_table.setItem(row, 1, valor_item)

            valor = float(item["valor"])
            if valor < 28:
                estado = "Frío"
                estado_color = {"foreground": "#1e40af"}
            elif valor > 32:
                estado = "Caliente"
                estado_color = {"foreground": "#b91c1c"}
            else:
                estado = "Ambiente"
                estado_color = {"foreground": "#15803d"}

            estado_item = QTableWidgetItem(estado)
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            estado_item.setForeground(QColor(estado_color["foreground"]))
            estado_font = QFont()
            estado_font.setBold(True)
            estado_item.setFont(estado_font)
            self.history_table.setItem(row, 2, estado_item)

            self.history_table.setRowHeight(row, 40)


    def update_status(self, value):
        self.value = float(value)
        if self.value < 28:  # Bajo
            status_text = "Frío"
            status_style = """
                background-color: #fef3c7;
                color: #92400e;
                font-weight: bold;
                font-size: 16px;
                border-radius: 4px;
                padding: 5px;
                margin-top: 10px;
                text-align: center;
            """
        elif self.value > 32:  # Alto
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
        else:  # Óptimo
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
        history_label = QLabel("Registro de temperatura")
        history_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #074E52;
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
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Temperatura", "Estado"])
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
                font-weight: bold;
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
