from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QDateEdit, QTableWidgetItem, 
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QComboBox, QGraphicsDropShadowEffect,
    QProgressBar, QStyle, QPushButton, QLineEdit
)
from PyQt6.QtCore import Qt, QSize, QDateTime, QDate, QTimer
from PyQt6.QtGui import QFont, QColor, QIcon, QPixmap, QBrush
from components.phGraph import phGraph
import os

class phComponent(QWidget):
    def __init__(self, graph_widget, parent=None):
        super().__init__(parent)
        self.graph_widget = phGraph()
        self.ph_value = 6.5
        self.table_height = 400
        
        # Definir rangos de pH como constantes
        # Para indicador en la card "ÓPTIMO"/"BAJO"/"ALTO"
        self.PH_MIN_OPTIMAL_INDICATOR = 6.8
        self.PH_MAX_OPTIMAL_INDICATOR = 7.2
        
        # Para rangos en la tabla "ÁCIDO"/"NEUTRO"/"ALCALINO"
        self.PH_MIN_NEUTRAL = 6.5
        self.PH_MAX_NEUTRAL = 7.5
        
        # Texto e índice para el efecto de carrusel del título
        self.title_text = "Potencial de hidrógeno (pH)   "
        self.title_index = 0
        
        self.setup_ui()
        self.populate_table()

    def setup_ui(self):
        # Layout principal con fondo suave
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #f5f7fa;")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Dos paneles superiores en fila con alturas iguales
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)
        top_layout.addWidget(self.create_summary_panel(), 1)
        top_layout.addWidget(self.create_graph_panel(), 4)
        
        main_layout.addLayout(top_layout, 1)
        main_layout.addWidget(self.create_history_panel(), 10)
        main_layout.setContentsMargins(20, 20, 20, 10)

        self.setLayout(main_layout)

    def scroll_title_text(self, label):
        #Función para hacer que el texto del título se desplace como un carrusel
        scrolled = self.title_text[self.title_index:] + self.title_text[:self.title_index]
        label.setText(scrolled)
        self.title_index = (self.title_index + 1) % len(self.title_text)

    def create_summary_panel(self):
        #Crea el panel de resumen del pH
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
        
        # Aplicar efecto de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(197, 239, 236))
        shadow.setOffset(0, 3)
        summary_panel.setGraphicsEffect(shadow)
        
        summary_layout = QVBoxLayout(summary_panel)
        summary_layout.setContentsMargins(15, 15, 15, 15)
        summary_layout.setSpacing(10)
        
        # Título con carrusel
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        # Texto del título con carrusel
        title_label = QLabel(self.title_text)
        title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #045859;
        """)
        title_label.setMinimumWidth(150)
        title_label.setMaximumWidth(200)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        # Iniciar el temporizador para el efecto de carrusel
        self.title_timer = QTimer()
        self.title_timer.timeout.connect(lambda: self.scroll_title_text(title_label))
        self.title_timer.start(150)  # Actualizar cada 150ms
        
        header_layout.addWidget(title_label)
        
        # Añadir espacio para empujar el icono a la derecha
        header_layout.addStretch()
        
        # Icono al lado del título
        icon_label = QLabel()
        icon_pixmap = QPixmap("./resources/icons/ph_icon.png")
        if not icon_pixmap.isNull():
            icon_label.setPixmap(icon_pixmap.scaled(QSize(30, 30), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            # Si el icono no se encuentra, usar un espacio reservado
            icon_label.setText("○")
            icon_label.setStyleSheet("font-size: 20px; color: #045859;")
        
        header_layout.addWidget(icon_label)
        summary_layout.addLayout(header_layout)
        
        # Añadir texto descriptivo debajo del título
        description_label = QLabel("Monitoreo del nivel de acidez del agua")
        description_label.setStyleSheet("""
            font-size: 12px;
            font-style: italic;
            color: #6b7280;
        """)
        summary_layout.addWidget(description_label)
        
        # Añadir espacio adicional
        summary_layout.addSpacing(2)
        
        # Contenedor para el valor pH con icono y unidad
        value_container = QHBoxLayout()
        value_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icono antes del valor
        ph_icon_label = QLabel()
        ph_icon_pixmap = QPixmap("./resources/icons/ph_icon.png")
        if not ph_icon_pixmap.isNull():
            ph_icon_label.setPixmap(ph_icon_pixmap.scaled(QSize(55, 55), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            # Si el icono no se encuentra, usar un espacio reservado
            ph_icon_label.setText("○")
            ph_icon_label.setStyleSheet("font-size: 24px; color: #045859;")
        
        value_container.addWidget(ph_icon_label)
        
        # Valor de pH grande
        self.ph_value_label = QLabel(str(self.ph_value))
        self.ph_value_label.setStyleSheet("""
            font-size: 56px;
            font-weight: bold;
            color: #045859;
            text-align: center;
        """)
        value_container.addWidget(self.ph_value_label)

        ph_unit_label = QLabel("ph")
        ph_unit_label.setStyleSheet("""
            font-size: 24px;
            color: #045859;
            margin-left: 2px;
            margin-top: 20px;
            font-weight: bold;
        """)
        value_container.addWidget(ph_unit_label)
        
        summary_layout.addLayout(value_container)
        summary_layout.addSpacing(5)
        
        # Etiquetas MIN y MAX arriba de la barra
        labels_layout = QHBoxLayout()
        labels_layout.setContentsMargins(0, 0, 0, 0)
        
        # Etiqueta MIN
        min_label = QLabel("MIN")
        min_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        min_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        labels_layout.addWidget(min_label)
        
        # Espaciador
        labels_layout.addStretch()
        
        # Etiqueta MAX
        max_label = QLabel("MÁX")
        max_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        max_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        labels_layout.addWidget(max_label)
        
        summary_layout.addLayout(labels_layout)
        
        # Barra de progreso unificada con QProgressBar
        progress_bar = QProgressBar()
        progress_bar.setFixedHeight(12)
        progress_bar.setTextVisible(False)
        
        # Calcular el valor en porcentaje (0-100) basado en el rango pH (0-14)
        ph_percent = min(max(self.ph_value / 14.0, 0), 1) * 100
        progress_bar.setValue(int(ph_percent))
        
        # Estilo para una barra única con color #045859
        progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #e2e8f0;
                border-radius: 6px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #4CA4A5;
                border-radius: 6px;
            }
        """)
        
        summary_layout.addWidget(progress_bar)
        summary_layout.addSpacing(20)
        
        # Panel de estado 
        self.status_chip = QLabel(self.get_ph_status_text())
        self.status_chip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_chip.setStyleSheet("""
            background-color: #c5efeb; 
            color: #2b6363;
            border-radius: 15px;
            padding: 6px;
            font-size: 18px;
            font-weight: bold;
        """)
        
        summary_layout.addWidget(self.status_chip)
        summary_layout.addStretch()
        
        return summary_panel

    def get_ph_status_text(self):
        #Determina el texto de estado según el valor de pH     
        ph_value = float(self.ph_value)
        if ph_value < self.PH_MIN_OPTIMAL_INDICATOR:
            return "Bajo"
        elif ph_value > self.PH_MAX_OPTIMAL_INDICATOR:
            return "Alto"
        else:
            return "Óptimo"

    def create_graph_panel(self):
        # Panel para gráfica de tendencia con altura fija igual a la del panel de resumen
        graph_panel = QFrame()
        graph_panel.setFrameShape(QFrame.Shape.StyledPanel)
        # Ajustar altura igual a la del panel de pH
        graph_panel.setMinimumHeight(280)
        graph_panel.setFixedHeight(280)
        graph_panel.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")
        
        # Color de la sombra
        graph_shadow = QGraphicsDropShadowEffect()
        graph_shadow.setBlurRadius(15)
        graph_shadow.setColor(QColor(197, 239, 236))
        graph_shadow.setOffset(0, 3)
        graph_panel.setGraphicsEffect(graph_shadow)
        
        graph_layout = QVBoxLayout(graph_panel)
        graph_layout.setContentsMargins(15, 15, 15, 15)
        graph_layout.setSpacing(10)
        
        # Configurar la gráfica para expandirse
        self.graph_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Añadir la gráfica con stretch factor para que ocupe todo el espacio disponible
        graph_layout.addWidget(self.graph_widget, 1)
        
        return graph_panel

    def create_history_panel(self):
        # Panel de historial con tabla de registros
        history_panel = QFrame()
        history_panel.setFrameShape(QFrame.Shape.StyledPanel)
        history_panel.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")

        # Sombra
        history_shadow = QGraphicsDropShadowEffect()
        history_shadow.setBlurRadius(15)
        history_shadow.setColor(QColor(197, 239, 236))
        history_shadow.setOffset(0, 3)
        history_panel.setGraphicsEffect(history_shadow)

        history_layout = QVBoxLayout(history_panel)
        history_layout.setSpacing(10)

        # Encabezado con título y campo de búsqueda
        history_header = QHBoxLayout()
        
        history_label = QLabel("Lecturas")
        history_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #074e52;")
        history_header.addWidget(history_label)
        
        history_header.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Añadir campo de búsqueda
        filter_label = QLabel("Filtrar por:")
        filter_label.setStyleSheet("font-size: 14px; color: #64748b;")
        history_header.addWidget(filter_label)
        
        # Crear un campo de texto para el filtro con ancho menor
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
        
        # Conectar la señal de cambio de texto para filtrar datos
        self.search_filter.textChanged.connect(self.filter_data)
        
        history_header.addWidget(self.search_filter)
        
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

        # Almacenar todos los datos originales para poder filtrar
        self.all_data = []

        return history_panel

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
        
        # Definir los iconos para cada estado
        icono_acido = QIcon("./resources/icons/acido.png")
        icono_neutro = QIcon("./resources/icons/neutro.png")
        icono_alcalino = QIcon("./resources/icons/alcalino.png")
        
        self.history_table.setRowCount(len(self.all_data))
        for row, (fecha, valor, estado) in enumerate(self.all_data):
            # Celda de fecha
            fecha_item = QTableWidgetItem(fecha)
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Celda de valor
            valor_item = QTableWidgetItem(valor)
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Celda de estado con color de fondo según pH
            estado_item = QTableWidgetItem(estado)
            # Cambiar a alineación izquierda
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            
            # Establecer icono según el estado
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
            self.history_table.setRowHeight(row, 35)

    def filter_data(self, text):
        #Filtra los datos de la tabla según el texto ingresado en el campo de búsqueda
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
        #Restablece el filtro para mostrar todos los datos

        # Limpiar el campo de búsqueda
        self.search_filter.clear()
        
        # Mostrar todas las filas
        for row in range(self.history_table.rowCount()):
            self.history_table.showRow(row)

    def set_ph_value(self, new_value):
        # Actualiza el valor y todos los componentes relacionados
        self.ph_value = float(new_value)
        self.ph_value_label.setText(str(self.ph_value))
        
        # Actualiza el estado de pH
        self.update_status_chip(self.ph_value)
        
        # También actualizar la barra de progreso personalizada si es necesario
        
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
            self.ph_value_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #045859;")
        else:
            # Modo normal
            self.ph_value_label.setStyleSheet("font-size: 56px; font-weight: bold; color: #045859;")

    def update_status_chip(self, ph_value):
        # Actualiza el chip de estado según los rangos definidos
        ph_value = float(ph_value)
        if ph_value < self.PH_MIN_OPTIMAL_INDICATOR:  # Bajo
            self.status_chip.setText("Bajo")
            self.status_chip.setStyleSheet("""
                background-color: #fef3c7;
                color: #92400e;
                font-weight: bold;
                font-size: 12px;
                border-radius: 8px;
                padding: 2px 8px;
            """)
        elif ph_value > self.PH_MAX_OPTIMAL_INDICATOR:  # Alto
            self.status_chip.setText("Alto")
            self.status_chip.setStyleSheet("""
                background-color: #fee2e2;
                color: #b91c1c;
                font-weight: bold;
                font-size: 12px;
                border-radius: 8px;
                padding: 2px 8px;
            """)
        else:  # Óptimo
            self.status_chip.setText("Óptimo")
            self.status_chip.setStyleSheet("""
                background-color: #dcfce7;
                color: #166534;
                font-weight: bold;
                font-size: 12px;
                border-radius: 8px;
                padding: 2px 8px;
            """)

    def get_ph_state(self, ph_value):
        # Determina el estado para la tabla de historial
        ph_value = float(ph_value)
        if ph_value < self.PH_MIN_NEUTRAL:
            return "Ácido"
        elif ph_value > self.PH_MAX_NEUTRAL:
            return "Alcalino"
        else:
            return "Neutro"