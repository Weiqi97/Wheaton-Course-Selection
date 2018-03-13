# coding=utf-8
"""This file contains needed constants."""

from typing import NamedTuple

# Web url constants
url = "https://weblprod1.wheatonma.edu/PROD/bzcrschd.P_ListSection"
base_url = "https://weblprod1.wheatonma.edu"


# Struct constants
class ClassNumber(NamedTuple):
    """Struct for class number information."""
    num: str
    link: str


class ClassExam(NamedTuple):
    """Struct for class exam information."""
    letter: str
    link: str


class ClassInstructor(NamedTuple):
    """Struct for class instructor information."""
    name: str
    link: str


class ClassConx(NamedTuple):
    """Struct for class connection information."""
    num: str
    link: str


class SeatInfo(NamedTuple):
    """Struct for seats information."""
    max: str
    taken: str
    avail: str
    wait_list: str


# Integer constants
# This value used to skip first three useless rows in the web content.
SKIP_BEGINNING = 3
# This value used to extract desired number of semester values.
#   - four full academic years and two more future semesters.
SEMESTER_NUMBER = 18
