import flet as ft

from generator.interface.widget import Widget


# Widget Circle
class Circle(Widget):
    def __init__(self, left=0, top=0, diameter=50, color="red"):
        super().__init__("", left, top, diameter, diameter)
        self.circle = ft.Container(bgcolor=color, top=self.top, left=self.left, width=self.width, height=self.height, border_radius=self.width / 2)

    def create(self):
        return self.circle
