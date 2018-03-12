
# coding=utf-8

import pandas as pd

from data_fetcher import ClassNumber, ClassExam, ClassInstructor, ClassConx, \
    SeatInfo


final_frame = pd.read_pickle("Test.pkl")
number = final_frame["number"][0]
print(number.num)
