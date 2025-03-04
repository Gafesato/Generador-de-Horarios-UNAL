import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from generator.app.browser_factory import BrowserFactory
from generator.app.subject_parser import SubjectParser


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

