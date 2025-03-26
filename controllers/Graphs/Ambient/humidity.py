from utils.BaseGraph import BaseGraph


class GraphHU(BaseGraph):
    def __init__(self):
        super().__init__(
            title="Gráfica de Humedad",
            x_label="Tiempo",
            y_label="%",
            line_color="#e74c3c",  # Rojo
            data_range=(20.0, 25.0),  # Rango inicial
        )

    def custom_config(self):
        """Configuración adicional específica para temperatura"""
        self.set_data_range(10, 40)  # Rango razonable para temperatura ambiente

    def updateHU(self, new_value: float):
        """Alias para mantener compatibilidad con código existente"""
        self.update_data(new_value)
