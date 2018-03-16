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
    data = pd.read_pickle(f"data/saved_data/pickle_data/{semester}.pkl")

    if subjects == ["%"]:
        pass
    else:
        data = data.loc[subjects]

    return data

