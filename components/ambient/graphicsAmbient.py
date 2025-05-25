from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

class GraphicsAmbient(QMainWindow):
    def __init__(self, temp_graph_panel=None, hum_graph_panel=None):
        super().__init__()

        # Crear widget central con layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(15, 0, 15, 0)
        central_widget.setStyleSheet("background-color: white;margin:0;")
        self.setCentralWidget(central_widget)

        # Añadir las gráficas si se proporcionan
        if temp_graph_panel:
            layout.addWidget(temp_graph_panel, stretch=1)

        if hum_graph_panel:
            layout.addWidget(hum_graph_panel, stretch=1)