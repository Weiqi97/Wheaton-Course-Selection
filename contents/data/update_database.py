# coding=utf-8
"""Run this file to update data base and selection drop downs."""

from contents.data.data_fetcher import save_fetched_data
from contents.data.data_processor import save_all_semesters

# This line will update selection drop downs.
save_fetched_data()

# This line will update class information.
save_all_semesters()

# This line update one semester based on inputs.
# save_one_semester(semester_value="201910", semester_name="Fall 2018")
