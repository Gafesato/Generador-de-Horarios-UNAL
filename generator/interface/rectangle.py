import flet as ft

from generator.interface.widget import Widget


# Widget Rectangle
class Rectangle(Widget):
    def __init__(self, left=0, top=0, width=100, height=50, color="blue"):
        super().__init__("", left, top, width, height)
        self.rectangle = ft.Container(bgcolor=color, top=self.top, left=self.left, width=self.width, height=self.height)

    def create(self):
        return self.rectangle
