# Gradebook CLI

A simple command-line application for managing students, courses, enrollments, and grades — built with Python.

---

## Project Structure

```
gradebook/
├── gradebook/
│   ├── __init__.py
│   ├── models.py       # Student, Course, Enrollment classes
│   ├── storage.py      # load_data() and save_data() with JSON
│   └── service.py      # Business logic (add, enroll, grade, average, GPA)
├── main.py             # CLI entry point (argparse)
├── tests/
│   └── test_service.py # Unit tests (unittest)
├── scripts/
│   └── seed.py         # Populates sample data
├── data/
│   └── gradebook.json  # Auto-generated data file
├── logs/
│   └── app.log         # Auto-generated log file
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd gradebook
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

This project uses only Python standard library modules — no extra packages needed.

---

## Seed Sample Data

Populate the database with sample students, courses, and grades:

```bash
python scripts/seed.py
```

Expected output:

```
  Seed complete! Data saved to data/gradebook.json
  Students   : 3
  Courses    : 2
  Enrollments: 4
```

---

## CLI Usage

### Add a student

```bash
python main.py add-student --name "Arlinda Beqiraj"
# Output: Student 'Arlinda Beqiraj' added with ID 1.
```

### Add a course

```bash
python main.py add-course --code AI101 --title "Intro to Artificial Intelligence"
# Output: Course 'AI101 – Intro to Artificial Intelligence' added.
```

### Enroll a student in a course

```bash
python main.py enroll --student-id 1 --course AI101
# Output: Student 1 enrolled in 'AI101'.
```

### Add a grade

```bash
python main.py add-grade --student-id 1 --course AI101 --grade 95
# Output: Grade 95.0 added for student 1 in 'AI101'.
```

### List students, courses, or enrollments

```bash
python main.py list students
python main.py list courses --sort code
python main.py list enrollments
```

### Compute average grade

```bash
python main.py avg --student-id 1 --course AI101
# Output: Average for student 1 in 'AI101': 90.00
```

### Compute GPA

```bash
python main.py gpa --student-id 1
# Output: GPA for student 1: 87.50
```

---

## Running Tests

```bash
python -m unittest tests/test_service.py -v
```

Expected output:

```
test_add_multiple_grades ... ok
test_add_multiple_students_increments_id ... ok
test_add_student_empty_name_raises ... ok
test_add_student_returns_id ... ok
...
OK
```

---

## Design Decisions

### Design Decisions

- **JSON storage** was chosen for simplicity and human-readability. No external database is required.
- **Pure functions in `service.py`** make the business logic easy to test and reuse independently of the CLI.
- **Relative imports** (`from .models import ...`) are used inside the `gradebook` package to follow Python packaging best practices.
- **`argparse` subcommands** provide a clean and extensible CLI structure.
- **`logging` module** writes all INFO/ERROR events to `logs/app.log` for easy debugging without cluttering the terminal.
