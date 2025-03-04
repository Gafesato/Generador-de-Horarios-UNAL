import flet as ft

from generator.interface.button import Button
from generator.interface.checkbox_group import CheckBoxGroup
from generator.interface.checkbox import CheckBox
from generator.interface.circle import Circle
from generator.interface.dropdown import Dropdown
from generator.interface.file_selector import FileSelector
from generator.interface.page_manager import PageManager
from generator.interface.popupmenu import PopupMenu
from generator.interface.progress_bar import ProgressBar
from generator.interface.radio_group import RadioGroup
from generator.interface.rectangle import Rectangle
from generator.interface.slider import Slider
from generator.interface.switch import Switch
from generator.interface.table import Table
from generator.interface.text_area import TextArea
from generator.interface.text_element import TextElement


# Clase principal de la aplicación
def main(page: ft.Page):
    # Configuración de la página
    page_manager = PageManager(page)
    page.bgcolor = ft.Colors.BLUE_GREY_500
    page.title = "App con Varios Widgets"
    # Crear un botón que se elimina a sí mismo al hacer clic
    def delete_self(e):
        delete_button_container.remove_self()  # Eliminar el botón de la página
        

    # Crear los widgets
    text1 = TextElement(value="Aquí van tus preguntas", size=14, left=0, top=125, width=1000, height=250, page=page, text_color=ft.Colors.WHITE, bg_color=ft.Colors.BLUE_GREY_900, text_align="center")
    text2 = TextElement(value="Text 2", left=500, top=180, text_color="black", bg_color="yellow", width=200, height=100, page=page, text_align="center")

    switch = Switch(left=50, top=320)
    table = Table([["Row 1 Col 1", "Row 1 Col 2"], ["Row 2 Col 1", "Row 2 Col 2"]], left=50, top=400)
    dropdown = Dropdown(["Option 1", "Option 2", "Option 3"], left=400, top=50)
    radio_group = RadioGroup(["Option A", "Option B", "Option C"], left=50, top=600)
    checkbox = CheckBox("Accept Terms", left=200, top=300)
    slider = Slider(left=50, top=800)
    #
    text_area = TextArea(left=50, top=100, hint_area="Ingrese algo :)", on_change=lambda e: add_x())
    rectangle = Rectangle(left=400, top=500, width=300, height=50, color="red")
    circle = Circle(left=1200, top=100, diameter=60, color="orange")
    progress_bar = ProgressBar(left=50, top=1200)

    button_add_x = Button("Add 'x'", lambda e: add_x(), left=50, top=320)
    button_change_color = Button("Change Color", lambda e: change_color(), left=200, top=320)
    button_p1 = Button(label="Ir a Página 2", action=lambda e: page_manager.show_page("page2"), top=150)
    button_p2 = Button(label="Ir a Página 1", action=lambda e: page_manager.show_page("page1"), top=150)   
    delete_button_container = Button(label="Eliminar botón", action=delete_self, left=50, top=200)
    # restore_button_container = Button(label="Restaurar botón", action=restore_button, left=50, top=250)   


    # Handle the FileSelector
    file_selector = FileSelector(page)
    
    button_select = Button(label="Select file", action=file_selector.select_file, left=50, top=20)

    menu = PopupMenu(options=["Option 1", "Option 2", "Option 3"], bg_color="blue", left=0, top=0, page=page, width=180, text_color="white")
    checkbox_group = CheckBoxGroup(
        options=["Opción 1", "Opción 2", "Opción 3"],
        left=10,
        top=10
    )
    # Función para añadir 'x' a ambos textos
    def add_x():
        text1.update(text=text1.text.value + "x")
        text2.update(text=text2.text.value + "x")
        page.update()

    # Función para cambiar el color de fondo y el color del texto de ambos textos
    def change_color():
        text1.update(bg_color="white")
        text2.update(bg_color="white")
        page.update()

        

    page1_widgets = [menu, text1, radio_group, checkbox, slider, text_area, rectangle, button_add_x, button_p1, delete_button_container]
    page2_widgets = [text2, switch, table, dropdown, circle, progress_bar, button_change_color, button_p2, checkbox_group, button_select]#, restore_button_container]

    # Agregar páginas al PageManager
    page_manager.add_page("page1", page1_widgets)
    page_manager.add_page("page2", page2_widgets)

    # Mostrar la primera página
    page_manager.show_page("page1")



    ft.app(target=main)

if __name__ == "__main__":
    main()