from .HistorialController import HistorialController


class CEController(HistorialController):
    def __init__(self):
        super().__init__(id_dispositivo=1)
