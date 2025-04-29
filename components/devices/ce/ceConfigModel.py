# ceConfigModel.py
"""
Modelo para cargar y guardar la configuración del sensor de cE en la base de datos.
"""

class CeConfigModel:
    def __init__(self):
        try:
            from dispositivos.controllers.deviceController import DispositivoController
            self.controller = DispositivoController()
        except Exception as e:
            self.controller = None
            print(f"Error al inicializar DispositivoController: {e}")

    def load(self):
        """
        Carga la configuración del sensor cE (ID 1) desde la base de datos.
        Devuelve un dict con los valores o None si falla.
        """
        if not self.controller:
            return None
        try:
            config = self.controller.get_dispositivo(1) or {}
            return {
                "valor_minimo": int(config.get("valor_minimo", 0)),
                "valor_maximo": int(config.get("valor_maximo", 14)),
                "tiempo_batido": int(config.get("tiempo_batido", config.get("tiempo_batido", 0))),
            }
        except Exception as e:
            print(f"Error al cargar configuración de cE: {e}")
            return None

    def save(self, min_val, max_val, batido_val):
        """
        Guarda los valores de configuración del sensor cE (ID ) en la base de datos.
        Devuelve True si fue exitoso, False si hubo error.
        """
        if not self.controller:
            return False
        try:
            data = {
                "valor_minimo": min_val,
                "valor_maximo": max_val,
                "tiempo_batido": batido_val,
            }
            ok = self.controller.update_dispositivo(1, data)
            return ok
        except Exception as e:
            print(f"Error al guardar configuración de cE: {e}")
            return False
