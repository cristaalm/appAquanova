from .HistorialController import HistorialController


class TempWaterController(HistorialController):
    def __init__(self):
        super().__init__(id_dispositivo=4)
