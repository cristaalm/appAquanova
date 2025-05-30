from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QLabel,
)


class MarqueeLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.full_text = text + "     "  # Espacio extra para que el texto dé la vuelta
        self.index = 0

        self.setText(self.full_text)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_text)
        self.timer.start(150)  # Menor valor = más rápido

    def scroll_text(self):
        scrolled = self.full_text[self.index :] + self.full_text[: self.index]
        self.setText(scrolled)
        self.index = (self.index + 1) % len(self.full_text)
