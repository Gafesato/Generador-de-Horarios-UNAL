import flet as ft

from generator.interface.widget import Widget


# Clase para manejar páginas y cambiar entre ellas
class PageManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.pages = {}  # Diccionario para almacenar las páginas
        self.current_page = None  # Página actual que se muestra

    def add_page(self, name: str, widgets: list):
        """Agrega una nueva página con un nombre y una lista de widgets."""
        self.pages[name] = widgets

    def show_page(self, name: str):
        """Muestra una página específica por su nombre."""
        if name in self.pages:
            self.page.controls.clear()
            self.page.add(ft.Stack(controls=[widget.create() for widget in self.pages[name]]))
            self.page.update()
            self.current_page = name