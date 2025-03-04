# principal.py

import heapq
from typing import List, Tuple, Dict, Any
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Class to represent a subject
class Subject:
    def __init__(self, name: str, group: int, professor: str, schedule: Tuple[str, str], days: List[str], preference: int = 0) -> None:
        self.name = name
        self.group = group
        self.professor = professor
        self.schedule = schedule  # (start, end)
        self.days = days  # List of days (e.g., ['MONDAY', 'WEDNESDAY'])
        self.preference = preference  # Subject preference

    def __lt__(self, other):
        """
        Defines how two subjects are compared. Used for sorting in the heap.
        """
        return self.preference < other.preference

    def __str__(self) -> str:
        """String representation of the subject."""
        return f"Materia: {self.name} \n" \
               f"\tProfesor: {self.professor} \n" \
               f"\tGrupo: {self.group} \n" \
               f"\tHorario: {self.schedule[0]} - {self.schedule[1]}\n" \
               f"\tDías: {', '.join(self.days)}\n" 
               #f"\tPreferencia: {self.preference}"


# Class to organize schedules and avoid conflicts
class ScheduleOrganizer:
    @staticmethod
    def has_conflict(subject: Subject, selected_subjects: List[Subject]) -> bool:
        """
        Checks if a subject conflicts with the already selected subjects.

        :param subject: Subject to check.
        :param selected_subjects: List of already selected subjects.
        :return: True if there is a conflict, False otherwise.
        """
        for selected in selected_subjects:
            # Check if there is at least one common day
            if set(subject.days) & set(selected.days):
                # Check if schedules overlap
                start1, end1 = subject.schedule
                start2, end2 = selected.schedule
                if not (end1 <= start2 or end2 <= start1):
                    return True  # There is a conflict
        return False


# Class to generate schedule combinations using a heap
class CombinationGenerator:
    @staticmethod
    def generate_combinations(subjects: List[List[Subject]], limit: int) -> List[List[Subject]]:
        """
        Generates valid schedule combinations using a heap.

        :param subjects: List of lists of subjects, where each inner list represents a subject and its groups.
        :param limit: Limit of combinations to generate.
        :return: List of valid combinations.
        """
        combinations = []  # List to store valid combinations
        heap = []  # Heap to prioritize combinations by accumulated preference

        # Initialize the heap with the root (no subjects selected)
        heapq.heappush(heap, (-0, [], 0))  # (negative accumulated preference, current combination, level)

        while heap and len(combinations) < limit:
            # Extract the combination with the highest accumulated preference
            neg_accumulated_preference, current_combination, level = heapq.heappop(heap)
            accumulated_preference = -neg_accumulated_preference  # Convert to positive

            # If all subjects have been processed, add the combination to the list
            if level == len(subjects):
                combinations.append((accumulated_preference, current_combination))
                continue

            # Get the current subject and its groups
            current_subject_groups = subjects[level]

            # Sort groups by preference (from highest to lowest)
            sorted_groups = sorted(current_subject_groups, key=lambda x: x.preference, reverse=True)

            # Try adding each group of the current subject
            for subject in sorted_groups:
                # Check if the subject conflicts with the already selected subjects
                if not ScheduleOrganizer.has_conflict(subject, current_combination):
                    # Calculate the new accumulated preference
                    new_accumulated_preference = accumulated_preference + subject.preference

                    # Create a new combination
                    new_combination = current_combination + [subject]

                    # Insert the new combination into the heap
                    heapq.heappush(heap, (-new_accumulated_preference, new_combination, level + 1))

        # Sort the final combinations by total preference (from highest to lowest)
        combinations.sort(reverse=True, key=lambda x: x[0])

        # Return only the combinations (without the accumulated preference)
        return [combo for (_, combo) in combinations]


# Class to represent a user with their data and preferences
class User:
    def __init__(self) -> None:
        """
        Representa un usuario con sus datos y preferencias.
        """
        # Valores por defecto
        self.nivel_de_estudios = "Pregrado"
        self.sede = "1101 SEDE BOGOTÁ"
        self.facultad = "2055 FACULTAD DE INGENIERÍA"
        self.plan_de_estudios = "2A74 INGENIERÍA DE SISTEMAS Y COMPUTACIÓN"
        self.navegador = "Edge"  # Navegador por defecto
        self.preferencias_generales = {
            "horario": "mañana",  # Horario por defecto
            "dias": ["LUNES", "MIÉRCOLES"]  # Días por defecto
        }
        self.pesos = {
            "grupo": 3,  # Peso por defecto para grupo
            "horario": 3,  # Peso por defecto para horario
            "dias": 3  # Peso por defecto para días
        }
        self.limit = 8  # Límite de horarios a generar (default 8)
        self.grupos_favoritos = {}  # Grupos favoritos por materia

    def ingresar_datos(self, navegador: str = None, plan_de_estudios: str = None, 
                       nivel_de_estudios: str = None, 
                       sede: str = None, facultad: str = None,
                       preferencias_generales: Dict[str, Any] = None, pesos: Dict[str, int] = None, limit: int = None):
        """
        Permite al usuario ingresar sus datos y preferencias. Si no se proporcionan, se usan los valores por defecto.
        """
        # Actualizar los valores si se proporcionan
        if navegador:
            self.navegador = navegador
        if plan_de_estudios:
            self.plan_de_estudios = plan_de_estudios
        if nivel_de_estudios:
            self.nivel_de_estudios = nivel_de_estudios
        if sede:
            self.sede = sede
        if facultad:
            self.facultad = facultad
        if preferencias_generales:
            self.preferencias_generales = preferencias_generales
        if pesos:
            self.pesos = pesos
        if limit:
            self.limit = limit

    def ingresar_grupos_favoritos(self, materias: List[str]):
        """
        Solicita al usuario que ingrese sus grupos favoritos para cada materia.

        :param materias: Lista de nombres de materias.
        """
        print("\nIngrese sus grupos favoritos para cada materia:")
        for materia in materias:
            grupos = input(f"Grupos favoritos para {materia} (ejemplo: 1,3): ").strip().split(",")
            self.grupos_favoritos[materia] = [int(grupo.strip()) for grupo in grupos]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte los datos del usuario a un diccionario.

        :return: Diccionario con los datos del usuario.
        """
        return {
            "nivel_de_estudios": self.nivel_de_estudios,
            "sede": self.sede,
            "facultad": self.facultad,
            "plan_de_estudios": self.plan_de_estudios,
            "navegador": self.navegador,
            "preferencias_generales": self.preferencias_generales,
            "pesos": self.pesos,
            "limit": self.limit
        }


# Class to scrape subjects from SIA
class SubjectScraper:
    def __init__(self, browser_name, nivel_de_estudios, sede, facultad, plan_de_estudios, codes):
        self.driver = BrowserFactory.get_browser(browser_name)  # Initialize the driver in headless mode
        self.url = "https://sia.unal.edu.co/Catalogo/facespublico/public/servicioPublico.jsf;PortalJSESSION=fMdOk3jZADUC9bEclL_BFOwAxNoviHdXCcxAw4QBrb8TXl2tXUkB!498583482?taskflowId=task-flow-AC_CatalogoAsignaturas"
        self.subject_codes = codes  # Subject codes
        self.nivel_de_estudios = nivel_de_estudios
        self.sede = sede
        self.facultad = facultad
        self.plan_de_estudios = plan_de_estudios
        self.subjects = []  # List of scraped subjects

    def open_website(self):
        """Abre la URL del sitio web."""
        self.driver.get(self.url)
        # Esperar a que la página cargue completamente
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "pt1:r1:0:soc1::content"))
        )

    def select_option_by_text(self, select_id, text):
        """Selecciona una opción en un <select> por su texto visible."""
        try:
            # Esperar a que el desplegable esté habilitado
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.ID, select_id))
            )
            select_element = self.driver.find_element(By.ID, select_id)
            select = Select(select_element)
            select.select_by_visible_text(text)
            time.sleep(1)  # Pequeña pausa para evitar errores
        except Exception as e:
            print(f"No se pudo seleccionar la opción '{text}' en el desplegable con ID {select_id}: {e}")
            raise

    def click_button(self, button_id):
        """Hace clic en un botón por su ID."""
        try:
            button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.ID, button_id)))
            button.click()
            time.sleep(3)  # Esperar para ver los cambios
        except Exception as e:
            print(f"No se pudo hacer clic en el botón con ID {button_id}: {e}")
            raise

    def return_to_main_page(self):
        """Vuelve a la página principal haciendo clic en el botón 'Volver'."""
        try:
            return_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@id, 'cb4')]//a[contains(@class, 'af_button_link') and contains(.//span, 'Volver')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", return_button)
            time.sleep(1)
            return_button.click()
            print("Se hizo clic en el botón 'Volver'")
            time.sleep(3)

            # Verificar que la página ha regresado correctamente
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "pt1:r1:0:it10::content"))
            )
        except Exception as e:
            print(f"No se pudo regresar a la página principal: {e}")
            self.reset_page()

    def reset_page(self):
        """Recarga la página y selecciona las opciones iniciales."""
        self.driver.get(self.url)
        time.sleep(5)
        self.select_initial_options()

    def select_initial_options(self):
        """Selecciona las opciones iniciales en el orden correcto."""
        self.select_option_by_text("pt1:r1:0:soc1::content", self.nivel_de_estudios)
        self.select_option_by_text("pt1:r1:0:soc9::content", self.sede)
        self.select_option_by_text("pt1:r1:0:soc2::content", self.facultad)
        self.select_option_by_text("pt1:r1:0:soc3::content", self.plan_de_estudios)

    def scrape_subject_info(self, subject_code):
        """Extrae la información de una materia específica."""
        try:
            # Esperar a que la tabla cargue
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{subject_code}')]"))
            )
            # Hacer clic en el enlace de la materia
            link = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{subject_code}')]"))
            )
            link.click()
            print(f"Se hizo clic en la materia {subject_code}")
            time.sleep(5)

            # Extraer el texto de la página
            page_text = self.driver.find_element(By.TAG_NAME, "body").text

            # Parsear la información de la materia
            subjects = SubjectParser.parse_subject_info(page_text)
            self.subjects.extend(subjects)  # Agregar las materias extraídas a la lista

            # Volver a la página principal
            self.return_to_main_page()
        except Exception as e:
            print(f"No se pudo procesar la materia con código {subject_code}: {e}")
            self.reset_page()

    def run(self):
        """Ejecuta el proceso completo de scraping."""
        try:
            self.open_website()
            self.select_initial_options()

            # Hacer clic en "Mostrar" una sola vez para cargar todas las materias
            self.click_button("pt1:r1:0:cb1")

            # Iterar sobre cada materia
            for subject_code in self.subject_codes:
                self.scrape_subject_info(subject_code)

        finally:
            # Cerrar el navegador al finalizar
            self.driver.quit()


# Class to parse subject information
class SubjectParser:
    @staticmethod
    def parse_subject_info(text: str) -> List[Subject]:
        subjects = []
        subject_name = re.search(r"Información de la asignatura\n\s+Volver\n(.+?)\n", text).group(1).strip()

        # Dividir el texto por la palabra "Grupo" y capturar el número de grupo
        group_matches = list(re.finditer(r"\((\d+)\) Grupo (\d+)\s+Profesor: (.+?)\.", text))
        for match in group_matches:
            group_number = int(match.group(2))  # Número de grupo
            professor = match.group(3).strip()  # Profesor

            # Extraer la sección correspondiente al grupo
            start = match.end()
            next_match = next((m for m in group_matches if m.start() > start), None)
            end = next_match.start() if next_match else len(text)
            section = text[start:end].strip()

            # Extraer los días de la semana (palabras en mayúscula)
            days = re.findall(r"\b(LUNES|MARTES|MIÉRCOLES|JUEVES|VIERNES|SÁBADO|DOMINGO)\b", section)

            # Extraer el horario (primera coincidencia)
            schedule_match = re.search(r"(\d{2}:\d{2}) a (\d{2}:\d{2})", section)
            schedule = (schedule_match.group(1), schedule_match.group(2)) if schedule_match else ("00:00", "00:00")

            # Crear instancia de Subject
            subject = Subject(
                name=subject_name,
                group=group_number,
                professor=professor,
                schedule=schedule,
                days=days
            )
            subjects.append(subject)

        return subjects


# Class to create browser instances
class BrowserFactory:
    """Factory para crear instancias de navegadores en modo headless."""
    @staticmethod
    def get_browser(browser_name):
        if browser_name.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Modo headless para Chrome
            return webdriver.Chrome(options=options)
        elif browser_name.lower() == "edge":
            options = webdriver.EdgeOptions()
            options.add_argument("--headless")  # Modo headless para Edge
            return webdriver.Edge(options=options)
        elif browser_name.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")  # Modo headless para Firefox
            return webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Navegador no soportado: {browser_name}")


# Class to calculate subject preferences
class PreferenceCalculator:
    @staticmethod
    def calcular_preferencia(subject: Subject, preferencias: Dict[str, Any], pesos: Dict[str, int], grupos_favoritos: Dict[str, List[int]]) -> int:
        """
        Calcula la preferencia de una materia en función de las preferencias del usuario.

        :param subject: Materia a evaluar.
        :param preferencias: Preferencias del usuario.
        :param pesos: Pesos asignados a los criterios (1 a 5).
        :param grupos_favoritos: Grupos favoritos del usuario.
        :return: Preferencia calculada.
        """
        preferencia = 0

        # Preferencia de horario
        hora_inicio = int(subject.schedule[0].split(':')[0])  # Extraer la hora y convertirla a entero
        if preferencias["horario"] == "mañana" and hora_inicio < 12:
            preferencia += pesos["horario"]
        elif preferencias["horario"] == "tarde" and hora_inicio >= 12:
            preferencia += pesos["horario"]

        # Preferencia de días
        dias_preferidos = set(preferencias["dias"])
        dias_materia = set(subject.days)
        if dias_preferidos & dias_materia:
            preferencia += pesos["dias"]

        # Preferencia de grupo favorito
        if subject.name in grupos_favoritos and subject.group in grupos_favoritos[subject.name]:
            preferencia += pesos["grupo"]

        return preferencia


# Main function
def main():
    # Crear una instancia de User con valores por defecto
    usuario = User()

    # Mostrar los datos del usuario
    print("\nDatos del usuario (valores por defecto):")
    print(f"Nivel de estudios: {usuario.nivel_de_estudios}")
    print(f"Sede: {usuario.sede}")
    print(f"Facultad: {usuario.facultad}")
    print(f"Plan de estudios: {usuario.plan_de_estudios}")
    print(f"Navegador: {usuario.navegador}")
    print(f"Preferencias generales: {usuario.preferencias_generales}")
    print(f"Pesos: {usuario.pesos}")
    print(f"Límite de horarios a generar: {usuario.limit}")

    # Crear una instancia de SubjectScraper para extraer las materias
    scraper = SubjectScraper(usuario.navegador, usuario.nivel_de_estudios, usuario.sede, usuario.facultad,
                              usuario.plan_de_estudios, ["2016707", "2016699", "2016375"])
    scraper.run()

    # Obtener las materias extraídas
    materias_extraidas = scraper.subjects

    # Solicitar al usuario que ingrese sus grupos favoritos
    materias_unicas = list(set(subject.name for subject in materias_extraidas))  # Nombres únicos de materias
    usuario.ingresar_grupos_favoritos(materias_unicas)

    # Calcular la preferencia de cada materia en función de las preferencias del usuario
    for subject in materias_extraidas:
        subject.preference = PreferenceCalculator.calcular_preferencia(
            subject, usuario.preferencias_generales, usuario.pesos, usuario.grupos_favoritos
        )

    # Organizar las materias en una lista de listas (una lista por materia)
    materias_organizadas = {}
    for subject in materias_extraidas:
        if subject.name not in materias_organizadas:
            materias_organizadas[subject.name] = []
        materias_organizadas[subject.name].append(subject)

    # Convertir el diccionario a una lista de listas
    subjects = list(materias_organizadas.values())

    # Generar combinaciones válidas usando el heap
    valid_schedules = CombinationGenerator.generate_combinations(subjects, usuario.limit)

    # Mostrar los horarios generados
    print("\nHorarios válidos generados:")
    for i, schedule in enumerate(valid_schedules, start=1):
        print(f"\nHorario {i}:")
        for subject in schedule:
            print(subject)


if __name__ == "__main__":
    main()