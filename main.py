import os
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QCursor
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve

# === Django Setup ===
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, "backend")
sys.path.append(backend_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django

django.setup()

from controllers.main_window import MainWindow
from dotenv import load_dotenv

load_dotenv()
COLOR_C8F5F2 = os.getenv("COLOR_C8F5F2")
COLOR_074E52 = os.getenv("COLOR_074E52")
MEDIA = os.getenv("MEDIA")


class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.is_maximized = True
        self.old_pos = self.pos()
        self.initUI()

    def initUI(self):
        # --- Central Widget ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Header ---
        header = QWidget()
        header.setFixedHeight(36)
        header.setStyleSheet(f"background-color: {COLOR_C8F5F2}")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setSpacing(6)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(f"{MEDIA}logo.png")
        pixmap = pixmap.scaled(
            24,
            24,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        logo_label.setPixmap(pixmap)

        # Título mejorado
        title_label = QLabel("Aquanova Monitor")
        title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        title_label.setStyleSheet(f"color: {COLOR_074E52} margin-left: 6px;")

        # Botones
        btn_style = """
            QPushButton {
                background-color: transparent;
                color: {COLOR_074E52}
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.6);
            }
        """

        minimize_btn = QPushButton("—")
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.setStyleSheet(btn_style)
        minimize_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        minimize_btn.clicked.connect(self.showMinimized)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        close_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                color: {COLOR_074E52};
                font-size: 14px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #ff5c5c;
                color: {COLOR_C8F5F2};
            }}
        """
        )
        close_btn.clicked.connect(self.animateClose)

        # Añadir al layout
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(minimize_btn)
        header_layout.addWidget(close_btn)

        # --- Contenido principal ---
        self.main_content = MainWindow()

        # --- Agregar a layout general ---
        main_layout.addWidget(header)
        main_layout.addWidget(self.main_content)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and not self.is_maximized:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def animateClose(self):
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(400)
        self.fade_anim.setStartValue(1)
        self.fade_anim.setEndValue(0)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_anim.finished.connect(self.close)
        self.fade_anim.start()


def main():
    app = QApplication(sys.argv)
    app.setStyle(
        "Fusion"
    )  # Al inicio de tu aplicación, antes de crear cualquier widget:
    app.setStyleSheet(
        "QToolTip { color: #000000; background-color: #ffffff; border: 1px solid black; }"
    )
    window = MainWindow()
    window.setWindowIcon(QIcon("media/logotipo_w.png"))
    window.setWindowTitle("Aquanova - Monitor")
    window.show()
    app.setStyle("Fusion")
    window = CustomMainWindow()
    window.setWindowIcon(QIcon(f"{MEDIA}logo.png"))
    window.setWindowTitle("Aquanova Monitor")
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
