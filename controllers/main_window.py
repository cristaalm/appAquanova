from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QSplitter
from .Sidebar import Sidebar
from .Container import ContentContainer
from PyQt6.QtCore import QSize, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Basic Window")
        self.resize(1280, 720)  # Tamaño inicial

        # Establecer tamaño mínimo de la ventana
        self.setMinimumSize(
            QSize(800, 500)
        )  # Aumenté el mínimo para mejor visualización

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
        self.central_widget.setLayout(self.layout)

        # Crear un divisor
        self.splitter = QSplitter()
        self.splitter.setHandleWidth(1)  # Hacer la línea divisoria más delgada
        self.layout.addWidget(self.splitter)

        # Crear widgets
        self.content_container = ContentContainer()
        self.sidebar_widget = Sidebar(self.content_container)

        # Añadir widgets al splitter
        self.splitter.addWidget(self.sidebar_widget)
        self.splitter.addWidget(self.content_container.get_container())

        # Configurar comportamiento del splitter
        self.splitter.setCollapsible(0, False)  # Evitar que el sidebar colapse
        self.splitter.setCollapsible(1, False)  # Evitar que el contenido colapse

        # Bloquear el ancho del sidebar
        self.sidebar_width = 250  # Ancho fijo en píxeles
        self.splitter.setSizes([self.sidebar_width, self.width() - self.sidebar_width])

        # Deshabilitar el redimensionamiento del splitter
        splitter_handle = self.splitter.handle(1)
        splitter_handle.setDisabled(True)  # Deshabilitar el handle del splitter

    def resizeEvent(self, event):
        """Mantener el ancho fijo del sidebar al redimensionar la ventana"""
        super().resizeEvent(event)
        # Mantener el ancho del sidebar constante y ajustar solo el contenido
        self.splitter.setSizes([self.sidebar_width, self.width() - self.sidebar_width])
