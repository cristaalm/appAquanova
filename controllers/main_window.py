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
        self.sidebar_width = 250  # Ancho inicial
        
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

        # Conectar señal de movimiento del splitter
        self.splitter.splitterMoved.connect(self.handle_splitter_move)

    def handle_splitter_move(self, pos, index):
        """Manejar el movimiento del splitter para mantener límites"""
        # Asegurarse de que el sidebar no sea más pequeño que el mínimo ni más grande que el máximo
        current_sizes = self.splitter.sizes()
        if current_sizes[0] < self.sidebar_min_width:
            self.splitter.blockSignals(True)
            self.splitter.setSizes([self.sidebar_min_width, current_sizes[1] - (self.sidebar_min_width - current_sizes[0])])
            self.splitter.blockSignals(False)
        elif current_sizes[0] > self.sidebar_max_width:
            self.splitter.blockSignals(True)
            self.splitter.setSizes([self.sidebar_max_width, current_sizes[1] + (current_sizes[0] - self.sidebar_max_width)])
            self.splitter.blockSignals(False)

    def resizeEvent(self, event):
        """Manejar el redimensionamiento de la ventana"""
        super().resizeEvent(event)
        
        # Obtener el tamaño actual del splitter
        current_sizes = self.splitter.sizes()
        
        # Si la ventana es muy pequeña, priorizar el contenido
        if event.size().width() < 800:
            new_sidebar_width = max(self.sidebar_min_width, min(self.sidebar_width, event.size().width() - 400))
            self.splitter.setSizes([new_sidebar_width, event.size().width() - new_sidebar_width])
        else:
            # Mantener proporción relativa del sidebar
            total = sum(current_sizes)
            if total > 0:  # Evitar división por cero
                ratio = current_sizes[0] / total
                new_sidebar_width = int(event.size().width() * ratio)
                new_sidebar_width = max(self.sidebar_min_width, min(new_sidebar_width, self.sidebar_max_width))
                self.splitter.setSizes([new_sidebar_width, event.size().width() - new_sidebar_width])