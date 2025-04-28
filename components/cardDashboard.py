from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect,
    QGridLayout, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPixmap, QFont
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()
ICONS = os.getenv("ICONS")
MEDIA = os.getenv("MEDIA")
SHADOW = os.getenv("SHADOW")


class MarqueeLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.full_text = text + "     "
        self.index = 0
        self.setText(self.full_text)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_text)
        self.timer.start(150)

    def scroll_text(self):
        scrolled = self.full_text[self.index:] + self.full_text[:self.index]
        self.setText(scrolled)
        self.index = (self.index + 1) % len(self.full_text)


class CardDashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Ejemplo de datos
        self.cards_data = [
            {
                "titulo": "Temperatura del agua",
                "valor": 24.5,
                "unidad": "°C",
                "icono": f"{MEDIA}thermometer.png",
                "hora": "11:00",
                "estado": "óptimo",  # óptimo, medio, malo
                "tendencia": "estable",  # subiendo, bajando, estable
                "min": 10,
                "max": 35,
                "descripcion": "El valor de la temperatura indica si el agua está en condiciones saludables.",
                "info": "Ideal para organismos acuáticos.",
                "color": "#4ade80"
            },
            {
                "titulo": "Conductividad eléctrica",
                "valor": 750,
                "unidad": "μS/cm",
                "icono": f"{MEDIA}conductividad.png",
                "hora": "11:05",
                "estado": "medio",
                "tendencia": "subiendo",
                "min": 500,
                "max": 1500,
                "descripcion": "Refleja la capacidad del agua para conducir corriente eléctrica.",
                "info": "Indicador indirecto de salinidad y minerales disueltos.",
                "color": "#facc15"
            },
            {
                "titulo": "Temperatura ambiente",
                "valor": 29.0,
                "unidad": "°C",
                "icono": f"{MEDIA}ambiente_temp.png",
                "hora": "11:10",
                "estado": "óptimo",
                "tendencia": "subiendo",
                "min": 15,
                "max": 35,
                "descripcion": "Mide el calor del entorno donde se encuentra el agua.",
                "info": "Afecta la temperatura del agua superficial.",
                "color": "#60a5fa"
            },
            {
                "titulo": "Humedad ambiente",
                "valor": 70,
                "unidad": "%",
                "icono": f"{MEDIA}humedad.png",
                "hora": "11:12",
                "estado": "óptimo",
                "tendencia": "estable",
                "min": 30,
                "max": 80,
                "descripcion": "La humedad relativa del ambiente que rodea al cuerpo de agua.",
                "info": "Niveles adecuados favorecen condiciones climáticas estables.",
                "color": "#c084fc"
            },
            {
                "titulo": "Nivel del agua",
                "valor": 1.2,
                "unidad": "m",
                "icono": f"{MEDIA}nivel_agua.png",
                "hora": "11:15",
                "estado": "malo",
                "tendencia": "bajando",
                "min": 1.5,
                "max": 2.5,
                "descripcion": "Nivel actual del volumen de agua medido verticalmente.",
                "info": "Puede indicar escasez o exceso de agua según el valor.",
                "color": "#f87171"
            },
            {
                "titulo": "Nivel de pH del agua",
                "valor": 6.8,
                "unidad": "pH",
                "icono": f"{MEDIA}ph.png",
                "hora": "11:18",
                "estado": "óptimo",
                "tendencia": "estable",
                "min": 6.5,
                "max": 8.5,
                "descripcion": "Indica la acidez o alcalinidad del agua.",
                "info": "Un pH equilibrado es fundamental para la vida acuática.",
                "color": "#34d399"
            }
        ]


        main_layout = QVBoxLayout(self)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        row = 0
        col = 0

        for i, data in enumerate(self.cards_data):
            card = self.create_card(data)
            grid_layout.addWidget(card, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        main_layout.addLayout(grid_layout)

    def create_card(self, data):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setMinimumWidth(280)
        frame.setMaximumWidth(300)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                border: 2px solid {data["color"]};
            }}
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        r, g, b = map(int, SHADOW.split(","))
        shadow.setColor(QColor(r, g, b))
        shadow.setOffset(0, 3)
        frame.setGraphicsEffect(shadow)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Fila superior: ícono + título
        title_row = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setFixedSize(24, 24)
        pixmap = QPixmap(data["icono"]).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        title_text = QLabel(data["titulo"])
        title_text.setStyleSheet("font-size: 16px; font-weight: bold; color: #0f172a;")
        title_row.addWidget(icon_label)
        title_row.addSpacing(5)
        title_row.addWidget(title_text)
        title_row.addStretch()
        layout.addLayout(title_row)

        # Subtítulo y estado
        sub_row = QHBoxLayout()
        subt = QLabel(f"ACTUALIZADO HOY {data['hora']}")
        subt.setStyleSheet("font-size: 12px; font-style: italic; color: #6b7280;")
        sub_row.addWidget(subt)

        estado_icon = QLabel("✔️" if data["estado"] == "óptimo" else "➖" if data["estado"] == "medio" else "❌")
        sub_row.addStretch()
        sub_row.addWidget(estado_icon)
        layout.addLayout(sub_row)

        # Valor principal
        valor_row = QHBoxLayout()
        valor = QLabel(f"{data['valor']}")
        valor.setStyleSheet("font-size: 28px; font-weight: bold; color: #074e52;")
        unidad = QLabel(data["unidad"])
        unidad.setStyleSheet("font-size: 14px; color: #6b7280;")
        valor_row.addWidget(valor)
        valor_row.addSpacing(4)
        valor_row.addWidget(unidad)
        layout.addLayout(valor_row)

        # Tendencia
        tendencia_label = QLabel(data["tendencia"].upper())
        tendencia_label.setStyleSheet(f"""
            background-color: #f1f5f9;
            border: 1px solid #cbd5e1;
            color: #0f172a;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 5px;
            max-width: 80px;
        """)
        layout.addWidget(tendencia_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Rango
        rango_row = QHBoxLayout()
        rango_row.addWidget(QLabel(f"MIN: {data['min']}"))
        rango_row.addStretch()
        rango_row.addWidget(QLabel(f"MAX: {data['max']}"))
        layout.addLayout(rango_row)

        # Barra de porcentaje
        porcentaje = int(((data["valor"] - data["min"]) / (data["max"] - data["min"])) * 100)
        barra = QProgressBar()
        barra.setValue(min(max(porcentaje, 0), 100))
        barra.setTextVisible(False)
        barra.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 5px;
                background-color: #e2e8f0;
                height: 10px;
            }}
            QProgressBar::chunk {{
                background-color: {data["color"]};
                border-radius: 5px;
            }}
        """)
        layout.addWidget(barra)

        # Descripción
        descripcion = QLabel(data["descripcion"])
        descripcion.setWordWrap(True)
        descripcion.setStyleSheet("font-size: 11px; color: #475569;")
        layout.addWidget(descripcion)

        # Info
        info_box = QHBoxLayout()
        info_icon = QLabel("ℹ️")
        info_icon.setStyleSheet("font-size: 12px;")
        info_text = QLabel(data["info"])
        info_text.setWordWrap(True)
        info_text.setStyleSheet("font-size: 11px; color: #1e293b; background-color: #f8fafc; padding: 6px; border-radius: 8px;")
        info_box.addWidget(info_icon)
        info_box.addWidget(info_text)
        layout.addLayout(info_box)

        return frame