# coding=utf-8
"""This file reads the data and select right query based on users request."""

import pandas as pd
from bs4 import BeautifulSoup

# This has to be set, otherwise long string will get concatenated.
pd.set_option("display.max_colwidth", -1)


def read_data(area: str,
              division: str,
              semester: str,
              subjects: list,
              foundation: str) -> str:
    """Read data from saved file and return values based on users request.

    :param semester: User selected semester value.
    :param subjects: User selected subject(s).
    :param foundation: User selected foundation.
    :param division: User selected division.
    :param area: User selected area.
    :return: A pandas data frame that contains desired information.
    """
    # Get the data frame with all saved information.
    data_frame = \
        pd.read_pickle(f"contents/data/course_data/pickle_data/{semester}.pkl")

    # If choose all subject, pass, otherwise select desired rows.
    if "%" in subjects or "" in subjects:
        pass
    else:
        data_frames = [data_frame.loc[data_frame["Subject"] == subject]
                       for subject in subjects]
        data_frame = pd.DataFrame(pd.concat(data_frames))

    # If choose all foundation, pass, otherwise select desired rows.
    if foundation == "%":
        pass
    else:
        data_frame = data_frame.loc[data_frame["Foundation"] == foundation]

    # If choose all divisions, pass, otherwise select desired rows.
    if division == "%":
        pass
    else:
        data_frame = data_frame.loc[data_frame["Division"] == division]

    # If choose all areas, pass, otherwise select desired rows.
    if area == "%":
        pass
    else:
        data_frame = data_frame.loc[data_frame["Area"] == area]

    # Convert refined data frame to html format.
    table = data_frame.to_html(
        index=False,
        escape=False,
        classes="table table-striped table-bordered nowrap"
    )

    # Parse the HTML table to beautiful soup object.
    table_soup = BeautifulSoup(table, "html.parser")
    # Give the table an ID for easier access.
    table_soup.find("table")["id"] = "course-table"
    # Return beautiful soup as string.
    return table_soup.prettify()


def read_subjects() -> pd.Series:
    """Read data from saved pickle file."""
    return pd.read_pickle("contents/data/web_data/subjects.pkl")


def read_semesters() -> pd.Series:
    """Read data from saved pickle file."""
    return pd.read_pickle("contents/data/web_data/semesters.pkl")


def read_foundations() -> pd.Series:
    """Read data from saved pickle file."""
    return pd.read_pickle("contents/data/web_data/foundations.pkl")


def read_divisions() -> pd.Series:
    """Read data from saved pickle file."""
    return pd.read_pickle("contents/data/web_data/divisions.pkl")


def read_areas() -> pd.Series:
    """Read data from saved pickle file."""
    return pd.read_pickle("contents/data/web_data/areas.pkl")


def read_current_semester() -> str:
    """Read data from saved pickle file."""
    # The list always contains only one element, grab it.
    return pd.read_pickle("contents/data/web_data/current_semester.pkl")[0]
