# coding=utf-8
"""This file reads the data and select right query based on users request."""

import pandas as pd


def read_data(area: str,
              semester: str,
              subjects: list,
              division: str,
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
    if "%" in subjects:
        pass
    else:
        data_frames = [data_frame.loc[data_frame["subject"] == subject]
                       for subject in subjects]
        data_frame = pd.DataFrame(pd.concat(data_frames))

    # If choose all foundation, pass, otherwise select desired rows.
    if foundation == "%":
        pass
    else:
        data_frame = data_frame.loc[data_frame["foundation"] == foundation]

    # If choose all divisions, pass, otherwise select desired rows.
    if division == "%":
        pass
    else:
        data_frame = data_frame.loc[data_frame["division"] == division]

    # If choose all areas, pass, otherwise select desired rows.
    if area == "%":
        pass
    else:
        data_frame = data_frame.loc[data_frame["area"] == area]

    # Return refined data frame.
    return data_frame.to_html(classes="table table-striped table-bordered")


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
