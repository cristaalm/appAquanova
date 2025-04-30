import os
import sys
import signal
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QCursor
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QSize

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
        self.is_maximized = False
        self.old_pos = QPoint()
        self.dragging = False
        self.resizing = False
        self.resize_direction = None
        self.resize_margin = 10  # Increased margin for better touch support
        self.min_width = 400
        self.min_height = 300
        self.initUI()

    def initUI(self):
        # Get screen dimensions
        screen = QApplication.primaryScreen().geometry()
        
        # Set initial size based on screen dimensions
        initial_width = min(1000, screen.width() * 0.8)
        initial_height = min(600, screen.height() * 0.8)
        self.resize(int(initial_width), int(initial_height))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header - responsive height based on screen
        header_height = max(36, int(screen.height() * 0.04))
        self.header = QWidget()
        self.header.setStyleSheet(f"""
            background-color: {COLOR_C8F5F2};
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        """)
        self.header.setFixedHeight(header_height)

        header_layout = QHBoxLayout(self.header)
        header_margin = max(10, int(header_height * 0.3))
        header_layout.setContentsMargins(header_margin, 0, header_margin, 0)
        header_layout.setSpacing(header_margin)

        # Logo with responsive size
        logo_size = max(24, int(header_height * 0.7))
        logo_label = QLabel()
        pixmap = QPixmap(f"{MEDIA}logo.png")
        pixmap = pixmap.scaled(
            logo_size, logo_size, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        logo_label.setPixmap(pixmap)

        # Title with responsive font
        title_font_size = max(11, int(header_height * 0.35))
        title_label = QLabel("Aquanova Monitor")
        title_label.setFont(QFont("Segoe UI", title_font_size, QFont.Weight.Medium))
        title_label.setStyleSheet(f"""
            color: {COLOR_074E52}; 
            margin-left: {int(header_margin * 0.6)}px;
        """)

        # Buttons with responsive styles
        btn_font_size = max(14, int(header_height * 0.4))
        btn_style = f"""
            QPushButton {{
                background-color: transparent;
                color: {COLOR_074E52};
                font-size: {btn_font_size}px;
                border: none;
                min-width: {header_height}px;
                min-height: {header_height}px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.6);
                border-radius: 4px;
            }}
        """

        minimize_btn = QPushButton("—")
        minimize_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        minimize_btn.setStyleSheet(btn_style)
        minimize_btn.clicked.connect(self.showMinimized)

        self.max_restore_btn = QPushButton("❐")
        self.max_restore_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.max_restore_btn.setStyleSheet(btn_style)
        self.max_restore_btn.clicked.connect(self.toggleMaxRestore)

        close_btn = QPushButton("✕")
        close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLOR_074E52};
                font-size: {btn_font_size}px;
                border: none;
                min-width: {header_height}px;
                min-height: {header_height}px;
            }}
            QPushButton:hover {{
                background-color: #ff5c5c;
                color: {COLOR_C8F5F2};
                border-radius: 4px;
            }}
        """)
        close_btn.clicked.connect(self.animateClose)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(minimize_btn)
        header_layout.addWidget(self.max_restore_btn)
        header_layout.addWidget(close_btn)

        # Main content - responsive
        self.main_content = MainWindow()
        self.main_content.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )

        main_layout.addWidget(self.header)
        main_layout.addWidget(self.main_content)

        # Set minimum size based on content
        self.setMinimumSize(QSize(self.min_width, self.min_height))

    def resizeEvent(self, event):
        # Update any elements that need to adjust on resize
        super().resizeEvent(event)

    def toggleMaxRestore(self):
        if self.isMaximized():
            self.showNormal()
            self.is_maximized = False
            self.max_restore_btn.setText("❐")
        else:
            self.showMaximized()
            self.is_maximized = True
            self.max_restore_btn.setText("🗗")

    def animateClose(self):
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(400)
        self.fade_anim.setStartValue(1)
        self.fade_anim.setEndValue(0)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_anim.finished.connect(self.close)
        self.fade_anim.start()

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        global_pos = event.globalPosition().toPoint()

        if event.button() == Qt.MouseButton.LeftButton:
            if self.isInResizeArea(pos):
                self.resizing = True
                self.resize_start_pos = global_pos
                self.resize_start_geometry = self.geometry()
            elif self.header.geometry().contains(pos):
                self.dragging = True
                self.old_pos = global_pos

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        global_pos = event.globalPosition().toPoint()

        if self.resizing:
            self.handleResize(global_pos)
        elif self.dragging and not self.isMaximized():
            delta = global_pos - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = global_pos
        else:
            self.updateCursor(pos)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.resizing = False
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def isInResizeArea(self, pos):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()
        margin = self.resize_margin

        if x < margin and y < margin:
            self.resize_direction = "topleft"
        elif x > w - margin and y < margin:
            self.resize_direction = "topright"
        elif x < margin and y > h - margin:
            self.resize_direction = "bottomleft"
        elif x > w - margin and y > h - margin:
            self.resize_direction = "bottomright"
        elif x < margin:
            self.resize_direction = "left"
        elif x > w - margin:
            self.resize_direction = "right"
        elif y < margin:
            self.resize_direction = "top"
        elif y > h - margin:
            self.resize_direction = "bottom"
        else:
            self.resize_direction = None
        return self.resize_direction is not None

    def updateCursor(self, pos):
        if self.isInResizeArea(pos):
            cursors = {
                "left": Qt.CursorShape.SizeHorCursor,
                "right": Qt.CursorShape.SizeHorCursor,
                "top": Qt.CursorShape.SizeVerCursor,
                "bottom": Qt.CursorShape.SizeVerCursor,
                "topleft": Qt.CursorShape.SizeFDiagCursor,
                "bottomright": Qt.CursorShape.SizeFDiagCursor,
                "topright": Qt.CursorShape.SizeBDiagCursor,
                "bottomleft": Qt.CursorShape.SizeBDiagCursor,
            }
            self.setCursor(cursors.get(self.resize_direction, Qt.CursorShape.ArrowCursor))
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def handleResize(self, global_pos):
        delta = global_pos - self.resize_start_pos
        geom = self.resize_start_geometry
        x, y, w, h = geom.x(), geom.y(), geom.width(), geom.height()

        if "left" in self.resize_direction:
            new_x = x + delta.x()
            new_w = w - delta.x()
            if new_w > self.min_width:
                self.setGeometry(new_x, y, new_w, h)
        elif "right" in self.resize_direction:
            new_w = w + delta.x()
            if new_w > self.min_width:
                self.setGeometry(x, y, new_w, h)

        if "top" in self.resize_direction:
            new_y = y + delta.y()
            new_h = h - delta.y()
            if new_h > self.min_height:
                self.setGeometry(self.x(), new_y, self.width(), new_h)
        elif "bottom" in self.resize_direction:
            new_h = h + delta.y()
            if new_h > self.min_height:
                self.setGeometry(self.x(), y, self.width(), new_h)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Responsive tooltip styling
    screen = QApplication.primaryScreen().geometry()
    tooltip_font_size = max(10, int(screen.height() * 0.02))
    app.setStyleSheet(f"""
        QToolTip {{
            color: #000000; 
            background-color: #ffffff; 
            border: 1px solid black;
            font-size: {tooltip_font_size}px;
            padding: {int(tooltip_font_size * 0.5)}px;
        }}
    """)
    
    window = CustomMainWindow()
    window.setWindowIcon(QIcon(f"{MEDIA}logo.png"))
    window.setWindowTitle("Aquanova Monitor")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()