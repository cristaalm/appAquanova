from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QComboBox, QGraphicsDropShadowEffect,
    QDateEdit
)
from PyQt6.QtCore import Qt, QSize, QDate, QDateTime
from PyQt6.QtGui import QFont, QColor, QIcon, QPixmap, QBrush
import pyqtgraph as pg
import os
import random
from dotenv import load_dotenv

load_dotenv()
SHADOW = os.getenv("SHADOW")

class EConductivityComponent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conductivity_value = 1200  # Valor en µS/cm
        self.table_height = 300
        self.history_data = []  # Para almacenar datos históricos
        
        # Inicializar gráfica primero
        self.setup_graph()
        self.setup_ui()
        self.generate_sample_data()
        self.populate_table()

    def setup_ui(self):
        self.setMinimumSize(700, 500)
        self.setStyleSheet("""
            background-color: #f5f7fa;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.create_summary_panel())
        top_layout.addWidget(self.create_graph_panel(), 3)
        top_layout.addWidget(self.create_emotion_panel())
        
        main_layout.addLayout(top_layout, 1)
        main_layout.addWidget(self.create_history_panel())
        
        self.setLayout(main_layout)

    def setup_graph(self):
        """Configura la gráfica con estilo pyqtgraph"""
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground("white")
        
        # Estilo de la gráfica
        style = {"color": "#4B5563", "font-size": "10px"}
        self.graph_widget.setLabel("left", "CE (µS/cm)", **style)
        self.graph_widget.setLabel("bottom", "Tiempo (min)", **style)
        self.graph_widget.showGrid(x=True, y=True, alpha=0.3)
        
        # Configurar eje Y con rango razonable
        self.graph_widget.setYRange(0, 2000)
        
        # Color de la línea (verde azulado)
        self.pen = pg.mkPen(color=(76, 164, 165), width=2.5)
        
        # Inicializar datos vacíos
        self.time = []
        self.ce_data = []

    def generate_sample_data(self):
        """Genera datos de ejemplo para la gráfica y el historial"""
        # Datos para la gráfica
        self.time = list(range(10))
        self.ce_data = [random.randint(800, 1500) for _ in range(10)]
        
        # Crear línea de la gráfica
        self.line = self.graph_widget.plot(
            self.time,
            self.ce_data,
            pen=self.pen,
            symbol="o",
            symbolSize=8,
            symbolBrush="#FFFFFF",
            symbolPen=pg.mkPen(color="#4CA4A5", width=1.5)
        )
        
        # Datos para el historial
        now = QDateTime.currentDateTime()
        self.history_data = []
        for i in range(8):
            value = random.randint(500, 1600)
            timestamp = now.addSecs(-i * 3600)  # Restar horas
            status = self.determine_status(value)
            self.history_data.append((
                timestamp.toString("dd/MM/yyyy hh:mm"),
                str(value),
                status
            ))

    def determine_status(self, value):
        """Determina el estado basado en el valor de CE"""
        if value < 800:
            return "Regular"
        elif value > 1500:
            return "Crítico"
        return "Óptimo"

    def create_summary_panel(self):
        """Panel de resumen con el valor actual"""
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
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 3)
        summary_panel.setGraphicsEffect(shadow)
        
        summary_layout = QVBoxLayout(summary_panel)
        summary_layout.setContentsMargins(20, 20, 20, 20)
        summary_layout.setSpacing(15)
        summary_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Valor y unidad
        value_layout = QVBoxLayout()
        value_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_layout.setSpacing(0)
        
        self.ce_value_label = QLabel(str(self.conductivity_value))
        self.ce_value_label.setStyleSheet("""
            font-size: 48px;
            font-weight: 600;
            color: #074e52;
            padding: 0;
            margin: 0;
        """)
        value_layout.addWidget(self.ce_value_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        unit_label = QLabel("CE (µS/cm)")
        unit_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 500;
            color: #64748b;
            padding: 0;
            margin: 0;
        """)
        value_layout.addWidget(unit_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        summary_layout.addLayout(value_layout)
        
        # Indicador de estado con colores
        self.status_indicator = QLabel()
        self.update_ce_status(self.conductivity_value)
        self.status_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.status_indicator)
        
        summary_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        return summary_panel

    def create_graph_panel(self):
        """Panel con la gráfica pyqtgraph"""
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
        graph_shadow.setColor(QColor(0, 0, 0, 20))
        graph_shadow.setOffset(0, 3)
        graph_panel.setGraphicsEffect(graph_shadow)
        
        graph_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        graph_layout = QVBoxLayout(graph_panel)
        graph_layout.setContentsMargins(15, 15, 15, 15)
        graph_layout.setSpacing(0)
        
        graph_layout.addWidget(self.graph_widget)
        
        return graph_panel

    def create_emotion_panel(self):
        """Panel de estados - solo iconos"""
        emotion_panel = QFrame()
        emotion_panel.setFrameShape(QFrame.Shape.StyledPanel)
        emotion_panel.setMinimumWidth(100)
        emotion_panel.setMaximumWidth(140)
        emotion_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        """)
        
        emotion_shadow = QGraphicsDropShadowEffect()
        emotion_shadow.setBlurRadius(15)
        emotion_shadow.setColor(QColor(0, 0, 0, 20))
        emotion_shadow.setOffset(0, 3)
        emotion_panel.setGraphicsEffect(emotion_shadow)
        
        emotion_layout = QVBoxLayout(emotion_panel)
        emotion_layout.setContentsMargins(15, 15, 15, 15)
        emotion_layout.setSpacing(20)
        emotion_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Iconos de estado
        icon_size = 44
        
        # Crear función auxiliar para cargar íconos
        def create_icon_label(icon_path, tooltip=""):
            label = QLabel()
            if os.path.exists(icon_path):
                pixmap = QPixmap(icon_path)
                pixmap = pixmap.scaled(icon_size, icon_size, 
                                     Qt.AspectRatioMode.KeepAspectRatio, 
                                     Qt.TransformationMode.SmoothTransformation)
                label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if tooltip:
                label.setToolTip(tooltip)
            return label
        
        # Icono óptimo
        optimal_icon = create_icon_label(
            "./resources/media/feliz.png",
            "Condición óptima (800-1500 µS/cm)"
        )
        emotion_layout.addWidget(optimal_icon)
        
        # Icono regular
        regular_icon = create_icon_label(
            "./resources/media/serio.png",
            "Condición regular (<800 µS/cm)"
        )
        emotion_layout.addWidget(regular_icon)
        
        # Icono crítico
        critical_icon = create_icon_label(
            "./resources/media/triste.png",
            "Condición crítica (>1500 µS/cm)"
        )
        emotion_layout.addWidget(critical_icon)
        
        emotion_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        return emotion_panel

    def create_history_panel(self):
        """Panel de historial con estilo mejorado"""
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

        # Encabezado con filtro
        history_header = QHBoxLayout()
        history_label = QLabel("Registros de Conductividad")
        history_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #074e52;
        """)
        history_header.addWidget(history_label)
        history_header.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        filter_label = QLabel("Filtrar por fecha:")
        filter_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
        """)
        history_header.addWidget(filter_label)

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
            QCalendarWidget QToolButton {
                background-color: #4CA4A5;
                color: white;
                border-radius: 4px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #4CA4A5;
            }
            QCalendarWidget QMenu {
                background-color: white;
                color: #4CA4A5;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: black;
                selection-background-color: #4CA4A5;
                selection-color: white;
            }
        """)
        self.date_filter.dateChanged.connect(self.filter_history_by_date)
        history_header.addWidget(self.date_filter)
        history_layout.addLayout(history_header)

        # Tabla de historial
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "CE (µS/cm)", "Estado"])
        
        # Configuración de la tabla
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.verticalHeader().setVisible(False)
        
        # Estilo de la tabla
        self.history_table.setStyleSheet("""
            QTableView {
                background-color: white;
                gridline-color: #c5efec;
                border: none;
                border-radius: 6px;
                selection-background-color: #d4f1f0;
                selection-color: black;
                alternate-background-color: #f8fafc;
                color: #4CA4A5;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #4CA4A5;
                padding: 8px;
                border: none;
                font-weight: bold;
                color: white;
                font-size: 15px;
            }
            QTableView::item {
                padding: 6px;
                border-bottom: 1px solid #c5efec;
                border-top: none;
                border-left: none;
                border-right: none;
            }
            QTableView::item:selected {
                border: none;
                background-color: #d4f1f0;
                color: black;
            }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #4CA4A5;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

        self.history_table.setMinimumHeight(self.table_height)
        self.history_table.setMaximumHeight(600)
        history_layout.addWidget(self.history_table)

        return history_panel

    def populate_table(self):
        """Llena la tabla con datos de ejemplo y estilos"""
        self.history_table.setRowCount(len(self.history_data))
        
        # Cargar íconos si existen
        ce_icon = None
        if os.path.exists("resources/icons/tapon-de-agua-circular.png"):
            ce_icon = QIcon(QPixmap("resources/icons/tapon-de-agua-circular.png").scaled(
                16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        optimal_icon = None
        regular_icon = None
        critical_icon = None
        if os.path.exists("resources/media/feliz.png"):
            optimal_icon = QIcon(QPixmap("resources/media/feliz.png").scaled(
                16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        if os.path.exists("resources/media/serio.png"):
            regular_icon = QIcon(QPixmap("resources/media/serio.png").scaled(
                16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        if os.path.exists("resources/media/triste.png"):
            critical_icon = QIcon(QPixmap("resources/media/triste.png").scaled(
                16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        for i, (fecha, valor, estado) in enumerate(self.history_data):
            # Celda de fecha
            fecha_item = QTableWidgetItem(fecha)
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.history_table.setItem(i, 0, fecha_item)

            # Celda de valor con ícono
            valor_item = QTableWidgetItem(valor)
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
            if ce_icon:
                valor_item.setIcon(ce_icon)
            self.history_table.setItem(i, 1, valor_item)

            # Celda de estado con color e ícono
            estado_item = QTableWidgetItem(estado)
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
            
            if estado == "Óptimo":
                estado_item.setForeground(QBrush(QColor("#166534")))
                if optimal_icon:
                    estado_item.setIcon(optimal_icon)
            elif estado == "Regular":
                estado_item.setForeground(QBrush(QColor("#92400e")))
                if regular_icon:
                    estado_item.setIcon(regular_icon)
            elif estado == "Crítico":
                estado_item.setForeground(QBrush(QColor("#b91c1c")))
                if critical_icon:
                    estado_item.setIcon(critical_icon)
            
            self.history_table.setItem(i, 2, estado_item)

    def filter_history_by_date(self, date):
        """Filtra el historial por fecha seleccionada"""
        filtered_data = [
            data for data in self.history_data 
            if QDate.fromString(data[0].split()[0], "dd/MM/yyyy") == date
        ]
        
        self.history_table.setRowCount(len(filtered_data))
        for i, (fecha, valor, estado) in enumerate(filtered_data):
            self.history_table.setItem(i, 0, QTableWidgetItem(fecha))
            self.history_table.setItem(i, 1, QTableWidgetItem(valor))
            self.history_table.setItem(i, 2, QTableWidgetItem(estado))

    def set_conductivity_value(self, new_value):
        """Actualiza el valor de conductividad"""
        try:
            self.conductivity_value = int(float(new_value))
            self.ce_value_label.setText(str(self.conductivity_value))
            self.update_ce_status(self.conductivity_value)
            
            # Actualizar gráfica
            if hasattr(self, 'time') and hasattr(self, 'ce_data'):
                self.time = self.time[1:] + [self.time[-1] + 1 if self.time else 0]
                self.ce_data = self.ce_data[1:] + [self.conductivity_value]
                self.line.setData(self.time, self.ce_data)
            
            # Añadir al historial
            timestamp = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm")
            status = self.determine_status(self.conductivity_value)
            self.history_data.insert(0, (timestamp, str(self.conductivity_value), status))
            
            # Actualizar tabla
            self.populate_table()
        except (ValueError, TypeError) as e:
            print(f"Error al actualizar valor de conductividad: {e}")
         
    def set_table_height(self, height):
        """Ajusta la altura de la tabla"""
        self.table_height = height
        self.history_table.setMinimumHeight(height)
        self.history_table.setMaximumHeight(height)
        
    def resizeEvent(self, event):
        """Ajusta tamaños al redimensionar"""
        super().resizeEvent(event)
        
        card_width = self.width()
        if card_width < 800:
            self.ce_value_label.setStyleSheet("font-size: 40px; font-weight: 600; color: #074e52;")
        else:
            self.ce_value_label.setStyleSheet("font-size: 48px; font-weight: 600; color: #074e52;")

    def update_ce_status(self, ce_value):
        """Actualiza el indicador de estado con colores"""
        try:
            ce_value = int(float(ce_value))
            status = self.determine_status(ce_value)
            
            if status == "Regular":
                status_text = "Regular"
                status_style = """
                    background-color: #fef3c7;
                    color: #92400e;
                    font-weight: bold;
                    font-size: 14px;
                    border-radius: 4px;
                    padding: 5px;
                    margin-top: 10px;
                    text-align: center;
                """
            elif status == "Crítico":
                status_text = "Crítico"
                status_style = """
                    background-color: #fee2e2;
                    color: #b91c1c;
                    font-weight: bold;
                    font-size: 14px;
                    border-radius: 4px;
                    padding: 5px;
                    margin-top: 10px;
                    text-align: center;
                """
            else:
                status_text = "Óptimo"
                status_style = """
                    background-color: #dcfce7;
                    color: #166534;
                    font-weight: bold;
                    font-size: 14px;
                    border-radius: 4px;
                    padding: 5px;
                    margin-top: 10px;
                    text-align: center;
                """
            
            self.status_indicator.setText(status_text)
            self.status_indicator.setStyleSheet(status_style)
        except (ValueError, TypeError) as e:
            print(f"Error al actualizar estado de CE: {e}")