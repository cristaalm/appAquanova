from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from components.ambient.currentAmbient import CurrentAmbient

class GraphicsAmbient(QMainWindow):
    def __init__(self, temp_graph_panel=None, hum_graph_panel=None, temp_value=None, hum_value=None):
        super().__init__()

        # Crear widget central con layout horizontal
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 0, 15, 0)
        central_widget.setStyleSheet("background-color: white;margin:0;")
        self.setCentralWidget(central_widget)

        # Contenedor de gráficas a la derecha
        graph_container = QWidget()
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.setContentsMargins(0, 0, 0, 0)
        graph_layout.setSpacing(10)

        if temp_graph_panel:
            graph_layout.addWidget(temp_graph_panel, stretch=1)
        if hum_graph_panel:
            graph_layout.addWidget(hum_graph_panel, stretch=1)

        main_layout.addWidget(graph_container, stretch=1)