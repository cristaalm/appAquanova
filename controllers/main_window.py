from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QSplitter
from .Sidebar import Sidebar
from .Container import ContentContainer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Basic Window")
        self.setFixedSize(1920, 1080)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout() 
        self.central_widget.setLayout(self.layout)

        # Crear un divisor para dividir la barra lateral y el área de contenido principal
        self.splitter = QSplitter()
        self.layout.addWidget(self.splitter)

        # Crear una instancia de ContentContainer para el área de contenido principal
        self.content_container = ContentContainer()

        # Usar la clase Sidebar para la barra lateral y pasar el contenedor de contenido
        self.sidebar_widget = Sidebar(self.content_container)
        self.splitter.addWidget(self.sidebar_widget)

        self.splitter.addWidget(self.content_container.get_container())

        # Establecer los tamaños iniciales del divisor
        self.splitter.setSizes([int(self.width() * 0.15), int(self.width() * 0.85)])
