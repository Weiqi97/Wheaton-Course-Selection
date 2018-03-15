# coding=utf-8
"""This file reads the data and select right query based on users request."""

import pandas as pd
from web_contents.data.data_processor import save_all_info
# from constants import ClassConx, ClassInstructor, ClassExam, ClassNumber
# TODO: See if I want to create a fake function to get rid of stupid warnings
# TODO: read documentation about queries
# http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-query


save_all_info()
final_frame = pd.read_pickle("FINAL_FRAME.pkl")
print("DONE")
