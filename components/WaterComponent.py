from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QComboBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor

class WaterComponent(QWidget):
    def __init__(self, graph_widget, parent=None):
        super().__init__(parent)
        self.graph_widget = graph_widget
        self.level_value = 14.5 # Nivel de agua simulado en litros
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
        top_layout.addWidget(self.create_graph_panel(), 3)
        top_layout.addWidget(self.create_emotion_panel(), 1)
        main_layout.addLayout(top_layout)

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

        water_title = QLabel("Nivel de Agua")
        water_title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #074e52;                                
        """)
        summary_layout.addWidget(water_title)

        water_subtitle = QLabel("Control de la capacidad de agua")
        water_subtitle.setStyleSheet("""
            font-size: 16px;
            color: #6b7280;
            margin-top: -5px;
        """)
        summary_layout.addWidget(water_subtitle)

        self.level_value_label = QLabel(f"{self.level_value} L")
        self.level_value_label.setStyleSheet("""
            font-size: 65px;
            font-weight: bold;
            margin: 15px 0;
            color: #074e52;
        """)
        self.level_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.level_value_label)

        water_status_label = QLabel("Rango entre\n10L y 18L")
        water_status_label.setStyleSheet("""
            font-style: italic;
            color: #64748b;
            font-size: 15px;
            text-align: center;
        """)
        water_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(water_status_label)

        self.status_indicator = QLabel()
        self.update_level_status(self.level_value)
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

        graph_title = QLabel("Tendencia del Nivel")
        graph_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #074e52;
            margin-bottom: 5px;
        """)
        graph_layout.addWidget(graph_title)

        self.graph_widget.setMinimumHeight(200)
        self.graph_widget.setMinimumWidth(700)  # O más, ajusta a lo que necesites

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
        emotion_layout.setContentsMargins(10, 15, 10, 15)
        emotion_layout.setSpacing(15)

        emotion_title = QLabel("Estado")
        emotion_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #074e52;
            text-align: center;
        """)
        emotion_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(emotion_title)

        happy_face = QLabel("Bueno")
        happy_face.setStyleSheet("""
            font-size: 30px;
            background-color: #dcfce7;
            font-weight: bold;
            border-radius: 5px;
            padding: 5px;
            color: #074e52;
        """)
        happy_face.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(happy_face)

        neutral_face = QLabel("Regular")
        neutral_face.setStyleSheet("""
            font-size: 30px;
            background-color: #fef3c7;
            font-weight: bold;
            border-radius: 5px;
            padding: 5px;
            color: #074e52;
        """)
        neutral_face.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(neutral_face)

        sad_face = QLabel("Malo")
        sad_face.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            background-color: #fee2e2;
            border-radius: 5px;
            padding: 5px;
            color: #074e52;
        """)
        sad_face.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(sad_face)

        emotion_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        return emotion_panel

    def update_level_status(self, level_value):
        level_value = float(level_value)
        if level_value < 10:
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
        elif 10 <= level_value < 12.5:
            status_text = "REGULAR"
            status_style = """
                background-color: #fef9c3;
                color: #b45309;
                font-weight: bold;
                font-size: 16px;
                border-radius: 4px;
                padding: 5px;
                margin-top: 10px;
                text-align: center;
            """
        elif level_value > 18:
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
        else:
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


    def set_level_value(self, new_value):
        self.level_value = float(new_value)
        self.level_value_label.setText(f"{self.level_value} L")
        self.update_level_status(self.level_value)

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
        history_label = QLabel("Historial de registro")
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
            color: #4CA4A5;
        """)
        history_header.addWidget(filter_label)

        filter_combo = QComboBox()
        filter_combo.addItems(["Todo", "Óptimo", "Bajo"])
        filter_combo.setStyleSheet("""
            QComboBox {
                background-color: #4CA4A5;  
                color: #074E52;
                padding: 5px 10px;
                border-radius: 6px;
                min-width: 100px;
                font-size: 14px;
            }
        """)
        history_header.addWidget(filter_combo)
        history_layout.addLayout(history_header)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Nivel (L)", "Estado"])
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
                background-color: #5CA4A5;
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

        return history_panel

    def populate_table(self):
        data = [
            {"fecha": "10/04/2025 09:00am", "valor": "14.2", "estado": "Óptimo"},
            {"fecha": "10/04/2025 12:00pm", "valor": "9.8", "estado": "Bajo"},
            {"fecha": "10/04/2025 03:00pm", "valor": "10.2", "estado": "Regular"},
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
            if item["estado"] == "Óptimo":
                estado_item.setForeground(QColor("#10b981"))
                estado_item.setBackground(QColor("#dcfce7"))
            elif item["estado"] == "Regular":
                estado_item.setForeground(QColor("#b45309"))
                estado_item.setBackground(QColor("#fef9c3"))
            elif item["estado"] == "Bajo":
                estado_item.setForeground(QColor("#ef4444"))
                estado_item.setBackground(QColor("#fee2e2"))
            else:  # Por si en el futuro agregas otro estado como "Alto"
                estado_item.setForeground(QColor("#b91c1c"))
                estado_item.setBackground(QColor("#fee2e2"))
            estado_font = QFont()
            estado_font.setBold(True)
            estado_item.setFont(estado_font)
            self.history_table.setItem(row, 2, estado_item)

            self.history_table.setRowHeight(row, 40)
