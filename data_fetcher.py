# coding=utf-8
"""This file will fetch all needed information from Wheaton's website."""

import pandas as pd
import mechanicalsoup
from typing import List
from constants import url, SEMESTER_NUMBER


# TODO: Careful about LAB. How to deal with them? (This might take longer...)
def fetch_web_content(subject: str, semester: str) -> str:
    """
    This function will submit the form based on the two inputs.
    :param subject: Desired subject users want to search for.
    :param semester: Desired semester users want to search for.
    :return: A string that contains web page information.
    """
    # Set up the fake browser object and open the target website.
    browser = mechanicalsoup.StatefulBrowser()
    web = browser.open(url)

    # Remove all submit button but the one called "Search Schedule"
    for each_input in web.soup.find_all("input"):
        if each_input.get("value") != "Search Schedule":
            each_input.extract()

    # Fill out the desired information in the form.
    form = browser.select_form('form[action="bzcrschd.P_OpenDoor"]')

    # Fill out the form with user desired input.
    form.set("subject_sch", subject)
    form.set("schedule_beginterm", semester)

    # Submit form.
    response = browser.submit_selected()

    return response.text


def fetch_subjects() -> List[str]:
    """
    Fetch all existing subject names.
    :return: A list of subject names.
    """
    # Set up the fake browser object and open the target website.
    browser = mechanicalsoup.StatefulBrowser()
    web_soup = browser.open(url).soup

    # Find the correct select tag.
    select_box = web_soup.find("select", {"name": "subject_sch"})

    # Extract values from the tag.
    options = select_box.find_all("option")

    # return the desired values. (Exclude: '%', it means all subject.)
    return [option["value"] for option in options if option["value"] != "%"]


def fetch_semesters() -> pd.Series:
    """
    Fetch all existing semester values and names.
    :return: A pandas series, where
            - Index are semester names, ie "Spring 2018"
            - Data are corresponding semester values, ie "201820"
    """
    # Set up the fake browser object and open the target website.
    browser = mechanicalsoup.StatefulBrowser()
    web_soup = browser.open(url).soup

    # Find the correct select tag.
    select_box = web_soup.find("select", {"name": "schedule_beginterm"})

    # Extract values from the tag.
    options = select_box.find_all("option")

    # Get values and names.
    option_values = [option["value"] for option in options]
    option_names = [str(option.contents[0]) for option in options]
    option_series = pd.Series(data=option_values, index=option_names)

    return option_series[:SEMESTER_NUMBER]
