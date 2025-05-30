from PyQt6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg

class GraphLvlWater(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("white")
        self.plot_widget.setLabel("left", "cm Nivel", color="#045859", size="11px")
        self.plot_widget.setLabel("bottom", "Tiempo (minutos)", color="#045859", size="11px")
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.enableAutoRange(axis=pg.ViewBox.XAxis, enable=True)
        self.plot_widget.enableAutoRange(axis=pg.ViewBox.YAxis, enable=True)

        pen = pg.mkPen(color=(57, 195, 239), width=1)

        self.level_data = []
        self.time_data = []

        self.level_line = self.plot_widget.plot(
            self.time_data,
            self.level_data,
            pen=pen,
            symbol="o",
            symbolSize=8,
            symbolBrush="#39C3EF",
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 30, 0, 0)
        layout.addWidget(self.plot_widget)

    def update_data(self, new_value):
        next_time = self.time_data[-1] + 1 if self.time_data else 0
        self.time_data.append(next_time)
        self.level_data.append(new_value)

        self.time_data = self.time_data[-20:]
        self.level_data = self.level_data[-20:]

        self.level_line.setData(self.time_data, self.level_data)

        # Autoajuste manual del eje Y si desactivas autoRange
        # min_y = min(self.level_data)
        # max_y = max(self.level_data)
        # self.plot_widget.setYRange(min_y - 5, max_y + 5)

    def updateLvlWater(self, new_value):
        self.update_data(new_value)
