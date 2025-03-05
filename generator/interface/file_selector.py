import flet as ft

from generator.interface.widget import Widget


# Class to select files
class FileSelector: #*******************************************************************************************************************************************Falta
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_file = None  # Stores the path of the selected file
        self.file_picker = ft.FilePicker(on_result=self._on_file_selected)
        self.page.overlay.append(self.file_picker)  # Adding the FilePicker to the page overlay

    def _on_file_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_file = e.files[0].path
            snack_bar = ft.SnackBar(ft.Text(f"Archivo seleccionado: {self.selected_file}"))
            self.page.overlay.append(snack_bar)  # Adding the SnackBar to the overlay
            snack_bar.open = True  # Show the SnackBar
            self.page.update()  # Update the page so it renders correctly

    def select_file(self, e):
        self.file_picker.pick_files(allow_multiple=False)
