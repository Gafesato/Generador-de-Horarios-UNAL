import flet as ft

from generator.interface.widget import Widget


# Widget CheckBox
class CheckBox(Widget):
    def __init__(self, label, left=0, top=0):
        super().__init__(label, left, top)
        self.state = False  # Initial state of the CheckBox (True o False)
        self.checkbox = ft.Checkbox(label=label, on_change=self.toggle_var)

    def toggle_var(self, e):
        """Actualiza el estado del CheckBox."""
        self.state = self.checkbox.value
        #print(f"CheckBox cambiado: {self.state}")  # To check in the console

    def create(self):
        return ft.Container(content=self.checkbox, left=self.left, top=self.top)
