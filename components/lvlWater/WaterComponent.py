from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QLineEdit, QProgressBar, QGraphicsDropShadowEffect, QPushButton
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QColor, QPixmap, QIcon, QBrush
from components.lvlWater.lvlWaterGraph import GraphLvlWater
import os


class WaterComponent(QWidget):
    def __init__(self, graph_widget, parent=None):
        super().__init__(parent)
        self.graph_widget = GraphLvlWater()
        self.water_value = 35
        self.water_min = 0
        self.water_max = 50
        self.table_height = 400
        self.page_buttons = []
        self.all_data = []
        self.items_per_page = 10
        self.current_page = 0
        self.setup_ui()
        self.populate_table()

    def setup_ui(self):
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #f5f7fa;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 0, 20, 0)
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
        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(197, 239, 236))
        shadow.setOffset(0, 3)
        summary_panel.setGraphicsEffect(shadow)

        layout = QVBoxLayout(summary_panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Título carrusel
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        self.title_text = "Capacidad disponible de agua      "
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

        header_icon = QLabel()
        pixmap = QPixmap("./resources/icons/botella-de-agua.png")
        if not pixmap.isNull():
            header_icon.setPixmap(pixmap.scaled(QSize(28, 28), Qt.AspectRatioMode.KeepAspectRatio))
        header_layout.addWidget(header_icon)

        layout.addLayout(header_layout)

        # Descripción
        description_label = QLabel("Estado de almacenamiento")
        description_label.setStyleSheet("font-size: 12px; font-style: italic; color: #6b7280;")
        layout.addWidget(description_label)

        # Contenedor horizontal para íconos y valores
        value_container = QHBoxLayout()
        value_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_container.setSpacing(4)  # Espacio entre elementos
        value_container.setContentsMargins(0, 0, 0, 0)

        # Ruta correcta a la imagen de gota rellena
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../resources/icons/icon_water.png")

        # Icono de gota rellena
        water_icon_label = QLabel()
        water_icon_pixmap = QPixmap(icon_path)

        if not water_icon_pixmap.isNull():
            water_icon_label.setPixmap(
                water_icon_pixmap.scaled(QSize(60, 60), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            )
        else:
            water_icon_label.setText("○")
            water_icon_label.setStyleSheet("font-size: 24px; color: #045859;")

        # Lo bajamos un poco para alinearlo mejor con el número
        water_icon_label.setContentsMargins(0, 6, 0, 0)
        value_container.addWidget(water_icon_label)

        # Icono de estado
        self.state_icon_label = QLabel()
        self.state_icon_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.state_icon_label.setContentsMargins(0, 8, 0, 0)  # Lo bajamos un poco
        value_container.addWidget(self.state_icon_label)

        # Valor numérico
        self.water_value_label = QLabel(str(self.water_value))
        self.water_value_label.setStyleSheet("font-size: 56px; font-weight: bold; color: #045859; text-align: center;")
        self.water_value_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.water_value_label.setContentsMargins(0, 0, 0, 0)
        value_container.addWidget(self.water_value_label)

        # Unidad (cm)
        unit_label = QLabel("cm")
        unit_label.setStyleSheet("font-size: 24px; color: #045859; margin-left: 0px; margin-top: 20px; font-weight: bold;")
        unit_label.setContentsMargins(0, 6, 0, 0)  # Lo bajamos un poco
        unit_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        value_container.addWidget(unit_label)

        # Agregar al layout principal
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

        # Barra con ícono dinámico encima
        percent = min(max(self.water_value / self.water_max, self.water_min), 1) * 100

        progress_container = QWidget()
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(0)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setTextVisible(False)
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
        progress_layout.addWidget(self.progress_bar)

        layout.addWidget(progress_container)
        layout.addSpacing(20)

        # Chip de estado
        self.status_chip_container = QWidget()
        self.status_chip_container.setStyleSheet("""
            background-color: #c5efeb; 
            border-radius: 15px;
        """)
        chip_layout = QHBoxLayout(self.status_chip_container)
        chip_layout.setContentsMargins(10, 6, 10, 6)
        chip_layout.setSpacing(5)
        chip_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_icon = QLabel()
        self.status_icon.setFixedSize(24, 24)
        chip_layout.addWidget(self.status_icon)

        self.status_text = QLabel("")
        self.status_text.setStyleSheet("""
            color: #2b6363;
            font-size: 18px;
            font-weight: bold;
            background-color: transparent;
        """)
        chip_layout.addWidget(self.status_text)

        layout.addWidget(self.status_chip_container)

        # Actualiza íconos y estado textual al iniciar
        self.update_status_chip()

        return summary_panel

    def get_water_status(self):
        if self.water_value < 20:
            return "Bajo"
        elif self.water_value > 35:
            return "Alto"
        else:
            return "Óptimo"

    def get_level_icon_name(self):
        estado = self.get_water_status()
        if estado == "Bajo":
            return "low-water.png"
        elif estado == "Alto":
            return "overflow-water.png"
        else:
            return "optimal-water.png"

    def update_status_chip(self):
        status = self.get_water_status()
        self.status_text.setText(status)

        if status == "Bajo":
            icon_name = "low-water.png"
            text_style = """
                color: #045859;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            """
        elif status == "Alto":
            icon_name = "overflow-water.png"
            text_style = """
                color: #045859;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            """
        else:
            icon_name = "optimal-water.png"
            text_style = """
                color: #045859;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            """

        icon_path = f"./resources/icons/{icon_name}"
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path).scaled(QSize(24, 24), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.status_icon.setPixmap(pixmap)
        else:
            self.status_icon.setText("●")

        self.status_text.setStyleSheet(text_style)

    
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
                padding-bottom: 0px;
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

        self.history_table.verticalHeader().setDefaultSectionSize(0)  
        self.history_table.verticalHeader().setMinimumSectionSize(0)
        #self.history_table.setMinimumHeight(self.table_height) 
        #self.history_table.setMaximumHeight(600)
        self.history_table.setMinimumHeight(0) 
        self.history_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addWidget(self.history_table)
        pagination_layout = QHBoxLayout()
        pagination_layout.setContentsMargins(0, 4, 0, 4)

        paging_container = QFrame()
        paging_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
            }
        """)
        container_layout = QHBoxLayout(paging_container)
        container_layout.setContentsMargins(4, 0, 4, 0)
        container_layout.setSpacing(4)

        self.prev_button = QPushButton()
        self.prev_button.setIcon(QIcon("./resources/icons/previous.png"))
        self.prev_button.clicked.connect(self.previous_page)
        self.prev_button.setStyleSheet(self.page_button_style())

        self.page_buttons_container = QFrame()
        self.page_buttons_layout = QHBoxLayout(self.page_buttons_container)
        self.page_buttons_layout.setSpacing(2)
        self.page_buttons_layout.setContentsMargins(0, 0, 0, 0)


        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon("./resources/icons/next.png"))
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setStyleSheet(self.page_button_style())

        container_layout.addStretch()
        container_layout.addWidget(self.prev_button)
        container_layout.addWidget(self.page_buttons_container)
        container_layout.addWidget(self.next_button)
        container_layout.addStretch()

        pagination_layout.addWidget(paging_container)
        layout.addLayout(pagination_layout)
        self.update_pagination_controls()

        return history_panel
    
    def page_button_style(self):
        return """
            QPushButton {
                background-color: #f8fafc;
                border: none;
                padding: 4px;
                border-radius: 4px;
                min-width: 28px;
                max-width: 28px;
                min-height: 28px;
                max-height: 28px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton:disabled {
                background-color: #f1f5f9;
                color: #94a3b8;
            }
        """
    def create_page_button(self, page_num, is_current=False):
        button = QPushButton(str(page_num))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#4CA4A5' if is_current else '#f8fafc'};
                color: {'white' if is_current else '#4CA4A5'};
                border: none;
                padding: 4px;
                border-radius: 6px;
                min-width: 28px;
                max-width: 28px;
                min-height: 28px;
                max-height: 28px;
                font-size: 12px;
                font-weight: {'bold' if is_current else 'normal'};
            }}
            QPushButton:hover {{
                background-color: {'#3B8A8B' if is_current else '#e2e8f0'};
            }}
        """)
        button.clicked.connect(lambda: self.go_to_page(page_num - 1))
        return button

    def update_pagination_controls(self):
        self.total_pages = max(1, (len(self.all_data) + self.items_per_page - 1) // self.items_per_page)

        # Limpiar botones anteriores
        layout = self.page_buttons_layout
        while layout.count():
            widget = layout.takeAt(0).widget()
            if widget:
                widget.setParent(None)

        self.page_buttons = []
        for page_num in range(1, self.total_pages + 1):
            button = self.create_page_button(page_num, page_num - 1 == self.current_page)
            self.page_buttons.append(button)
            layout.addWidget(button)

        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self.total_pages - 1)


    def go_to_page(self, page):
        self.current_page = page
        self.populate_table()
        self.update_pagination_controls()


    def next_page(self):
        total_pages = max(1, (len(self.all_data) + self.items_per_page - 1) // self.items_per_page)
        if self.current_page + 1 < total_pages:
            self.current_page += 1
            self.populate_table()
            self.update_pagination_controls()


    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.populate_table()
            self.update_pagination_controls()


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
        ("27/04/2025 09:40", "10.0", "Bajo"),
        ("27/04/2025 09:50", "35.5", "Alto"),
        ("27/04/2025 10:00", "23.4", "Óptimo"),
        ("27/04/2025 10:10", "9.0", "Bajo"),
        ("27/04/2025 10:20", "42.1", "Alto"),
    ]
        self.history_table.setRowCount(0)
        start = self.current_page * self.items_per_page
        end = min(start + self.items_per_page, len(self.all_data))
        page_data = self.all_data[start:end]
        self.history_table.setRowCount(len(page_data))
        for row, (fecha, valor, estado) in enumerate(page_data):
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
                estado_item.setIcon(QIcon("./resources/icons/low-water-blue.png"))
                estado_item.setBackground(QBrush(QColor("#1E89CF")))
                estado_item.setForeground(QColor("#1E89CF"))
            elif estado == "Óptimo":
                estado_item.setIcon(QIcon("./resources/icons/optimal-water-green.png"))
                estado_item.setBackground(QBrush(QColor("#27b061")))
                estado_item.setForeground(QColor("#27b061"))
            elif estado == "Alto":
                estado_item.setIcon(QIcon("./resources/icons/overflow-water-yellow.png"))
                estado_item.setBackground(QBrush(QColor("#f4b400")))
                estado_item.setForeground(QColor("#f4b400"))

            self.history_table.setItem(row, 2, estado_item)
            self.history_table.setRowHeight(row, 31)
        self.update_pagination_controls()

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


    def get_status_style(self):
        status = self.get_water_status()
        if status == "Bajo":
            return "background-color: #fef3c7; color: #92400e; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"
        elif status == "Alto":
            return "background-color: #fee2e2; color: #b91c1c; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"
        else:  # Óptimo
            return "background-color: #dcfce7; color: #166534; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"