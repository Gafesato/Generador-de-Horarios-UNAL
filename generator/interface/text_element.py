import flet as ft

from generator.interface.widget import Widget


# Clase para los textos que extiende de Widget
class TextElement(Widget):
    def __init__(
        self,
        value="",
        size=24,
        left=0,
        top=0,
        text_color="black",
        bg_color="white",
        width=100,
        height=50,
        page=None,
        text_align="top-left",  # Nuevo atributo para controlar la alineación del texto
    ):
        super().__init__(value, left, top, width, height)
        self.size = size
        self.text_color = text_color
        self.bg_color = bg_color
        self.page = page  # Pasar la referencia de la página
        self.text_align = text_align  # Alineación del texto

        # Crear el Text
        self.text = ft.Text(value=self.value, size=self.size, color=self.text_color)

        # Configurar la alineación del texto dentro del Container
        self.container = ft.Container(
            content=ft.Column(
                controls=[self.text],
                scroll=ft.ScrollMode.AUTO,  # Habilitar el desplazamiento
            ),
            left=self.left,
            top=self.top,
            width=self.width,
            height=self.height,
            bgcolor=self.bg_color,
            padding=10,
            border_radius=5,
        )

        # Aplicar la alineación del texto
        self._apply_text_alignment()

    def _apply_text_alignment(self):
        """Aplica la alineación del texto según el valor de text_align."""
        if self.text_align == "center":
            # Centrar el texto vertical y horizontalmente
            self.container.alignment = ft.alignment.center
        elif self.text_align == "center-left":
            # Centrar verticalmente y alinear a la izquierda
            self.container.alignment = ft.alignment.center_left
        else:
            # Por defecto: alinear en la parte superior izquierda
            self.container.alignment = ft.alignment.top_left

    def create(self):
        return self.container  # Retornar el container creado

    def update(self, text=None, text_color=None, bg_color=None, text_align=None):
        """Actualiza las propiedades del texto: texto, color del texto, color de fondo y alineación."""
        if text is not None:
            self.text.value = text  # Actualizar el texto
        if text_color is not None:
            self.text.color = text_color  # Actualizar color del texto
        if bg_color is not None:
            self.bg_color = bg_color  # Actualizar el color de fondo
            self.container.bgcolor = bg_color  # Actualizar el color de fondo del container
        if text_align is not None:
            self.text_align = text_align  # Actualizar la alineación del texto
            self._apply_text_alignment()  # Aplicar la nueva alineación

        if self.page:  # Asegurarse de que page esté disponible
            self.page.update()  # Actualizar la página para reflejar el cambio


