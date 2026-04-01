"""Core data models for the Gradebook application."""


class Student:
    """Represents a student with an ID and name."""

    def __init__(self, student_id: int, name: str):
        if not name.strip():
            raise ValueError("Student name cannot be empty.")
        self.id = student_id
        self.name = name.strip()

    def __str__(self):
        return f"[{self.id}] {self.name}"


class Course:
    """Represents a course with a code and title."""

    def __init__(self, code: str, title: str):
        if not code.strip():
            raise ValueError("Course code cannot be empty.")
        if not title.strip():
            raise ValueError("Course title cannot be empty.")
        self.code = code.strip().upper()
        self.title = title.strip()

    def __str__(self):
        return f"[{self.code}] {self.title}"


class Enrollment:
    """Represents a student's enrollment in a course, with a list of grades."""

    def __init__(self, student_id: int, course_code: str, grades: list = None):
        self.student_id = student_id
        self.course_code = course_code.strip().upper()
        self.grades = []
        if grades:
            for g in grades:
                self.add_grade(g)

    def add_grade(self, grade: float):
        """Add a grade after validating it is between 0 and 100."""
        if not (0 <= grade <= 100):
            raise ValueError(f"Grade {grade} is invalid. Must be between 0 and 100.")
        self.grades.append(grade)

    def __str__(self):
        return (f"Student {self.student_id} | "
                f"Course {self.course_code} | "
                f"Grades: {self.grades}")