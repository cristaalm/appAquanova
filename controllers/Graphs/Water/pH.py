from utils.BaseGraph import BaseGraph
import pyqtgraph as pg

class GraphHp(BaseGraph):
    def __init__(self):
        super().__init__(
            title="",
            x_label="Tiempo (horas)",
            y_label="Valor (pH)",
            line_color="#e63757",
            data_range=(0, 14),  # Rango completo de pH
        )
        # Aplica configuración personalizada
        self.custom_config()
        
        # Establece un rango inicial adecuado para la visualización
        self.setYRange(0.0, 20.0)  # Establece el zoom inicial en un rango típico de pH

    def custom_config(self):
        """Configuración adicional específica para pH"""
        # Aplicar estilos
        style = {"color": "#333", "font-size": "11px"}
        
        # Establecer fondo blanco
        self.setBackground("white")
        
        # Configurar etiquetas con el estilo deseado
        self.getPlotItem().setLabel("left", "pH potencial de hidrógeno", **style)
        self.getPlotItem().setLabel("bottom", "Tiempo (horas)", **style)
        
        # Añadir leyenda
        self.getPlotItem().addLegend()
        
        # Mostrar cuadrícula
        self.getPlotItem().showGrid(x=True, y=True, alpha=0.3)
        
        # Modificar el estilo de la línea para añadir símbolos
        pen = pg.mkPen(color="#6CC6C1")
        self.curve.setPen(pen)
        self.curve.setSymbol('o')
        self.curve.setSymbolSize(7)
        self.curve.setSymbolBrush("#6CC6C1")
        
        # Configura los límites físicos (min/max permitidos)
        self.getViewBox().setLimits(yMin=0, yMax=14)

    def updateHp(self, new_value: float):
        """Alias para mantener compatibilidad con código existente"""
        self.update_data(new_value)