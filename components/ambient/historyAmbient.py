from PyQt6.QtWidgets import (
    QFrame, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QGraphicsDropShadowEffect,
    QLineEdit, QTableWidgetItem, QPushButton
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPixmap, QIcon
import os 
from dotenv import load_dotenv
load_dotenv()
COLOR_TEXT = os.getenv("COLOR_TEXT")

class historyAmbient(QFrame):
    def __init__(self, data, parent=None, table_height=300):  
        super().__init__(parent)
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.table_height = table_height 
        
        # Extraer datos del JSON
        self.data = data
        self.temp_data = data.get("temperatura", {}).get("historial", [])
        self.hum_data = data.get("humedad", {}).get("historial", [])
        
        # Obtener rangos
        rango = data.get("rango", {})
        self.temp_min = rango.get("rango_min", 18)
        self.temp_max = rango.get("rango_max", 26)
        
        # Rangos de humedad (puedes ajustar estos valores según tus necesidades)
        self.hum_min = 40  # Humedad mínima ideal
        self.hum_max = 70  # Humedad máxima ideal
        
        # Combinar datos de temperatura y humedad por fecha
        self.combined_data = self.combine_data()
        
        self.items_per_page = 20
        self.current_page = 0
        self.total_pages = max(1, (len(self.combined_data) + self.items_per_page - 1) // self.items_per_page)
        self.current_filter = "Todo" 
        
        self.create_history_panel()
        self.populate_table()

    def combine_data(self):
        """Combina los datos de temperatura y humedad por fecha"""
        combined = []
        
        # Crear un diccionario de humedad indexado por fecha para búsqueda rápida
        hum_dict = {
            item["fecha_ingreso"]: item["valor"]["actual"]
            for item in self.hum_data
            if "valor" in item and isinstance(item["valor"], dict) and "actual" in item["valor"]
        }
        
        # Iterar sobre los datos de temperatura y buscar humedad correspondiente
        for temp_item in self.temp_data:
            fecha = temp_item["fecha_ingreso"]
            combined_item = {
                "fecha_ingreso": fecha,
                "temperatura": temp_item["valor"],
                "humedad": hum_dict.get(fecha, None)  # None si no hay dato de humedad para esa fecha
            }
            combined.append(combined_item)
        
        return combined

    def load(self, path, icon_name, size):
        icon_path = os.path.join(
            self.base_dir,  
            "..",        
            "..",   
            "resources",    
            path,       
            icon_name
        )
        if os.path.exists(icon_path):
            return QPixmap(icon_path).scaled(
                size, 
                size, 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        else:
            print(f"Error: No se encontró el ícono en {icon_path}")
            return None
        
    def create_history_panel(self):
        """Crea el panel de historial con el filtro.""" 

        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)

        history_layout = QVBoxLayout(self)
        
        # Encabezado de historial
        history_header = QHBoxLayout()
        history_label = QLabel("Lecturas")
        history_label.setStyleSheet("""
            font-size: 18px;
            color: #074e52;
            font-weight: bold;
        """)
        history_header.addWidget(history_label)
        history_header.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        filter_label = QLabel("Filtrar por:")
        filter_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
        """)
        history_header.addWidget(filter_label)
        
        self.search_filter = QLineEdit()
        self.search_filter.setPlaceholderText("Fecha, valor o condición...")
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

        history_header.addWidget(self.search_filter)
        history_layout.addLayout(history_header)
        
        # Tabla de historial
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels([
            "Fecha y hora",
            "Temperatura (°C)",
            "Estado temperatura",
            "Humedad (%)",
            "Estado humedad"
        ])
        
        # Asegurar que la tabla ocupe todo el ancho disponible
        self.history_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.history_table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Configurar el estiramiento de columnas para ocupar todo el ancho
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

        self.history_table.verticalHeader().setDefaultSectionSize(25)  
        self.history_table.verticalHeader().setMinimumSectionSize(25)
        self.history_table.setMinimumHeight(self.table_height)
        self.history_table.setMaximumHeight(600)
        
        # Añadir la tabla al contenedor
        history_layout.addWidget(self.history_table)
          
        paging_layout = QHBoxLayout()
        paging_layout.setContentsMargins(0, 4, 0, 4)
        
        # Contenedor para la paginación
        paging_container = QFrame()
        paging_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                margin-top: -1px; 
            }
        """)
        container_layout = QHBoxLayout(paging_container)
        container_layout.setContentsMargins(4, 0, 4, 0)
        container_layout.setSpacing(4)
        
        # Botón Anterior
        self.prev_button = QPushButton()
        prev_icon = self.load("icons", "previous.png", 16)
        if prev_icon:
            self.prev_button.setIcon(QIcon(prev_icon))
        else:
            self.prev_button.setText("<")
            
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
        page_buttons_layout.setSpacing(2)   
        page_buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        # Lista para mantener los botones de página
        self.page_buttons = []
        
        # Botón Siguiente
        self.next_button = QPushButton()
        next_icon = self.load("icons", "next.png", 16)
        if next_icon:
            self.next_button.setIcon(QIcon(next_icon))
        else:
            self.next_button.setText(">")
            
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
        
        paging_layout.addWidget(paging_container)
        
        # Añadir el frame de paginación al layout principal
        history_layout.addLayout(paging_layout)
        
        return self
    
    def populate_table(self):
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.combined_data))
        page_data = self.combined_data[start_idx:end_idx]

        self.history_table.setRowCount(len(page_data))

        for row, item in enumerate(page_data):
            # Fecha
            fecha_item = QTableWidgetItem(item.get("fecha_ingreso", "Sin fecha"))
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.history_table.setItem(row, 0, fecha_item)

            # ----------- Temperatura -----------
            valor_temp = float(item.get("temperatura", 0.0))
            if valor_temp < self.temp_min:
                estado_temp = "Frío"
                icon_temp = "cold.png"
                color_temp = "color: #2980B9;"
            elif valor_temp > self.temp_max:
                estado_temp = "Caliente"
                icon_temp = "hot.png"
                color_temp = "color: #D9534F;"
            else:
                estado_temp = "Ambiente"
                icon_temp = "good.png"
                color_temp = "color: #2ECC71;"

            self.history_table.setCellWidget(row, 1, self.create_icon_text_cell("temp.png", f"{valor_temp:.1f}", color_temp))
            self.history_table.setCellWidget(row, 2, self.create_icon_text_cell(icon_temp, estado_temp, color_temp))

            # ----------- Humedad -----------
            valor_hum = item.get("humedad")
            if valor_hum is not None:
                valor_hum = float(valor_hum)
                if valor_hum < self.hum_min:
                    estado_hum = "Bajo"
                    icon_hum = "cold.png"
                    color_hum = "color: #2980B9;"
                elif valor_hum > self.hum_max:
                    estado_hum = "Alto"
                    icon_hum = "hot.png"
                    color_hum = "color: #D9534F;"
                else:
                    estado_hum = "Ambiente"
                    icon_hum = "good.png"
                    color_hum = "color: #2ECC71;"

                self.history_table.setCellWidget(row, 3, self.create_icon_text_cell("nube.png", f"{valor_hum:.1f}", color_hum))
                self.history_table.setCellWidget(row, 4, self.create_icon_text_cell(icon_hum, estado_hum, color_hum))
            else:
                # No hay datos de humedad para esta fecha
                no_data_item = QTableWidgetItem("Sin dato")
                no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.history_table.setItem(row, 3, no_data_item)
                
                no_data_item2 = QTableWidgetItem("Sin dato")
                no_data_item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.history_table.setItem(row, 4, no_data_item2)

            self.history_table.setRowHeight(row, 28)

        self.update_paging_controls()

    def create_icon_text_cell(self, icon_name, text, style=""):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)

        icon_label = QLabel()
        pixmap = self.load("icons", icon_name, 16)
        if pixmap:
            icon_label.setPixmap(pixmap)

        text_label = QLabel(text)
        text_label.setStyleSheet(f"{style} font-size: 13px;")

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()

        return container

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

    def filter_data(self):
        """Implementa el filtrado de datos"""
        filter_text = self.search_filter.text().lower()
        if not filter_text:
            self.combined_data = self.combine_data()
        else:
            all_data = self.combine_data()
            self.combined_data = []
            for item in all_data:
                # Buscar en fecha, temperatura o humedad
                if (filter_text in item["fecha_ingreso"].lower() or
                    filter_text in str(item["temperatura"]) or
                    (item["humedad"] is not None and filter_text in str(item["humedad"]))):
                    self.combined_data.append(item)
        
        # Actualizar paginación
        self.current_page = 0
        self.total_pages = max(1, (len(self.combined_data) + self.items_per_page - 1) // self.items_per_page)
        self.populate_table()

    def previous_page(self):
        """Ir a la página anterior"""
        if self.current_page > 0:
            self.current_page -= 1
            self.populate_table()

    def next_page(self):
        """Ir a la página siguiente"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.populate_table()

    def go_to_page(self, page_num):
        """Ir a una página específica"""
        if 0 <= page_num < self.total_pages:
            self.current_page = page_num
            self.populate_table()

    def update_paging_controls(self):
        """Actualiza los controles de paginación"""
        # Limpiar botones existentes
        for button in self.page_buttons:
            button.setParent(None)
        self.page_buttons.clear()

        # Actualizar estado de botones anterior/siguiente
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self.total_pages - 1)

        # Crear nuevos botones de página
        layout = self.page_buttons_container.layout()
        for i in range(min(5, self.total_pages)):  # Mostrar máximo 5 botones
            page_num = i + 1
            button = self.create_page_button(page_num, i == self.current_page)
            self.page_buttons.append(button)
            layout.addWidget(button)

    def create_icon_text_cell(self, icon_name, text, style=""):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)

        icon_label = QLabel()
        pixmap = self.load("icons", icon_name, 16)
        if pixmap:
            icon_label.setPixmap(pixmap)

        text_label = QLabel(text)
        text_label.setStyleSheet(f"{style} font-size: 13px;")

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()

        return container

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

    def update_paging_controls(self):
        """Actualiza los controles de paginación"""
        self.total_pages = max(1, (len(self.temp_data) + self.items_per_page - 1) // self.items_per_page)
        
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
            if not hasattr(self, '_cached_range') or self._cached_range_total != total:
                self._cached_range = range(1, total + 1)
                self._cached_range_total = total 
            return [1, 2, 3, 4, 5, -1, total]
        
    def get_visible_pages(self): 
        current = self.current_page + 1
        total = self.total_pages

        if total <= 7: 
            return list(range(1, total + 1))

        if current <= 3: 
            return [1, 2, 3, 4, 5, -1, total]

        if current >= total - 2: 
            return [1, -1, total - 4, total - 3, total - 2, total - 1, total]
        return [1, -1, current - 1, current, current + 1, -1, total]

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

    def filter_data(self, text):
        """Filtra los datos de la tabla según el texto ingresado en el campo de búsqueda"""
        search_text = text.lower()
        
        # Ocultar todas las filas
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
    
    def clear_and_update_table(self, new_data):
        """Actualiza la tabla con nuevos datos, limpiando completamente el contenido anterior"""
        self.temp_data = new_data
        current_page = self.current_page
        self.current_page = 0
        self.history_table.clearContents()
        self.history_table.setRowCount(0)
         
        self.populate_table() 
        current_filter = self.search_filter.text()
        if current_page != self.current_page:
            self.current_page = current_page
            self.populate_table()
        if current_filter:
            self.filter_data(current_filter)
            
    def update_table(self, new_data):
        """Método alternativo que mantiene la compatibilidad con el código existente"""
        self.clear_and_update_table(new_data)