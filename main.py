import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from controllers.main_window import (
    MainWindow,
)  # Importamos el controlador de la ventana principal


def main():
    app = QApplication(sys.argv)  # Creamos la aplicación de Qt
    app.setStyle("Fusion")  # Esto establece el estilo claro
    window = MainWindow()  # Instanciamos la ventana principal
    window.setWindowIcon(
        QIcon("media/logotipo_w.png")
    )  # Establecemos el ícono de la ventana
    window.setWindowTitle("Aquanova - Monitor")  # Establecemos el nombre de la ventana
    window.show()  # Mostramos la ventana
    sys.exit(app.exec())  # Ejecutamos el loop de eventos de Qt


if __name__ == "__main__":
    main()
