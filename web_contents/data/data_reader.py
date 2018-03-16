# coding=utf-8
"""This file reads the data and select right query based on users request."""

import pandas as pd


def read_data(semester: str, subjects: list, foundation: str, division: str,
              area: str, intmajor: str) -> pd.DataFrame:
    """
    This function will reads data from saved file and return proper values
    based on users request.
    :param semester:
    :param subjects:
    :param foundation:
    :param division:
    :param area:
    :param intmajor:
    """
    data_frame = pd.read_pickle(f"data/saved_data/pickle_data/{semester}.pkl")

    if subjects == ["%"]:
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

    if intmajor == "%":
        pass
    else:
        data_frame = data_frame.loc[data_frame["intmajor"] == intmajor]

    return data_frame
