# coding=utf-8
"""This file reads the data and select right query based on users request."""

import pandas as pd


# TODO: See if I want to create a fake function to get rid of stupid warnings
# TODO: read documentation about queries
# http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-query


def read_data(semester: str, subjects: list, foundation: str, division: str,
              area: str, intmajor: str) -> pd.DataFrame:
    """

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

    if foundation == ["%"]:
        pass
    else:
        data_frame = data_frame.loc[data_frame["foundation"] == foundation]

    if division == ["%"]:
        pass
    else:
        data_frame = data_frame.loc[data_frame["division"] == division]

    return data_frame

