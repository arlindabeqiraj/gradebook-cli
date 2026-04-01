"""Seed script: populates data/gradebook.json with sample data."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gradebook.storage import save_data
from gradebook.service import (
    add_student,
    add_course,
    enroll,
    add_grade,
)


def seed():
    """Create sample students, courses, enrollments, and grades."""
    data = {"students": [], "courses": [], "enrollments": []}

    id1 = add_student(data, "Arlinda Beqiraj")
    id2 = add_student(data, "Veriona Beqiraj")
    id3 = add_student(data, "Bardhe Beqiraj")

    add_course(data, "AI101", "Intro to Artificial Intelligence")
    add_course(data, "ML201", "Machine Learning")

    enroll(data, id1, "AI101")
    enroll(data, id1, "ML201")
    enroll(data, id2, "AI101")
    enroll(data, id3, "ML201")

    add_grade(data, id1, "AI101", 92)
    add_grade(data, id1, "AI101", 88)
    add_grade(data, id1, "ML201", 75)
    add_grade(data, id1, "ML201", 81)

    add_grade(data, id2, "AI101", 70)
    add_grade(data, id2, "AI101", 65)

    add_grade(data, id3, "ML201", 95)
    add_grade(data, id3, "ML201", 100)

    save_data(data)
    print("  Seed complete! Data saved to data/gradebook.json")
    print(f"  Students   : {len(data['students'])}")
    print(f"  Courses    : {len(data['courses'])}")
    print(f"  Enrollments: {len(data['enrollments'])}")


if __name__ == "__main__":
    seed()