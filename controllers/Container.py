from .Graphs.Hp import GraphHp
from .Graphs.Temp import GraphTemp
from .Graphs.LvlWater import GraphLvlWater
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class ContentContainer(QWidget):
    def __init__(self):
        super().__init__()
        # Layout principal (vertical)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Parte superior: Título
        self.title_label = QLabel("Título del Contenedor")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar el texto
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")  # Estilo del título
        self.layout.addWidget(self.title_label)

        # Parte inferior: Contenedor para la gráfica
        self.graph_container = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_container)
        self.graph_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar la gráfica
        self.layout.addWidget(self.graph_container)

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 48))  # Soft dark color
        self.setPalette(palette)

        # Initialize graphs
        self.graph_hp = GraphHp()
        self.graph_temp = GraphTemp()
        self.graph_lvl_water = GraphLvlWater()

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
            self.graph_layout.addWidget(QLabel("Seleccione una gráfica"))  # Mensaje predeterminado
        elif self.content_state == 1:
            self.title_label.setText("Gráfica de Nivel de Agua")
            self.graph_layout.addWidget(self.graph_lvl_water)
        elif self.content_state == 2:
            self.title_label.setText("Gráfica de HP")
            self.graph_layout.addWidget(self.graph_hp)
        elif self.content_state == 3:
            self.title_label.setText("Gráfica de Temperatura")
            self.graph_layout.addWidget(self.graph_temp)
        else:
            self.title_label.setText("Estado Desconocido")
            self.graph_layout.addWidget(QLabel("Estado no válido"))

    def set_content_state(self, state):
        self.content_state = state
        self.update_content()

    def get_container(self):
        return self