from utils.BaseGraph import BaseGraph
import pyqtgraph as pg
import time

class GraphHp(BaseGraph):   
    def __init__(self, theme_manager=None):
        # Importar el theme_manager si no se proporciona
        if theme_manager is None:
            from utils.theme_manager import theme_manager as tm
            self.theme_manager = tm
        else:
            self.theme_manager = theme_manager
            
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
        
        # Conectar al cambio de tema
        self.theme_manager.theme_changed.connect(self.apply_theme)
        
        # Aplicar configuración inicial
        self.custom_config()
        self.setYRange(0.0, 14.0)
        
        # Aplicar tema actual
        self.apply_theme()

    def get_theme_colors_for_graph(self):
        """Obtiene los colores específicos para la gráfica según el tema actual"""
        is_dark = self.theme_manager.is_dark_mode()
        
        if is_dark:
            return {
                "background": "#1A4A4D",  # surface del tema oscuro
                "text": "#FFFFFF",       # text_primary del tema oscuro
                "grid": "#2A5A5D",       # border del tema oscuro
                "line": "#4CA4A5",       # accent color
                "symbol": "#4CA4A5",     # accent color
                "axis": "#FFFFFF"        # text_primary para los ejes
            }
        else:
            return {
                "background": "#FFFFFF",  # surface del tema claro
                "text": "#333333",       # text_primary del tema claro
                "grid": "#E0E0E0",       # border del tema claro
                "line": "#6CC6C1",       # color más suave para tema claro
                "symbol": "#6CC6C1",     # color más suave para tema claro
                "axis": "#045859"        # color más oscuro para los ejes
            }

    def custom_config(self):
        """Configuración adicional específica para pH"""
        colors = self.get_theme_colors_for_graph()
        
        # Aplicar estilos según el tema
        style = {"color": colors["text"], "font-size": "11px"}

        # Establecer fondo según el tema
        self.setBackground(colors["background"])

        # Configurar etiquetas con el estilo deseado
        self.getPlotItem().setLabel("left", "Escala de pH", **style)
        self.getPlotItem().setLabel("bottom", "Tiempo (horas)", **style)

        # Configurar el color de los ticks (números) en ambos ejes
        self.getPlotItem().getAxis("left").setPen(pg.mkPen(colors["axis"]))
        self.getPlotItem().getAxis("bottom").setPen(pg.mkPen(colors["axis"]))
        
        # Configurar el color del texto de los ticks
        self.getPlotItem().getAxis("left").setTextPen(colors["text"])
        self.getPlotItem().getAxis("bottom").setTextPen(colors["text"])

        # Añadir leyenda si no existe
        if not hasattr(self, 'legend_added'):
            self.getPlotItem().addLegend()
            self.legend_added = True

        # Mostrar cuadrícula con color según el tema
        self.getPlotItem().showGrid(x=True, y=True, alpha=0.3)
        # Configurar color de la cuadrícula
        self.getPlotItem().getViewBox().setBackgroundColor(colors["background"])

        # Modificar el estilo de la línea para añadir símbolos
        pen = pg.mkPen(color=colors["line"], width=2)
        self.curve.setPen(pen)
        self.curve.setSymbol('o')
        self.curve.setSymbolSize(7)
        self.curve.setSymbolBrush(colors["symbol"])

        # Configura los límites físicos (min/max permitidos)
        self.getViewBox().setLimits(yMin=0, yMax=14)

    def apply_theme(self):
        """Aplica el tema actual a la gráfica"""
        colors = self.get_theme_colors_for_graph()
        
        # Actualizar fondo
        self.setBackground(colors["background"])
        
        # Actualizar estilo de texto
        style = {"color": colors["text"], "font-size": "11px"}
        
        # Actualizar etiquetas
        self.getPlotItem().setLabel("left", "Escala de pH", **style)
        self.getPlotItem().setLabel("bottom", "Tiempo (horas)", **style)
        
        # Actualizar color de los ejes
        self.getPlotItem().getAxis("left").setPen(pg.mkPen(colors["axis"]))
        self.getPlotItem().getAxis("bottom").setPen(pg.mkPen(colors["axis"]))
        
        # Actualizar color del texto de los ticks
        self.getPlotItem().getAxis("left").setTextPen(colors["text"])
        self.getPlotItem().getAxis("bottom").setTextPen(colors["text"])
        
        # Actualizar estilo de la línea y símbolos
        pen = pg.mkPen(color=colors["line"], width=2)
        self.curve.setPen(pen)
        self.curve.setSymbolBrush(colors["symbol"])
        
        # Actualizar color de fondo del ViewBox
        self.getPlotItem().getViewBox().setBackgroundColor(colors["background"])
        
        # Forzar actualización visual
        self.update()

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