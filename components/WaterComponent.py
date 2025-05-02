from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QLineEdit, QProgressBar, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QColor, QPixmap, QIcon
from components.lvlWaterGraph import GraphLvlWater


class WaterComponent(QWidget):
    def __init__(self, graph_widget, parent=None):
        super().__init__(parent)
        self.graph_widget = GraphLvlWater()
        self.water_value = 41
        self.water_min = 0
        self.water_max = 50
        self.table_height = 400
        self.setup_ui()
        self.populate_table()

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

        self.setLayout(main_layout)

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
        # Aplicar efecto de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(197, 239, 236))
        shadow.setOffset(0, 3)
        summary_panel.setGraphicsEffect(shadow)

        layout = QVBoxLayout(summary_panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        # Carrusel del título
        self.title_text = "Capacidad disponible de agua                "
        self.title_index = 0

        self.title_label = QLabel(self.title_text)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #045859;")
        self.title_label.setMinimumWidth(150)
        self.title_label.setMaximumWidth(200)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.title_timer = QTimer()
        self.title_timer.timeout.connect(self.scroll_title_text)
        self.title_timer.start(150)

        header_layout.addWidget(self.title_label)

        # Icono
        header_icon = QLabel()
        pixmap = QPixmap("./resources/icons/botella-de-agua.png")
        if not pixmap.isNull():
            header_icon.setPixmap(pixmap.scaled(QSize(28, 28), Qt.AspectRatioMode.KeepAspectRatio))
        header_layout.addWidget(header_icon)

        layout.addLayout(header_layout)

        # Descripción
        description_label = QLabel("Estado del nivel de agua")
        description_label.setStyleSheet("font-size: 12px; font-style: italic; color: #6b7280;")
        layout.addWidget(description_label)

        # Valor
        value_container = QHBoxLayout()
        value_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.state_icon_label = QLabel()
        self.update_state_icon(self.get_water_status())
        self.state_icon_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.state_icon_label.setContentsMargins(0, 8, 0, 0)
        value_container.addWidget(self.state_icon_label)

        self.water_value_label = QLabel(str(self.water_value))
        self.water_value_label.setStyleSheet("font-size: 56px; font-weight: bold; color: #045859;")
        self.water_value_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        value_container.addWidget(self.water_value_label)

        unit_label = QLabel("cm")
        unit_label.setStyleSheet("""
            font-size: 24px;
            color: #045859;
            margin-left: 0px;
            margin-top: 20px;
            font-weight: bold;
        """)
        unit_label.setContentsMargins(-2, 7, 0, 0)
        unit_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        value_container.addWidget(unit_label)

        layout.addLayout(value_container)

        # Etiquetas MIN y MAX
        labels_layout = QHBoxLayout()
        min_label = QLabel("MÍN 0 CM")
        min_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        min_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        labels_layout.addWidget(min_label)
        labels_layout.addStretch()
        max_label = QLabel("MÁX 50 CM")
        max_label.setStyleSheet("font-size: 14px; color: #045859; font-weight: bold;")
        max_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        labels_layout.addWidget(max_label)
        layout.addLayout(labels_layout)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setTextVisible(False)
        percent = min(max(self.water_value / self.water_max, self.water_min), 1) * 100
        self.progress_bar.setValue(int(percent))
        self.progress_bar.setStyleSheet("""
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
        layout.addWidget(self.progress_bar)
        layout.addSpacing(20)

        # Estado con ícono y texto combinados
        self.status_chip_container = QWidget()
        self.status_chip_container.setStyleSheet("""
            background-color: #c5efeb;
            border-radius: 15px;
        """)
        chip_layout = QHBoxLayout(self.status_chip_container)
        chip_layout.setContentsMargins(12, 4, 12, 4)
        chip_layout.setSpacing(8)
        chip_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Imagen de estado
        self.status_icon = QLabel()
        self.status_icon.setFixedSize(24, 24)
        chip_layout.addWidget(self.status_icon)

        # Texto del estado
        self.status_text = QLabel(self.get_water_status())
        self.status_text.setStyleSheet("""
            color: #2b6363;
            font-size: 18px;
            font-weight: bold;
        """)
        chip_layout.addWidget(self.status_text)

        layout.addWidget(self.status_chip_container)


        return summary_panel
    
    def scroll_title_text(self):
        scrolled = self.title_text[self.title_index:] + self.title_text[:self.title_index]
        self.title_label.setText(scrolled)
        self.title_index = (self.title_index + 1) % len(self.title_text)


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
        history_panel = QFrame()
        history_panel.setFrameShape(QFrame.Shape.StyledPanel)
        history_panel.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")
        history_shadow = QGraphicsDropShadowEffect()
        history_shadow.setBlurRadius(15)
        history_shadow.setColor(QColor(197, 239, 236))
        history_shadow.setOffset(0, 3)
        history_panel.setGraphicsEffect(history_shadow)

        layout = QVBoxLayout(history_panel)
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
        layout.addWidget(self.history_table)
        return history_panel

    def populate_table(self):
        self.all_data = [
            ("27/04/2025 08:00", "12.5 cm", "Óptimo"),
            ("27/04/2025 12:00", "9.0 cm", "Bajo"),
            ("27/04/2025 20:00", "18.5 cm", "Óptimo"),
            ("28/04/2025 08:00", "19.2 cm", "Alto"),
            ("27/04/2025 08:00", "12.5 cm", "Óptimo"),
            ("27/04/2025 12:00", "9.0 cm", "Bajo"),
            ("27/04/2025 20:00", "18.5 cm", "Óptimo"),
            ("28/04/2025 08:00", "19.2 cm", "Alto"),
            ("27/04/2025 08:00", "12.5 cm", "Óptimo"),
            ("27/04/2025 12:00", "9.0 cm", "Bajo"),
            ("27/04/2025 20:00", "18.5 cm", "Óptimo"),
            ("28/04/2025 08:00", "19.2 cm", "Alto"),
            ("27/04/2025 08:00", "12.5 cm", "Óptimo"),
            ("27/04/2025 12:00", "9.0 cm", "Bajo"),
            ("27/04/2025 20:00", "18.5 cm", "Óptimo"),
            ("28/04/2025 08:00", "19.2 cm", "Alto"),
        ]

        self.history_table.setRowCount(len(self.all_data))
        for row, (fecha, valor, estado) in enumerate(self.all_data):
            # Columna 1: Fecha y hora
            fecha_item = QTableWidgetItem(fecha)
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.history_table.setItem(row, 0, fecha_item)

            # Columna 2: Nivel (cm) con ícono de botella
            valor_item = QTableWidgetItem(valor)
            valor_item.setIcon(QIcon("./resources/icons/botella-de-agua.png"))  # <- Aquí se agrega el ícono
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.history_table.setItem(row, 1, valor_item)

            # Columna 3: Estado con íconos por nivel
            estado_item = QTableWidgetItem(estado)
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

            if estado == "Bajo":
                estado_item.setIcon(QIcon("./resources/icons/low-water.png"))
                estado_item.setForeground(QColor("#92400e"))
            elif estado == "Óptimo":
                estado_item.setIcon(QIcon("./resources/icons/optimal-water.png"))
                estado_item.setForeground(QColor("#166534"))
            elif estado == "Alto":
                estado_item.setIcon(QIcon("./resources/icons/overflow-water.png"))
                estado_item.setForeground(QColor("#b91c1c"))

            self.history_table.setItem(row, 2, estado_item)
            self.history_table.setRowHeight(row, 35)



    def set_water_value(self, new_value):
        self.water_value = float(new_value)
        self.water_value_label.setText(str(self.water_value))
        self.progress_bar.setValue(min(max(self.water_value / self.water_max, self.water_min), 1) * 100)
        estado = self.get_water_status()
        self.status_text.setText(estado)

        self.status_chip_container.setStyleSheet(f"""
            background-color: {self.get_status_bg_color(estado)};
            border-radius: 15px;
        """)

        self.status_text.setStyleSheet(f"""
            color: {self.get_status_fg_color(estado)};
            font-size: 18px;
            font-weight: bold;
        """)

        self.status_icon.setPixmap(QPixmap(self.get_status_icon_path(estado)).scaled(
            24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))

        self.update_state_icon(self.get_water_status())

    def get_status_icon_path(self, estado):
        if estado == "Bajo":
            return "./resources/icons/low-water.png"
        elif estado == "Óptimo":
            return "./resources/icons/optimal-water.png"
        elif estado == "Alto":
            return "./resources/icons/overflow-water.png"
        return ""

    def get_status_bg_color(self, estado):
        if estado == "Bajo":
            return "#fef3c7"
        elif estado == "Óptimo":
            return "#dcfce7"
        elif estado == "Alto":
            return "#fee2e2"
        return "#c5efeb"

    def get_status_fg_color(self, estado):
        if estado == "Bajo":
            return "#92400e"
        elif estado == "Óptimo":
            return "#166534"
        elif estado == "Alto":
            return "#b91c1c"
        return "#2b6363"

    def update_state_icon(self, estado):
        if estado == "Bajo":
            pixmap = QPixmap("./resources/icons/low-water.png")
        elif estado == "Óptimo":
            pixmap = QPixmap("./resources/icons/optimal-water.png")
        elif estado == "Alto":
            pixmap = QPixmap("./resources/icons/overflow-water.png")
        else:
            pixmap = QPixmap()

        self.state_icon_label.setPixmap(pixmap.scaled(55, 55, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

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

    def get_water_status(self):
        if self.water_value < 20:
            return "Bajo"
        elif self.water_value > 40:
            return "Alto"
        else:
            return "Óptimo"


    def get_status_style(self):
        status = self.get_water_status()
        if status == "Bajo":
            return "background-color: #fef3c7; color: #92400e; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"
        elif status == "Alto":
            return "background-color: #fee2e2; color: #b91c1c; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"
        else:  # Óptimo
            return "background-color: #dcfce7; color: #166534; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"
