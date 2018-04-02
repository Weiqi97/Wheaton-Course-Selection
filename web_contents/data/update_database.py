# coding=utf-8
"""Run this file to update data base and selection drop downs."""
from web_contents.data.data_fetcher import save_fetched_data
from web_contents.data.data_processor import save_all_info

# This line will update selection drop downs.
save_fetched_data()
save_all_info()

