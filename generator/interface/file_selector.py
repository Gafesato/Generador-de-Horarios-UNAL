import flet as ft

from generator.interface.widget import Widget


# Class to select files
class FileSelector: #*******************************************************************************************************************************************Falta
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_file = None  # Almacena la ruta del archivo seleccionado
        self.file_picker = ft.FilePicker(on_result=self._on_file_selected)
        self.page.overlay.append(self.file_picker)  # Agregar el FilePicker al overlay de la página

    def _on_file_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_file = e.files[0].path
            snack_bar = ft.SnackBar(ft.Text(f"Archivo seleccionado: {self.selected_file}"))
            self.page.overlay.append(snack_bar)  # Agregar el SnackBar al overlay
            snack_bar.open = True  # Mostrar el SnackBar
            self.page.update()  # Actualizar la página para que se renderice correctamente

    def select_file(self, e):
        self.file_picker.pick_files(allow_multiple=False)
