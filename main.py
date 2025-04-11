import os
import sys

# === Configuración de Django ===
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, "backend")
sys.path.append(backend_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
import django

django.setup()

# === Ahora sí se puede importar PyQt y tus módulos ===
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from controllers.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.setWindowIcon(QIcon("media/logotipo_w.png"))
    window.setWindowTitle("Aquanova - Monitor")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
