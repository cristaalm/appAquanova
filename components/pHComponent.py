from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QDateEdit, QTableWidgetItem, 
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QComboBox, QGraphicsDropShadowEffect,
    QProgressBar
)
from PyQt6.QtCore import Qt, QSize, QDateTime, QDate
from PyQt6.QtGui import QFont, QColor, QIcon, QPixmap, QBrush
import os

class phComponent(QWidget):
    def __init__(self, graph_widget, parent=None):
        super().__init__(parent)
        self.graph_widget = graph_widget
        self.ph_value = 6.8
        self.table_height = 400
        
        # Definir rangos de pH como constantes
        # Para indicador en la card "ÓPTIMO"/"BAJO"/"ALTO"
        self.PH_MIN_OPTIMAL_INDICATOR = 6.8
        self.PH_MAX_OPTIMAL_INDICATOR = 7.2
        
        # Para rangos en la tabla "ÁCIDO"/"NEUTRO"/"ALCALINO"
        self.PH_MIN_NEUTRAL = 6.5
        self.PH_MAX_NEUTRAL = 7.5
        
        self.setup_ui()
        self.populate_table()

    def setup_ui(self):
        # Layout principal con fondo suave
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #f5f7fa;")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Tres paneles superiores en fila
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)
        top_layout.addWidget(self.create_summary_panel(), 1)
        top_layout.addWidget(self.create_graph_panel(), 3)
        top_layout.addWidget(self.create_emotion_panel(), 1)
        
        main_layout.addLayout(top_layout, 1)
        main_layout.addWidget(self.create_history_panel(), 10)
        main_layout.setContentsMargins(20, 20, 20, 10)

        self.setLayout(main_layout)

    def create_summary_panel(self):
        # Panel de resumen del pH actual
        summary_panel = QFrame()
        summary_panel.setFrameShape(QFrame.Shape.StyledPanel)
        summary_panel.setMinimumWidth(180)
        summary_panel.setMaximumWidth(280)
        summary_panel.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")
        
        # Efecto de sombra para darle profundidad
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 3)
        summary_panel.setGraphicsEffect(shadow)
        
        summary_layout = QVBoxLayout(summary_panel)
        summary_layout.setContentsMargins(15, 15, 15, 15)
        summary_layout.setSpacing(8)
        
        # Encabezado con ícono
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        
        ph_title = QLabel("Nivel actual")
        ph_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #074e52;")
        title_layout.addWidget(ph_title)
        
        title_icon = QLabel()
        icon_pixmap = QPixmap("./resources/icons/gota.png")
        icon_pixmap = icon_pixmap.scaled(22, 22, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        title_icon.setPixmap(icon_pixmap)
        title_layout.addWidget(title_icon)
        
        title_layout.addStretch()
        summary_layout.addLayout(title_layout)
        
        # Descripción del pH
        ph_subtitle = QLabel("Grado de alcalinidad o acidez")
        ph_subtitle.setStyleSheet("font-size: 12px; font-style: italic; color: #6b7280;")
        summary_layout.addWidget(ph_subtitle)
        
        # Valor con formato grande
        ph_value_layout = QHBoxLayout()
        ph_value_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value_icon = QLabel()
        value_icon_pixmap = QPixmap("./resources/icons/gota.png")
        value_icon_pixmap = value_icon_pixmap.scaled(28, 28, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        value_icon.setPixmap(value_icon_pixmap)
        ph_value_layout.addWidget(value_icon)
        
        self.ph_value_label = QLabel(str(self.ph_value))
        self.ph_value_label.setStyleSheet("font-size: 60px; font-weight: bold; color: #074e52; line-height: 1;")
        ph_value_layout.addWidget(self.ph_value_label)
        
        ph_unit_label = QLabel("pH")
        ph_unit_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #074e52; padding-top: 12px; margin-left: -10px;")
        ph_value_layout.addWidget(ph_unit_label)
        
        summary_layout.addLayout(ph_value_layout)
        
        # Información de rango
        ph_status_label = QLabel("Rango entre 6.5 y 7.5")
        ph_status_label.setStyleSheet("font-style: italic; color: #64748b; font-size: 14px; text-align: center;")
        ph_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(ph_status_label)
        
        # Indicador visual de estado
        self.status_indicator = QLabel()
        self.update_ph_status(self.ph_value)
        self.status_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.status_indicator)
        
        return summary_panel

    def create_graph_panel(self):
        # Panel para gráfica de tendencia
        graph_panel = QFrame()
        graph_panel.setFrameShape(QFrame.Shape.StyledPanel)
        graph_panel.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")
        
        graph_shadow = QGraphicsDropShadowEffect()
        graph_shadow.setBlurRadius(15)
        graph_shadow.setColor(QColor(0, 0, 0, 40))
        graph_shadow.setOffset(0, 3)
        graph_panel.setGraphicsEffect(graph_shadow)
        
        graph_layout = QVBoxLayout(graph_panel)
        graph_layout.setContentsMargins(15, 15, 15, 15)
        graph_layout.setSpacing(10)
        
        graph_title = QLabel("Tendencia del pH")
        graph_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #074e52; margin-bottom: 2px;")
        graph_layout.addWidget(graph_title)
        
        self.graph_widget.setMinimumHeight(180)
        graph_layout.addWidget(self.graph_widget)
        
        return graph_panel

    def create_emotion_panel(self):
        # Panel de caritas que indican estado
        emotion_panel = QFrame()
        emotion_panel.setFrameShape(QFrame.Shape.StyledPanel)
        emotion_panel.setMinimumWidth(150)
        emotion_panel.setMaximumWidth(200)
        emotion_panel.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")
        
        emotion_shadow = QGraphicsDropShadowEffect()
        emotion_shadow.setBlurRadius(15)
        emotion_shadow.setColor(QColor(0, 0, 0, 40))
        emotion_shadow.setOffset(0, 3)
        emotion_panel.setGraphicsEffect(emotion_shadow)
        
        emotion_layout = QVBoxLayout(emotion_panel)
        emotion_layout.setContentsMargins(5, 15, 5, 15)
        emotion_layout.setSpacing(10)
        
        emotion_title = QLabel("Estado")
        emotion_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #074e52; text-align: center;")
        emotion_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(emotion_title)
        
        # Caritas con versión normal y desactivada
        self.happy_face = QLabel()
        self.happy_face_normal = QPixmap("./resources/media/feliz.png")
        self.happy_face_disabled = QPixmap("./resources/media/des_feliz.png")
        self.happy_face_normal = self.happy_face_normal.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.happy_face_disabled = self.happy_face_disabled.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.happy_face.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(self.happy_face)
        
        self.neutral_face = QLabel()
        self.neutral_face_normal = QPixmap("./resources/media/serio.png")
        self.neutral_face_disabled = QPixmap("./resources/media/des_serio.png") 
        self.neutral_face_normal = self.neutral_face_normal.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.neutral_face_disabled = self.neutral_face_disabled.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.neutral_face.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(self.neutral_face)
        
        self.sad_face = QLabel()
        self.sad_face_normal = QPixmap("./resources/media/triste.png")
        self.sad_face_disabled = QPixmap("./resources/media/des_triste.png")
        self.sad_face_normal = self.sad_face_normal.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.sad_face_disabled = self.sad_face_disabled.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.sad_face.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(self.sad_face)
        
        # Inicializar estados de caritas
        self.update_emotion_faces(self.ph_value)
        
        return emotion_panel

    def create_history_panel(self):
        # Panel de historial con tabla de registros
        history_panel = QFrame()
        history_panel.setFrameShape(QFrame.Shape.StyledPanel)
        history_panel.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")

        # Sombra para profundidad visual
        history_shadow = QGraphicsDropShadowEffect()
        history_shadow.setBlurRadius(15)
        history_shadow.setColor(QColor(0, 0, 0, 40))
        history_shadow.setOffset(0, 3)
        history_panel.setGraphicsEffect(history_shadow)

        history_layout = QVBoxLayout(history_panel)
        history_layout.setSpacing(10)

        # Encabezado con título
        history_header = QHBoxLayout()
        
        history_label = QLabel("Historial de registros")
        history_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #074e52;")
        history_header.addWidget(history_label)
        
        history_header.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        history_layout.addLayout(history_header)

        # Tabla de registros históricos
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Valor", "Estado"])
        
        # Configuración de scroll y visualización
        self.history_table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.verticalHeader().setVisible(False)

        # Estilo completo para la tabla
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

        return history_panel

    def populate_table(self):
        # Datos históricos para la tabla
        data = [
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
        
        self.history_table.setRowCount(len(data))
        for row, (fecha, valor, estado) in enumerate(data):
            # Celda de fecha
            fecha_item = QTableWidgetItem(fecha)
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Celda de valor
            valor_item = QTableWidgetItem(valor)
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Celda de estado con color de fondo según pH
            estado_item = QTableWidgetItem(estado)
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Colorear según el estado
            if estado == "ÁCIDO":
                estado_item.setBackground(QBrush(QColor("#fee2e2")))
                estado_item.setForeground(QBrush(QColor("#b91c1c")))
            elif estado == "ALCALINO":
                estado_item.setBackground(QBrush(QColor("#fef3c7")))
                estado_item.setForeground(QBrush(QColor("#92400e")))
            else:  # NEUTRO
                estado_item.setBackground(QBrush(QColor("#dcfce7")))
                estado_item.setForeground(QBrush(QColor("#166534")))
            
            # Ícono opcional
            icon_path = "resources/icons/ph_icon.png"
            if os.path.exists(icon_path):
                valor_item.setIcon(QIcon(icon_path))
            
            self.history_table.setItem(row, 0, fecha_item)
            self.history_table.setItem(row, 1, valor_item)
            self.history_table.setItem(row, 2, estado_item)
            self.history_table.setRowHeight(row, 35)

    def set_ph_value(self, new_value):
        # Actualiza el valor y todos los componentes relacionados
        self.ph_value = float(new_value)
        self.ph_value_label.setText(str(self.ph_value))
        self.update_ph_status(self.ph_value)
        self.update_emotion_faces(self.ph_value)
         
    def set_table_height(self, height):
        # Ajusta la altura de la tabla
        self.table_height = height
        self.history_table.setMinimumHeight(height)
        
    def resizeEvent(self, event):
        # Ajusta tamaños cuando se redimensiona
        super().resizeEvent(event)
        
        card_width = self.width()
        
        if card_width < 800:
            # Modo compacto
            self.ph_value_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #074e52;")
        else:
            # Modo normal
            self.ph_value_label.setStyleSheet("font-size: 60px; font-weight: bold; color: #074e52;")

    def update_ph_status(self, ph_value):
        # Actualiza el indicador de texto usando los rangos definidos
        ph_value = float(ph_value)
        if ph_value < self.PH_MIN_OPTIMAL_INDICATOR:  # Bajo
            status_text = "BAJO"
            status_style = """
                background-color: #fef3c7;
                color: #92400e;
                font-weight: bold;
                font-size: 16px;
                border-radius: 4px;
                padding: 5px;
                margin-top: 5px;
                text-align: center;
            """
        elif ph_value > self.PH_MAX_OPTIMAL_INDICATOR:  # Alto
            status_text = "ALTO"
            status_style = """
                background-color: #fee2e2;
                color: #b91c1c;
                font-weight: bold;
                font-size: 16px;
                border-radius: 4px;
                padding: 5px;
                margin-top: 5px;
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
                margin-top: 5px;
                text-align: center;
            """
        self.status_indicator.setText(status_text)
        self.status_indicator.setStyleSheet(status_style)

    def update_emotion_faces(self, ph_value):
        # Actualiza qué carita está activa según el valor de pH
        ph_value = float(ph_value)
        
        # Determinar qué cara activar según el rango definido
        if ph_value >= self.PH_MIN_OPTIMAL_INDICATOR and ph_value <= self.PH_MAX_OPTIMAL_INDICATOR:  # Óptimo
            self.happy_face.setPixmap(self.happy_face_normal)
            self.neutral_face.setPixmap(self.neutral_face_disabled)
            self.sad_face.setPixmap(self.sad_face_disabled)
        elif ph_value < self.PH_MIN_OPTIMAL_INDICATOR:  # Bajo
            self.happy_face.setPixmap(self.happy_face_disabled)
            self.neutral_face.setPixmap(self.neutral_face_normal)
            self.sad_face.setPixmap(self.sad_face_disabled)
        else:  # Alto
            self.happy_face.setPixmap(self.happy_face_disabled)
            self.neutral_face.setPixmap(self.neutral_face_disabled)
            self.sad_face.setPixmap(self.sad_face_normal)

    def get_ph_state(self, ph_value):
        # Determina el estado para la tabla de historial
        ph_value = float(ph_value)
        if ph_value < self.PH_MIN_NEUTRAL:
            return "ÁCIDO"
        elif ph_value > self.PH_MAX_NEUTRAL:
            return "ALCALINO"
        else:
            return "NEUTRO"