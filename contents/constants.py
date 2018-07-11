# coding=utf-8
"""This file contains needed constants."""

import pandas as pd
from typing import NamedTuple


# Struct constants
class SeatInfo(NamedTuple):
    """Struct for seats information."""
    max: str
    taken: str
    avail: str
    wait_list: str


# Web url constants
url = "https://weblprod1.wheatonma.edu/PROD/bzcrschd.P_ListSection"
base_url = "https://weblprod1.wheatonma.edu"

# Integer constants
# This value used to skip first three useless rows in the web content.
SKIP_BEGINNING = 3
# This value used to extract desired number of semester values.
SEMESTER_NUMBER = 18

# Time filter constants
TIME_FILTER = pd.Series(data=["", "", "", "Monday", "Tuesday", "Wednesday",
                              "Thursday", "Friday"],
                        index=["AM", "PM", "TBA", "M", "T", "W", "R", "F"])
