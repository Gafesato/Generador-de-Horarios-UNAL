import flet as ft

from generator.interface.widget import Widget


# Widget Switch 
class Switch(Widget):
    def __init__(self, value=False, left=0, top=0):
        super().__init__("", left, top)  # "" porque no necesita una etiqueta
        self.state = value  # Estado inicial del Switch (True o False)
        self.switch = ft.Switch(value=value, on_change=self.toggle_state)

    def toggle_state(self, e):
        """Actualiza el estado del Switch."""
        self.state = self.switch.value
        #print(f"Switch cambiado: {self.state}")  # Para verificar en la consola

    def create(self):
        return ft.Container(content=self.switch, left=self.left, top=self.top)
