import flet as ft
import requests
import webbrowser


import generator.app.user as user
import generator.app.subject_scraper as subject_scraper
import generator.app.combination_generator as combination_generator
import generator.interface.page_manager as pm
from generator.interface.button import Button
from generator.interface.checkbox_group import CheckBoxGroup
from generator.interface.dropdown import Dropdown
from generator.interface.radio_group import RadioGroup
from generator.interface.rectangle import Rectangle
from generator.interface.text_area import TextArea
from generator.interface.text_element import TextElement


###############################################################################
def app(page: ft.Page) -> None:
    # Initial requirements (local mutable variables)
    page.title = "Organizador de horarios"  # Título de la app
    # Background color (opacity 0 to 1, color code in hexadecimal)
    page.bgcolor = ft.Colors.with_opacity(1, '#222831')

    # Key Instances
    page_manager = pm.PageManager(page)

    # Variables to store selections
    selected_days = []  # Stores the selected days
    selected_schedule = None  # Stores the selected time (morning/afternoon)
    codigos_materias = []  # Stores subject codes

    # Global variables to store preferences
    selected_group_pref = None
    selected_schedule_pref = None
    selected_days_pref = None

    # Global variables to store user data
    user_study_level = ""
    user_sede = ""
    user_faculty = ""
    user_studies = ""
    user_browser = ""
    user_limit = 0
    selected_folder = None

    # Create an instance of User
    usuario = user.User()

    ##############################################################
    # Function to handle folder selection
    # Global variable to store the selected folder

    def handle_folder_selection(e: ft.FilePickerResultEvent):
        global selected_folder
        if e.path:
            selected_folder = e.path
            text_process2.update(
                text=f"Carpeta seleccionada: {selected_folder}", bg_color=ft.Colors.with_opacity(0.7, '#18f850'))
        else:
            text_process2.update(text="No se seleccionó ninguna carpeta.",
                                bg_color=ft.Colors.with_opacity(0.7, '#e03838'))

    # Create the FilePicker and assign it to the page
    file_picker = ft.FilePicker(on_result=handle_folder_selection)
    page.overlay.append(file_picker)

    # Function to open the instructions page in the browser
    def open_instructions(e):
        # Change the URL to whatever you want
        webbrowser.open(
            "https://github.com/Gafesato/Generador-de-Horarios-UNAL.git")
        
    def cargar_icono(url, ruta_local):
        try:
            # Try to load icon from URL
            response = requests.get(url)
            if response.status_code == 200:
                return url  # Use URL if available
        except:
            pass  # If it fails, use local file

        # If can't load from URL, use local file
        return ruta_local

    # Function to handle day selection
    def handle_day_selection(e):
        day = e.control.label
        is_selected = e.control.value
        if is_selected:
            selected_days.append(day)
        else:
            selected_days.remove(day)
        usuario.preferencias_generales["dias"] = selected_days  # Update the attribute in User
        print(f"Días seleccionados: {selected_days}")

    # Function to manage time selection
    def handle_schedule_selection(schedule):
        nonlocal selected_schedule
        selected_schedule = schedule
        usuario.preferencias_generales["horario"] = selected_schedule  # Update the attribute in User
        print(f"Horario seleccionado: {selected_schedule}")

    # Función para añadir un código de materia
    def add_code(e):
        codigo = input_codigo.value.strip()
        if codigo not in codigos_materias:
            if codigo:
                codigos_materias.append(codigo)
                input_codigo.value = ""  # Clear input field
                text_process.update(
                    text=f"Código añadido: {codigo}", bg_color=ft.Colors.with_opacity(0.7, '#18f850'))
                print(f"Códigos de materias: {codigos_materias}")
                text_codes.update(text="\n".join(codigos_materias))
            else:
                text_process.update(text="Por favor, ingrese un código válido.",
                                    bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
        else:
            text_process.update(text="El código ingresado ya está en la lista.",
                                bg_color=ft.Colors.with_opacity(0.7, '#18f850'))

    # Function to remove a subject code
    def remove_code(e):
        codigo = input_codigo.value.strip()
        if codigo in codigos_materias:
            if codigo:
                codigos_materias.remove(codigo)
                input_codigo.value = ""  # Clear input field
                text_process.update(
                    text=f"Código removido: {codigo}", bg_color=ft.Colors.with_opacity(0.7, '#18f850'))
                print(f"Códigos de materias: {codigos_materias}")
                text_codes.update(text="\n".join(codigos_materias))
            else:
                text_process.update(text="Por favor, ingrese un código válido.",
                                    bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
        else:
            text_process.update(text="El código ingresado no está en la lista.",
                                bg_color=ft.Colors.with_opacity(0.7, '#e03838'))

    def verificar_datos_usuario():
        if not usuario.nivel_de_estudios:
            return "Nivel de estudios no seleccionado."
        if not usuario.sede:
            return "Sede no seleccionada."
        if not usuario.facultad:
            return "Facultad no seleccionada."
        if not usuario.plan_de_estudios:
            return "Plan de estudios no seleccionado."
        if not usuario.navegador:
            return "Navegador no seleccionado."
        if not usuario.limit:
            return "Límite de horarios no seleccionado."
        return None

    # Function to process subject codes
    def process_codes(e):
        global materias_extraidas  # Make it global so it's available in other functions
        
        # Verify that subject codes have been entered
        if not codigos_materias:
            text_process.update(text="No hay códigos de materias para procesar.",
                                bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
            return

        # Verify that the user data is complete
        error = verificar_datos_usuario()
        if error:
            text_process.update(text=error, bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
            return

        # Show processing message
        text_process.update(text="Procesando información de materias...",
                            bg_color=ft.Colors.with_opacity(0.6, '#222831'))

        try:
            # Create a Subject Scraper instance with user data
            scraper = subject_scraper.SubjectScraper(
                browser_name=usuario.navegador,
                nivel_de_estudios=usuario.nivel_de_estudios,
                sede=usuario.sede,
                facultad=usuario.facultad,
                plan_de_estudios=usuario.plan_de_estudios,
                codes=codigos_materias
            )

            # Run the scraping process
            scraper.run()

            # Obtaining the extracted subjects
            materias_extraidas = scraper.subjects

            # Check if subjects were obtained
            if not materias_extraidas:
                text_process.update(text="No se encontraron materias con los códigos proporcionados.",
                                bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
                return

            # Get unique subject names
            nombres_materias = list(set(materia.name for materia in materias_extraidas))

            # Update the dropdown with the unique names of the subjects
            menu_doc.options = nombres_materias
            menu_doc.dropdown.options = [ft.dropdown.Option(materia) for materia in nombres_materias]
            menu_doc.dropdown.update()

            # Display a success message
            text_process.update(text="Información de materias procesada.",
                                bg_color=ft.Colors.with_opacity(0.7, '#18f850'))

        except Exception as e:
            # Handling errors during scraping
            text_process.update(text=f"Error durante el scraping: {str(e)}",
                                bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
            print(f"Error durante el scraping: {str(e)}")


    # Function to handle group preference selection
    def handle_group_pref(e):
        global selected_group_pref
        selected_group_pref = int(e.control.value)
        usuario.pesos["grupo"] = selected_group_pref  #Update the attribute in User
        print(f"Preferencia de grupo seleccionada: {selected_group_pref}")
        text_process2.update(
            text=f"Preferencia de grupo seleccionada: {selected_group_pref}", bg_color=ft.Colors.with_opacity(0.7, '#18f850'))

    # Function to handle the selection of schedule preferences
    def handle_schedule_pref(e):
        global selected_schedule_pref
        selected_schedule_pref = int(e.control.value)
        usuario.pesos["horario"] = selected_schedule_pref  # Update the attribute in User
        print(f"Preferencia de horario seleccionada: {selected_schedule_pref}")
        text_process2.update(
            text=f"Preferencia de horario seleccionada: {selected_schedule_pref}", bg_color=ft.Colors.with_opacity(0.7, '#18f850'))

    # Function to handle the selection of day preferences
    def handle_days_pref(e):
        global selected_days_pref
        selected_days_pref = int(e.control.value)
        usuario.pesos["dias"] = selected_days_pref  # Update the attribute in User
        print(f"Preferencia de días seleccionada: {selected_days_pref}")
        text_process2.update(
            text=f"Preferencia de días seleccionada: {selected_days_pref}", bg_color=ft.Colors.with_opacity(0.7, '#18f850'))

    # Function to manage time limits
    def handle_limit(e):
        global user_limit
        if e.control.value:
            user_limit = int(e.control.value)
            usuario.limit = user_limit  # Update the attribute in User
            print(f"Límite de horarios seleccionado: {user_limit}")
            label_limit.update(user_limit)
            text_process2.update(
                text=f"Límite de horarios seleccionado: {user_limit}", bg_color=ft.Colors.with_opacity(0.7, '#18f850'))

    # Function to manage the selection of the level of studies
    def handle_study_level(e):
        global user_study_level
        if e.control.value:
            user_study_level = e.control.value
            usuario.nivel_de_estudios = user_study_level  # Update the attribute in User
            print(f"Nivel de estudios seleccionado: {user_study_level}")
            label_study_level.update(user_study_level)
            text_process2.update(
                text=f"Nivel de estudios seleccionado: {user_study_level}", bg_color=ft.Colors.with_opacity(0.7, '#18f850'))

    # Function to handle venue selection
    def handle_sede(e):
        global user_sede
        if e.control.value:
            user_sede = e.control.value
            usuario.sede = user_sede  # Update the attribute in User
            print(f"Sede seleccionada: {user_sede}")
            label_sede.update(user_sede)
            text_process2.update(
                text=f"Sede seleccionada: {user_sede}", bg_color=ft.Colors.with_opacity(0.7, '#18f850'))

    # Function to manage faculty selection
    def handle_faculty(e):
        global user_faculty
        if e.control.value:
            user_faculty = e.control.value
            usuario.facultad = user_faculty  # Update the attribute in User
            print(f"Facultad seleccionada: {user_faculty}")
            label_faculty.update(user_faculty)
            text_process2.update(
                text=f"Facultad seleccionada: {user_faculty}", bg_color=ft.Colors.with_opacity(0.7, '#18f850'))

    # Function to manage the selection of the curriculum
    def handle_studies(e):
        global user_studies
        if e.control.value:
            user_studies = e.control.value
            usuario.plan_de_estudios = user_studies  # Update the attribute in User
            print(f"Plan de estudios seleccionado: {user_studies}")
            label_studies.update(user_studies)
            text_process2.update(
                text=f"Plan de estudios seleccionado: {user_studies}", bg_color=ft.Colors.with_opacity(0.7, '#18f850'))

    def handle_browser(e):
        global user_browser
        if e.control.value:
            if e.control.value not in ["Chrome", "FireFox", "Edge"]:
                text_process2.update(
                    text="Por favor, ingrese un navegador válido (Chrome/FireFox/Edge).", bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
            else:
                user_browser = e.control.value
                usuario.navegador = user_browser  # Update the attribute in User
                print(f"Navegador seleccionado: {user_browser}")
                text_process2.update(
                    text=f"Navegador seleccionado: {user_browser}", bg_color=ft.Colors.with_opacity(0.7, '#18f850'))
    

    def handle_materia_selection(e):
        materia_seleccionada = menu_doc.selected_option
        if materia_seleccionada:
            print(f"Materia seleccionada: {materia_seleccionada}")
            
            # Filter the groups of the selected subject
            grupos_materia = [subject for subject in materias_extraidas if subject.name == materia_seleccionada]
            
            # Display full group information in text_groups, with a dividing line between each group
            grupos_info = "\n______________\n".join([str(subject) for subject in grupos_materia])
            text_groups.update(text=grupos_info)
            

    def handle_button_next1(e):
        materia_seleccionada = menu_doc.selected_option
        if materia_seleccionada:
            # Get the entered groups (comma separated)
            grupos_ingresados = input_groups.value.strip()
            
            if grupos_ingresados:  # Check if anything is entered
                try:
                    # Convert the entered groups into a list of integers
                    grupos_favoritos = [int(grupo.strip()) for grupo in grupos_ingresados.split(",")]
                    
                    # Assign favorite groups to the selected subject
                    usuario.grupos_favoritos[materia_seleccionada] = grupos_favoritos
                    
                    # Display a confirmation message
                    text_process.update(text=f"Grupos favoritos asignados a {materia_seleccionada}: {grupos_favoritos}",
                                        bg_color=ft.Colors.with_opacity(0.7, '#18f850'))
                    print(f"Grupos favoritos para {materia_seleccionada}: {grupos_favoritos}")
                    
                    # Clear input_groups field for next input
                    
                except ValueError:
                    # Handle errors if the user enters something that is not a number
                    text_process.update(text="Por favor, ingrese solo números separados por comas.",
                                        bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
            else:
                # If no groups were entered, display an error message
                text_process.update(text="No se ingresaron grupos favoritos.",
                                    bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
        else:
            # If a subject has not been selected, display an error message
            text_process.update(text="No se ha seleccionado ninguna materia.",
                                bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
    
    def handle_generate_schedules(e):

        # Check that favorite subjects and groups have been selected
        if not materias_extraidas:
            text_process.update(text="No hay materias disponibles para generar horarios.",
                                bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
            return

        if not usuario.grupos_favoritos:
            text_process.update(text="No se han asignado grupos favoritos.",
                                bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
            return

        # Organize subjects into a list of lists (one list per subject)
        materias_organizadas = {}
        for subject in materias_extraidas:
            if subject.name not in materias_organizadas:
                materias_organizadas[subject.name] = []
            materias_organizadas[subject.name].append(subject)

        # Convert dictionary to a list of lists
        subjects = list(materias_organizadas.values())

        # Generate valid combinations using the heap
        try:
            valid_schedules = combination_generator.CombinationGenerator.generate_combinations(subjects, usuario.limit)

            # Show generated schedules
            if valid_schedules:
                print("\nHorarios válidos generados:")
                schedules_text = ""
                for i, schedule in enumerate(valid_schedules, start=1):
                    schedules_text += f"\nHorario {i}:\n"
                    for subject in schedule:
                        schedules_text += f"{subject}\n"
                    schedules_text += "______________\n"

                # Update text_schedules text
                text_schedules.update(text=schedules_text)  # Make sure to use value= to update the text
                page.update()  # Refresh the page to reflect changes
                page.set_clipboard(schedules_text)  # Copy schedules to clipboard

                # Display a SnackBar indicating that the schedules were generated successfully
                page.snack_bar = ft.SnackBar(content=ft.Text("Horarios generados exitosamente."))
                page.snack_bar.open = True
                page.update()
            else:
                text_process.update(text="No se encontraron horarios válidos.",
                                    bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
        except Exception as e:
            # Handling errors during schedule generation
            text_process.update(text=f"Error al generar horarios: {str(e)}",
                                bg_color=ft.Colors.with_opacity(0.7, '#e03838'))
            print(f"Error al generar horarios: {str(e)}")

    def cargar_imagen(url, ruta_local):
        try:
            # Try to load the image from the URL
            response = requests.get(url)
            if response.status_code == 200:
                return url  # Use URL if available
        except:
            pass  # If it fails, use local file

        # If can't load from URL, use local file
        return ruta_local

    ##############################################################
    # "Home" Page Widgets
    rec1_right = Rectangle(left=965, top=0, width=285, height=705,
                           # Gray right bar
                           color=ft.Colors.with_opacity(1, '#393E46'))
    rect2_right = Rectangle(left=965, top=0, width=285, height=140,
                            # Blue right bar
                            color=ft.Colors.with_opacity(1, '#00ADB5'))
    rect1_up = Rectangle(left=10, top=0, width=900, height=140,
                         # Gray top bar
                         color=ft.Colors.with_opacity(1, '#393E46'))
    label_codes = TextElement(value="Códigos", size=20, left=35, top=140, width=240, height=490,
                              page=page, text_color=ft.Colors.WHITE, bg_color=None)  # Label that says "Códigos"
    label_doc = TextElement(value="Grupos", size=20, left=400, top=140, width=240, height=490,
                            page=page, text_color=ft.Colors.WHITE, bg_color=None)  # Label that says "Docentes"
    label_hor = TextElement(value="Horario", size=20, left=730, top=140, width=240, height=490,
                            page=page, text_color=ft.Colors.WHITE, bg_color=None)  # Label that says "Horario"
    label_days = TextElement(value="Días", size=20, left=730, top=320, width=240, height=490,
                             page=page, text_color=ft.Colors.WHITE, bg_color=None)  # Label that says "Días"
    rect1_down = Rectangle(left=10, top=190, width=320, height=515,
                           # Gray bottom bar
                           color=ft.Colors.with_opacity(1, '#393E46'))
    rect2_down = Rectangle(left=370, top=190, width=320, height=515,
                           # Gray bottom bar
                           color=ft.Colors.with_opacity(1, '#393E46'))
    input_codigo = TextArea(
        hint_area="Ingrese el código de las materias", left=20, top=205)
    input_groups = TextArea(
        hint_area="Grupos de interés", 
        left=380, 
        top=630 # Assign the function to the on_blur event
    )
    text_codes = TextElement(value="Sin códigos registrados", size=20, left=28, top=267, width=285, height=345, page=page,
                             # Input field for the subject code
                             text_color=ft.Colors.WHITE, bg_color=ft.Colors.with_opacity(0.6, '#222831'))
    text_groups = TextElement(value="", size=16, left=387, top=267, width=285, height=345, page=page,
                              # Input field for the subject code
                              text_color=ft.Colors.WHITE, bg_color=ft.Colors.with_opacity(0.6, '#222831'))
    #text_inf = TextElement(value="Materias: 0\nNúmero de créditos: 0", size=20, left=990, top=585, width=240, height=220,
                           # Timetable information is displayed
                        #    page=page, text_color=ft.Colors.with_opacity(1, '#4ad0d4'), bg_color=None)
    text_process = TextElement(value="Bienvenido!", size=18, left=640, top=20, width=240, height=90, page=page, text_color=ft.Colors.WHITE,
                               # Text showing the processes that are occurring in the app
                               bg_color=ft.Colors.with_opacity(1, '#00ADB5'), text_align="center")
    button_user = Button(label="Información de usuario", action=lambda e: page_manager.show_page("user_data"), left=35, top=13, width=550, height=50,
                         # Button that takes you to the "user_data" page
                         text_color=ft.Colors.with_opacity(1, '#4ad0d4'), bg_color=ft.Colors.with_opacity(0, '#393E46'))
    button_subjects = Button(label="Buscar materias", font_size=18, action=process_codes, left=35, top=630, width=270,
                             # Button that deletes data
                             height=50, text_color=ft.Colors.WHITE, bg_color=ft.Colors.with_opacity(1, '#00ADB5'))
    button_inst = Button(label="⚙️ Instrucciones", action=open_instructions, left=35, top=75, width=550, height=50, text_color=ft.Colors.with_opacity(
        # Button that opens the instruction page
        1, '#4ad0d4'), bg_color=ft.Colors.with_opacity(0, '#393E46'))
    button_plus = Button(label="+", action=add_code, left=215, top=150, width=30, height=30, font_size=20, text_color=ft.Colors.with_opacity(
        # Button that adds a code to the list
        1, '#4ad0d4'), bg_color=ft.Colors.with_opacity(0, '#393E46'))
    button_less = Button(label="-", action=remove_code, left=260, top=150, width=30, height=30, font_size=20,
                         # Button that adds a code to the list
                         text_color=ft.Colors.with_opacity(1, '#4ad0d4'), bg_color=ft.Colors.with_opacity(0, '#393E46'))
    button_next1 = Button(label="+", action=handle_button_next1, left=625, top=150, width=30, height=30, font_size=20, text_color=ft.Colors.with_opacity(1, '#4ad0d4'), bg_color=ft.Colors.with_opacity(0, '#393E46'))
    #button_prev1 = Button(label="<", action=None, left=580, top=150, width=30, height=30, font_size=20, text_color=ft.Colors.with_opacity(1, '#4ad0d4'), bg_color=ft.Colors.with_opacity(0, '#393E46'))
    button_hor = Button(label="Generar\nhorarios", action=lambda e: page_manager.show_page("schedule"), left=965, top=0, width=285, height=140,
                        # Button that processes subject codes
                        bg_color=ft.Colors.with_opacity(1, '#00ADB5'), text_color="white", font_size=24)
    # menu_doc = PopupMenu(options=["Sin opciones registradas"], icon="  Materia                ▼", left=387, top=210, width=180, bg_color=ft.Colors.with_opacity(1, '#00ADB5'), tooltip="Mostrar materias", border_radius=4)  # PopupMenu para seleccionar el docente
    # Dropdown to select the teacher
    menu_doc = Dropdown(
        options=["Sin opciones registradas"], 
        left=387, 
        top=205, 
        width=285,
        on_change=handle_materia_selection  # Assign the function to the on_change event
    )
    rg_hor = RadioGroup(options=["Mañana", "Tarde"], left=760, top=200,
                        # Schedule options
                        on_change=lambda e: handle_schedule_selection(e.control.value))
    cbg_days = CheckBoxGroup(
        options=["Lunes", "Martes", "Miércoles",
                 "Jueves", "Viernes", "Sábado"],
        left=760,
        top=390,
        on_change=handle_day_selection
    )

    ##############################################################
    # "user_data" page widgets
    text_process2 = TextElement(value="Datos personales", size=18, left=350, top=15, width=240, height=90, page=page, text_color=ft.Colors.WHITE,
                                # Text showing the processes that are occurring in the app
                                bg_color=ft.Colors.with_opacity(1, '#00ADB5'), text_align="center")
    text_block = TextElement(value="", size=20, left=370, top=200, width=235,
                             height=450, page=page, bg_color=ft.Colors.with_opacity(0.6, '#222831'))
    text_block2 = TextElement(value="", size=20, left=715, top=268, width=476,
                              height=225, page=page, bg_color=ft.Colors.with_opacity(0.6, '#222831'))
    # button_folder = Button(label="Seleccionar carpeta 📂", action=lambda e: file_picker.get_directory_path(), left=706, top=585, width=490, height=58,
    #                        # Button to select folder to save things to
    #                        font_size=18, text_color=ft.Colors.WHITE, bg_color=ft.Colors.with_opacity(0, '#393E46'))
    button1_return = Button(label="Volver", action=lambda e: page_manager.show_page("principal"), left=20, top=30, width=170, height=30, font_size=20,
                            # Button to return to the "main" page
                            text_color=ft.Colors.with_opacity(1, '#393E46'), bg_color=ft.Colors.with_opacity(1, '#4ad0d4'))
    rect1_down2 = Rectangle(left=20, top=180, width=605, height=500,
                            # Gray bottom bar
                            color=ft.Colors.with_opacity(1, '#393E46'))
    rect2_down2 = Rectangle(left=680, top=180, width=540, height=400,
                            # Gray bottom bar
                            color=ft.Colors.with_opacity(1, '#393E46'))
    rect3_down2 = Rectangle(left=680, top=550, width=540, height=130,
                            # Gray bottom bar
                            color=ft.Colors.with_opacity(1, '#393E46'))
    rect1_up2 = Rectangle(left=310, top=0, width=910, height=122,
                          # Gray top bar
                          color=ft.Colors.with_opacity(1, '#393E46'))
    label_pers_info = TextElement(value="Información personal", size=20, left=35, top=127, width=240, height=490,
                                  # Label that says "Información personal"
                                  page=page, text_color=ft.Colors.WHITE, bg_color=None)
    label_preferences = TextElement(value="Prioridades", size=20, left=685, top=127, width=240,
                                    # Label that says "Prioridades"
                                    height=490, page=page, text_color=ft.Colors.WHITE, bg_color=None)
    label_study_level = TextElement(value="Pregrado", size=20, left=380, top=210, width=240, height=490,
                                    # Label that indicates the level of studies
                                    page=page, text_color=ft.Colors.WHITE, bg_color=None)
    label_sede = TextElement(value="1101 SEDE BOGOTÁ", size=20, left=380, top=295, width=240,
                             # Label that says the headquarters
                             height=490, page=page, text_color=ft.Colors.WHITE, bg_color=None)
    label_faculty = TextElement(value="2055 FACULTAD DE INGENIERÍA", size=20, left=380, top=365, width=240,
                                # Label that says the faculty
                                height=490, page=page, text_color=ft.Colors.WHITE, bg_color=None)
    label_studies = TextElement(value="2A74 INGENIERÍA DE SISTEMAS Y COMPUTACIÓN", size=20, left=380, top=455, width=240,
                                # Label that says the curriculum
                                height=490, page=page, text_color=ft.Colors.WHITE, bg_color=None)
    label_limit = TextElement(value="8", size=20, left=380, top=575, width=240, height=490, page=page,
                              # Label that says the number of time limits to generate
                              text_color=ft.Colors.WHITE, bg_color=None)
    label_group = TextElement(value="Grupo:", size=20, left=733, top=215, width=240, height=60,
                              page=page, text_color=ft.Colors.WHITE, bg_color=None)  # Label that says "Grupo"
    label_sch = TextElement(value="Horario:", size=20, left=905, top=215, width=240, height=60,
                            page=page, text_color=ft.Colors.WHITE, bg_color=None)  # Label that says "Horario"
    label_days_pr = TextElement(value="Días:", size=20, left=1090, top=215, width=240, height=60,
                                page=page, text_color=ft.Colors.WHITE, bg_color=None)  # Label that says "Días"
    
    input_study_level = TextArea(
        hint_area="Nivel de estudios", left=40, top=215,)
    input_sede = TextArea(hint_area="Sede", left=40, top=300)
    input_faculty = TextArea(hint_area="Facultad", left=40, top=385)
    input_studies = TextArea(hint_area="Plan de estudios", left=40, top=470)
    input_browser = TextArea(
        hint_area="Navegador (Chrome/FireFox/Edge)", left=630, top=35)
    input_limit = TextArea(
        hint_area="Número máximo de horarios", left=40, top=585,)
    # Group Preferences Options
    rg_group = RadioGroup(
        options=[1, 2, 3, 4, 5], left=750, top=280, on_change=handle_group_pref)
    # Time preference options
    rg_sch = RadioGroup(options=[1, 2, 3, 4, 5], left=930,
                        top=280, on_change=handle_schedule_pref)
    # Day preference options
    rg_days = RadioGroup(options=[1, 2, 3, 4, 5],
                         left=1100, top=280, on_change=handle_days_pref)

    ###############################################################
    # "schedule" page widgets
    text_schedules = TextElement(
        value="Horarios generados aparecerán aquí.", 
        size=24, 
        left=20, 
        top=100, 
        width=950, 
        height=600,
        page=page, 
        text_color=ft.Colors.WHITE, 
        bg_color=ft.Colors.with_opacity(1, '#393E46')
    )
    button_generate = Button(label="Generar", font_size=20, left=1070, top=40, width=150, action=handle_generate_schedules,
                                 height=60, text_color=ft.Colors.WHITE, bg_color=ft.Colors.with_opacity(1, '#4ad0d4'))
   
    rect1_down3 = Rectangle(left=1020, top=20, width=250, height=680,
                            # Gray bottom bar
                            color=ft.Colors.with_opacity(1, '#393E46'))

    ##############################################################

    #Assign the function to the on_blur event of the TextArea
    input_limit.text_area.on_blur = handle_limit
    input_study_level.text_area.on_blur = handle_study_level
    input_sede.text_area.on_blur = handle_sede
    input_faculty.text_area.on_blur = handle_faculty
    input_studies.text_area.on_blur = handle_studies
    input_browser.text_area.on_blur = handle_browser


    principal_widgtes = [rec1_right, rect2_right, rect1_up, rect1_down, rect2_down,
                         label_codes, label_doc, label_hor, label_days,
                         text_process, text_codes, text_groups, # text_inf,
                         button_user, button_inst, button_plus, button_hor, button_less, button_subjects, button_next1, 
                         menu_doc,
                         rg_hor,
                         cbg_days,
                         input_codigo, input_groups
                         ]
    user_data_widgets = [rect1_down2, rect2_down2, rect1_up2, rect3_down2, text_block, text_block2,
                         label_pers_info, label_preferences, label_group, label_sch, label_days_pr, label_study_level, label_sede, label_faculty, label_studies, label_limit,
                         text_process2,
                         rg_group, rg_sch, rg_days,
                         input_study_level, input_sede, input_faculty, input_studies, input_browser, input_limit,
                         button1_return, # button_folder,
                         ]
    schedule_widgets = [rect1_down3,
                        button_generate,
                        text_schedules,
                        button1_return,
                        ]

    # Adding Pages to PageManager
    page_manager.add_page("principal", principal_widgtes)
    page_manager.add_page("user_data", user_data_widgets)
    page_manager.add_page("schedule", schedule_widgets)

    # Show the first (main) page
    page_manager.show_page("principal")


ft.app(target=app)
