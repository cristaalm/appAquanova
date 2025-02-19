from PyQt6.QtWidgets import QVBoxLayout, QWidget, QSpacerItem, QSizePolicy, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class Sidebar(QWidget):
    def __init__(self, content_container):
        super().__init__()
        self.content_container = content_container
        self.sidebar_layout = QVBoxLayout()
        self.setLayout(self.sidebar_layout)

        # Create a layout to center the logo and company name
        self.logo_layout = QVBoxLayout()
        self.sidebar_layout.addLayout(self.logo_layout)

        # Add fixed spacers to limit the height of the logo and company name container
        self.logo_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Add logo and company name to the sidebar
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap("/home/eduarduar/dev/PI/semestre4/interface_setup/media/logo.png")
        self.logo_pixmap = self.logo_pixmap.scaled(32, 32)  # Scale the image to 32x32
        self.logo_label.setPixmap(self.logo_pixmap)
        self.company_name_label = QLabel("AQUA NOVA")
        self.company_name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: lightblue;")  # Change color to light blue

        self.logo_layout.addWidget(self.logo_label, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.logo_layout.addWidget(self.company_name_label, 0, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Add another fixed spacer to limit the height of the logo and company name container
        self.logo_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Add buttons to the sidebar
        self.button1 = QPushButton("Nivel del agua")
        self.button2 = QPushButton("Ph del agua")
        self.button3 = QPushButton("Temperatura")

        # Apply styles to the buttons
        button_style = """
        QPushButton {
            background-color: #1f2027;
            color: white;   
            padding: 15px 30px;
            border: none;
            margin-bottom: 0;
            border-top: 1px solid #4d6c83;
            border-bottom: 1px solid #4d6c83;
        }
        QPushButton:hover {
            background-color: #555;
        }
        """
        self.button1.setStyleSheet(button_style)
        self.button2.setStyleSheet(button_style)
        self.button3.setStyleSheet(button_style)

        self.sidebar_layout.addWidget(self.button1)
        self.sidebar_layout.addWidget(self.button2)
        self.sidebar_layout.addWidget(self.button3)

        # Connect buttons to the set_content_state method
        self.button1.clicked.connect(lambda: self.content_container.set_content_state(1))
        self.button2.clicked.connect(lambda: self.content_container.set_content_state(2))
        self.button3.clicked.connect(lambda: self.content_container.set_content_state(3))

        # Add a spacer to push the buttons to the top
        self.sidebar_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))