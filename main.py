import sys
from PyQt6.QtWidgets import QApplication
from controllers.main_window import MainWindow  # Importamos el controlador de la ventana principal

def main():
    app = QApplication(sys.argv)  # Creamos la aplicación de Qt
    window = MainWindow()  # Instanciamos la ventana principal
    window.show()  # Mostramos la ventana
    sys.exit(app.exec())  # Ejecutamos el loop de eventos de Qt

if __name__ == "__main__":
    main()

