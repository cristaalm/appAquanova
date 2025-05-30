from .HistorialController import HistorialController


class TempAmbientController(HistorialController):
    def __init__(self):
        super().__init__(id_dispositivo=3)
