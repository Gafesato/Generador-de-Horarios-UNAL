import flet as ft

from generator.interface.widget import Widget


# Widget Slider
class Slider(Widget):
    def __init__(self, min_value=0, max_value=100, left=0, top=0):
        super().__init__("", left, top)
        self.slider = ft.Slider(min=min_value, max=max_value)

    def create(self):
        return ft.Container(content=self.slider, left=self.left, top=self.top)
