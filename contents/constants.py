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
TO_CALENDAR = '<span class="to-calendar">' \
              '<i class="fas fa-plus-circle fa-lg" style="color: green"></i>' \
              '</span>'

# Span for show details.
SHOW_DETAIL = '<span class="show-detail">' \
              '<i class="fas fa-angle-down fa-lg"></i>' \
              '</span>'


# TODO: This should be used.. Really..
# Helper constants to slice the data frame.
class ColIndex(Enum):
    """Indexes for columns in pandas data frame."""

    subject = 2
    course_number = 3
    title = 4
    time = 5
    CRN = 6
    location = 7
    instructor = 8
    exam = 9
    foundation = 10
    division = 11
    area = 12
    connection = 13
    seat = 14
    textbook = 15
    special = 16
    hidden = 17
