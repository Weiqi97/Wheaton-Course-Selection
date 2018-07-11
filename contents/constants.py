# coding=utf-8
"""This file contains needed constants."""
import pandas as pd
from enum import Enum

# Web url constants
URL = "https://weblprod1.wheatonma.edu/PROD/bzcrschd.P_ListSection"
BASE_URL = "https://weblprod1.wheatonma.edu"

# This value used to get rid of first three useless rows in the web content.
SKIP_BEGINNING = 3
# This value used to extract desired number of semester values.
SEMESTER_NUMBER = 18

# Time filter constants
TIME_FILTER = pd.Series(
    data=["", "", "", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    index=["AM", "PM", "TBA", "M", "T", "W", "R", "F"]
)

# Icon for add class to calendar.
TO_CALENDAR = '<i id="to-calendar" class="fas fa-plus-circle fa-lg" ' \
              'style="color: green"></i>'


# Helper constants to slice the data frame.
class ColIndex(Enum):
    subject = 0
    course_number = 1
    title = 2
    time = 3
    exam = 4
    CRN = 5
    location = 6
    instructor = 7
    foundation = 8
    division = 9
    seat = 10
    area = 11
    connection = 12
    textbook = 13
    special = 14
    hidden = 15
