from utils.BaseGraph import BaseGraph
import pyqtgraph as pg
import time

class GraphHp(BaseGraph):   
    def __init__(self):
        super().__init__(
            title="",
            x_label="Tiempo (horas)",
            y_label="Valor (pH)",
            line_color="#045859",
            data_range=(0, 14),
            initial_data_length=1  # Iniciar con un solo punto
        )
        # Limpiar los datos iniciales aleatorios
        self.x_data = []
        self.y_data = []
        self.last_value = None
        self.curve.setData(self.x_data, self.y_data)  # Actualizar la curva para que empiece vacía
        
        self.custom_config()
        self.setYRange(0.0, 14.0)

    def custom_config(self):
        """Configuración adicional específica para pH"""
        # Aplicar estilos
        style = {"color": "#045859", "font-size": "11px"}

        # Establecer fondo blanco
        self.setBackground("white")

        # Configurar etiquetas con el estilo deseado
        self.getPlotItem().setLabel("left", "Escala de pH", **style)
        self.getPlotItem().setLabel("bottom", "Tiempo (horas)", **style)

        # Configurar el color de los ticks (números) en ambos ejes
        self.getPlotItem().getAxis("left").setPen(pg.mkPen(style["color"]))
        self.getPlotItem().getAxis("bottom").setPen(pg.mkPen(style["color"]))

        # Añadir leyenda
        self.getPlotItem().addLegend()

        # Mostrar cuadrícula
        self.getPlotItem().showGrid(x=True, y=True, alpha=0.3)

        # Modificar el estilo de la línea para añadir símbolos
        pen = pg.mkPen(color="#6CC6C1", width=2)
        self.curve.setPen(pen)
        self.curve.setSymbol('o')
        self.curve.setSymbolSize(7)
        self.curve.setSymbolBrush("#6CC6C1")

        # Configura los límites físicos (min/max permitidos)
        self.getViewBox().setLimits(yMin=0, yMax=14)

    def updateHp(self, new_value: float):
        """Actualiza la gráfica con un nuevo valor de pH"""
        # Verificar si el valor es realmente nuevo
        if self.last_value == new_value:
            return
            
        self.last_value = new_value
        
        if not self.x_data:  # Si es el primer punto
            self.x_data = [0]
            self.y_data = [new_value]
        else:
            self.x_data.append(self.x_data[-1] + 1)
            self.y_data.append(new_value)
            
            # Mantener solo los últimos 24 puntos
            if len(self.x_data) > 24:
                self.x_data = self.x_data[-24:]
                self.y_data = self.y_data[-24:]

        # Actualizar la gráfica
        self.curve.setData(self.x_data, self.y_data)
        
        # Ajustar el rango visible
        if len(self.x_data) > 1:
            latest_x = self.x_data[-1]
            self.getViewBox().setXRange(max(0, latest_x - 23), latest_x + 1)