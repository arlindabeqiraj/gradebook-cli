"""Business logic for the Gradebook application."""

import logging
from .models import Student, Course, Enrollment

logger = logging.getLogger(__name__)


def parse_grade(value) -> float:
    """Convert value to a float grade in [0, 100].

    Raises ValueError with a friendly message on bad input.
    """
    try:
        grade = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"'{value}' is not a valid number.")
    if not (0 <= grade <= 100):
        raise ValueError(f"Grade {grade} must be between 0 and 100.")
    return grade


def _next_id(records: list) -> int:
    """Return the next auto-increment ID for a list of dicts."""
    if not records:
        return 1
    return max(r["id"] for r in records) + 1


def add_student(data: dict, name: str) -> int:
    """Add a new student and return the assigned ID."""
    student_id = _next_id(data["students"])
    student = Student(student_id, name)
    data["students"].append({"id": student.id, "name": student.name})
    logger.info("Added student: %s", student)
    return student_id


def list_students(data: dict, sort_by: str = "name") -> list:
    """Return a sorted list of student dicts."""
    key = "name" if sort_by == "name" else "id"
    return sorted(data["students"], key=lambda s: s[key])


def add_course(data: dict, code: str, title: str) -> None:
    """Add a new course."""
    course = Course(code, title)
    if any(c["code"] == course.code for c in data["courses"]):
        raise ValueError(f"Course '{course.code}' already exists.")
    data["courses"].append({"code": course.code, "title": course.title})
    logger.info("Added course: %s", course)


def list_courses(data: dict, sort_by: str = "code") -> list:
    """Return a sorted list of course dicts."""
    key = "title" if sort_by == "title" else "code"
    return sorted(data["courses"], key=lambda c: c[key])


def _get_student(data: dict, student_id: int) -> dict:
    """Return a student dict or raise ValueError."""
    matches = [s for s in data["students"] if s["id"] == student_id]
    if not matches:
        raise ValueError(f"No student found with ID {student_id}.")
    return matches[0]


def _get_course(data: dict, course_code: str) -> dict:
    """Return a course dict or raise ValueError."""
    code = course_code.strip().upper()
    matches = [c for c in data["courses"] if c["code"] == code]
    if not matches:
        raise ValueError(f"No course found with code '{course_code}'.")
    return matches[0]


def _get_enrollment(data: dict, student_id: int, course_code: str) -> dict:
    """Return an enrollment dict or raise ValueError."""
    code = course_code.strip().upper()
    matches = [
        e for e in data["enrollments"]
        if e["student_id"] == student_id and e["course_code"] == code
    ]
    if not matches:
        raise ValueError(
            f"Student {student_id} is not enrolled in '{course_code}'."
        )
    return matches[0]


def enroll(data: dict, student_id: int, course_code: str) -> None:
    """Enroll a student in a course."""
    _get_student(data, student_id)
    course = _get_course(data, course_code)
    existing = [
        e for e in data["enrollments"]
        if e["student_id"] == student_id and e["course_code"] == course["code"]
    ]
    if existing:
        raise ValueError(
            f"Student {student_id} is already enrolled in '{course['code']}'."
        )
    enrollment = Enrollment(student_id, course["code"])
    data["enrollments"].append({
        "student_id": enrollment.student_id,
        "course_code": enrollment.course_code,
        "grades": enrollment.grades
    })
    logger.info("Enrolled student %d in %s", student_id, course["code"])


def add_grade(data: dict, student_id: int, course_code: str, grade) -> None:
    """Add a grade to a student's enrollment."""
    _get_student(data, student_id)
    _get_course(data, course_code)
    enrollment_dict = _get_enrollment(data, student_id, course_code)
    enrollment = Enrollment(
        enrollment_dict["student_id"],
        enrollment_dict["course_code"],
        enrollment_dict["grades"]
    )
    validated = parse_grade(grade)
    enrollment.add_grade(validated)
    enrollment_dict["grades"] = enrollment.grades
    logger.info(
        "Added grade %.1f for student %d in %s", validated, student_id, course_code
    )


def list_enrollments(data: dict) -> list:
    """Return all enrollments sorted by student_id."""
    return sorted(data["enrollments"], key=lambda e: e["student_id"])


def compute_average(data: dict, student_id: int, course_code: str) -> float:
    """Return the average grade for a student in a course."""
    enrollment = _get_enrollment(data, student_id, course_code)
    grades = enrollment["grades"]
    if not grades:
        raise ValueError(
            f"No grades recorded for student {student_id} in '{course_code}'."
        )
    return sum(grades) / len(grades)


def compute_gpa(data: dict, student_id: int) -> float:
    """Return the GPA (mean of all course averages) for a student."""
    _get_student(data, student_id)
    enrollments = [
        e for e in data["enrollments"]
        if e["student_id"] == student_id and e["grades"]
    ]
    if not enrollments:
        raise ValueError(f"Student {student_id} has no graded enrollments.")
    averages = [sum(e["grades"]) / len(e["grades"]) for e in enrollments]
    return sum(averages) / len(averages)