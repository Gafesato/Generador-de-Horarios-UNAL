from typing import List, Tuple

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





