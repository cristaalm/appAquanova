from random import randint
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QFrame
from PyQt6.QtGui import QColor

from PyQt6 import QtCore, QtWidgets
import pyqtgraph as pg

class GraphicsAmbient(QtWidgets.QMainWindow):
    def __init__(self, temp_graph_data=None, hum_graph_data=None):
        super().__init__()
        # Crear un widget central con layout vertical
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 1. Gráfica de temperatura
        self.plot_temp = pg.PlotWidget()
        self.plot_temp.setBackground("white")
        pen_temp = pg.mkPen(color=(230, 126, 34))
        style = {"color": "#333", "font-size": "11px"}
        self.plot_temp.setLabel("left", "°C Temperatura", **style)
        self.plot_temp.setLabel("bottom", "Tiempo (min)", **style)
        self.plot_temp.addLegend()
        self.plot_temp.showGrid(x=True, y=True)
        self.plot_temp.setYRange(20, 40)
        layout.addWidget(self.plot_temp)

        # 2. Gráfica de humedad
        self.plot_hum = pg.PlotWidget()
        self.plot_hum.setBackground("white")
        pen_hum = pg.mkPen(color=(30, 137, 207))
        self.plot_hum.setLabel("left", "% Humedad", **style)
        self.plot_hum.setLabel("bottom", "Tiempo (min)", **style)
        self.plot_hum.addLegend()
        self.plot_hum.showGrid(x=True, y=True)
        self.plot_hum.setYRange(30, 90)
        layout.addWidget(self.plot_hum)

        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: white;margin:0;")  # Fondo blanco

        # Frame con sombra
        frame = QFrame()
        frame.setStyleSheet("margin:0;")
        frame_layout = QtWidgets.QVBoxLayout(frame)

        # Añadir gráficas al frame
        frame_layout.addWidget(self.plot_temp)
        frame_layout.addWidget(self.plot_hum)

        # Añadir frame al layout principal
        layout.addWidget(frame)

        # Datos iniciales
        self.time = list(range(10))
        self.temp_data = [randint(20, 40) for _ in range(10)]
        self.hum_data = [randint(40, 80) for _ in range(10)]

        # Crear líneas
        self.line_temp = self.plot_temp.plot(
            self.time,
            self.temp_data,
            name="Sensor Temp",
            pen=pen_temp,
            symbol="+",
            symbolSize=10,
            symbolBrush="#E67E22",
        )

        self.line_hum = self.plot_hum.plot(
            self.time,
            self.hum_data,
            name="Sensor Humedad",
            pen=pen_hum,
            symbol="o",
            symbolSize=10,
            symbolBrush="#1E89CF",
        )

        # Timer para actualizar datos
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

    def update_data(self):
        # Actualizar datos
        self.time = self.time[1:] + [self.time[-1] + 1]
        self.temp_data = self.temp_data[1:] + [randint(20, 40)]
        self.hum_data = self.hum_data[1:] + [randint(40, 80)]

        # Redibujar
        self.line_temp.setData(self.time, self.temp_data)
        self.line_hum.setData(self.time, self.hum_data)