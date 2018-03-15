# coding=utf-8
"""This file will process web content to human readable data."""

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from typing import List
from constants import base_url, ClassConx, ClassExam, ClassNumber, \
    ClassInstructor, SeatInfo, SKIP_BEGINNING
from data_fetcher import fetch_web_content, fetch_subjects, fetch_semesters


def extract_class_info(web_content: str) -> List[list]:
    """
    This function will extract class information from the given web page.
    :param web_content: A string that contains web page information.
    :return: A list of lists, where each list holds information for one class.
    """
    # Get the web content in text and parse it to html.
    web_soup = BeautifulSoup(web_content, "html5lib")

    # Find the table that contains desired class information.
    table = web_soup.find("table", {"class": "dataentrytable"})

    # Get all rows of the table.
    table_rows = table.find_all("tr")

    # Get rid of the first couple useless lines.
    info_rows = table_rows[SKIP_BEGINNING:]

    # Eliminate all the empty rows.
    class_rows = [row for row in info_rows if len(row.find_all("td")) > 1]

    # Work on separating the class each_class_info.
    class_index = [index for index, row in enumerate(class_rows)
                   if row.find("a")]

    # Check if exists more than one class.
    if len(class_index) > 1:
        combined_classes = \
            [class_rows[class_index[index]: class_index[index + 1]]
             for index, _ in enumerate(class_index[:-1])]
        combined_classes.append(class_rows[class_index[-1]:])

    # Check if exists only one class.
    elif len(class_index) == 1:
        combined_classes = [class_rows]

    # Check if nothing was found for one subject.
    else:
        combined_classes = []

    return combined_classes


def get_number_info(class_basic_info: list) -> List[ClassNumber]:
    """
    Get class number information.
    :param class_basic_info: A list of class basic information.
    :return: A list of refined class number information.
    """

    def _number_info_helper(each_class: list) -> ClassNumber:
        """
        Helper function for getting the class number information.
        :return: a ClassNumber object.
        """
        number_info = each_class[0].find("a")
        return ClassNumber(num=str(number_info.contents[0]),
                           link=base_url + number_info["href"])

    return [_number_info_helper(each_class)
            for each_class in class_basic_info]


def get_exam_info(class_basic_info: list) -> List[ClassExam]:
    """
    Get class exam information.
    :param class_basic_info: A list of class basic information.
    :return: A list of refined class exam information.
    """

    def _exam_info_helper(each_class: list) -> ClassExam:
        """
        Helper function for getting the class exam information.
        :return: a ClassExam object.
        """
        exam_info = each_class[1].find("a")

        # Error checking.
        if exam_info.contents:
            return ClassExam(letter=str(exam_info.contents[0]),
                             link=base_url + exam_info['href'])
        else:
            return ClassExam(letter="", link="")

    return [_exam_info_helper(each_class)
            for each_class in class_basic_info]


def get_time_info(class_basic_info: list) -> List[str]:
    """
    Get class time information.
    :param class_basic_info: A list of class basic information.
    :return: A list of class time information.
    """

    def _time_info_helper(each_class: list) -> List[str]:
        """
        Helper function for getting the class time information.
        :return: a list of class time information.
        """
        return [" ".join(content.replace("\n", "").split())
                if index % 4 == 0 else None
                for index, content in enumerate(each_class[4].contents)]

    return ["!".join(filter(None, _time_info_helper(each_class=each_class)))
            if _time_info_helper(each_class=each_class) is not None else ""
            for each_class in class_basic_info]


def get_location_info(class_basic_info: list) -> List[str]:
    """
    Get class location information.
    :param class_basic_info: A list of class basic information.
    :return: A list of class location information.
    """

    def _location_info_helper(each_class: list) -> List[str]:
        """
        Helper function for getting the class time information.
        :return: a list of class time information.
        """
        return [" ".join(content.replace("\n", "").split())
                if index % 4 != 0 and index % 2 == 0 else None
                for index, content in enumerate(each_class[4].contents)]

    return \
        ["!".join(filter(None, _location_info_helper(each_class=each_class)))
         if _location_info_helper(each_class=each_class) is not None else ""
         for each_class in class_basic_info]


def get_instructor_info(class_basic_info: list) -> List[List[ClassInstructor]]:
    """
    Get class instructor information.
    :param class_basic_info: A list of class basic information.
    :return: A list of list of class instructor(s) information.
    """

    def _instructor_info_helper(each_class: list):
        instructor_info = each_class[5].find_all("a")
        return [ClassInstructor(name=str(each_class_info.contents[0]),
                                link=each_class_info['href'])
                if instructor_info else
                ClassInstructor(name="DEPT", link="")
                for each_class_info in instructor_info]

    return [_instructor_info_helper(each_class)
            for each_class in class_basic_info]


def get_conx_info(each_class: BeautifulSoup) -> List[ClassConx]:
    """
    Get class connection information.
    :param each_class: A beautiful soup object that contains class information.
    :return: A list of class connection information.
    """
    connection_info = each_class[9].find_all("a")
    return [ClassConx(num=str(each_class_info.contents[0]),
                      link=each_class_info['href'])
            if connection_info else None
            for each_class_info in connection_info]


def refine_class_info(class_info_list: list, subject: str):
    """
    This function will refine class information from the web page.
    :param class_info_list: A list that contains all class web pages.
    :param subject: Name of the subject.
    :return: A pandas data frame that has all class information.
    """
    # Set data frame that holds all class information.
    class_info_frame = pd.DataFrame(
        data=0,
        index=np.arange(len(class_info_list)),
        columns=["subject", "number", "exam", "title", "CRN", "time",
                 "location", "instructor", "foundation", "division", "area",
                 "connection", "textbook", "seats", "special_info"]
    )

    # Get class seats information and store in the data frame..
    class_seats_info = [each_class[-1].find_all("td")
                        for each_class in class_info_list]

    class_info_frame["seats"] = [
        SeatInfo(max=str(each_class[1].contents[0]),
                 taken=str(each_class[1].contents[0]),
                 avail=str(each_class[1].contents[0]),
                 wait_list=str(each_class[1].contents[0]))
        for each_class in class_seats_info]

    # Get class special information, if any stores in the data frame.
    class_info_frame["special_info"] = [
        each_class[1].find_all("td")[1].contents[0].replace("\n", "")
        if len(each_class) > 2 else ""
        for each_class in class_info_list
    ]

    # Get class basic information.
    class_basic_info = [each_class[0].find_all("td")
                        for each_class in class_info_list]

    # Set all basic information.
    class_info_frame["subject"] = subject

    class_info_frame["number"] = \
        get_number_info(class_basic_info=class_basic_info)

    class_info_frame["exam"] = \
        get_exam_info(class_basic_info=class_basic_info)

    class_info_frame["title"] = [str(each_class[2].contents[0])
                                 for each_class in class_basic_info]

    class_info_frame["CRN"] = [str(each_class[3].contents[0])
                               for each_class in class_basic_info]

    class_info_frame["time"] = \
        get_time_info(class_basic_info=class_basic_info)

    class_info_frame["location"] = \
        get_location_info(class_basic_info=class_basic_info)

    class_info_frame["instructor"] = \
        get_instructor_info(class_basic_info=class_basic_info)

    class_info_frame["foundation"] = \
        [each_class[6].contents[0].replace("\n", "")
         for each_class in class_basic_info]

    class_info_frame["division"] = \
        [each_class[7].contents[0].replace("\n", "")
         for each_class in class_basic_info]

    class_info_frame["area"] = \
        [each_class[8].contents[0].replace("\n", "")
         for each_class in class_basic_info]

    class_info_frame["connection"] = [get_conx_info(each_class=each_class)
                                      for each_class in class_basic_info]

    class_info_frame["textbook"] = \
        [each_class[10].find("a")['href'] for each_class in class_basic_info]

    return class_info_frame


def get_specific_class_info(subject: str, semester: str) -> pd.DataFrame:
    """
    Return all class information for one subject within a semester.
    :param subject: A subject from subjects fetched.
    :param semester: A recent semester value from semesters fetched.
    :return: A pandas data frame that contains class information.
    """
    # Grab web content from Wheaton's website.
    web_content = fetch_web_content(subject=subject, semester=semester)

    # Find class information fromm the web content.
    class_info_list = extract_class_info(web_content=web_content)

    # Return refined class information.
    if class_info_list is not None:
        return refine_class_info(class_info_list=class_info_list,
                                 subject=subject)
    else:
        return pd.DataFrame()


def get_semester_class_info(semester_name: str, semester_value: str):
    """
    This function will get all class information for one semester.
    :param semester_name: A recent name value from semesters fetched.
    :param semester_value: A recent semester value from semesters fetched.
    """
    # Fetch all subject names.
    subjects = fetch_subjects()

    # Get information for all classes within the semester.
    all_class = \
        [get_specific_class_info(subject=subject, semester=semester_value)
         for subject in subjects]

    # Concatenate all data frames together to one.
    semester_frame = pd.DataFrame(pd.concat(all_class, ignore_index=True))

    # Save it as a pickle file.
    semester_frame.to_pickle(f"pickle_data/{semester_name}.pkl")

    # Save to CSV in order to easily compare with web page.
    semester_frame.to_csv(f"csv_data/{semester_name}.csv")


def save_all_info():
    """This function will get all needed information."""
    semesters = fetch_semesters()
    for semester_name, semester_value in semesters.iteritems():
        get_semester_class_info(semester_name=semester_name,
                                semester_value=semester_value)
