from typing import List

from generator.app.subject import Subject


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



