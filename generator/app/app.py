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
    # Create a User instance with default values
    usuario = User()

    # Display user data
    print("\nDatos del usuario (valores por defecto):")
    print(f"Nivel de estudios: {usuario.nivel_de_estudios}")
    print(f"Sede: {usuario.sede}")
    print(f"Facultad: {usuario.facultad}")
    print(f"Plan de estudios: {usuario.plan_de_estudios}")
    print(f"Navegador: {usuario.navegador}")
    print(f"Preferencias generales: {usuario.preferencias_generales}")
    print(f"Pesos: {usuario.pesos}")
    print(f"Límite de horarios a generar: {usuario.limit}")

    # Create a SubjectScraper instance to extract the subjects
    scraper = SubjectScraper(usuario.navegador, usuario.nivel_de_estudios, usuario.sede, usuario.facultad,
                              usuario.plan_de_estudios, ["2016707", "2016699", "2016375"])
    scraper.run()

    # Obtaining the extracted subjects
    materias_extraidas = scraper.subjects

    # Ask the user to enter their favorite groups
    materias_unicas = list(set(subject.name for subject in materias_extraidas))  # Unique subject names
    usuario.ingresar_grupos_favoritos(materias_unicas)

    # Calculate the preference of each subject based on user preferences
    for subject in materias_extraidas:
        subject.preference = PreferenceCalculator.calcular_preferencia(
            subject, usuario.preferencias_generales, usuario.pesos, usuario.grupos_favoritos
        )

    # Organize subjects into a list of lists (one list per subject)
    materias_organizadas = {}
    for subject in materias_extraidas:
        if subject.name not in materias_organizadas:
            materias_organizadas[subject.name] = []
        materias_organizadas[subject.name].append(subject)

    # Convert dictionary to a list of lists
    subjects = list(materias_organizadas.values())

    # Generate valid combinations using the heap
    valid_schedules = CombinationGenerator.generate_combinations(subjects, usuario.limit)

    # Show generated schedules
    print("\nHorarios válidos generados:")
    for i, schedule in enumerate(valid_schedules, start=1):
        print(f"\nHorario {i}:")
        for subject in schedule:
            print(subject)


if __name__ == "__main__":
    main()
