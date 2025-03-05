import flet as ft

from generator.interface.widget import Widget


# Widget PopupMenu
class PopupMenu(Widget):
    def __init__(self, options, icon="▼", left=0, top=0, text_color="white", tooltip="Show menu",
        bg_color="gray", font_size=16, border_radius=5, width=120, height=40, page=None
    ):
        super().__init__("", left, top, width, height)
        self.options = options
        self.selected_option = options[0] if options else None
        self.text_color = text_color
        self.bg_color = bg_color
        self.font_size = font_size
        self.border_radius = border_radius
        self.page = page

        # Creating the custom PopupMenuButton
        self.popup_menu = ft.PopupMenuButton(
            icon=icon,
            tooltip=tooltip,
            content=ft.Container(
                bgcolor=self.bg_color,
                border_radius=self.border_radius,
                padding=10,
                content=ft.Text(
                    value=icon,  
                    size=self.font_size,
                    color=self.text_color,
                ),
            ),
            items=[
                ft.PopupMenuItem(text=option, on_click=self.update_selected_option)
                for option in options
            ],
        )



    def update_selected_option(self, e):
        """Actualiza la opción seleccionada en el PopupMenu."""
        self.selected_option = e.control.text
        #print(f"Opción seleccionada: {self.selected_option}")

    def create(self):
        """Crea y retorna el contenedor del PopupMenu."""
        return ft.Container(
            content=self.popup_menu,
            left=self.left,
            top=self.top,
            width=self.width,
            height=self.height,
        )
