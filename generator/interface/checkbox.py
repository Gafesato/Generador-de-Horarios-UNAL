import flet as ft

from generator.interface.widget import Widget


# Widget CheckBox
class CheckBox(Widget):
    def __init__(self, label, left=0, top=0):
        super().__init__(label, left, top)
        self.state = False  # Estado inicial del CheckBox (True o False)
        self.checkbox = ft.Checkbox(label=label, on_change=self.toggle_var)

    def toggle_var(self, e):
        """Actualiza el estado del CheckBox."""
        self.state = self.checkbox.value
        #print(f"CheckBox cambiado: {self.state}")  # Para verificar en la consola

    def create(self):
        return ft.Container(content=self.checkbox, left=self.left, top=self.top)

