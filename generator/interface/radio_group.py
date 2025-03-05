import flet as ft

from generator.interface.widget import Widget


# Widget RadioGroup
class RadioGroup(Widget):
    def __init__(self, options, left=0, top=0, on_change=None):
        super().__init__("", left, top)
        self.options = options  # RadioGroup Options
        self.selected_option = options[0] if options else None  # Option selected by default
        self.on_change = on_change  # Function to handle selection change

        # Create the RadioGroup with the options
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

        # Associate an event to handle selection change
        if self.on_change:
            self.radio_group.on_change = self._handle_change

    def _handle_change(self, e):
        """Actualiza la opción seleccionada en el RadioGroup."""
        self.selected_option = e.control.value
        if self.on_change:
            self.on_change(e)  # Call the provided on_change function

    def create(self):
        return ft.Container(content=self.radio_group, left=self.left, top=self.top)


