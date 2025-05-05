from utils.BaseGraph import BaseGraph
import time

class GraphLvlWater(BaseGraph):
    def __init__(self):
        super().__init__(
            x_label="Tiempo (Minutos)",
            y_label="Nivel (Litros)",
            line_color="#39C3EF",  # Azúl
            data_range=(0.0, 25.0),  # Rango inicial
        )
        self.start_time = time.time()
        self.x_data = []
        self.y_data = []

    def custom_config(self):
        """Configuración adicional específica para nivel de agua"""
        self.set_data_range(0, 25)  # Ahora de 0 a 25 litros

    def updateLvlWater(self, new_value: float):
        """Agrega punto en el tiempo, eje X en minutos desde inicio"""
        current_time = time.time()
        elapsed_minutes = (current_time - self.start_time) / 60.0  # segundos → minutos

        self.x_data.append(elapsed_minutes)
        self.y_data.append(new_value)

        # Opcional: mantén últimos 100 puntos
        self.x_data = self.x_data[-100:]
        self.y_data = self.y_data[-100:]

        self.getPlotItem().clear()
        # Dibuja la nueva curva y guarda el objeto para futuras actualizaciones
        self.curve = self.plot(self.x_data, self.y_data, pen="#39C3EF")
