import flet as ft

from generator.interface.widget import Widget


# Widget Dropdown
class Dropdown(Widget):
    def __init__(self, options, left=0, top=0, width=200, on_change=None):
        super().__init__("", left, top)
        self.options = options
        self.selected_option = options[0] if options else None
        self.on_change_callback = on_change  # Callback para manejar el evento on_change

        self.dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(option) for option in options],
            on_change=self.update_selected_option,
            width=width,
            content_padding=ft.padding.symmetric(horizontal=10),  # Ajusta el padding interno
            alignment=ft.alignment.center_left,  # Alinea el contenido a la izquierda
        )

    def update_selected_option(self, e):
        self.selected_option = e.control.value
        if self.on_change_callback:  # Si hay un callback, llamarlo
            self.on_change_callback(e)

    def create(self):
        return ft.Container(content=self.dropdown, left=self.left, top=self.top)



