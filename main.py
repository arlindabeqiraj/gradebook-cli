"""Command-line interface for the Gradebook application."""

import argparse
import logging
import os

from gradebook.storage import load_data, save_data
from gradebook import service


#  Logging setup

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
    ]
)

logger = logging.getLogger(__name__)



#  CLI handlers

def handle_add_student(args, data):
    try:
        student_id = service.add_student(data, args.name)
        save_data(data)
        print(f"  Student '{args.name}' added with ID {student_id}.")
    except ValueError as e:
        print(f"  Error: {e}")


def handle_add_course(args, data):
    try:
        service.add_course(data, args.code, args.title)
        save_data(data)
        print(f"  Course '{args.code} - {args.title}' added.")
    except ValueError as e:
        print(f"  Error: {e}")


def handle_enroll(args, data):
    try:
        service.enroll(data, args.student_id, args.course)
        save_data(data)
        print(f"  Student {args.student_id} enrolled in '{args.course}'.")
    except ValueError as e:
        print(f"  Error: {e}")


def handle_add_grade(args, data):
    try:
        service.add_grade(data, args.student_id, args.course, args.grade)
        save_data(data)
        print(
            f"  Grade {args.grade} added for student {args.student_id} "
            f"in '{args.course}'."
        )
    except ValueError as e:
        print(f"  Error: {e}")


def handle_list(args, data):
    sort = getattr(args, "sort", None)

    if args.target == "students":
        students = service.list_students(data, sort_by=sort or "name")
        if not students:
            print("  No students found.")
        for s in students:
            print(f"  [{s['id']}] {s['name']}")

    elif args.target == "courses":
        courses = service.list_courses(data, sort_by=sort or "code")
        if not courses:
            print("  No courses found.")
        for c in courses:
            print(f"  [{c['code']}] {c['title']}")

    elif args.target == "enrollments":
        enrollments = service.list_enrollments(data)
        if not enrollments:
            print("  No enrollments found.")
        for e in enrollments:
            print(
                f"  Student {e['student_id']} | "
                f"Course {e['course_code']} | "
                f"Grades: {e['grades']}"
            )


def handle_avg(args, data):
    try:
        avg = service.compute_average(data, args.student_id, args.course)
        print(
            f"  Average for student {args.student_id} "
            f"in '{args.course}': {avg:.2f}"
        )
    except ValueError as e:
        print(f"  Error: {e}")


def handle_gpa(args, data):
    try:
        gpa = service.compute_gpa(data, args.student_id)
        print(f"  GPA for student {args.student_id}: {gpa:.2f}")
    except ValueError as e:
        print(f"  Error: {e}")



#  Argument parser

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gradebook",
        description="A simple CLI gradebook application."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add-student
    p_as = sub.add_parser("add-student", help="Add a new student.")
    p_as.add_argument("--name", required=True, help="Student full name.")

    # add-course
    p_ac = sub.add_parser("add-course", help="Add a new course.")
    p_ac.add_argument("--code", required=True, help="Course code (e.g. CS101).")
    p_ac.add_argument("--title", required=True, help="Course title.")

    # enroll
    p_en = sub.add_parser("enroll", help="Enroll a student in a course.")
    p_en.add_argument("--student-id", required=True, type=int, dest="student_id")
    p_en.add_argument("--course", required=True, help="Course code.")

    # add-grade
    p_ag = sub.add_parser("add-grade", help="Add a grade for a student.")
    p_ag.add_argument("--student-id", required=True, type=int, dest="student_id")
    p_ag.add_argument("--course", required=True, help="Course code.")
    p_ag.add_argument("--grade", required=True, type=float, help="Grade (0-100).")

    # list
    p_li = sub.add_parser("list", help="List students, courses, or enrollments.")
    p_li.add_argument(
        "target",
        choices=["students", "courses", "enrollments"],
        help="What to list."
    )
    p_li.add_argument(
        "--sort",
        choices=["name", "code"],
        default=None,
        help="Sort by name or code."
    )

    # avg
    p_av = sub.add_parser("avg", help="Compute average grade.")
    p_av.add_argument("--student-id", required=True, type=int, dest="student_id")
    p_av.add_argument("--course", required=True, help="Course code.")

    # gpa
    p_gp = sub.add_parser("gpa", help="Compute student GPA.")
    p_gp.add_argument("--student-id", required=True, type=int, dest="student_id")

    return parser



#  Entry point

HANDLERS = {
    "add-student": handle_add_student,
    "add-course":  handle_add_course,
    "enroll":      handle_enroll,
    "add-grade":   handle_add_grade,
    "list":        handle_list,
    "avg":         handle_avg,
    "gpa":         handle_gpa,
}


def main():
    parser = build_parser()
    args = parser.parse_args()
    data = load_data()
    HANDLERS[args.command](args, data)


if __name__ == "__main__":
    main()