import heapq
from typing import List

from generator.app.schedule_organizer import ScheduleOrganizer
from generator.app.subject import Subject


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


