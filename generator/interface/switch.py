import flet as ft

from generator.interface.widget import Widget


# Widget Switch 
class Switch(Widget):
    def __init__(self, value=False, left=0, top=0):
        super().__init__("", left, top)  # "" because it doesn't need a tag
        self.state = value  # Initial state of the switch (True o False)
        self.switch = ft.Switch(value=value, on_change=self.toggle_state)

    def toggle_state(self, e):
        """Actualiza el estado del Switch."""
        self.state = self.switch.value
        #print(f"Switch cambiado: {self.state}")  # To check in the console

    def create(self):
        return ft.Container(content=self.switch, left=self.left, top=self.top)
