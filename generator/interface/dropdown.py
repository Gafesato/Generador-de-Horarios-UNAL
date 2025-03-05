import flet as ft

from generator.interface.widget import Widget


# Widget Dropdown
class Dropdown(Widget):
    def __init__(self, options, left=0, top=0, width=200, on_change=None):
        super().__init__("", left, top)
        self.options = options
        self.selected_option = options[0] if options else None
        self.on_change_callback = on_change  # Callback to handle the on_change event

        self.dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(option) for option in options],
            on_change=self.update_selected_option,
            width=width,
            content_padding=ft.padding.symmetric(horizontal=10),  # Adjusts the internal padding
            alignment=ft.alignment.center_left,  # Align content to the left
        )

    def update_selected_option(self, e):
        self.selected_option = e.control.value
        if self.on_change_callback:  # If there is a callback, call it
            self.on_change_callback(e)

    def create(self):
        return ft.Container(content=self.dropdown, left=self.left, top=self.top)



