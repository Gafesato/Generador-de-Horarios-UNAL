import flet as ft

from generator.interface.widget import Widget


# Widget CheckBoxGroup
class CheckBoxGroup(Widget):
    def __init__(self, options, left=0, top=0, on_change=None):
        super().__init__("", left, top)
        self.options = options  # CheckBoxGroup Options
        self.selected_options = []  # List of selected options
        self.on_change = on_change  # Function to handle selection change
        
        # Create the individual CheckBoxes
        self.checkboxes = [
            ft.Checkbox(
                label=option,
                value=False,
                on_change=self._handle_change
            ) for option in options
        ]

    def _handle_change(self, e):
        """Actualiza la lista de opciones seleccionadas."""
        self.selected_options = [
            checkbox.label for checkbox in self.checkboxes if checkbox.value
        ]
        if self.on_change:
            self.on_change(e)  # Call the provided on_change function

    def create(self):
        """Crea y retorna el contenedor del CheckBoxGroup."""
        return ft.Container(
            content=ft.Column(controls=self.checkboxes),
            left=self.left,
            top=self.top,
        )
