import flet as ft

from generator.interface.widget import Widget


# Class to manage pages and switch between them
class PageManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.pages = {}  # Dictionary for storing pages
        self.current_page = None  # Current page being displayed
        
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
