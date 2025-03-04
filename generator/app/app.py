import heapq
import time
import re
import os
from typing import List, Tuple, Dict, Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from generator.app.browser_factory import BrowserFactory
from generator.app.combination_generator import CombinationGenerator
from generator.app.preference_calculator import PreferenceCalculator
from generator.app.schedule_organizer import ScheduleOrganizer
from generator.app.subject_parser import SubjectParser
from generator.app.subject_scraper import SubjectScraper
from generator.app.subject import Subject
from generator.app.user import User


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