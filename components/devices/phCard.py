from PyQt6.QtWidgets import (
    QFrame, QLabel, QHBoxLayout, QVBoxLayout, QSlider, QLineEdit, QTextEdit, QSizePolicy, QPushButton, QGraphicsDropShadowEffect
)
from components.ImageViewer import ImageViewer
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIntValidator, QColor
from components.devices.phConfigModel import PhConfigModel
import os
from dotenv import load_dotenv
load_dotenv()
SHADOW = os.getenv("SHADOW", "0,0,0")

class PhCard(QFrame):
    def __init__(self, notificationes, parent=None):
        super().__init__(parent)
        self.setObjectName("phCard")
        self.notification = notificationes
        self.setStyleSheet("""
            QFrame#phCard {
                background: #fff;
                border-radius: 16px;
                border: 1px solid #eee;
            }
            QLabel, QLineEdit {
                color: #000;
            }
            QTextEdit {
                background: #fff;
                color: #000;
                border-radius: 8px;
                border: 1px solid #eee;
                font-size: 11pt;
                padding: 4px;
            }
            QTextEdit::teaser {
                color: #777;
            }
            QScrollBar:vertical {
                border: none;
                background: #ccc;
                width: 6px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #999;
                min-height: 25px;
                border-radius: 3px;
            }
            QScrollBar::add-line:vertical {
                background: none;
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        """)
        self.setMinimumWidth(600)
        self.setMaximumWidth(900)
        self.setContentsMargins(16, 16, 16, 16)

        # --- SOMBRA estilo cardDashboard.py ---
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        r, g, b = map(int, SHADOW.split(","))
        shadow.setColor(QColor(r, g, b))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(16, 16, 16, 16)

        self.toggle_button = QPushButton("▼")
        self.toggle_button.setFixedSize(28, 28)
        self.toggle_button.setStyleSheet('''
            QPushButton {
                background: transparent;
                border: none;
                font-size: 18px;
                color: #045859;
            }
            QPushButton:hover {
                color: #4ca4a5;
            }
        ''')
        self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.clicked.connect(self.toggle_arrow)

        # Título con imagen clickable y botón
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes internos
        title_layout.setSpacing(6)  # Espaciado mínimo entre elementos

        img_label = QLabel()
        img_label.setFixedSize(36, 36)
        img_label.setCursor(Qt.CursorShape.PointingHandCursor)
        img_label.setStyleSheet("background: none; margin: 0 10px 0 0; padding: 0px;")
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_path = os.path.join(os.path.dirname(__file__), '../../resources/media/sensores/ph.jpg')
        if os.path.exists(img_path):
            img_label.setPixmap(QPixmap(img_path).scaled(36, 36, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            img_label.setText("PH")
        img_label.mousePressEvent = lambda event: self._show_image_viewer(img_path)

        title = QLabel("<b>Sensor de pH</b>")
        title.setFont(QFont("Arial", 14))
        title.setStyleSheet("color: #045859; padding: 0px; margin: 0px;")
        title.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        title_layout.addWidget(self.toggle_button)
        title_layout.addWidget(img_label)
        title_layout.addWidget(title)
        title_layout.addStretch()

        main_layout.addLayout(title_layout)

        # Área de configuración
        self.config_widget = QFrame()
        config_layout = QHBoxLayout(self.config_widget)
        config_layout.setSpacing(24)
        config_layout.setContentsMargins(0, 0, 0, 0)
        self.config_widget.hide()

        # Columna izquierda (sliders)
        left_col = QVBoxLayout()
        left_col.setSpacing(16)

        # Valor mínimo
        min_label = QLabel("Valor Mínimo")
        min_label.setFont(QFont("Arial", 10))
        left_col.addWidget(min_label)

        min_slider_layout = QHBoxLayout()
        min_slider_layout.setContentsMargins(0, 0, 0, 0)  # Espaciado vertical extra
        min_slider_layout.setSpacing(12)
        self.min_slider = QSlider(Qt.Orientation.Horizontal)
        self.min_slider.setMinimum(0)
        self.min_slider.setMaximum(14)
        self.min_slider.setValue(0)
        self.min_slider.setMinimumHeight(20)  # Altura mínima para evitar corte de la bolita
        self.min_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.min_slider.setStyleSheet(self.slider_style())

        self.min_input = QLineEdit("0")
        self.min_input.setFixedWidth(40)
        self.min_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.min_input.setReadOnly(True)
        self.min_input.setStyleSheet(self.input_style())

        min_slider_layout.addWidget(self.min_slider)
        min_slider_layout.addWidget(self.min_input)
        left_col.addLayout(min_slider_layout)

        # Valor máximo
        max_label = QLabel("Valor Máximo")
        max_label.setFont(QFont("Arial", 10))
        left_col.addWidget(max_label)

        max_slider_layout = QHBoxLayout()
        max_slider_layout.setContentsMargins(0, 0, 0, 0)  # Espaciado vertical extra
        max_slider_layout.setSpacing(12)
        self.max_slider = QSlider(Qt.Orientation.Horizontal)
        self.max_slider.setMinimum(0)
        self.max_slider.setMaximum(14)
        self.max_slider.setValue(14)
        self.max_slider.setMinimumHeight(20)  # Altura mínima para evitar corte de la bolita
        self.max_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.max_slider.setStyleSheet(self.slider_style())

        self.max_input = QLineEdit("14")
        self.max_input.setFixedWidth(40)
        self.max_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.max_input.setReadOnly(True)
        self.max_input.setStyleSheet(self.input_style())

        max_slider_layout.addWidget(self.max_slider)
        max_slider_layout.addWidget(self.max_input)
        left_col.addLayout(max_slider_layout)

        # Batido cítrico
        citrico_label = QLabel("Tiempo batido cítrico (s)")
        citrico_label.setFont(QFont("Arial", 10))
        left_col.addWidget(citrico_label)

        citrico_slider_layout = QHBoxLayout()
        citrico_slider_layout.setContentsMargins(0, 0, 0, 0)  # Espaciado vertical extra
        citrico_slider_layout.setSpacing(12)
        self.citrico_slider = QSlider(Qt.Orientation.Horizontal)
        self.citrico_slider.setMinimum(0)
        self.citrico_slider.setMaximum(120)
        self.citrico_slider.setValue(0)
        self.citrico_slider.setMinimumHeight(20)  # Altura mínima para evitar corte de la bolita
        self.citrico_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.citrico_slider.setStyleSheet(self.slider_style())

        self.citrico_input = QLineEdit("0")
        self.citrico_input.setFixedWidth(40)
        self.citrico_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.citrico_input.setReadOnly(True)
        self.citrico_input.setStyleSheet(self.input_style())

        citrico_slider_layout.addWidget(self.citrico_slider)
        citrico_slider_layout.addWidget(self.citrico_input)
        left_col.addLayout(citrico_slider_layout)
        self.citrico_slider.valueChanged.connect(lambda val: self.citrico_input.setText(str(val)))

        # Bicarbonato de sodio
        bicarb_label = QLabel("Tiempo batido bicarbonato (s)")
        bicarb_label.setFont(QFont("Arial", 10))
        left_col.addWidget(bicarb_label)

        bicarb_slider_layout = QHBoxLayout()
        bicarb_slider_layout.setContentsMargins(0, 0, 0, 0)  # Espaciado vertical extra
        bicarb_slider_layout.setSpacing(12)
        self.bicarb_slider = QSlider(Qt.Orientation.Horizontal)
        self.bicarb_slider.setMinimum(0)
        self.bicarb_slider.setMaximum(120)
        self.bicarb_slider.setValue(0)
        self.bicarb_slider.setMinimumHeight(20)  # Altura mínima para evitar corte de la bolita
        self.bicarb_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.bicarb_slider.setStyleSheet(self.slider_style())

        self.bicarb_input = QLineEdit("0")
        self.bicarb_input.setFixedWidth(40)
        self.bicarb_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bicarb_input.setReadOnly(True)
        self.bicarb_input.setStyleSheet(self.input_style())

        bicarb_slider_layout.addWidget(self.bicarb_slider)
        bicarb_slider_layout.addWidget(self.bicarb_input)
        left_col.addLayout(bicarb_slider_layout)
        self.bicarb_slider.valueChanged.connect(lambda val: self.bicarb_input.setText(str(val)))

        left_col.addStretch()

        # Columna derecha (descripción)
        right_col = QVBoxLayout()
        right_col.setSpacing(16)

        desc_label = QLabel("Descripción")
        desc_label.setFont(QFont("Arial", 10))
        right_col.addWidget(desc_label)

        self.desc_text = QTextEdit()
        self.desc_text.setText(
            "Mide la acidez o alcalinidad del agua. Un pH de 7 es neutro, por debajo es ácido y por encima es alcalino.\n\n"
        )
        self.desc_text.setFont(QFont("Arial", 10))
        self.desc_text.setStyleSheet("background: #fff; color: #000; border-radius: 8px; border: 1px solid #eee;")
        self.desc_text.setMaximumHeight(120)  # Limita a aprox 3 líneas
        self.desc_text.textChanged.connect(self._limit_desc_text)
        right_col.addWidget(self.desc_text)

        self.save_button = QPushButton("Guardar configuración")
        self.save_button.setStyleSheet('''
            QPushButton {
                background-color: #074E52;
                color: #fff;
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 12pt;
                font-weight: bold;
                margin-top: 12px;
            }
            QPushButton:hover {
                background-color: #0b6a6f;
            }
        ''')
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        right_col.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.save_button.clicked.connect(self.save_ph_config)

        config_layout.addLayout(left_col)
        config_layout.addLayout(right_col)

        main_layout.addWidget(self.config_widget)

        # Cargar configuración inicial desde el modelo
        self._config_model = PhConfigModel()
        config = self._config_model.load() or {}
        min_val = config.get("valor_minimo", self.min_slider.value())
        max_val = config.get("valor_maximo", self.max_slider.value())
        citrico_val = config.get("tiempo_batido_citrico", self.citrico_slider.value())
        bicarb_val = config.get("tiempo_batido_bicarbonato", self.bicarb_slider.value())

        # Variables privadas para los valores
        self._min_val = min_val
        self._max_val = max_val
        self._citrico_val = citrico_val
        self._bicarb_val = bicarb_val
        self.min_slider.setValue(min_val)
        self.max_slider.setValue(max_val)
        self.citrico_slider.setValue(citrico_val)
        self.bicarb_slider.setValue(bicarb_val)

        # Guardar los valores originales para validación
        self._last_saved = {
            'min': self._min_val,
            'max': self._max_val,
            'citrico': self._citrico_val,
            'bicarb': self._bicarb_val
        }

        # Sincronización de sliders con inputs y variables
        self.min_slider.valueChanged.connect(self._update_min)
        self.max_slider.valueChanged.connect(self._update_max)
        self.citrico_slider.valueChanged.connect(self._update_citrico)
        self.bicarb_slider.valueChanged.connect(self._update_bicarb)
        # Validar cambios para el botón guardar
        self.min_slider.valueChanged.connect(self._validate_changes)
        self.max_slider.valueChanged.connect(self._validate_changes)
        self.citrico_slider.valueChanged.connect(self._validate_changes)
        self.bicarb_slider.valueChanged.connect(self._validate_changes)
        self.save_button.setEnabled(False)

    def _limit_desc_text(self):
        max_chars = 200
        current_text = self.desc_text.toPlainText()
        if len(current_text) > max_chars:
            # Bloquear señales para evitar bucles al actualizar el texto
            self.desc_text.blockSignals(True)
            self.desc_text.setPlainText(current_text[:max_chars])
            # Mueve el cursor al final
            cursor = self.desc_text.textCursor()
            cursor.setPosition(len(current_text[:max_chars]))
            self.desc_text.setTextCursor(cursor)
            self.desc_text.blockSignals(False)


    def set_config_values(self, min_val, max_val, citrico_val, bicarb_val):
        """
        Actualiza los 4 valores de configuración de la card y sincroniza sliders y QLineEdit.        """

        self._min_val = min_val
        self._max_val = max_val
        self._citrico_val = citrico_val
        self._bicarb_val = bicarb_val
        self.min_slider.setValue(min_val)
        self.max_slider.setValue(max_val)
        self.citrico_slider.setValue(citrico_val)
        self.bicarb_slider.setValue(bicarb_val)
        # Actualizar los valores guardados para la validación
        self._last_saved = {
            'min': min_val,
            'max': max_val,
            'citrico': citrico_val,
            'bicarb': bicarb_val
        }
        self._validate_changes()
        # Los QLineEdit se actualizan por las señales conectadas

    def _update_min(self, val):
        self._min_val = val
        self.min_input.setText(str(val))

    def _update_max(self, val):
        self._max_val = val
        self.max_input.setText(str(val))

    def _update_citrico(self, val):
        self._citrico_val = val
        self.citrico_input.setText(str(val))

    def _update_bicarb(self, val):
        self._bicarb_val = val
        self.bicarb_input.setText(str(val))

    def save_ph_config(self):
        """
        Guarda los valores de configuración de pH en la base de datos.
        """
        if self._min_val > self._max_val:
            self.notification.show_message("El valor mínimo no puede ser mayor que el valor máximo", "error")
            return
        ok = self._config_model.save(self._min_val, self._max_val, self._citrico_val, self._bicarb_val)
        if ok:
            self.notification.show_message("Configuración de pH guardada correctamente.", "success")
            # Actualiza los valores guardados
            self._last_saved = {
                'min': self._min_val,
                'max': self._max_val,
                'citrico': self._citrico_val,
                'bicarb': self._bicarb_val
            }
            self._validate_changes()
        else:
            self.notification.show_message("No se pudo guardar la configuración de pH.", "error")

    def _validate_changes(self):
        # Habilita el botón solo si hay cambios respecto a los valores guardados
        changed = (
            self._min_val != self._last_saved['min'] or
            self._max_val != self._last_saved['max'] or
            self._citrico_val != self._last_saved['citrico'] or
            self._bicarb_val != self._last_saved['bicarb']
        )
        self.save_button.setEnabled(changed)

    def toggle_arrow(self):
        if not self.toggle_button.isChecked():
            self.toggle_button.setText("▲")
            self.config_widget.show()
        else:
            self.toggle_button.setText("▼")
            self.config_widget.hide()

    def slider_style(self):
        return """
            QSlider::groove:horizontal {
                height: 6px;
                background: #c5efeb;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #4ca4a5;
                border-radius: 3px;
            }
            QSlider::add-page:horizontal {
                background: #c5efeb;
                border-radius: 3px;
            }
            QSlider::handle:horizontal { 
                background: #fff; 
                border: 2px solid #aaa; 
                width: 15px; 
                margin: -7px 0; 
                border-radius: 9px; 
            }
        """

    def _show_image_viewer(self, img_path):
        if os.path.exists(img_path):
            viewer = ImageViewer(img_path, self.window())
            viewer.show()

    def input_style(self):
        return """
            QLineEdit {
                color: #fff;
                border-radius: 8px;
                border: 2px solid #4ca4a5;
                padding: 4px 8px;
                margin-left: 8px;
                margin-right: 8px;
                min-width: 40px;
                background: #4ca4a5;
            }
        """
