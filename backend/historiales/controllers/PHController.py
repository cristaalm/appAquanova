from .HistorialController import HistorialController


class PHController(HistorialController):
    def __init__(self):
        super().__init__(id_dispositivo=2)
