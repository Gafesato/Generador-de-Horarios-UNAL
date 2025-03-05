import flet as ft

from generator.interface.widget import Widget


# Class for texts that extends from Widget
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
        text_align="top-left",  # New attribute to control text alignment
    ):
        super().__init__(value, left, top, width, height)
        self.size = size
        self.text_color = text_color
        self.bg_color = bg_color
        self.page = page  # Pass the page reference
        self.text_align = text_align  # Text alignment

        # Create the Text
        self.text = ft.Text(value=self.value, size=self.size, color=self.text_color)

        # Setting text alignment inside the Container
        self.container = ft.Container(
            content=ft.Column(
                controls=[self.text],
                scroll=ft.ScrollMode.AUTO,  # Enable scrolling
            ),
            left=self.left,
            top=self.top,
            width=self.width,
            height=self.height,
            bgcolor=self.bg_color,
            padding=10,
            border_radius=5,
        )

        # Apply text alignment
        self._apply_text_alignment()

    def _apply_text_alignment(self):
        """Aplica la alineación del texto según el valor de text_align."""
        if self.text_align == "center":
            # Center text vertically and horizontally
            self.container.alignment = ft.alignment.center
        elif self.text_align == "center-left":
            # Center vertically and align left
            self.container.alignment = ft.alignment.center_left
        else:
            # Default: Align Top Left
            self.container.alignment = ft.alignment.top_left

    def create(self):
        return self.container  # Return the created container

    def update(self, text=None, text_color=None, bg_color=None, text_align=None):
        """Actualiza las propiedades del texto: texto, color del texto, color de fondo y alineación."""
        if text is not None:
            self.text.value = text  # Update text
        if text_color is not None:
            self.text.color = text_color  # Update text color
        if bg_color is not None:
            self.bg_color = bg_color  # Update background color
            self.container.bgcolor = bg_color  # Update the container background color
        if text_align is not None:
            self.text_align = text_align  # Update text alignment
            self._apply_text_alignment()  # Apply the new alignment

        if self.page:  # Make sure page is available
            self.page.update()  # Update the page to reflect the change


