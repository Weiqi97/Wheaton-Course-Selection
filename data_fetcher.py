# coding=utf-8
"""This file will fetch all class information from Wheaton's website."""

import numpy as np
import pandas as pd
import mechanicalsoup
from bs4 import BeautifulSoup
from typing import List
from constants import url, base_url, ClassConx, ClassExam, ClassNumber, \
    ClassInstructor, SeatInfo


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
    Fetch all the existing subject names.
    :return: A list of subject names.
    """
    # Set up the fake browser object and open the target website.
    browser = mechanicalsoup.StatefulBrowser()
    web_soup = browser.open(url).soup

    # Find the correct select tag.
    select_box = web_soup.find("select", {"name": "subject_sch"})

    # Extract values from the tag.
    options = select_box.find_all("option")

    # return the desired values. ('%' means all subject.)
    return [option["value"] for option in options if option != "%"]


def fetch_semesters() -> List[str]:
    """

    :return:
    """
    browser = mechanicalsoup.StatefulBrowser()
    web_soup = browser.open(url).soup
    select_box = web_soup.find("select", {"name": "schedule_beginterm"})
    options = select_box.find_all("option")

    return [option["value"] for option in options]


def extract_class_info(web_content: str) -> List[list]:
    """
    This function will extract class information from the given web page
    content.
    :param web_content: A string that contains web page information.
    :return: A list of lists, where each list holds information
    for one class.
    """
    # Get the web content in text and parse it to html.
    web_soup = BeautifulSoup(web_content, "html5lib")

    # Find the table that contains desired class information.
    table = web_soup.find("table", {"class": "dataentrytable"})

    # Get all rows of the table.
    table_rows = table.find_all("tr")

    # TODO: think about a way to beautify this
    # Get rid of the first couple useless lines.
    info_rows = table_rows[3:]

    # Eliminate all the empty rows.
    class_rows = [row for row in info_rows if len(row.find_all("td")) > 1]

    # Work on separating the class info.
    class_index = [index for index, row in enumerate(class_rows)
                   if row.find("a")]

    if len(class_index) > 1:
        combined_classes = \
            [class_rows[class_index[index]: class_index[index + 1]]
             for index, _ in enumerate(class_index[:-1])]
        combined_classes.append(class_rows[class_index[-1]:])

    elif len(class_index) == 1:
        combined_classes = [class_rows]

    else:
        combined_classes = []

    return combined_classes


def refine_class_info(class_info_list: list, subject: str):
    """
    This function will refine class information from the web page.
    :param class_info_list: A list that contains all class web pages.
    :param subject: Name of the subject.
    :return: A pandas data frame that has all class information.
    """
    class_basic_info = [class_info[0].find_all("td")
                        for class_info in class_info_list]

    class_info_frame = pd.DataFrame(
        0,
        index=np.arange(len(class_info_list)),
        columns=["subject", "number", "exam", "title", "CRN", "time",
                 "location", "instructor", "foundation", "division", "area",
                 "connection", "textbook", "seats", "special_info"]
    )

    # Set all the subject name
    class_info_frame["subject"] = subject

    # This section will set the numbers
    def _number_info_helper(class_info: list):
        number_info = class_info[0].find("a")
        return ClassNumber(num=str(number_info.contents[0]),
                           link=base_url + number_info['href'])

    number_infos = [_number_info_helper(class_info)
                    for class_info in class_basic_info]
    class_info_frame["number"] = number_infos

    # This section will set the exams.
    def _exam_info_helper(class_info: list):
        exam_info = class_info[1].find("a")
        if exam_info.contents:
            return ClassExam(letter=str(exam_info.contents[0]),
                             link=base_url + exam_info['href'])
        else:
            return ClassExam(letter="", link="")

    class_info_frame["exam"] = [_exam_info_helper(class_info)
                                for class_info in class_basic_info]

    # This section will set the titles.
    class_info_frame["title"] = [str(class_info[2].contents[0])
                                 for class_info in class_basic_info]

    # This section will set the CRN.
    class_info_frame["CRN"] = [str(class_info[3].contents[0])
                               for class_info in class_basic_info]

    # This section will set the time.
    class_info_frame["time"] = [
        class_info[4].contents[0].replace('\n', '')
        for class_info in class_basic_info]
    # adjust time styles
    class_info_frame["time"] = [" ".join(time.split())
                                for time in class_info_frame["time"]]

    # This section will set the location.
    class_info_frame["location"] = [
        class_info[4].contents[2].replace('\n', '')
        for class_info in class_basic_info]

    # This section will set the instructor(s).
    def _instructor_info_helper(class_info: list):
        instructor_info = class_info[5].find_all("a")
        return [ClassInstructor(name=str(info.contents[0]),
                                link=info['href'])
                if instructor_info else
                [ClassInstructor(name="DEPT",
                                 link="")]
                for info in instructor_info]

    class_info_frame["instructor"] = [_instructor_info_helper(class_info)
                                      for class_info in class_basic_info]

    # This section will set the foundation, division and area.
    class_info_frame["foundation"] = \
        [class_info[6].contents[0].replace('\n', '')
         for class_info in class_basic_info]

    # This section will set the titles.
    class_info_frame["division"] = \
        [class_info[7].contents[0].replace('\n', '')
         for class_info in class_basic_info]

    # This section will set the CRN.
    class_info_frame["area"] = \
        [class_info[8].contents[0].replace('\n', '')
         for class_info in class_basic_info]

    # This section will set the connection information.
    def _conx_info_helper(class_info: list):
        connection_info = class_info[9].find_all("a")
        return [ClassConx(num=str(info.contents[0]),
                          link=info['href'])
                if connection_info else None
                for info in connection_info]

    class_info_frame["connection"] = [_conx_info_helper(class_info)
                                      for class_info in class_basic_info]

    # This section will set the textbook link.
    class_info_frame["textbook"] = \
        [class_info[10].find("a")['href'] for class_info in class_basic_info]

    # TODO: MOVE THIS SECTION TO SOMEWHERE ELSE
    # This part grab the seats information
    class_seats_info = [class_info[-1].find_all("td")
                        for class_info in class_info_list]

    class_info_frame["seats"] = [
        SeatInfo(max=str(info[1].contents[0]),
                 taken=str(info[1].contents[0]),
                 avail=str(info[1].contents[0]),
                 wait_list=str(info[1].contents[0]))
        for info in class_seats_info]

    # This part grab the special information
    class_info_frame["special_info"] = [
        class_info[1].find_all("td")[1].contents[0].replace("\n", "")
        if len(class_info) > 2 else ""
        for class_info in class_info_list
    ]

    return class_info_frame


def get_final_frame():
    """

    :return: A data frame that contains all class information.
    """
    final_frame_list = []
    all_subjects = fetch_subjects()
    subjects = all_subjects[1:]
    for subject in subjects:
        web_content = fetch_web_content(subject)
        class_info_list = extract_class_info(web_content)
        class_frame = refine_class_info(class_info_list, subject)
        final_frame_list.append(class_frame)

    final_frame = pd.DataFrame(pd.concat(final_frame_list, ignore_index=True))
    final_frame.to_pickle("FINAL_FRAME.pkl")


all_semesters = fetch_semesters()
print("DONE")
