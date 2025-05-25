from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPalette, QColor
import json
import os

class ThemeManager(QObject):
    theme_changed = pyqtSignal(str)  # Señal que emite cuando cambia el tema
    
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        self.config_file = "theme_config.json"
        self.load_theme_preference()
        
    def get_theme_colors(self):
        """Retorna los colores del tema actual basados en el mockup"""
        themes = {
            "light": {
                # Sidebar
                "sidebar_bg": "#E4FAFA",  # Color de fondo claro
                "sidebar_text": "#666666",  # Texto de categorías
                
                # Botones
                "button_bg": "#FFFFFF",
                "button_text": "#4CA4A5",
                "button_hover_bg": "#E4FFF3",
                "button_selected_bg": "#4CA4A5",
                "button_selected_text": "#FFFFFF",
                
                # General
                "text_primary": "#333333",
                "text_secondary": "#666666",
                "accent": "#4CA4A5",
                "surface": "#FFFFFF",
                "border": "#E0E0E0",
                
                # Panel específicos
                "panel_bg": "#FFFFFF",
                "table_header_bg": "#4CA4A5",
                "table_grid": "#c5efec",
                "table_selection": "#d4f1f0",
                "table_alternate": "#f8fafc"
            },
            "dark": {
                # Sidebar  (#013134)
                "sidebar_bg": "#013134",  # Color principal 
                "sidebar_text": "#FFFFFF",  # Texto blanco para categorías
                
                # Botones - Estados del mockup
                "button_bg": "#1A4A4D",  # Ligeramente más claro que el fondo
                "button_text": "#FFFFFF",
                "button_hover_bg": "#2A5A5D",  # Estado HOVER del mockup
                "button_selected_bg": "#4CA4A5",  # Mantener el accent color
                "button_selected_text": "#FFFFFF",
                
                # General
                "text_primary": "#FFFFFF",
                "text_secondary": "#B0B0B0",
                "accent": "#4CA4A5",
                "surface": "#1A4A4D",
                "border": "#2A5A5D",
                
                # Panel específicos para modo oscuro
                "panel_bg": "#1A4A4D",  # Fondo de paneles en modo oscuro
                "table_header_bg": "#4CA4A5",  # Mantener el accent para headers
                "table_grid": "#2A5A5D",  # Líneas de la tabla
                "table_selection": "#2A5A5D",  # Selección en tabla
                "table_alternate": "#013134"  # Filas alternadas
            }
        }
        return themes.get(self.current_theme, themes["light"])
    
    def toggle_theme(self):
        """Alterna entre modo claro y oscuro"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.save_theme_preference()
        self.theme_changed.emit(self.current_theme)
        return self.current_theme
    
    def set_theme(self, theme_name):
        """Establece un tema específico"""
        if theme_name in ["light", "dark"]:
            self.current_theme = theme_name
            self.save_theme_preference()
            self.theme_changed.emit(self.current_theme)
    
    def is_dark_mode(self):
        """Retorna True si está en modo oscuro"""
        return self.current_theme == "dark"
    
    def get_sidebar_stylesheet(self):
        """Retorna el stylesheet para el sidebar según el tema actual"""
        colors = self.get_theme_colors()
        
        return f"""
        QWidget {{
            background-color: {colors['sidebar_bg']};
        }}
        """
    
    def get_button_stylesheet(self):
        """Retorna el stylesheet para los botones según el tema actual"""
        colors = self.get_theme_colors()
        
        return f"""
        QPushButton {{
            background-color: {colors['button_bg']};
            border-radius: 8px;
            border: none;
            color: {colors['button_text']};
            font-size: 14px;
            font-weight: 500;  
            padding-left: 15px;
            padding: 10px 15px;
            text-align: left;
            padding-right: 15px;
        }}
        QPushButton:hover {{
            background-color: {colors['button_hover_bg']};
        }}
        QPushButton:checked {{
            background-color: {colors['button_selected_bg']};
            color: {colors['button_selected_text']};
            font-weight: 600;
        }}
        QPushButton::icon {{
            padding-left: 20px;
        }}
        """
    
    def get_category_label_stylesheet(self):
        """Retorna el stylesheet para las etiquetas de categoría"""
        colors = self.get_theme_colors()
        
        return f"""
        color: {colors['sidebar_text']};
        font-size: 12px;
        font-weight: bold;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
        """
    
    def get_theme_toggle_stylesheet(self):
        """Retorna el stylesheet para el botón de alternancia de tema"""
        colors = self.get_theme_colors()
        
        return f"""
        QPushButton {{
            background-color: {colors['button_bg']};
            border-radius: 20px;
            border: 2px solid {colors['accent']};
            color: {colors['button_text']};
            font-size: 12px;
            font-weight: 600;
            padding: 8px 16px;
            min-width: 80px;
        }}
        QPushButton:hover {{
            background-color: {colors['button_hover_bg']};
        }}
        QPushButton:pressed {{
            background-color: {colors['accent']};
            color: {colors['button_selected_text']};
        }}
        """
    
    def get_panel_stylesheet(self):
        """Retorna el stylesheet base para paneles"""
        colors = self.get_theme_colors()
        
        return f"""
        QFrame {{
            background-color: {colors['panel_bg']};
            border-radius: 12px;
            border: none;
        }}
        """
    
    def get_input_stylesheet(self):
        """Retorna el stylesheet para campos de entrada"""
        colors = self.get_theme_colors()
        
        return f"""
        QLineEdit {{
            background-color: {colors['surface']};
            border: 1px solid {colors['accent']};
            color: {colors['text_primary']};
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 14px;
        }}
        QLineEdit:focus {{
            border: 2px solid {colors['accent']};
        }}
        """
    
    def save_theme_preference(self):
        """Guarda la preferencia de tema en un archivo"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({"theme": self.current_theme}, f)
        except Exception as e:
            print(f"Error al guardar preferencia de tema: {e}")
    
    def load_theme_preference(self):
        """Carga la preferencia de tema desde archivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.current_theme = data.get("theme", "light")
        except Exception as e:
            print(f"Error al cargar preferencia de tema: {e}")
            self.current_theme = "light"

# Instancia global del theme manager
theme_manager = ThemeManager()