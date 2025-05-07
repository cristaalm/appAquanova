from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
import pyqtgraph as pg
from PyQt6 import QtWidgets
from random import randint

class GraphLvlWater(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 30, 0, 0)
        layout.setSpacing(0)

        # Crear el plot
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("white")

        # Estilo de etiquetas
        label_style = {"color": "#045859", "font-size": "11px"}
        self.plot_widget.setLabel("left", "cm Nivel", **label_style)
        self.plot_widget.setLabel("bottom", "Tiempo (horas)", **label_style)
        self.plot_widget.addLegend()
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setYRange(0, 50)  # Rango de agua (puedes ajustarlo)
        self.plot_widget.enableAutoRange(axis=pg.ViewBox.XAxis, enable=True)

        # Estilo del trazo
        pen = pg.mkPen(color=(76, 164, 165), width=1)

        # Datos iniciales simulados
        self.time_data = list(range(25))
        self.level_data = [randint(1, 50) for _ in range(25)]

        # Dibujar línea inicial
        self.level_line = self.plot_widget.plot(
            self.time_data,
            self.level_data,
            pen=pen,
            symbol="o",
            symbolSize=8,
            symbolBrush="#39C3EF",
        )

        # Frame decorativo con sombra
        frame = QFrame()
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(self.plot_widget)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(255, 255, 255))  # Misma sombra que tu panel
        shadow.setOffset(0, 3)
        frame.setGraphicsEffect(shadow)

        layout.addWidget(frame)

    def update_data(self, new_value):
        """
        Agrega un nuevo dato de nivel de agua y actualiza la gráfica.
        """
        self.time_data.append(self.time_data[-1] + 1 if self.time_data else 0)
        self.level_data.append(new_value)

        # Mantener los últimos 20 datos para no saturar la gráfica
        self.time_data = self.time_data[-20:]
        self.level_data = self.level_data[-20:]

        self.level_line.setData(self.time_data, self.level_data)
