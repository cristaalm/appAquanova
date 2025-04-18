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
        self.graph_widget = graph_widget  # Recibe la gráfica real como argumento
        self.ph_value = 6.8  # Valor de pH simulado
        self.table_height = 250  # Altura para la tabla
        self.setup_ui()
        self.populate_table()

    def setup_ui(self):
        # Configuración principal del formulario
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #f5f7fa;")
        
        # Layout principal - asegurar que expande verticalmente
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Layout horizontal para los tres paneles
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.create_summary_panel())
        top_layout.addWidget(self.create_graph_panel(), 3)  # Aumentado a 3 para darle más espacio
        top_layout.addWidget(self.create_emotion_panel())
        
        # Añadir el layout superior con factor de estiramiento
        main_layout.addLayout(top_layout, 1)  # Factor 1 para que se expanda
        
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
        
        # Título del panel con icono
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)  # Espacio entre el texto y el icono
        
        ph_title = QLabel("Nivel actual")
        ph_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #074e52;                                
        """)
        title_layout.addWidget(ph_title)
        
        # Icono al lado del título
        title_icon = QLabel()
        icon_pixmap = QPixmap("./resources/icons/gota.png")  # Reemplaza con la ruta a tu icono
        icon_pixmap = icon_pixmap.scaled(22, 22, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        title_icon.setPixmap(icon_pixmap)
        title_layout.addWidget(title_icon)
        
        # Añadir espacio flexible para empujar el icono a la derecha
        title_layout.addStretch()
        
        # Agregar el layout del título al layout principal
        summary_layout.addLayout(title_layout)
        
        # Subtítulo
        ph_subtitle = QLabel("HOY")
        ph_subtitle.setStyleSheet("""
            font-size: 12px;
            font-style: italic;
            color: #6b7280;
        """)
        summary_layout.addWidget(ph_subtitle)
        
        # Área para el valor del pH con icono y unidad
        ph_value_layout = QHBoxLayout()
        ph_value_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icono antes del valor de pH
        value_icon = QLabel()
        value_icon_pixmap = QPixmap("./resources/icons/gota.png")  # Mismo icono o uno diferente
        value_icon_pixmap = value_icon_pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        value_icon.setPixmap(value_icon_pixmap)
        ph_value_layout.addWidget(value_icon)
        
        # Valor numérico del pH
        self.ph_value_label = QLabel(str(self.ph_value))
        self.ph_value_label.setStyleSheet("""
            font-size: 65px;
            font-weight: bold;
            color: #074e52;
        """)
        ph_value_layout.addWidget(self.ph_value_label)
        
        # Unidad pH
        ph_unit_label = QLabel("pH")
        ph_unit_label.setStyleSheet("""
            font-size: 40px;
            font-weight: bold;
            color: #074e52;  
            padding-top: 15px;  /* Ajustar alineación vertical con el número */
            margin-left: -13px;
        """)
        ph_value_layout.addWidget(ph_unit_label)
        
        # Agregar el layout del valor al layout principal
        summary_layout.addLayout(ph_value_layout)
        
        # Etiqueta descriptiva
        ph_status_label = QLabel("Rango entre 6.5 y 7.5")
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
        
        # Establecer política de tamaño para el panel
        graph_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Usar un QVBoxLayout para el contenido
        graph_layout = QVBoxLayout(graph_panel)
        graph_layout.setContentsMargins(15, 15, 15, 15)
        graph_layout.setSpacing(5)
        
        # Título para la gráfica
        graph_title = QLabel("Tendencia del pH")
        graph_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #074e52;
            margin-bottom: 5px;
        """)
        graph_layout.addWidget(graph_title)
        
        # Crear un widget contenedor para la gráfica
        graph_container = QWidget()
        graph_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        container_layout = QVBoxLayout(graph_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        # Asegurarse de que la gráfica tenga la política de tamaño correcta
        self.graph_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Si BaseGraph está basado en matplotlib, esto puede ser necesario
        if hasattr(self.graph_widget, 'canvas'):
            self.graph_widget.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Añadir la gráfica al contenedor
        container_layout.addWidget(self.graph_widget)
        
        # Añadir el contenedor al layout principal con factor de estiramiento
        graph_layout.addWidget(graph_container, 1)
        
        return graph_panel

    def create_emotion_panel(self):
        """Crea el panel que muestra las caritas (estado)."""
        emotion_panel = QFrame()
        emotion_panel.setFrameShape(QFrame.Shape.StyledPanel)
        emotion_panel.setMinimumWidth(100)  # Reducido de 120 a 100
        emotion_panel.setMaximumWidth(150)  # Reducido de 180 a 150
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
        emotion_layout.setSpacing(12)  # Reducido de 15 a 12
        
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
        
        # Carita feliz (verde) - sin fondo de color
        happy_face = QLabel()
        happy_pixmap = QPixmap("./resources/media/feliz.png")
        happy_pixmap = happy_pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        happy_face.setPixmap(happy_pixmap)
        happy_face.setStyleSheet("""
            border-radius: 5px;
            padding: 3px;
        """)
        happy_face.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(happy_face)
        
        # Carita seria (amarilla) - sin fondo de color
        neutral_face = QLabel()
        neutral_pixmap = QPixmap("./resources/media/serio.png")
        neutral_pixmap = neutral_pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        neutral_face.setPixmap(neutral_pixmap)
        neutral_face.setStyleSheet("""
            border-radius: 5px;
            padding: 3px;
        """)
        neutral_face.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(neutral_face)
        
        # Carita triste (roja) - sin fondo de color
        sad_face = QLabel()
        sad_pixmap = QPixmap("./resources/media/triste.png")
        sad_pixmap = sad_pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        sad_face.setPixmap(sad_pixmap)
        sad_face.setStyleSheet("""
            border-radius: 5px;
            padding: 3px;
        """)
        sad_face.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emotion_layout.addWidget(sad_face)
        
        # Espaciador para empujar las caritas hacia arriba
        emotion_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        return emotion_panel

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

        # 1. ENCABEZADO CON TÍTULO Y FILTRO (MANTENIDO)
        history_header = QHBoxLayout()
        
        # Título "Lecturas detalladas"
        history_label = QLabel("Historial de registros")
        history_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #074e52;
        """)
        history_header.addWidget(history_label)
        
        # Espaciador para alinear a la derecha
        history_header.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Etiqueta "Filtrar por fecha:"
        filter_label = QLabel("Filtrar por fecha:")
        filter_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
        """)
        history_header.addWidget(filter_label)

        # Selector de fecha (QDateEdit)
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
        """)
        history_header.addWidget(self.date_filter)
        history_layout.addLayout(history_header)

        # 2. TABLA CON ESTILO MEJORADO (SCROLL Y VISUALIZACIÓN)
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Valor"])
        
        # Configuración de comportamiento
        self.history_table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)  # Scroll suave
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.verticalHeader().setVisible(False)

        # Estilo completo (incluyendo scrollbar)
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
                padding-bottom: 20px
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

        # Asegura que el alto de las filas sea consistente
        self.history_table.verticalHeader().setDefaultSectionSize(40)  
        self.history_table.verticalHeader().setMinimumSectionSize(40)
        # Ajuste de altura
        self.history_table.setMinimumHeight(self.table_height)
        self.history_table.setMaximumHeight(600)
        history_layout.addWidget(self.history_table)

        return history_panel

    def populate_table(self):
        """Llena la tabla con datos de ejemplo (incluyendo íconos)"""
        # Datos de ejemplo (20 registros para forzar scroll)
        data = [
            ("15/04/2024 08:30", "6.8"),
            ("15/04/2024 10:15", "7.1"),
            ("14/04/2024 09:00", "6.9"),
            ("14/04/2024 14:20", "7.2"),
            ("13/04/2024 11:45", "6.7"),
            ("15/04/2024 08:30", "6.8"),
            ("15/04/2024 10:15", "7.1"),
            ("14/04/2024 09:00", "6.9")
            # ... agregar más registros según necesidad
        ]
        
        self.history_table.setRowCount(len(data))
        for row, (fecha, valor) in enumerate(data):
            # Celda de fecha
            fecha_item = QTableWidgetItem(fecha)
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Celda de valor (con ícono si está disponible)
            valor_item = QTableWidgetItem(valor)
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Opcional: Añadir ícono (ajustar ruta)
            icon_path = "resources/icons/ph_icon.png"
            if os.path.exists(icon_path):
                valor_item.setIcon(QIcon(icon_path))
            
            self.history_table.setItem(row, 0, fecha_item)
            self.history_table.setItem(row, 1, valor_item)
            self.history_table.setRowHeight(row, 40)

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
        
    def resizeEvent(self, event):

        """Maneja el evento de redimensión para ajustar tamaños de fuente"""
        super().resizeEvent(event)
        
        # Obtener ancho actual de la card
        card_width = self.width()
        
        # Ajustar tamaños de fuente basados en el ancho de la ventana
        if card_width < 800:
            # Modo compacto
            self.ph_value_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #074e52;")
        else:
            # Modo normal
            self.ph_value_label.setStyleSheet("font-size: 60px; font-weight: bold; color: #074e52;")

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