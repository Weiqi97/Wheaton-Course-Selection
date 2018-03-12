
# coding=utf-8

import pandas as pd

from data_fetcher import ClassNumber, ClassExam, ClassInstructor, ClassConx, \
    SeatInfo

# TODO: See if I want to create a fake function to get rid of stupid warnings
# TODO: read documentation about queries
# http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-query

final_frame = pd.read_pickle("FINAL_FRAME.pkl")
result = final_frame.query("CRN == \'10018\'")

title = result['title'].values

print("DONE")
