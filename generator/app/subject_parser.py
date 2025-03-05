import re
from typing import List

from generator.app.subject import Subject

# Class to parse subject information
class SubjectParser:
    @staticmethod
    def parse_subject_info(text: str) -> List[Subject]:
        subjects = []
        subject_name = re.search(r"Información de la asignatura\n\s+Volver\n(.+?)\n", text).group(1).strip()

        # Split the text by the word "Group" and capture the group numbero
        group_matches = list(re.finditer(r"\((\d+)\) Grupo (\d+)\s+Profesor: (.+?)\.", text))
        for match in group_matches:
            group_number = int(match.group(2))  # Group number
            professor = match.group(3).strip()  # Teacher

            # Extract the section corresponding to the group
            start = match.end()
            next_match = next((m for m in group_matches if m.start() > start), None)
            end = next_match.start() if next_match else len(text)
            section = text[start:end].strip()

            # Extract the days of the week (capitalized words)
            days = re.findall(r"\b(LUNES|MARTES|MIÉRCOLES|JUEVES|VIERNES|SÁBADO|DOMINGO)\b", section)

            # Extract schedule (first match)
            schedule_match = re.search(r"(\d{2}:\d{2}) a (\d{2}:\d{2})", section)
            schedule = (schedule_match.group(1), schedule_match.group(2)) if schedule_match else ("00:00", "00:00")

            # Create Subject instance
            subject = Subject(
                name=subject_name,
                group=group_number,
                professor=professor,
                schedule=schedule,
                days=days
            )
            subjects.append(subject)

        return subjects


