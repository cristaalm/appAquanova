from PyQt6.QtWidgets import QVBoxLayout, QWidget, QSplitter, QHBoxLayout
from PyQt6.QtCore import Qt
from components.devices.phCard import PhCard

class DevicesView(QWidget):
    def __init__(self, notification):
        super().__init__()

        # componente de notificaciones global
        self.notification = notification

        # creación de los componentes
        # self.distance_card = DistanceCard()
        self.ph_card = PhCard(self.notification)

        # creación del layout principal vertical
        self.layout = QVBoxLayout()

        # layout para las tarjetas
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Centrarlas horizontalmente

        # agregar las tarjetas
        # self.cards_layout.addWidget(self.distance_card)
        self.cards_layout.addWidget(self.ph_card)

        # creación del splitter
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.splitter.addWidget(QWidget())
        self.splitter.addWidget(QWidget())
        self.splitter.setSizes([1, 1])

        # agregar los layouts al principal
        self.layout.addLayout(self.cards_layout)
        self.layout.addWidget(self.splitter)

        self.setLayout(self.layout)
