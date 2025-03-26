from .Graphs.Water.pH import GraphHp as GraphHpWater
from .Graphs.Water.Temp import GraphTemp as GraphTempWater
from .Graphs.Water.LvlWater import GraphLvlWater
from .Graphs.Water.CE import GraphCE as GraphCEWater
from .Graphs.Ambient.Temp import GraphTemp as GraphTempAmbient
from .Graphs.Ambient.humidity import GraphHU as GraphHumidityAmbient
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


class ContentContainer(QWidget):
    def __init__(self):
        super().__init__()
        # Layout principal (vertical)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Parte superior: Título
        self.title_label = QLabel("Bienvenido a el monitor de AquaNova")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar el texto
        self.title_label.setStyleSheet(
            """
            font-size: 20px; 
            font-weight: bold; 
            color: #333333;
            padding: 10px;
            border-bottom: 2px solid #e0e0e0;
        """
        )  # Estilo del título con tema claro
        self.layout.addWidget(self.title_label)

        # Parte central: Contenedor para la gráfica (ocupará solo la parte superior)
        self.graph_container = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_container)
        self.graph_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Centrar la gráfica
        self.graph_layout.setContentsMargins(10, 10, 10, 10)  # Márgenes internos

        # Añadir el contenedor de gráficas al layout principal
        self.layout.addWidget(self.graph_container)

        # Añadir un espaciador que empujará todo hacia arriba
        self.spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.layout.addItem(self.spacer)

        # Configurar tema claro
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(
            QPalette.ColorRole.Window, QColor(240, 240, 240)
        )  # Fondo claro
        palette.setColor(
            QPalette.ColorRole.WindowText, QColor(51, 51, 51)
        )  # Texto oscuro
        palette.setColor(
            QPalette.ColorRole.Base, QColor(255, 255, 255)
        )  # Fondo de widgets
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))  # Texto en widgets
        self.setPalette(palette)

        # Initialize graphs
        self.graph_hp_water = GraphHpWater()
        self.graph_temp_water = GraphTempWater()
        self.graph_lvl_water = GraphLvlWater()
        self.graph_ce_water = GraphCEWater()
        self.graph_temp_ambient = GraphTempAmbient()
        self.graph_humidity_ambient = GraphHumidityAmbient()

        # Instance variable to track content state
        self.content_state = 0

    def update_content(self):
        # Limpiar el contenedor de la gráfica
        for i in reversed(range(self.graph_layout.count())):
            widget = self.graph_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Actualizar el contenido basado en el estado
        if self.content_state == 0:
            self.title_label.setText("Contenido Principal")
            default_msg = QLabel("Seleccione una gráfica")
            default_msg.setStyleSheet("color: #666666; font-size: 16px;")
            self.graph_layout.addWidget(default_msg)
        elif self.content_state == 1:
            self.title_label.setText("Gráfica de Nivel de Agua")
            self.graph_layout.addWidget(self.graph_lvl_water)
        elif self.content_state == 2:
            self.title_label.setText("Gráfica de HP")
            self.graph_layout.addWidget(self.graph_hp_water)
        elif self.content_state == 3:
            self.title_label.setText("Gráfica de Temperatura")
            self.graph_layout.addWidget(self.graph_temp_water)
        elif self.content_state == 4:
            self.title_label.setText("Gráfica de Conductividad")
            self.graph_layout.addWidget(self.graph_ce_water)
        elif self.content_state == 5:
            self.title_label.setText("Gráfica de Temperatura Ambiente")
            self.graph_layout.addWidget(self.graph_temp_ambient)
        elif self.content_state == 6:
            self.title_label.setText("Gráfica de Humedad Ambiente")
            self.graph_layout.addWidget(self.graph_humidity_ambient)
        else:
            self.title_label.setText("Estado Desconocido")
            error_msg = QLabel("Estado no válido")
            error_msg.setStyleSheet("color: #cc0000; font-size: 16px;")
            self.graph_layout.addWidget(error_msg)

    def set_content_state(self, state):
        self.content_state = state
        self.update_content()

    def get_container(self):
        return self
