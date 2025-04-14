from .HistorialController import HistorialController


class DistanceController(HistorialController):
    def __init__(self):
        super().__init__(id_dispositivo=5)
