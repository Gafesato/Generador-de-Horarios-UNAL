import flet as ft

from generator.interface.widget import Widget


# Widget TextArea
class TextArea(Widget):
    def __init__(self, left=0, top=0, hint_area="Text Area", on_change=None):
        super().__init__("", left, top)
        self.value = ""  # Para almacenar el texto ingresado
        self.on_change = on_change

        self.text_area = ft.TextField(
            multiline=True,
            label=hint_area,
            height=100,
            on_change=self.on_change,
            on_blur=self.update_text  # Actualizar el valor al perder foco
        )

    def update_text(self, e):
        """Actualiza el valor del TextArea cuando pierde el foco."""
        self.value = e.control.value
        #print(f"Texto actualizado: {self.value}")  # Para depuración

    def create(self):
        return ft.Container(content=self.text_area, left=self.left, top=self.top)

