from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QComboBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor

class phComponent(QWidget):
    def __init__(self, graph_widget, parent=None):
        super().__init__(parent)
        self.graph_widget = graph_widget  # Recibe la gráfica real como argumento
        self.ph_value = 7.2  # Valor de pH simulado
        self.table_height = 250  # Altura para la tabla
        self.setup_ui()

    def setup_ui(self):
        # Configuración principal del formulario
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #f5f7fa;")
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Layout horizontal para los tres paneles: resumen, gráfica y caritas
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.create_summary_panel())
        top_layout.addWidget(self.create_graph_panel(), 2)
        top_layout.addWidget(self.create_emotion_panel(), 1)
        main_layout.addLayout(top_layout)
        
        # Sección de historial
        main_layout.addWidget(self.create_history_panel())
        
        self.setLayout(main_layout)

    def create_summary_panel(self):
        """Crea el panel de resumen del pH."""
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
        # Aplicar efecto de sombra para la card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 3)
        summary_panel.setGraphicsEffect(shadow)
        
        summary_layout = QVBoxLayout(summary_panel)
        summary_layout.setContentsMargins(15, 15, 15, 15)
        summary_layout.setSpacing(10)
        
        # Título del panel
        ph_title = QLabel("Nivel de pH")
        ph_title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #074e52;                                
        """)
        summary_layout.addWidget(ph_title)
        
        # Subtítulo
        ph_subtitle = QLabel("HOY")
        ph_subtitle.setStyleSheet("""
            font-size: 16px;
            color: #6b7280;
            margin-top: -5px;
        """)
        summary_layout.addWidget(ph_subtitle)
        
        # Área para el valor del pH
        self.ph_value_label = QLabel(str(self.ph_value))
        self.ph_value_label.setStyleSheet("""
            font-size: 65px;
            font-weight: bold;
            margin: 15px 0;
            color: #074e52;
        """)
        self.ph_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.ph_value_label)
        
        # Etiqueta descriptiva
        ph_status_label = QLabel("Rango entre\n6.5 y 7.5")
        ph_status_label.setStyleSheet("""
            font-style: italic;
            color: #64748b;
            font-size: 15px;
            text-align: center;
        """)
        ph_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(ph_status_label)
        
        # Indicador visual automático basado en el valor del pH
        self.status_indicator = QLabel()
        self.update_ph_status(self.ph_value)  # Actualizar el estado inicial
        self.status_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.status_indicator)
        
        # Espaciador para empujar todo hacia arriba
        summary_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        return summary_panel

    def create_graph_panel(self):
        """Crea el panel de la gráfica."""
        graph_panel = QFrame()
        graph_panel.setFrameShape(QFrame.Shape.StyledPanel)
        graph_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        # Aplicar efecto de sombra para la gráfica
        graph_shadow = QGraphicsDropShadowEffect()
        graph_shadow.setBlurRadius(15)
        graph_shadow.setColor(QColor(0, 0, 0, 40))
        graph_shadow.setOffset(0, 3)
        graph_panel.setGraphicsEffect(graph_shadow)
        
        graph_layout = QVBoxLayout(graph_panel)
        graph_layout.setContentsMargins(15, 15, 15, 15)
        
        # Título para la gráfica
        graph_title = QLabel("Tendencia del pH")
        graph_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #074e52;
            margin-bottom: 5px;
        """)
        graph_layout.addWidget(graph_title)
        
        # Añadir la gráfica real
        self.graph_widget.setMinimumHeight(200)
        graph_layout.addWidget(self.graph_widget)
        
        return graph_panel

    def create_emotion_panel(self):
        """Crea el panel que muestra las caritas (estado)."""
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
        # Aplicar efecto de sombra para el panel de caritas
        emotion_shadow = QGraphicsDropShadowEffect()
        emotion_shadow.setBlurRadius(15)
        emotion_shadow.setColor(QColor(0, 0, 0, 40))
        emotion_shadow.setOffset(0, 3)
        emotion_panel.setGraphicsEffect(emotion_shadow)
        
        emotion_layout = QVBoxLayout(emotion_panel)
        emotion_layout.setContentsMargins(10, 15, 10, 15)
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
        
        # Carita feliz (verde)
        happy_face = QLabel("😀")
        happy_face.setStyleSheet("""
            font-size: 30px;
            background-color: #dcfce7;
            border-radius: 5px;
            padding: 5px;
        """)
        happy_face.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(happy_face)
        
        # Carita seria (amarilla)
        neutral_face = QLabel("😐")
        neutral_face.setStyleSheet("""
            font-size: 30px;
            background-color: #fef3c7;
            border-radius: 5px;
            padding: 5px;
        """)
        neutral_face.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(neutral_face)
        
        # Carita triste (roja)
        sad_face = QLabel("☹️")
        sad_face.setStyleSheet("""
            font-size: 30px;
            background-color: #fee2e2;
            border-radius: 5px;
            padding: 5px;
        """)
        sad_face.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(sad_face)
        
        # Espaciador para empujar las caritas hacia arriba
        emotion_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        return emotion_panel

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
        filter_combo.addItems(["Todo", "Bueno", "Regular", "Malo"])
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
        """Llena la tabla de historial con datos de ejemplo."""
        data = [
            {"fecha": "10/04/2025 09:00am", "valor": "7.2", "estado": "Bueno"},
            {"fecha": "10/04/2025 12:00pm", "valor": "6.9", "estado": "Regular"},
            {"fecha": "10/04/2025 03:00pm", "valor": "7.4", "estado": "Bueno"},
            {"fecha": "10/04/2025 06:00pm", "valor": "7.1", "estado": "Bueno"},
        ]
        self.history_table.setRowCount(len(data))
        for row, item in enumerate(data):
            fecha_item = QTableWidgetItem(item["fecha"])
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 0, fecha_item)

            valor_item = QTableWidgetItem(item["valor"])
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            valor_font = QFont()
            valor_font.setBold(True)
            valor_item.setFont(valor_font)
            self.history_table.setItem(row, 1, valor_item)

            estado_item = QTableWidgetItem(item["estado"])
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if item["estado"] == "Bueno":
                estado_item.setForeground(QColor("#10b981"))
                estado_item.setBackground(QColor("#dcfce7"))
            elif item["estado"] == "Malo":
                estado_item.setForeground(QColor("#ef4444"))
                estado_item.setBackground(QColor("#fee2e2"))
            elif item["estado"] == "Regular":
                estado_item.setForeground(QColor("#f59e0b"))
                estado_item.setBackground(QColor("#fef3c7"))
            estado_font = QFont()
            estado_font.setBold(True)
            estado_item.setFont(estado_font)
            self.history_table.setItem(row, 2, estado_item)

            self.history_table.setRowHeight(row, 40)

    def update_ph_status(self, ph_value):
        """Actualiza el indicador de estado según el valor de pH"""
        ph_value = float(ph_value)
        if ph_value < 6.8:  # Bajo
            status_text = "BAJO"
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
        elif ph_value > 7.2:  # Alto
            status_text = "ALTO"
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
            status_text = "ÓPTIMO"
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

    def set_ph_value(self, new_value):
        """Actualiza el valor de pH y su indicador de estado"""
        self.ph_value = float(new_value)
        self.ph_value_label.setText(str(self.ph_value))
        self.update_ph_status(self.ph_value)
        
    def set_table_height(self, height):
        """Permite ajustar la altura de la tabla dinámicamente"""
        self.table_height = height
        self.history_table.setMinimumHeight(height)
        self.history_table.setMaximumHeight(height)
