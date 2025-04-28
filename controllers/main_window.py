from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QSplitter
from .Sidebar import Sidebar
from .Container import ContentContainer
from PyQt6.QtCore import QSize, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AquaNova - Hidroponía")
        # self.resize(1280, 720)  # Tamaño inicial

        # Establecer tamaño mínimo de la ventana
        self.setMinimumSize(QSize(600, 400))  # Tamaño mínimo más pequeño para mejor adaptabilidad

        # Widget central y layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.central_widget.setLayout(self.layout)

        # Crear splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(1)
        self.layout.addWidget(self.splitter)

        # Crear widgets
        self.content_container = ContentContainer()
        self.sidebar_widget = Sidebar(self.content_container)

        # Añadir widgets al splitter
        self.splitter.addWidget(self.sidebar_widget)
        self.splitter.addWidget(self.content_container.get_container())

        # Configurar comportamiento del splitter
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)

        # Configuración inicial de tamaños
        self.sidebar_min_width = 200
        self.sidebar_max_width = 300
       
        # Abrir la ventana en pantalla com        # Bloquear el ancho del sidebar
        self.sidebar_width = 250  # Ancho fijo en píxeles
        self.splitter.setSizes([self.sidebar_width, self.width() - self.sidebar_width])
        
        # Establecer estilos
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #B6F1ED;
                width: 1px;
            }
            QSplitter::handle:hover {
                background-color: #5BC3BA;
            }
        """)

        # Abrir la ventana en pantalla completa al iniciar
        self.showMaximized()
