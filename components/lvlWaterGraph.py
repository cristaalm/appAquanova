from utils.BaseGraph import BaseGraph
import time

class GraphLvlWater(BaseGraph):
    def __init__(self):
        super().__init__(
            x_label="Tiempo (minutos)",
            y_label="Nivel (itros)",
            line_color="#39C3EF",  # Azul
            data_range=(0.0, 25.0),
        )
        self.start_time = time.time()
        self.x_data = []
        self.y_data = []

    def custom_config(self):
        """Configuración específica para nivel de agua"""
        self.getPlotItem().setXRange(0, 10)  # ← Aquí fijo el eje X
        self.set_data_range(0, 25)            # ← El eje Y (función ya hecha)
        self.getPlotItem().setMouseEnabled(x=False, y=False)  # ← Esto bloquea movimiento de zoom/pan (si quieres fijo)

    def updateLvlWater(self, new_value: float):
        """Agrega nuevo dato en tiempo real"""
        current_time = time.time()
        elapsed_minutes = (current_time - self.start_time) / 60.0

        self.x_data.append(elapsed_minutes)
        self.y_data.append(new_value)

        # Mantener últimos 100 puntos
        self.x_data = self.x_data[-100:]
        self.y_data = self.y_data[-100:]

        self.getPlotItem().clear()
        self.getPlotItem().plot(self.x_data, self.y_data, pen=self.curve.opts['pen'])
