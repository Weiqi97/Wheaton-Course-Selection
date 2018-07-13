# coding=utf-8
"""This file will fetch all needed information from Wheaton's website."""

import pandas as pd
import mechanicalsoup
from contents.constants import URL, SEMESTER_NUMBER


def fetch_web_content(subject: str, semester: str) -> str:
    """Submit the form based on desired subject and semester.

    :param subject: Desired subject users want to search for.
    :param semester: Desired semester users want to search for.
    :return: A string that contains web page information.
    """
    # Set up the fake browser object and open the target website.
    browser = mechanicalsoup.StatefulBrowser()
    web = browser.open(URL)

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


def fetch_semesters() -> pd.Series:
    """Fetch all existing semester values and names from the HTML.

    :return: A pandas series, where
            - Index are semester names, ie "Spring 2018"
            - Data are corresponding semester values, ie "201820"
    """
    # Set up the fake browser object and open the target website.
    browser = mechanicalsoup.StatefulBrowser()
    web_soup = browser.open(URL).soup

    # Find the correct select tag.
    select_box = web_soup.find("select", {"name": "schedule_beginterm"})

    # Extract values from the tag.
    options = select_box.find_all("option")

    # Get values and names.
    option_values = [option["value"] for option in options]
    option_names = [str(option.contents[0]) for option in options]
    option_series = pd.Series(data=option_values, index=option_names)

    return option_series[:SEMESTER_NUMBER]


def fetch_subjects() -> pd.Series:
    """Fetch all existing subject names.

    :return: A pandas series, where
            - index are subject names.
            - Data are corresponding subject values.
    """
    # Set up the fake browser object and open the target website.
    browser = mechanicalsoup.StatefulBrowser()
    web_soup = browser.open(URL).soup

    # Find the correct select tag.
    select_box = web_soup.find("select", {"name": "subject_sch"})

    # Extract values from the tag.
    options = select_box.find_all("option")

    # Get values and names.
    option_values = [option["value"] for option in options]
    option_names = [str(option.contents[0]) for option in options]
    option_series = pd.Series(data=option_values, index=option_names)

    return pd.Series(option_series.drop(["CONNECTIONS"]))


def fetch_foundations() -> pd.Series:
    """Fetch all existing foundation names.

    :return: A pandas series, where
            - index are foundation names.
            - Data are corresponding foundation values.
    """
    # Set up the fake browser object and open the target website.
    browser = mechanicalsoup.StatefulBrowser()
    web_soup = browser.open(URL).soup

    # Find the correct select tag.
    select_box = web_soup.find("select", {"name": "foundation_sch"})

    # Extract values from the tag.
    options = select_box.find_all("option")

    # Get values and names.
    option_values = [option["value"] for option in options]
    option_names = [str(option.contents[0]).replace("Found: ", "")
                    for option in options]

    return pd.Series(data=option_values, index=option_names)


def fetch_divisions() -> pd.Series:
    """Fetch all existing foundation names.

    :return: A pandas series, where
            - index are division names.
            - Data are corresponding division values.
    """
    # Set up the fake browser object and open the target website.
    browser = mechanicalsoup.StatefulBrowser()
    web_soup = browser.open(URL).soup

    # Find the correct select tag.
    select_box = web_soup.find("select", {"name": "division_sch"})

    # Extract values from the tag.
    options = select_box.find_all("option")

    # Get values and names.
    option_values = [option["value"] for option in options]
    option_names = [str(option.contents[0]).replace("Division: ", "")
                    for option in options]

    return pd.Series(data=option_values, index=option_names)


def fetch_areas() -> pd.Series:
    """Fetch all existing foundation names.

    :return: A pandas series, where
            - index are area names.
            - Data are corresponding area values.
    """
    # Set up the fake browser object and open the target website.
    browser = mechanicalsoup.StatefulBrowser()
    web_soup = browser.open(URL).soup

    # Find the correct select tag.
    select_box = web_soup.find("select", {"name": "area_sch"})

    # Extract values from the tag.
    options = select_box.find_all("option")

    # Get values and names.
    option_values = [option["value"] for option in options]
    option_names = [str(option.contents[0]).replace("Area: ", "")
                    for option in options]

    return pd.Series(data=option_values, index=option_names)


def fetch_current_semester() -> pd.Series:
    """Fetch the current selected semester.

    :return: A pandas series contains desired value.
    """
    # Set up the fake browser object and open the target website.
    browser = mechanicalsoup.StatefulBrowser()
    web_soup = browser.open(URL).soup

    # Find the correct select tag.
    select_box = web_soup.find("select", {"name": "schedule_beginterm"})

    # Find the content of the selected tag.
    select_value = str(select_box.find("option", selected=True).contents[0])

    return pd.Series(data=select_value)


def save_fetched_data():
    """Fetch all the selection drop down data from the web and save them."""
    fetch_areas().to_pickle("web_data/areas.pkl")
    fetch_subjects().to_pickle("web_data/subjects.pkl")
    fetch_divisions().to_pickle("web_data/divisions.pkl")
    fetch_semesters().to_pickle("web_data/semesters.pkl")
    fetch_foundations().to_pickle("web_data/foundations.pkl")
    fetch_current_semester().to_pickle("web_data/current_semester.pkl")
