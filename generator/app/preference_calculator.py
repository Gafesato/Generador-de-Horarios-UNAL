from typing import List, Dict, Any

from generator.app.subject import Subject

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