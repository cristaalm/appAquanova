from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QCheckBox,
    QDoubleSpinBox,
    QLabel,
    QFrame,
    QSpinBox,
    QSizePolicy,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import Qt

from dispositivos.controllers.deviceController import DispositivoController


class DeviceOptions(QWidget):
    def __init__(self, notification, device_type, parent=None):
        super().__init__(parent)
        self.device_type = device_type
        self.notification = notification
        self.config = DispositivoController()
        self.inputs = {}  # Para acceder a los valores fácilmente
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(8)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: #f8fafc;
                border-radius: 12px;
                border: none;
            }

            QLabel {
                color: #1e293b;
                font-size: 14px;
            }

            QSpinBox, QDoubleSpinBox {
                background-color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 14px;
                color: #0f172a;
            }

            QSpinBox::up-button,
            QSpinBox::down-button,
            QDoubleSpinBox::up-button,
            QDoubleSpinBox::down-button {
                width: 0;
                height: 0;
                border: none;
            }

            QSpinBox::up-arrow,
            QSpinBox::down-arrow,
            QDoubleSpinBox::up-arrow,
            QDoubleSpinBox::down-arrow {
                width: 0;
                height: 0;
            }

            QSpinBox QLineEdit, QDoubleSpinBox QLineEdit {
                padding: 4px;
                border: none;
                background: transparent;
            }
        """
        )

        self.frame_layout = QVBoxLayout(frame)
        self.frame_layout.setSpacing(6)

        # Llama la función específica del tipo
        self.configure_options()

        # Botón de guardar
        save_button = QPushButton("Guardar configuración")
        save_button.setStyleSheet(
            "padding: 8px; font-weight: bold; background-color: #3b82f6; color: white; border-radius: 8px;"
        )
        save_button.clicked.connect(self.save_config)
        self.frame_layout.addWidget(save_button)

        self.layout.addWidget(frame)

    def configure_options(self):
        tipo = self.device_type
        if tipo == "sensor_tds":
            self.config
            self.add_tds_options(self.frame_layout)
        elif tipo == "sensor_ph":
            self.add_ph_options(self.frame_layout)
        elif tipo == "sensor_dht11":
            self.add_temp_hum_options(self.frame_layout)
        elif tipo == "sensor_ds18b20":
            self.add_temp_sumergible_options(self.frame_layout)
        elif tipo == "sensor_ultrasonico":
            self.add_ultrasonico_options(self.frame_layout)
        else:
            label = QLabel("No hay opciones configuradas para este dispositivo")
            label.setStyleSheet("color: #000; font-style: italic;")
            self.frame_layout.addWidget(label)

    def get_loaded_config(self, device_id):
        config_data = self.config.get_dispositivo(device_id)
        return config_data or {}

    def add_tds_options(self, layout):
        config = self.get_loaded_config(1)
        print(config)

        layout.addWidget(QLabel("Opciones del Sensor TDS"))
        spin = QSpinBox()
        spin.setRange(1, 120)
        spin.setValue(config.get("tiempo_batido", 30))
        self.inputs["tds_tiempo_batido"] = spin
        layout.addWidget(QLabel("Tiempo de batido (segundos):"))
        layout.addWidget(spin)

        min_spin = QDoubleSpinBox()
        max_spin = QDoubleSpinBox()
        for s in (min_spin, max_spin):
            s.setRange(0, 9999)
        min_spin.setValue(config.get("valor_minimo", 0))
        max_spin.setValue(config.get("valor_maximo", 1000))
        self.inputs["tds_min"] = min_spin
        self.inputs["tds_max"] = max_spin
        layout.addWidget(QLabel("Conductividad mínima (ppm):"))
        layout.addWidget(min_spin)
        layout.addWidget(QLabel("Conductividad máxima (ppm):"))
        layout.addWidget(max_spin)

    def add_ph_options(self, layout):
        config = self.get_loaded_config(2)

        layout.addWidget(QLabel("Opciones del Sensor de pH"))
        spin = QSpinBox()
        spin.setRange(1, 120)
        spin.setValue(config.get("tiempo_batido", 30))
        self.inputs["ph_tiempo_batido"] = spin
        layout.addWidget(QLabel("Tiempo de batido (segundos):"))
        layout.addWidget(spin)

        min_spin = QDoubleSpinBox()
        max_spin = QDoubleSpinBox()
        for s in (min_spin, max_spin):
            s.setRange(0, 14)
        min_spin.setValue(config.get("valor_minimo", 0))
        max_spin.setValue(config.get("valor_maximo", 14))
        self.inputs["ph_min"] = min_spin
        self.inputs["ph_max"] = max_spin
        layout.addWidget(QLabel("pH mínimo:"))
        layout.addWidget(min_spin)
        layout.addWidget(QLabel("pH máximo:"))
        layout.addWidget(max_spin)

    def add_temp_hum_options(self, layout):
        temp_config = self.get_loaded_config(3)
        hum_config = self.get_loaded_config(6)

        layout.addWidget(QLabel("Opciones del Sensor DHT11"))

        tmin = QDoubleSpinBox()
        tmax = QDoubleSpinBox()
        tmin.setRange(-20, 60)
        tmax.setRange(-20, 60)
        tmin.setValue(temp_config.get("valor_minimo", 0))
        tmax.setValue(temp_config.get("valor_maximo", 40))
        self.inputs["dht11_tmin"] = tmin
        self.inputs["dht11_tmax"] = tmax
        layout.addWidget(QLabel("Temperatura mínima (°C):"))
        layout.addWidget(tmin)
        layout.addWidget(QLabel("Temperatura máxima (°C):"))
        layout.addWidget(tmax)

        hmin = QDoubleSpinBox()
        hmax = QDoubleSpinBox()
        hmin.setRange(0, 100)
        hmax.setRange(0, 100)
        hmin.setValue(hum_config.get("valor_minimo", 30))
        hmax.setValue(hum_config.get("valor_maximo", 90))
        self.inputs["dht11_hmin"] = hmin
        self.inputs["dht11_hmax"] = hmax
        layout.addWidget(QLabel("Humedad mínima (%):"))
        layout.addWidget(hmin)
        layout.addWidget(QLabel("Humedad máxima (%):"))
        layout.addWidget(hmax)

    def add_temp_sumergible_options(self, layout):
        config = self.get_loaded_config(4)

        layout.addWidget(QLabel("Opciones del Sensor DS18B20"))

        tmin = QDoubleSpinBox()
        tmax = QDoubleSpinBox()
        tmin.setRange(-55, 125)
        tmax.setRange(-55, 125)
        tmin.setValue(config.get("valor_minimo", 0))
        tmax.setValue(config.get("valor_maximo", 100))
        self.inputs["ds_tmin"] = tmin
        self.inputs["ds_tmax"] = tmax
        layout.addWidget(QLabel("Temperatura mínima (°C):"))
        layout.addWidget(tmin)
        layout.addWidget(QLabel("Temperatura máxima (°C):"))
        layout.addWidget(tmax)

    def add_ultrasonico_options(self, layout):
        config = self.get_loaded_config(5)

        layout.addWidget(QLabel("Opciones del Sensor Ultrasónico"))

        dmin = QDoubleSpinBox()
        dmax = QDoubleSpinBox()
        dmin.setRange(0, 600)
        dmax.setRange(0, 600)
        dmin.setValue(config.get("valor_minimo", 10))
        dmax.setValue(config.get("valor_maximo", 300))
        self.inputs["ultra_dmin"] = dmin
        self.inputs["ultra_dmax"] = dmax
        layout.addWidget(QLabel("Distancia mínima (cm):"))
        layout.addWidget(dmin)
        layout.addWidget(QLabel("Distancia máxima (cm):"))
        layout.addWidget(dmax)

    def save_config(self):
        # Validaciones mínimas vs máximas
        errores = []
        pares = [
            ("tds_min", "tds_max", "Conductividad"),
            ("ph_min", "ph_max", "pH"),
            ("dht11_tmin", "dht11_tmax", "Temperatura DHT11"),
            ("dht11_hmin", "dht11_hmax", "Humedad DHT11"),
            ("ds_tmin", "ds_tmax", "Temperatura DS18B20"),
            ("ultra_dmin", "ultra_dmax", "Distancia Ultrasónica"),
        ]
        for min_key, max_key, label in pares:
            min_val = self.inputs.get(min_key)
            max_val = self.inputs.get(max_key)
            if min_val and max_val and min_val.value() > max_val.value():
                self.notification.show_message(
                    f"Error: {label} mínimo no puede ser mayor que máximo", "error"
                )
                errores.append(label)

        if errores:
            return False

        # Guardar valores con config.update(id, datos)
        try:
            # TDS (1)
            if "tds_min" in self.inputs:
                self.config.update_dispositivo(
                    1,
                    {
                        "valor_minimo": self.inputs["tds_min"].value(),
                        "valor_maximo": self.inputs["tds_max"].value(),
                        "tiempo_batido": self.inputs["tds_tiempo_batido"].value(),
                    },
                )

            # PH (2)
            if "ph_min" in self.inputs:
                self.config.update_dispositivo(
                    2,
                    {
                        "valor_minimo": self.inputs["ph_min"].value(),
                        "valor_maximo": self.inputs["ph_max"].value(),
                        "tiempo_batido": self.inputs["ph_tiempo_batido"].value(),
                    },
                )

            # TEMP DHT11 (3) y HUM DHT11 (6)
            if "dht11_tmin" in self.inputs:
                self.config.update_dispositivo(
                    3,
                    {
                        "valor_minimo": self.inputs["dht11_tmin"].value(),
                        "valor_maximo": self.inputs["dht11_tmax"].value(),
                    },
                )
            if "dht11_hmin" in self.inputs:
                self.config.update_dispositivo(
                    6,
                    {
                        "valor_minimo": self.inputs["dht11_hmin"].value(),
                        "valor_maximo": self.inputs["dht11_hmax"].value(),
                    },
                )

            # TEMP DS18B20 (4)
            if "ds_tmin" in self.inputs:
                self.config.update_dispositivo(
                    4,
                    {
                        "valor_minimo": self.inputs["ds_tmin"].value(),
                        "valor_maximo": self.inputs["ds_tmax"].value(),
                    },
                )

            # ULTRASONICO (5)
            if "ultra_dmin" in self.inputs:
                self.config.update_dispositivo(
                    5,
                    {
                        "valor_minimo": self.inputs["ultra_dmin"].value(),
                        "valor_maximo": self.inputs["ultra_dmax"].value(),
                    },
                )

            self.notification.show_message(
                "Configuración guardada correctamente", "success"
            )

        except Exception as e:
            self.notification.show_message(f"Error al guardar: {str(e)}", "error")
            return False
