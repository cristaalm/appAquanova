from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 App")
        self.setFixedSize(400, 200)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.label = QLabel("Hello, world!", alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)
        self.button = QPushButton("Click me!")
        self.button.clicked.connect(self.on_button_click)
        self.layout.addWidget(self.button)

    def on_button_click(self):
        self.label.setText("Button was clicked!")
