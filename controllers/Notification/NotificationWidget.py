from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtGui import QColor


class NotificationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Configuración de la ventana
        self.setWindowFlags(
            Qt.WindowType.SubWindow
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFixedSize(300, 80)
        self.setStyleSheet(
            """
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 12px;
        """
        )

        # Layout y contenido
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.setLayout(self.layout)

        self.label = QLabel("", self)
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.label)

        # Animaciones
        self.enter_animation = QPropertyAnimation(self, b"geometry")
        self.enter_animation.setDuration(400)
        self.enter_animation.setEasingCurve(QEasingCurve.Type.OutBack)

        self.exit_animation = QPropertyAnimation(self, b"windowOpacity")
        self.exit_animation.setDuration(500)
        self.exit_animation.setEasingCurve(QEasingCurve.Type.InQuad)

        # Temporizador
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_exit_animation)

        # Estado interno
        self._is_showing = False
        self._enter_connected = False
        self._exit_connected = False
        self.hide()

    def show_message(self, message, message_type="info"):
        """Muestra un mensaje con animación de entrada"""
        if self._is_showing:
            self._cancel_pending_animations()

        # Configurar estilo según el tipo de mensaje
        styles = {
            "success": {
                "background": "#d4edda",
                "border": "#c3e6cb",
                "text": "#155724",
                "icon": "✓",
            },
            "error": {
                "background": "#f8d7da",
                "border": "#f5c6cb",
                "text": "#721c24",
                "icon": "✗",
            },
            "warning": {
                "background": "#fff3cd",
                "border": "#ffeeba",
                "text": "#856404",
                "icon": "⚠",
            },
            "info": {
                "background": "#d1ecf1",
                "border": "#bee5eb",
                "text": "#0c5460",
                "icon": "ℹ",
            },
        }

        style = styles.get(message_type, styles["info"])
        self.label.setText(f"{style['icon']} {message}")
        self.setStyleSheet(
            f"""
            background-color: {style['background']};
            border: 1px solid {style['border']};
            border-radius: 8px;
            padding: 12px;
            color: {style['text']};
            font-weight: bold;
        """
        )

        # Calcular posición relativa dentro de la ventana principal
        parent_rect = self.parent().rect()
        margin = 20

        # Posición final (esquina inferior derecha relativa al padre)
        end_x = parent_rect.width() - self.width() - margin
        end_y = parent_rect.height() - self.height() - margin
        end_pos = QRect(end_x, end_y, self.width(), self.height())

        # Posición inicial (fuera del borde derecho del padre)
        start_pos = QRect(parent_rect.width() + 10, end_y, self.width(), self.height())

        # Configurar animación de entrada
        self.enter_animation.setStartValue(start_pos)
        self.enter_animation.setEndValue(end_pos)

        # Conectar señal solo si no está conectada
        if not self._enter_connected:
            self.enter_animation.finished.connect(self._on_enter_animation_finished)
            self._enter_connected = True

        # Mostrar y animar
        self.show()
        self.raise_()
        self.setWindowOpacity(1.0)
        self._is_showing = True
        self.enter_animation.start()

        # Programar temporizador para ocultar
        self.timer.start(4000)

    def _cancel_pending_animations(self):
        """Cancela animaciones pendientes de forma segura"""
        self.timer.stop()
        self.enter_animation.stop()
        self.exit_animation.stop()

        # Desconectar solo si estaba conectado
        if self._enter_connected:
            try:
                self.enter_animation.finished.disconnect()
            except TypeError:
                pass
            self._enter_connected = False

        if self._exit_connected:
            try:
                self.exit_animation.finished.disconnect()
            except TypeError:
                pass
            self._exit_connected = False

    def _on_enter_animation_finished(self):
        """Manejador cuando termina la animación de entrada"""
        self._enter_connected = False

    def start_exit_animation(self):
        """Inicia la animación de salida"""
        if not self._is_showing:
            return

        self._cancel_pending_animations()
        self.exit_animation.setStartValue(1.0)
        self.exit_animation.setEndValue(0.0)

        # Conectar señal solo si no está conectada
        if not self._exit_connected:
            self.exit_animation.finished.connect(self._on_exit_animation_finished)
            self._exit_connected = True

        self.exit_animation.start()

    def _on_exit_animation_finished(self):
        """Manejador cuando termina la animación de salida"""
        self._exit_connected = False
        self._is_showing = False
        self.hide()

    def hide(self):
        """Oculta la notificación de forma segura"""
        super().hide()
        self.setWindowOpacity(1.0)
        self._is_showing = False
        self._cancel_pending_animations()

    def resizeEvent(self, event):
        """Ajusta posición cuando cambia el tamaño de la ventana principal"""
        if self.isVisible():
            parent_rect = self.parent().rect()
            margin = 20
            new_x = parent_rect.width() - self.width() - margin
            new_y = parent_rect.height() - self.height() - margin
            self.move(new_x, new_y)
        super().resizeEvent(event)
