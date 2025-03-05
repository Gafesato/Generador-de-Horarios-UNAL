from typing import List, Dict, Any


# Class to represent a user with their data and preferences
class User:
    def __init__(self) -> None:
        """
        Representa un usuario con sus datos y preferencias.
        """
        # Default values
        self.nivel_de_estudios = "Pregrado"
        self.sede = "1101 SEDE BOGOTÁ"
        self.facultad = "2055 FACULTAD DE INGENIERÍA"
        self.plan_de_estudios = "2A74 INGENIERÍA DE SISTEMAS Y COMPUTACIÓN"
        self.navegador = "Edge"  # Default browser
        self.preferencias_generales = {
            "horario": "mañana",  # Default schedule
            "dias": ["LUNES", "MIÉRCOLES"]  # Default days
        }
        self.pesos = {
            "grupo": 3,  # Default weight for group
            "horario": 3,  # Default weight for schedule
            "dias": 3  # Default weight for days
        }
        self.limit = 8  # Limit of schedules to generate (default 8)
        self.grupos_favoritos = {}  # Favorite groups by subject

    def ingresar_datos(self, navegador: str = None, plan_de_estudios: str = None, 
                       nivel_de_estudios: str = None, 
                       sede: str = None, facultad: str = None,
                       preferencias_generales: Dict[str, Any] = None, pesos: Dict[str, int] = None, limit: int = None):
        """
        Permite al usuario ingresar sus datos y preferencias. Si no se proporcionan, se usan los valores por defecto.
        """
        # Update values ​​if provided
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
