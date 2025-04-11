import serial
import serial.tools.list_ports
import json
import os
from dotenv import load_dotenv
from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QMutexLocker

# Cargar variables del .env
load_dotenv()
SERIAL_PORT = os.getenv("SERIAL_PORT")
BAUD_RATE = int(os.getenv("BAUD_RATE", 9600))  # Valor por defecto: 9600
print(f"Puerto serial: {SERIAL_PORT}, Baud rate: {BAUD_RATE}")


class SerialWorker(QThread):
    data_received = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    status_changed = pyqtSignal(str)

    def __init__(self, port=SERIAL_PORT, baud_rate=BAUD_RATE):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.serial_conn = None
        self._is_running = False
        self.mutex = QMutex()

    def run(self):
        self._is_running = True
        self.status_changed.emit(f"Conectando a {self.port}...")

        while self._is_running:
            try:
                available_ports = [p.device for p in serial.tools.list_ports.comports()]
                if self.port not in available_ports:
                    self.error_occurred.emit(
                        f"⚠️ Puerto {self.port} no encontrado. Conéctelo y espere..."
                    )
                    self.sleep(5)
                    continue

                self.serial_conn = serial.Serial(
                    port=self.port, baudrate=self.baud_rate, timeout=1, write_timeout=1
                )
                self.status_changed.emit(f"✅ Conectado en {self.port}")

                while self._is_running and self.serial_conn.is_open:
                    try:
                        if self.serial_conn.in_waiting > 0:
                            raw_data = self.serial_conn.readline()
                            line = raw_data.decode("utf-8").strip()
                            if line:
                                data = json.loads(line)
                                self.data_received.emit(data)
                    except (UnicodeDecodeError, json.JSONDecodeError) as e:
                        self.error_occurred.emit(f"⚠️ Error en los datos: {str(e)}")
                    except serial.SerialException:
                        self.error_occurred.emit(
                            "⚠️ Desconexión detectada. Reintentando..."
                        )
                        break

                self.close_serial()

            except serial.SerialException as e:
                self.error_occurred.emit(f"❌ Error de conexión: {str(e)}")

            self.error_occurred.emit("🔴 Se ha desconectado. Intentando reconectar...")
            self.sleep(5)

    def close_serial(self):
        with QMutexLocker(self.mutex):
            if self.serial_conn:
                try:
                    self.serial_conn.close()
                except serial.SerialException:
                    pass
                finally:
                    self.serial_conn = None

    def stop(self):
        self._is_running = False
        self.wait(1000)
