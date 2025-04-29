from PyQt6.QtWidgets import QVBoxLayout, QWidget, QSplitter, QFrame, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt
from components.devices.ph.phCard import PhCard
from components.devices.ce.ceCard import CeCard
from components.devices.temp.tempCard import TempCard
from components.devices.distance.distanceCard import DistanceCard
from components.devices.ambient.ambientCard import AmbientCard

class DevicesView(QWidget):
    def __init__(self, notification):
        super().__init__()

        # componente de notificaciones global
        self.notification = notification

        # creación de los componentes
        self.distance_card = DistanceCard(self.notification)
        self.ph_card = PhCard(self.notification)
        self.ce_card = CeCard(self.notification)
        self.temp_card = TempCard(self.notification)
        self.ambient_card = AmbientCard(self.notification)

        # creación del layout principal vertical
        self.layout = QVBoxLayout()

        # Widget contenedor para las cards (necesario para QScrollArea)
        self.cards_container = QFrame()
        self.cards_container.setStyleSheet('background: #f0fffe; border: none; padding: 5px;')
        self.cards_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)

        # agregar las tarjetas
        self.cards_layout.addWidget(self.ph_card)
        self.cards_layout.addWidget(self.ce_card)
        self.cards_layout.addWidget(self.temp_card)
        self.cards_layout.addWidget(self.distance_card)
        self.cards_layout.addWidget(self.ambient_card)

        # Scroll Area para las cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setWidget(self.cards_container)
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll_area.setStyleSheet('''
            QScrollArea {
                border: none;
                background: #f0fffe;
                padding: 5px;
            }
            QScrollBar:vertical {
                border: none;
                background: #e0f2fe;
                width: 10px;
                margin: 4px 0 4px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #4ca4a5;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
                background: #f0fffe;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #f0fffe;
            }
        ''')

        # agregar el scroll al layout principal (ocupa todo el espacio)
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)
