import flet as ft

from generator.interface.widget import Widget


# Widget Button
class Button(Widget):
    def __init__(self, label, action=None, left=0, top=0, 
                 bg_color=ft.Colors.GREY_900, text_color=ft.Colors.BLUE_200, 
                 width=90, height=60, border_radius=8, font_size=16):
        super().__init__("", left, top)

        # Crear el botón con las propiedades personalizadas
        self.button = ft.ElevatedButton(
            text=label,
            on_click=action,
            bgcolor=bg_color,  # Color de fondo
            color=text_color,  # Color del texto
            width=width,       # Ancho del botón
            height=height,     # Alto del botón
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=border_radius),
                text_style=ft.TextStyle(size=font_size)
            )
        )

    def create(self):
        return ft.Container(
            content=self.button,
            left=self.left,
            top=self.top
        )


