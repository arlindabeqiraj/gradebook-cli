"""Unit tests for gradebook.service module."""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gradebook.service import (
    add_student,
    add_course,
    enroll,
    add_grade,
    compute_average,
    compute_gpa,
)


def empty_data() -> dict:
    """Return a fresh empty data structure."""
    return {"students": [], "courses": [], "enrollments": []}


class TestAddStudent(unittest.TestCase):
    """Tests for add_student()."""

    def test_add_student_returns_id(self):
        """Happy path: adding a student returns an integer ID."""
        data = empty_data()
        student_id = add_student(data, "Arlinda Beqiraj")
        self.assertEqual(student_id, 1)
        self.assertEqual(len(data["students"]), 1)
        self.assertEqual(data["students"][0]["name"], "Arlinda Beqiraj")

    def test_add_multiple_students_increments_id(self):
        """IDs should increment with each new student."""
        data = empty_data()
        id1 = add_student(data, "Arlinda Beqiraj")
        id2 = add_student(data, "Veriona Beqiraj")
        self.assertEqual(id1, 1)
        self.assertEqual(id2, 2)

    def test_add_student_empty_name_raises(self):
        """Edge case: empty name should raise ValueError."""
        data = empty_data()
        with self.assertRaises(ValueError):
            add_student(data, "   ")


class TestAddGrade(unittest.TestCase):
    """Tests for add_grade()."""

    def setUp(self):
        """Set up a student, course, and enrollment before each test."""
        self.data = empty_data()
        add_student(self.data, "Arlinda Beqiraj")
        add_course(self.data, "AI101", "Intro to Artificial Intelligence")
        enroll(self.data, 1, "AI101")

    def test_add_grade_happy_path(self):
        """Happy path: valid grade is added to enrollment."""
        add_grade(self.data, 1, "AI101", 95)
        enrollment = self.data["enrollments"][0]
        self.assertIn(95.0, enrollment["grades"])

    def test_add_multiple_grades(self):
        """Multiple grades can be added to the same enrollment."""
        add_grade(self.data, 1, "AI101", 80)
        add_grade(self.data, 1, "AI101", 90)
        enrollment = self.data["enrollments"][0]
        self.assertEqual(len(enrollment["grades"]), 2)

    def test_add_grade_above_100_raises(self):
        """Edge case: grade above 100 should raise ValueError."""
        with self.assertRaises(ValueError):
            add_grade(self.data, 1, "AI101", 105)

    def test_add_grade_below_0_raises(self):
        """Edge case: negative grade should raise ValueError."""
        with self.assertRaises(ValueError):
            add_grade(self.data, 1, "AI101", -5)

    def test_add_grade_unenrolled_raises(self):
        """Edge case: adding grade for unenrolled course raises ValueError."""
        add_course(self.data, "ML201", "Machine Learning")
        with self.assertRaises(ValueError):
            add_grade(self.data, 1, "ML201", 88)


class TestComputeAverage(unittest.TestCase):
    """Tests for compute_average()."""

    def setUp(self):
        """Set up a student, course, and enrollment before each test."""
        self.data = empty_data()
        add_student(self.data, "Arlinda Beqiraj")
        add_course(self.data, "AI101", "Intro to Artificial Intelligence")
        enroll(self.data, 1, "AI101")

    def test_compute_average_happy_path(self):
        """Happy path: average is correctly computed."""
        add_grade(self.data, 1, "AI101", 80)
        add_grade(self.data, 1, "AI101", 100)
        avg = compute_average(self.data, 1, "AI101")
        self.assertAlmostEqual(avg, 90.0)

    def test_compute_average_single_grade(self):
        """Average of a single grade equals that grade."""
        add_grade(self.data, 1, "AI101", 75)
        avg = compute_average(self.data, 1, "AI101")
        self.assertAlmostEqual(avg, 75.0)

    def test_compute_average_no_grades_raises(self):
        """Edge case: no grades recorded should raise ValueError."""
        with self.assertRaises(ValueError):
            compute_average(self.data, 1, "AI101")


class TestComputeGPA(unittest.TestCase):
    """Tests for compute_gpa()."""

    def test_compute_gpa_happy_path(self):
        """Happy path: GPA is mean of course averages."""
        data = empty_data()
        add_student(data, "Arlinda Beqiraj")
        add_course(data, "AI101", "Intro to Artificial Intelligence")
        add_course(data, "ML201", "Machine Learning")
        enroll(data, 1, "AI101")
        enroll(data, 1, "ML201")
        add_grade(data, 1, "AI101", 90)
        add_grade(data, 1, "ML201", 80)
        gpa = compute_gpa(data, 1)
        self.assertAlmostEqual(gpa, 85.0)

    def test_compute_gpa_no_grades_raises(self):
        """Edge case: student with no grades raises ValueError."""
        data = empty_data()
        add_student(data, "Veriona Beqiraj")
        with self.assertRaises(ValueError):
            compute_gpa(data, 1)


if __name__ == "__main__":
    unittest.main()