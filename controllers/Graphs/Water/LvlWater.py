from utils.BaseGraph import BaseGraph

# import random


class GraphLvlWater(BaseGraph):
    def __init__(self):
        super().__init__(
            title="Nivel de Agua",
            x_label="Tiempo",
            y_label="Nivel (cm)",
            line_color="#27ae60",  # Verde
            data_range=(50.0, 70.0),  # Rango inicial
        )

    def custom_config(self):
        """Configuración adicional específica para nivel de agua"""
        self.set_data_range(0, 100)  # Rango de 0% a 100%

    def updateLvlWater(self, new_value: float):
        """Alias para mantener compatibilidad con código existente"""
        self.update_data(new_value)
