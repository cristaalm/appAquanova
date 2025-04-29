from PyQt6.QtWidgets import QVBoxLayout, QWidget, QSplitter
from PyQt6.QtCore import Qt
from components.devices.ph.phCard import PhCard
from components.devices.ce.ceCard import CeCard

class DevicesView(QWidget):
    def __init__(self, notification):
        super().__init__()

        # componente de notificaciones global
        self.notification = notification

        # creación de los componentes
        # self.distance_card = DistanceCard()
        self.ph_card = PhCard(self.notification)
        self.ce_card = CeCard(self.notification)

        # creación del layout principal vertical
        self.layout = QVBoxLayout()

        # layout para las tarjetas
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Centrarlas horizontalmente

        # agregar las tarjetas
        # self.cards_layout.addWidget(self.distance_card)
        self.cards_layout.addWidget(self.ph_card)
        self.cards_layout.addWidget(self.ce_card)

        # creación del splitter
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.splitter.addWidget(QWidget())
        self.splitter.addWidget(QWidget())
        self.splitter.setSizes([1, 1])

        # agregar los layouts al principal
        self.layout.addLayout(self.cards_layout)
        self.layout.addWidget(self.splitter)

        self.setLayout(self.layout)
