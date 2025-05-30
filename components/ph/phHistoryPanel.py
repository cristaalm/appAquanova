from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView, QSpacerItem, QSizePolicy,
    QGraphicsDropShadowEffect, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QBrush
from .phConstants import *
from utils.theme_manager import theme_manager  # Importar el theme manager

class PhHistoryPanel(QFrame):
    def __init__(self, historial=None, parent=None):
        super().__init__(parent)
        self.table_height = 170
        self.all_data = historial if historial is not None else []
        self.items_per_page = 20
        self.current_page = 0
        self.total_pages = max(1, (len(self.all_data) + self.items_per_page - 1) // self.items_per_page)
        
        self.setup_ui()
        self.populate_table()
        
        # Conectar al cambio de tema
        theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme()  # Aplicar tema inicial
    
    def setup_ui(self):
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(SHADOW_COLOR)
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Encabezado con título y búsqueda
        header = QHBoxLayout()
        
        self.history_label = QLabel("Lecturas")
        header.addWidget(self.history_label)
        
        header.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        self.filter_label = QLabel("Filtrar por:")
        header.addWidget(self.filter_label)
        
        self.search_filter = QLineEdit()
        self.search_filter.setPlaceholderText("Fecha, valor o estado...")
        
        self.search_filter.textChanged.connect(self.filter_data)
        header.addWidget(self.search_filter)
        layout.addLayout(header)

        # Tabla
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Medida del pH", "Estado"])
        
        self.history_table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.verticalHeader().setVisible(False)

        self.history_table.verticalHeader().setDefaultSectionSize(25)  
        self.history_table.verticalHeader().setMinimumSectionSize(25)
        self.history_table.setMinimumHeight(self.table_height)
        self.history_table.setMaximumHeight(600)
        layout.addWidget(self.history_table)
        
        # Controles de paginación
        pagination_layout = QHBoxLayout()
        pagination_layout.setSpacing(4)
        pagination_layout.setContentsMargins(0, 4, 0, 4)
        
        # Contenedor para la paginación
        self.pagination_container = QFrame()
        container_layout = QHBoxLayout(self.pagination_container)
        container_layout.setContentsMargins(8, 4, 8, 4)
        container_layout.setSpacing(4)
        
        # Botón Anterior
        self.prev_button = QPushButton()
        self.prev_button.setIcon(QIcon("./resources/icons/previous.png"))
        self.prev_button.clicked.connect(self.previous_page)
        
        # Contenedor para los botones de página
        self.page_buttons_container = QFrame()
        page_buttons_layout = QHBoxLayout(self.page_buttons_container)
        page_buttons_layout.setSpacing(2)
        page_buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        # Lista para mantener los botones de página
        self.page_buttons = []
        
        # Botón Siguiente
        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon("./resources/icons/next.png"))
        self.next_button.clicked.connect(self.next_page)
        
        container_layout.addStretch()
        container_layout.addWidget(self.prev_button)
        container_layout.addWidget(self.page_buttons_container)
        container_layout.addWidget(self.next_button)
        container_layout.addStretch()
        
        pagination_layout.addWidget(self.pagination_container)
        layout.addLayout(pagination_layout)
    
    def apply_theme(self):
        """Aplica el tema actual a todos los componentes"""
        colors = theme_manager.get_theme_colors()
        is_dark = theme_manager.is_dark_mode()
        
        # Estilo del panel principal
        panel_bg = colors['surface'] if is_dark else "white"
        self.setStyleSheet(f"""
        QFrame {{ 
            background-color: {panel_bg}; 
            border-radius: 12px; 
            border: none; 
        }}
        """)
        
        # Estilo del título
        title_color = colors['text_primary']
        self.history_label.setStyleSheet(f"""
        font-size: 18px; 
        font-weight: bold; 
        color: {title_color};
        """)
        
        # Estilo del label de filtro
        self.filter_label.setStyleSheet(f"""
        font-size: 14px; 
        color: {colors['text_secondary']};
        """)
        
        # Estilo del campo de búsqueda
        search_bg = colors['surface'] if is_dark else "white"
        search_border = colors['accent']
        search_text = colors['text_primary']
        self.search_filter.setStyleSheet(f"""
        QLineEdit {{
            background-color: {search_bg};
            border: 1px solid {search_border};
            color: {search_text};
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 14px;
            max-width: 250px;
        }}
        QLineEdit:focus {{
            border: 2px solid {search_border};
        }}
        """)
        
        # Estilo de la tabla
        table_bg = colors['surface'] if is_dark else "white"
        grid_color = "#2A5A5D" if is_dark else "#c5efec"
        selection_bg = "#2A5A5D" if is_dark else "#d4f1f0"
        alternate_bg = "#1A4A4D" if is_dark else "#f8fafc"
        text_color = colors['text_primary']
        header_bg = colors['accent']
        
        self.history_table.setStyleSheet(f"""
        QTableWidget {{
            background-color: {table_bg};
            gridline-color: {grid_color};
            border: none;
            border-radius: 6px;
            selection-background-color: {selection_bg};
            selection-color: {text_color};
            alternate-background-color: {alternate_bg};
            color: {text_color};
            font-size: 14px;
            padding-bottom: 0px;
            margin-right: 5px;
        }}
        QHeaderView::section {{
            background-color: {header_bg};
            padding: 8px;
            border: none;
            font-weight: bold;
            color: white;
            font-size: 15px;
        }}
        QTableWidget::item {{
            padding: 6px;
            border-bottom: 1px solid {grid_color};
        }}
        QScrollBar:vertical {{
            background: {alternate_bg};
            width: 10px;
            border-radius: 5px;
            margin-left: 5px;
        }}
        QScrollBar::handle:vertical {{
            background: {colors['accent']};
            min-height: 30px;
            border-radius: 5px;
        }}
        QScrollBar::add-line:vertical, 
        QScrollBar::sub-line:vertical {{
            height: 0;
            background: none;
        }}
        """)
        
        # Estilo del contenedor de paginación
        self.pagination_container.setStyleSheet(f"""
        QFrame {{
            background-color: {table_bg};
            border-radius: 8px;
        }}
        """)
        
        # Aplicar estilos a los botones de navegación
        self.apply_navigation_button_styles()
        
        # Repoblar la tabla para aplicar los nuevos colores a los elementos
        self.populate_table()
    
    def apply_navigation_button_styles(self):
        """Aplica estilos a los botones de navegación"""
        colors = theme_manager.get_theme_colors()
        is_dark = theme_manager.is_dark_mode()
        
        button_bg = colors['button_bg']
        button_hover = colors['button_hover_bg']
        button_disabled = "#1A4A4D" if is_dark else "#f1f5f9"
        
        nav_button_style = f"""
        QPushButton {{
            background-color: {button_bg};
            border: none;
            padding: 4px;
            border-radius: 4px;
            min-width: 28px;
            max-width: 28px;
            min-height: 28px;
            max-height: 28px;
        }}
        QPushButton:hover {{
            background-color: {button_hover};
        }}
        QPushButton:disabled {{
            background-color: {button_disabled};
            color: #94a3b8;
        }}
        """
        
        self.prev_button.setStyleSheet(nav_button_style)
        self.next_button.setStyleSheet(nav_button_style)
    
    def populate_table(self):
        # Iconos para estados
        icono_acido = QIcon("./resources/icons/acido.png")
        icono_neutro = QIcon("./resources/icons/neutro.png")
        icono_alcalino = QIcon("./resources/icons/alcalino.png")
        icono_valor = QIcon("./resources/icons/ph_icon.png")

        # Calcular índices para la página actual
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.all_data))
        page_data = self.all_data[start_idx:end_idx]

        self.history_table.setRowCount(len(page_data))
        
        # Obtener colores del tema actual
        colors = theme_manager.get_theme_colors()
        text_color = colors['text_primary']
        
        for row, item in enumerate(page_data):
            if isinstance(item, dict):
                fecha = item.get("fecha_ingreso", "")
                valor = str(item.get("valor", ""))
            else:
                fecha, valor = item["fecha_ingreso"], str(item["valor"])

            try:
                ph_value = float(valor)
                estado = self.get_ph_state(ph_value)
            except:
                ph_value = 0
                estado = "N/A"

            fecha_item = QTableWidgetItem(fecha)
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            fecha_item.setForeground(QBrush(QColor(text_color)))

            valor_item = QTableWidgetItem(valor)
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            valor_item.setIcon(icono_valor)
            valor_item.setForeground(QBrush(QColor(colors['accent'])))

            estado_item = QTableWidgetItem(estado)
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            
            # Colores de estado que funcionan bien en ambos temas
            if estado == "Ácido":
                estado_item.setBackground(QBrush(QColor("#fee2e2")))
                estado_item.setForeground(QBrush(QColor("#dc2626")))
                estado_item.setIcon(icono_acido)
            elif estado == "Alcalino":
                estado_item.setBackground(QBrush(QColor("#fef3c7")))
                estado_item.setForeground(QBrush(QColor("#d97706")))
                estado_item.setIcon(icono_alcalino)
            else:  # NEUTRO
                estado_item.setBackground(QBrush(QColor("#dcfce7")))
                estado_item.setForeground(QBrush(QColor("#16a34a")))
                estado_item.setIcon(icono_neutro)

            self.history_table.setItem(row, 0, fecha_item)
            self.history_table.setItem(row, 1, valor_item)
            self.history_table.setItem(row, 2, estado_item)
            self.history_table.setRowHeight(row, 28)

        # Actualizar controles de paginación
        self.update_pagination_controls()

    def create_page_button(self, page_num, is_current=False):
        """Crea un botón de página con el estilo apropiado"""
        colors = theme_manager.get_theme_colors()
        
        button = QPushButton(str(page_num))
        
        if is_current:
            bg_color = colors['accent']
            text_color = "white"
            hover_color = "#3B8A8B"
        else:
            bg_color = colors['button_bg']
            text_color = colors['accent']
            hover_color = colors['button_hover_bg']
        
        button.setStyleSheet(f"""
        QPushButton {{
            background-color: {bg_color};
            color: {text_color};
            border: none;
            padding: 4px;
            border-radius: 4px;
            font-weight: {'bold' if is_current else 'normal'};
            min-width: 28px;
            max-width: 28px;
            min-height: 28px;
            max-height: 28px;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        """)
        button.clicked.connect(lambda: self.go_to_page(page_num - 1))
        return button

    def update_pagination_controls(self):
        """Actualiza los controles de paginación"""
        self.total_pages = max(1, (len(self.all_data) + self.items_per_page - 1) // self.items_per_page)
        
        # Limpiar botones existentes
        for button in self.page_buttons:
            self.page_buttons_container.layout().removeWidget(button)
            button.deleteLater()
        self.page_buttons.clear()
        
        # Determinar qué páginas mostrar
        visible_pages = self.get_visible_pages()
        
        # Obtener colores del tema
        colors = theme_manager.get_theme_colors()
        
        # Crear y agregar los botones de página
        for page_num in visible_pages:
            if page_num == -1:  # Indicador de "..."
                label = QLabel("...")
                label.setStyleSheet(f"""
                QLabel {{
                    color: {colors['accent']};
                    padding: 8px;
                    min-width: 36px;
                    max-width: 36px;
                    qproperty-alignment: AlignCenter;
                }}
                """)
                self.page_buttons.append(label)
                self.page_buttons_container.layout().addWidget(label)
            else:
                button = self.create_page_button(page_num, page_num - 1 == self.current_page)
                self.page_buttons.append(button)
                self.page_buttons_container.layout().addWidget(button)
        
        # Actualizar estado de los botones de navegación
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self.total_pages - 1)

    def get_visible_pages(self):
        """Determina qué números de página mostrar"""
        current = self.current_page + 1
        total = self.total_pages
        
        if total <= 7:
            return range(1, total + 1)
        
        if current <= 4:
            return [1, 2, 3, 4, 5, -1, total]
        if current >= total - 3:
            return [1, -1, total-4, total-3, total-2, total-1, total]
            
        return [1, -1, current-1, current, current+1, -1, total]

    def go_to_page(self, page):
        """Va a una página específica"""
        if 0 <= page < self.total_pages and page != self.current_page:
            self.current_page = page
            self.populate_table()
            self.update_pagination_label()
            
    def next_page(self):
        """Avanza a la siguiente página"""
        self.go_to_page(self.current_page + 1)
    
    def previous_page(self):
        """Retrocede a la página anterior"""
        self.go_to_page(self.current_page - 1)
        
    def clear_and_update_table(self, new_data):
        """Actualiza la tabla con nuevos datos sin afectar otros componentes"""
        self.all_data = new_data
        self.current_page = 0
        self.total_pages = max(1, -(-len(self.all_data) // self.items_per_page))  # Ceiling division
        self.populate_table()
        self.update_pagination_controls()
        self.update_pagination_label()

    def filter_data(self, text):
        search_text = text.lower()
        
        for row in range(self.history_table.rowCount()):
            self.history_table.hideRow(row)
        
        for row in range(self.history_table.rowCount()):
            show_row = False
            
            for col in range(self.history_table.columnCount()):
                item = self.history_table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            
            if show_row or search_text == "":
                self.history_table.showRow(row)
    
    def get_ph_state(self, ph_value):
        ph_value = float(ph_value)
        if ph_value < PH_MIN_NEUTRAL:
            return "Ácido"
        elif ph_value > PH_MAX_NEUTRAL:
            return "Alcalino"
        else:
            return "Neutro"
    
    def update_pagination_label(self):
        """Actualiza la etiqueta de paginación con el conteo actual"""
        start_idx = self.current_page * self.items_per_page + 1
        end_idx = min((self.current_page + 1) * self.items_per_page, len(self.all_data))
        total = len(self.all_data)
        
        pagination_text = f"Mostrando {start_idx}-{end_idx} de {total}"
        self.setStatusTip(pagination_text)