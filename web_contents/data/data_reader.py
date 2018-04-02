# coding=utf-8
"""This file reads the data and select right query based on users request."""

import pandas as pd


def read_data(semester: str, subjects: list, foundation: str, division: str,
              area: str) -> pd.DataFrame:
    """
    This function will reads data from saved file and return proper values
    based on users request.
    :param semester: User selected semester value.
    :param subjects: User selected subject(s).
    :param foundation: User selected foundation.
    :param division: User selected division.
    :param area: User selected area.
    :return: A pandas data frame that contains desired information.
    """
    data_frame = pd.read_pickle(f"data/course_data/pickle_data/{semester}.pkl")

    if "%" in subjects:
        pass
    else:
        data_frames = [data_frame.loc[data_frame["subject"] == subject]
                       for subject in subjects]
        data_frame = pd.DataFrame(pd.concat(data_frames))

    if foundation == "%":
        pass
    else:
        data_frame = data_frame.loc[data_frame["foundation"] == foundation]

    if division == "%":
        pass
    else:
        data_frame = data_frame.loc[data_frame["division"] == division]

    if area == "%":
        pass
    else:
        data_frame = data_frame.loc[data_frame["area"] == area]

    return data_frame


def read_subjects() -> list:
    """Reads data from saved pickle file."""
    return pd.read_pickle("data/web_data/subjects.pkl")


def read_semesters() -> list:
    """Reads data from saved pickle file."""
    return pd.read_pickle("data/web_data/semesters.pkl")


def read_foundations() -> list:
    """Reads data from saved pickle file."""
    return pd.read_pickle("data/web_data/foundations.pkl")


def read_divisions() -> list:
    """Reads data from saved pickle file."""
    return pd.read_pickle("data/web_data/divisions.pkl")


def read_areas() -> list:
    """Reads data from saved pickle file."""
    return pd.read_pickle("data/web_data/areas.pkl")
