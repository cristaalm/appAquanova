from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView, QSpacerItem, QSizePolicy,
    QGraphicsDropShadowEffect, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QBrush
from .phConstants import *

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
    
    def setup_ui(self):
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")

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
        
        history_label = QLabel("Lecturas")
        history_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #074e52;")
        header.addWidget(history_label)
        
        header.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        filter_label = QLabel("Filtrar por:")
        filter_label.setStyleSheet("font-size: 14px; color: #64748b;")
        header.addWidget(filter_label)
        
        self.search_filter = QLineEdit()
        self.search_filter.setPlaceholderText("Fecha, valor o estado...")
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
            }            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                height: 0;
                background: none;
            }
        """)
        self.history_table.verticalHeader().setDefaultSectionSize(0)  
        self.history_table.verticalHeader().setMinimumSectionSize(0)
        self.history_table.setMinimumHeight(self.table_height)
        self.history_table.setMaximumHeight(600)
        layout.addWidget(self.history_table)
        
        # Controles de paginación
        pagination_layout = QHBoxLayout()
        pagination_layout.setSpacing(4)
        pagination_layout.setContentsMargins(0, 4, 0, 4)
        
        # Contenedor para la paginación
        pagination_container = QFrame()
        pagination_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
            }
        """)
        container_layout = QHBoxLayout(pagination_container)
        container_layout.setContentsMargins(8, 4, 8, 4)
        container_layout.setSpacing(4)
        
        # Botón Anterior
        self.prev_button = QPushButton()
        self.prev_button.setIcon(QIcon("./resources/icons/previous.png"))
        self.prev_button.setStyleSheet("""
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
        """)
        self.prev_button.clicked.connect(self.previous_page)
        
        # Contenedor para los botones de página
        self.page_buttons_container = QFrame()
        page_buttons_layout = QHBoxLayout(self.page_buttons_container)
        page_buttons_layout.setSpacing(2)  # Reducir el espacio entre botones
        page_buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        # Lista para mantener los botones de página
        self.page_buttons = []
        
        # Botón Siguiente
        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon("./resources/icons/next.png"))
        self.next_button.setStyleSheet("""
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
        """)
        self.next_button.clicked.connect(self.next_page)
        
        container_layout.addStretch()
        container_layout.addWidget(self.prev_button)
        container_layout.addWidget(self.page_buttons_container)
        container_layout.addWidget(self.next_button)
        container_layout.addStretch()
        
        pagination_layout.addWidget(pagination_container)
        layout.addLayout(pagination_layout)
    
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

            valor_item = QTableWidgetItem(valor)
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            valor_item.setIcon(icono_valor)

            if ph_value < PH_MIN_NEUTRAL:
                valor_item.setForeground(QBrush(QColor("#4ca4a5")))
            elif ph_value > PH_MAX_NEUTRAL:
                valor_item.setForeground(QBrush(QColor("#4ca4a5")))
            else:
                valor_item.setForeground(QBrush(QColor("#4ca4a5")))

            estado_item = QTableWidgetItem(estado)
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            
            if estado == "Ácido":
                estado_item.setBackground(QBrush(QColor("#fee2e2")))
                estado_item.setForeground(QBrush(QColor("#d9536f")))
                estado_item.setIcon(icono_acido)
            elif estado == "Alcalino":
                estado_item.setBackground(QBrush(QColor("#fef3c7")))
                estado_item.setForeground(QBrush(QColor("#f4bc19")))
                estado_item.setIcon(icono_alcalino)
            else:  # NEUTRO
                estado_item.setBackground(QBrush(QColor("#dcfce7")))
                estado_item.setForeground(QBrush(QColor("#27b061")))
                estado_item.setIcon(icono_neutro)

            self.history_table.setItem(row, 0, fecha_item)
            self.history_table.setItem(row, 1, valor_item)
            self.history_table.setItem(row, 2, estado_item)
            self.history_table.setRowHeight(row, 28)

        # Actualizar controles de paginación
        self.update_pagination_controls()

    def create_page_button(self, page_num, is_current=False):
        """Crea un botón de página con el estilo apropiado"""
        button = QPushButton(str(page_num))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {('#4CA4A5' if is_current else '#f8fafc')};
                color: {('white' if is_current else '#4CA4A5')};
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
                background-color: {('#3B8A8B' if is_current else '#e2e8f0')};
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
        
        # Crear y agregar los botones de página
        for page_num in visible_pages:
            if page_num == -1:  # Indicador de "..."
                label = QLabel("...")
                label.setStyleSheet("""
                    QLabel {
                        color: #4CA4A5;
                        padding: 8px;
                        min-width: 36px;
                        max-width: 36px;
                        qproperty-alignment: AlignCenter;
                    }
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
            
    def next_page(self):
        """Avanza a la siguiente página"""
        self.go_to_page(self.current_page + 1)

    def previous_page(self):
        """Retrocede a la página anterior"""
        self.go_to_page(self.current_page - 1)
        
    def clear_and_update_table(self, new_data):
        """Actualiza la tabla con nuevos datos"""
        self.all_data = new_data
        self.current_page = 0  # Resetear a la primera página
        self.history_table.clearContents()
        self.history_table.setRowCount(0)
        self.populate_table()
        current_filter = self.search_filter.text()
        if current_filter:
            self.filter_data(current_filter)
    
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