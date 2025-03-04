import flet as ft

from generator.interface.widget import Widget


# Widget RadioGroup
class RadioGroup(Widget):
    def __init__(self, options, left=0, top=0, on_change=None):
        super().__init__("", left, top)
        self.options = options  # Opciones del RadioGroup
        self.selected_option = options[0] if options else None  # Opción seleccionada por defecto
        self.on_change = on_change  # Función para manejar el cambio de selección

        # Crear el RadioGroup con las opciones
        self.radio_group = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Radio(
                        value=option,
                        label=option,
                    ) for option in options
                ]
            )
        )

        # Asociar un evento para manejar el cambio de selección
        if self.on_change:
            self.radio_group.on_change = self._handle_change

    def _handle_change(self, e):
        """Actualiza la opción seleccionada en el RadioGroup."""
        self.selected_option = e.control.value
        if self.on_change:
            self.on_change(e)  # Llamar a la función on_change proporcionada

    def create(self):
        return ft.Container(content=self.radio_group, left=self.left, top=self.top)


