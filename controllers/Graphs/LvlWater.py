import random
import pyqtgraph as pg

class GraphLvlWater(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1920 - 450 , 400)  # Hacer la gráfica más pequeña

        # Configurar PyQtGraph con fondo oscuro
        self.setBackground("#222222")
        self.getPlotItem().getAxis("bottom").setPen("w")  # Ejes en blanco
        self.getPlotItem().getAxis("left").setPen("w")

        # Agregar etiquetas a los ejes
        self.getPlotItem().setLabel('left', 'Nivel del agua')
        self.getPlotItem().setLabel('bottom', 'Tiempo')

        self.data_x = list(range(100))
        self.data_y = [random.randint(0, 30) for _ in range(100)]
        self.curve = self.plot(self.data_x, self.data_y, pen="c")  # Color cyan

    def updateLvlWater(self, new_value):
        """ Actualiza la gráfica en tiempo real con un nuevo valor """
        self.data_x = self.data_x[1:] + [self.data_x[-1] + 1]
        self.data_y = self.data_y[1:] + [new_value]
        self.curve.setData(self.data_x, self.data_y)
