from utils.BaseGraph import BaseGraph
import pyqtgraph as pg

class GraphHp(BaseGraph):
    def __init__(self):
        super().__init__(
            title="",
            x_label="Tiempo (horas)",
            y_label="Valor (pH)",
            line_color="#e63757",  # Rojo
            data_range=(6.0, 8.0),  # Rango típico de pH
        )
        # Configuración adicional específica para pH
        self.set_data_range(0, 14)  # Rango completo de pH

    def custom_config(self):
        """Configuración adicional específica para temperatura"""
        # Configuración de rango de temperatura
        self.set_data_range(10, 40)  # Rango razonable para temperatura ambiente
        
        # Aplicar estilos de TempGraph
        style = {"color": "#333", "font-size": "11px"}
        
        # Establecer fondo blanco
        self.setBackground("white")
        
        # Configurar etiquetas con el estilo deseado
        self.getPlotItem().setLabel("left", "Potencial de hidrógeno", **style)
        self.getPlotItem().setLabel("bottom", "Tiempo (horas)", **style)
        
        # Añadir leyenda
        self.getPlotItem().addLegend()
        
        # Mostrar cuadrícula
        self.getPlotItem().showGrid(x=True, y=True, alpha=0.3)
        
        # Modificar el estilo de la línea para añadir símbolos
        pen = pg.mkPen(color="#6cc6c1")
        self.curve.setPen(pen)
        self.curve.setSymbol('o')
        self.curve.setSymbolSize(7)
        self.curve.setSymbolBrush("#6cc6c1")
        
        # Habilitar auto-rango
        self.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=True)
        self.getViewBox().autoRange()

    def updateHp(self, new_value: float):
        """Alias para mantener compatibilidad con código existente"""
        self.update_data(new_value)
