# Generador-de-Horarios-UNAL
Proyecto desarrollado en el curso de Programación Orientada a Objetos (POO) - 2024-2S.

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Problema a Resolver](#problema-a-resolver)
3. [Solución Propuesta](#solución-propuesta)
4. [Principios de Programación Utilizados](#principios-de-programación-utilizados)
   - [Programación Orientada a Objetos](#programación-orientada-a-objetos)
   - [Patrones de Diseño](#patrones-de-diseño)
5. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
   - [Diagrama de Clases](#diagrama-de-clases)
   - [Estructura del Proyecto](#estructura-del-proyecto)
6. [Interfaz Gráfica de Usuario (GUI)](#interfaz-gráfica-de-usuario-gui)
7. [Requisitos de Instalación](#requisitos-de-instalación)
8. [Ejemplo de Uso](#ejemplo-de-uso)
9. [Conclusiones](#conclusiones)

---

## Introducción
El proceso de inscripción de materias en la Universidad Nacional de Colombia (UNAL) puede ser un desafío, ya que los estudiantes deben seleccionar grupos específicos y evitar conflictos de horarios en una franja de tiempo reducida. Este proyecto automatiza la generación de combinaciones de horarios óptimos para reducir el estrés y mejorar la planificación académica.

## Problema a Resolver
Durante la inscripción de materias en el SIA UNAL, los estudiantes deben:

1. Seleccionar las materias requeridas.
2. Elegir un grupo específico con un horario determinado.
3. Evitar conflictos entre horarios.
4. Optimizar su horario según preferencias personales (mañana/tarde, días específicos, profesores, etc.).

Este proyecto facilita el proceso generando múltiples combinaciones de horarios sin solapamientos y ordenadas por preferencia.

## Solución a la Propuesta
Se ha desarrollado un sistema basado en Programación Orientada a Objetos (POO) que:
- Extrae datos de las materias y sus horarios usando Web Scraping.
- Utiliza estructuras de datos eficientes como heaps para optimizar la generación de combinaciones.
- Permite a los estudiantes establecer criterios personalizados para generar un horario ideal.

## Principios de Programación Utilizados
### Programación Orientada a Objetos
- Explicación de las clases principales utilizadas y su relación.
1. `Subject`: Representa una materia con atributos clave. Se comparan objetos `Subject` con < para así establecer un orden en base a la preferencia. Esto será útil para la estructura heap como se verá más adelante.
2. `ScheduleOrganizer`: Maneja el conflicto de horarios verificando si una materia se cruza con otras ya seleccionadas.
3. `CombinationGenerator`: Usa una cola `heap` para priorizar combinaciones con mayor preferencia total, luego ordena los horarios generados y devuelve las mejores combinaciones.
4. `Usuario`: Representa al estudiante con sus datos acádemicos y preferencias.
5. `GestorJSON`: Manejo de datos del usuario.
6. `SubjectScraper`: Extrae la información necesaria desde el buscador de cursos del SIA (web).
7. `SubjectParser`: Procesa los datos obtenidos por el scraper.
8. `BrowserFactory`: Crea instancias de navegadores para el scraper.
- A modo general, tenemos la clase `SubjectParser` la cual estructura los datos extraídos por `SubjectScraper`. La primera clase crea múltiples instancias de `Subject`. El estudiante a través de `Usuario` define las preferencias que afectan la generación de horarios en `CombinationGenerator`. Finalmente `GestorJSON` maneja la gestión de los datos del usuario, permitiendo su almacenamiento para su uso en la aplicación.
- Conceptos aplicados como encapsulamiento, herencia y polimorfismo.

### Patrones de Diseño
- Explicación de patrones de diseño empleados (si aplica), como iteradores, generadores o decoradores.

## Arquitectura del Proyecto
### Diagrama de Clases
- Representación general de la estructura del sistema y sus relaciones.
```mermaid
classDiagram
    class Subject {
        -name: str
        -group: int
        -professor: str
        -schedule: Tuple[str, str]
        -days: List[str]
        -preference: int
        +__lt__(other)
        +__str__()
    }

    class ScheduleOrganizer {
        +has_conflict(subject: Subject, selected_subjects: List[Subject]) bool
    }

    class CombinationGenerator {
        +generate_combinations(subjects: List[List[Subject]], limit: int) List[List[Subject]]
    }

    class Usuario {
        -nivel_de_estudios: str
        -sede: str
        -facultad: str
        -plan_de_estudios: str
        -navegador: Any
        -preferencias_generales: Dict[str, Any]
        -pesos: Dict[str, int]
        -limit: int
        -grupos_favoritos: Dict[str, List[int]]
        +ingresar_datos()
        +asignar_pesos()
        +ingresar_grupos_favoritos(materias: List[str])
        +to_dict() Dict[str, Any]
        +from_dict(datos: Dict[str, Any])
    }

    class GestorJSON {
        -carpeta: str
        +guardar_datos(datos: Dict[str, Any], nombre_archivo: str)
        +cargar_datos(nombre_archivo: str) Dict[str, Any]
    }

    class SubjectScraper {
        -driver: Any
        -url: str
        -subject_codes: List[str]
        -nivel_de_estudios: str
        -sede: str
        -facultad: str
        -plan_de_estudios: str
        -subjects: List[Subject]
        +open_website()
        +select_option_by_text(select_id, text)
        +click_button(button_id)
        +return_to_main_page()
        +reset_page()
        +select_initial_options()
        +scrape_subject_info(subject_code)
        +run()
    }

    class SubjectParser {
        +parse_subject_info(text: str) List[Subject]
    }

    class BrowserFactory {
        +get_browser(browser_name)
    }

    %% Relationships
    SubjectScraper --> BrowserFactory : uses
    ScheduleOrganizer --> Subject : checks conflict
    CombinationGenerator --> Subject : generates combinations
    SubjectParser --> Subject : creates and returns
    Usuario --> GestorJSON : saves and loads
    SubjectScraper --> SubjectParser : parses subject info
```
Clases `Subject`, `ScheduleOrganizer` y `CombinationGenerator`. 
```mermaid
classDiagram
    class Subject {
        -name: str
        -group: int
        -professor: str
        -schedule: Tuple[str, str]
        -days: List[str]
        -preference: int
        +__lt__(other)
        +__str__()
    }

    class ScheduleOrganizer {
        +has_conflict(subject: Subject, selected_subjects: List[Subject]) bool
    }

    class CombinationGenerator {
        +generate_combinations(subjects: List[List[Subject]], limit: int) List[List[Subject]]
    }
    %% Relationships
    ScheduleOrganizer --> Subject : checks conflict
    CombinationGenerator --> Subject : generates combinations
```
Clases `Usuario` y `GestorJSON`.
```mermaid
classDiagram
     class Usuario {
        -nivel_de_estudios: str
        -sede: str
        -facultad: str
        -plan_de_estudios: str
        -navegador: Any
        -preferencias_generales: Dict[str, Any]
        -pesos: Dict[str, int]
        -limit: int
        -grupos_favoritos: Dict[str, List[int]]
        +ingresar_datos()
        +asignar_pesos()
        +ingresar_grupos_favoritos(materias: List[str])
        +to_dict() Dict[str, Any]
        +from_dict(datos: Dict[str, Any])
    }

    class GestorJSON {
        -carpeta: str
        +guardar_datos(datos: Dict[str, Any], nombre_archivo: str)
        +cargar_datos(nombre_archivo: str) Dict[str, Any]
    }
    %% Relationships
generates combinations
    Usuario --> GestorJSON : saves and loads
```
Clases `SubjectScraper`, `SubjectParser` y `BrowserFactory`.
```mermaid
classDiagram
     class SubjectScraper {
        -driver: Any
        -url: str
        -subject_codes: List[str]
        -nivel_de_estudios: str
        -sede: str
        -facultad: str
        -plan_de_estudios: str
        -subjects: List[Subject]
        +open_website()
        +select_option_by_text(select_id, text)
        +click_button(button_id)
        +return_to_main_page()
        +reset_page()
        +select_initial_options()
        +scrape_subject_info(subject_code)
        +run()
    }

    class SubjectParser {
        +parse_subject_info(text: str) List[Subject]
    }

    class BrowserFactory {
        +get_browser(browser_name)
    }
    %% Relationships
    SubjectScraper --> BrowserFactory : uses
    SubjectParser --> Subject : creates and returns
    SubjectScraper --> SubjectParser : parses subject 
```
### Estructura del Proyecto
```
📂 generador_horarios
 ├── 📂 data                    # Archivos JSON de configuración
 ├── 📂 src                     # Código fuente
 │   ├── subject.py             # Clase Subject
 │   ├── schedule_organizer.py  # Clase ScheduleOrganizer
 │   ├── combination_generator.py  # Generación de combinaciones
 │   ├── user.py                # Clase Usuario
 │   ├── scraper.py             # Web Scraping del SIA
 │   ├── gestor_json.py         # Gestión de archivos JSON
 ├── 📂 tests                   # Pruebas unitarias
 ├── README.md                  # Documentación
 ├── LICENSE.md                 # Licencia
 ├── requirements.txt           # Dependencias del proyecto
 ├── main.py                    # Punto de entrada
```
## Interfaz Gráfica de Usuario (GUI)
- Descripción de la GUI desarrollada y cómo mejora la experiencia del usuario.
- Capturas de pantalla (si aplica).

## Requisitos de Instalación
Pasos detallados para instalar y configurar el entorno de desarrollo:
```bash
# Clonar el repositorio
git clone https://github.com/usuario/generador_horarios_unal.git
cd generador_horarios_unal

# Crear entorno virtual
python -m venv env

# Activar entorno virtual
# En Windows:
env\Scripts\activate
# En macOS/Linux:
source env/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejemplo de Uso
```bash
python main.py
```
El sistema solicitará la información del usuario y generará combinaciones de horarios óptimos evitando conflicto

## Conclusiones
Este proyecto automatiza la creación de horarios optimizados para estudiantes de la UNAL, permitiendo una selección rápida y eficiente de materias sin conflictos. Se pueden implementar mejoras como una interfaz gráfica y soporte para más criterios de preferencia en futuras versiones.

---
Autores: 
- [Samuel Fernando Garzón Toro](https://github.com/Gafesato)
- [Juan Esteban Molina Rey](https://github.com/eljuanessoy)
- [Ever Nicolás Muñoz Cortés](https://github.com/nicolasmcort)
- Grupo: [ERROR404]
- Licencia: [AGPL-3.0]

