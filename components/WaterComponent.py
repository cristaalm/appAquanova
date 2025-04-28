from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QSpacerItem, QSizePolicy, QFrame, QLineEdit, QProgressBar, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPixmap, QIcon, QBrush

class WaterComponent(QWidget):
    def __init__(self, graph_widget, parent=None):
        super().__init__(parent)
        self.graph_widget = graph_widget
        self.water_value = 2.0
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
        summary_panel.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        summary_panel.setGraphicsEffect(shadow)

        layout = QVBoxLayout(summary_panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        title_label = QLabel("Nivel de Agua Actual")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #045859;")
        header_layout.addWidget(title_label)

        header_icon = QLabel()
        pixmap = QPixmap("./resources/icons/botella-de-agua.png")
        if not pixmap.isNull():
            header_icon.setPixmap(pixmap.scaled(QSize(30, 30), Qt.AspectRatioMode.KeepAspectRatio))
        header_layout.addWidget(header_icon)

        layout.addLayout(header_layout)

        description_label = QLabel("Monitoreo de la capacidad del tanque")
        description_label.setStyleSheet("font-size: 12px; font-style: italic; color: #6b7280;")
        layout.addWidget(description_label)

        value_container = QHBoxLayout()
        value_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icono que cambia según estado
        self.state_icon_label = QLabel()
        self.update_state_icon(self.get_water_status())
        self.state_icon_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # Alinear verticalmente
        self.state_icon_label.setContentsMargins(0, 8, 0, 0)  # Bajar ligeramente la imagen si quieres
        value_container.addWidget(self.state_icon_label)

        # Número grande de litros
        self.water_value_label = QLabel(str(self.water_value))
        self.water_value_label.setStyleSheet("font-size: 56px; font-weight: bold; color: #045859;")
        self.water_value_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        value_container.addWidget(self.water_value_label)

        # Unidad "L"
        liter_label = QLabel("L")
        liter_label.setStyleSheet("font-size: 24px; color: #045859; margin-top: 20px; font-weight: bold;")
        liter_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        value_container.addWidget(liter_label)

        layout.addLayout(value_container)

        labels_layout = QHBoxLayout()
        min_label = QLabel("MÍN")
        min_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #045859;")
        labels_layout.addWidget(min_label)
        labels_layout.addStretch()
        max_label = QLabel("MÁX")
        max_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #045859;")
        labels_layout.addWidget(max_label)
        layout.addLayout(labels_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setTextVisible(False)
        percent = min(max(self.water_value / 20.0, 0), 1) * 100
        self.progress_bar.setValue(int(percent))
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #e2e8f0;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background-color: #4CA4A5;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.progress_bar)

        self.status_chip = QLabel(self.get_water_status())
        self.status_chip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_chip.setStyleSheet(self.get_status_style())
        layout.addWidget(self.status_chip)
        layout.addStretch()

        return summary_panel

    def create_graph_panel(self):
        graph_panel = QFrame()
        graph_panel.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 3)
        graph_panel.setGraphicsEffect(shadow)

        layout = QVBoxLayout(graph_panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.addWidget(self.graph_widget)

        return graph_panel

    def create_history_panel(self):
        history_panel = QFrame()
        history_panel.setStyleSheet("QFrame { background-color: white; border-radius: 12px; border: none; }")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 3)
        history_panel.setGraphicsEffect(shadow)

        layout = QVBoxLayout(history_panel)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        label = QLabel("Lecturas detalladas")
        label.setStyleSheet("font-size: 18px; font-weight: bold; color: #074e52;")
        header_layout.addWidget(label)

        header_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        filter_label = QLabel("Filtrar por:")
        filter_label.setStyleSheet("font-size: 14px; color: #64748b;")
        header_layout.addWidget(filter_label)

        self.search_filter = QLineEdit()
        self.search_filter.setPlaceholderText("Filtrar por fecha, nivel o estado...")
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
        self.search_filter.textChanged.connect(self.filter_data)

        header_layout.addWidget(self.search_filter)
        layout.addLayout(header_layout)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Fecha y hora", "Nivel (L)", "Estado"])
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setAlternatingRowColors(True)
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
            }
            QHeaderView::section {
                background-color: #4CA4A5;
                padding: 8px;
                border: none;
                font-weight: bold;
                color: white;
                font-size: 15px;
            }
        """)

        layout.addWidget(self.history_table)
        return history_panel

    def populate_table(self):
        icon_low = QIcon(QPixmap("./resources/icons/low-water.png").scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_medium = QIcon(QPixmap("./resources/icons/medium-water.png").scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_optimal = QIcon(QPixmap("./resources/icons/optimal-water.png").scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_overflow = QIcon(QPixmap("./resources/icons/overflow-water.png").scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        self.all_data = [
            ("27/04/2025 08:00", "12.5", "Óptimo"),
            ("27/04/2025 12:00", "9.0", "Bajo"),
            ("27/04/2025 16:00", "10.5", "Regular"),
            ("27/04/2025 20:00", "18.5", "Óptimo"),
            ("28/04/2025 08:00", "19.2", "Alto"),
            ("27/04/2025 08:00", "12.5", "Óptimo"),
            ("27/04/2025 12:00", "9.0", "Bajo"),
            ("27/04/2025 16:00", "10.5", "Regular"),
            ("27/04/2025 20:00", "18.5", "Óptimo"),
            ("28/04/2025 08:00", "19.2", "Alto"),
        ]

        self.history_table.setRowCount(len(self.all_data))
        for row, (fecha, valor, estado) in enumerate(self.all_data):
            fecha_item = QTableWidgetItem(fecha)
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 0, fecha_item)

            valor_item = QTableWidgetItem(valor)
            valor_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 1, valor_item)

            estado_item = QTableWidgetItem(estado)
            if estado == "Bajo":
                estado_item.setIcon(icon_low)
            elif estado == "Regular":
                estado_item.setIcon(icon_medium)
            elif estado == "Óptimo":
                estado_item.setIcon(icon_optimal)
            elif estado == "Alto":
                estado_item.setIcon(icon_overflow)

            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.history_table.setItem(row, 2, estado_item)
            self.history_table.setRowHeight(row, 36)

    def set_water_value(self, new_value):
        self.water_value = float(new_value)
        self.water_value_label.setText(str(self.water_value))
        self.progress_bar.setValue(min(max(self.water_value / 20.0, 0), 1) * 100)
        self.status_chip.setText(self.get_water_status())
        self.status_chip.setStyleSheet(self.get_status_style())
        self.update_state_icon(self.get_water_status())

    def update_state_icon(self, estado):
        if estado == "Bajo":
            pixmap = QPixmap("./resources/icons/low-water.png")
        elif estado == "Regular":
            pixmap = QPixmap("./resources/icons/medium-water.png")
        elif estado == "Óptimo":
            pixmap = QPixmap("./resources/icons/optimal-water.png")
        elif estado == "Alto":
            pixmap = QPixmap("./resources/icons/overflow-water.png")
        else:
            pixmap = QPixmap()

        self.state_icon_label.setPixmap(pixmap.scaled(55, 55, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def filter_data(self, text):
        text = text.lower()
        for row in range(self.history_table.rowCount()):
            match = False
            for col in range(self.history_table.columnCount()):
                item = self.history_table.item(row, col)
                if item and text in item.text().lower():
                    match = True
                    break
            self.history_table.setRowHidden(row, not match)

    def get_water_status(self):
        if self.water_value < 10:
            return "Bajo"
        elif self.water_value > 18:
            return "Alto"
        elif 10 <= self.water_value < 12.5:
            return "Regular"
        else:
            return "Óptimo"

    def get_status_style(self):
        status = self.get_water_status()
        if status == "Bajo":
            return "background-color: #fef3c7; color: #92400e; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"
        elif status == "Alto":
            return "background-color: #fee2e2; color: #b91c1c; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"
        elif status == "Regular":
            return "background-color: #fef9c3; color: #b45309; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"
        else:
            return "background-color: #dcfce7; color: #166534; font-weight: bold; padding: 6px; border-radius: 15px; font-size: 18px;"
