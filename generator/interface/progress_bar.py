import flet as ft

from generator.interface.widget import Widget


# Widget ProgressBar
class ProgressBar(Widget):
    def __init__(self, value=0, left=0, top=0):
        super().__init__("", left, top)
        self.progress_bar = ft.ProgressBar(value=value)

    def create(self):
        return ft.Container(content=self.progress_bar, left=self.left, top=self.top)

