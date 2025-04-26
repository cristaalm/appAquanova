from random import randint
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QFrame
from PyQt6.QtGui import QColor

from PyQt6 import QtCore, QtWidgets
import pyqtgraph as pg

class TempGraph(QtWidgets.QMainWindow):
    def __init__(self, water_temp_graph_data=None):
        super().__init__()
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        style = {"color": "#333", "font-size": "11px"}

        self.plot_temp = pg.PlotWidget()
        self.plot_temp.setBackground("white")
        pen_temp = pg.mkPen(color=(30, 137, 207))
        self.plot_temp.setLabel("left", "°C Temperatura", **style)
        self.plot_temp.setLabel("bottom", "Tiempo(min)", **style)
        self.plot_temp.addLegend()
        self.plot_temp.showGrid(x=True, y=True)
        self.plot_temp.setYRange(30, 90)
        layout.addWidget(self.plot_temp)

        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: white;margin:0;")  # Fondo blanco

        # Frame con sombra
        frame = QFrame()
        frame.setStyleSheet("margin:0;")
        frame_layout = QtWidgets.QVBoxLayout(frame)

        # Añadir gráficas al frame
        frame_layout.addWidget(self.plot_temp)

        # Añadir frame al layout principal
        layout.addWidget(frame)

        # Datos iniciales
        self.time = list(range(10))
        self.temp_data = [randint(25, 35) for _ in range(10)]

        self.line_temp = self.plot_temp.plot(
            self.time,
            self.temp_data,
            pen=pen_temp,
            symbol="o",
            symbolSize=10,
            symbolBrush="#1E89CF",
        )

        self.plot_temp.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=True)
        self.plot_temp.getViewBox().autoRange()

