from utils.BaseGraph import BaseGraph


class GraphHp(BaseGraph):
    def __init__(self):
        super().__init__(
            title="Gráfica de pH",
            x_label="Tiempo",
            y_label="pH",
            line_color="#e63757",  # Rojo
            data_range=(6.0, 8.0),  # Rango típico de pH
        )
        # Configuración adicional específica para pH
        self.set_data_range(0, 14)  # Rango completo de pH

    def custom_config(self):
        """Configuración adicional específica para pH"""
        # Puedes añadir aquí cualquier personalización adicional
        pass

    def updateHp(self, new_value: float):
        """Alias para mantener compatibilidad con código existente"""
        self.update_data(new_value)
