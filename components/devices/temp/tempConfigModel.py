# ceConfigModel.py
"""
Modelo para cargar y guardar la configuración del sensor de cE en la base de datos.
"""

class TempConfigModel:
    def __init__(self):
        try:
            from dispositivos.controllers.deviceController import DispositivoController
            self.controller = DispositivoController()
        except Exception as e:
            self.controller = None
            print(f"Error al inicializar DispositivoController: {e}")

    def load(self):
        """
        Carga la configuración del sensor cE (ID 4) desde la base de datos.
        Devuelve un dict con los valores o None si falla.
        """
        if not self.controller:
            return None
        try:
            config = self.controller.get_dispositivo(4) or {}
            return {
                "valor_minimo": int(config.get("valor_minimo", 0)),
                "valor_maximo": int(config.get("valor_maximo", 50)),
            }
        except Exception as e:
            print(f"Error al cargar configuración de temperatura: {e}")
            return None

    def save(self, min_val, max_val):
        """
        Guarda los valores de configuración del sensor cE (ID 4) en la base de datos.
        Devuelve True si fue exitoso, False si hubo error.
        """
        if not self.controller:
            return False
        try:
            data = {
                "valor_minimo": min_val,
                "valor_maximo": max_val,
            }
            ok = self.controller.update_dispositivo(4, data)
            return ok
        except Exception as e:
            print(f"Error al guardar configuración de temperatura: {e}")
            return False
