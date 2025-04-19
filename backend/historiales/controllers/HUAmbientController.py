from .HistorialController import HistorialController


class HUAmbientController(HistorialController):
    def __init__(self):
        super().__init__(id_dispositivo=6)
