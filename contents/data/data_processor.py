# coding=utf-8
"""This file will process web content to human readable data."""

import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Optional
from contents.constants import BASE_URL, SKIP_BEGINNING, TIME_FILTER, \
    TO_CALENDAR, SHOW_DETAIL
from contents.data.data_fetcher import fetch_semesters, fetch_subjects, \
    fetch_web_content


def extract_class_info(web_content: str) -> Optional[List[list]]:
    """Extract class information from the given web page.

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
        combined_classes = None

    return combined_classes


def to_html_link(title: str, link: str) -> str:
    """Convert the two inputs to a HTML link.

    :param title: Title of the link.
    :param link: Url of the link.
    :return: HTML formatted link.
    """
    return f'<a target="_blank" href="{link}">{title}</a>'


def get_number_info(class_basic_info: list) -> List[str]:
    """Get class number information.

    :param class_basic_info: A list of class basic information.
    :return: A list of refined class number information.
    """
    def number_info_helper(each_class: list) -> str:
        """Get the class number information.

        :param each_class: information of one class.
        :return: a ClassNumber object.
        """
        number_info = each_class[0].find("a")
        return to_html_link(title=str(number_info.contents[0]),
                            link=BASE_URL + number_info["href"])

    return [
        number_info_helper(each_class) for each_class in class_basic_info
    ]


def get_exam_info(class_basic_info: list) -> List[str]:
    """Get class exam information.

    :param class_basic_info: A list of class basic information.
    :return: A list of refined class exam information.
    """
    def exam_info_helper(each_class: list) -> str:
        """Get the class exam information.

        :param each_class: information of one class.
        :return: a ClassExam object.
        """
        exam_info = each_class[1].find("a")

        # Error checking.
        if exam_info.contents:
            return to_html_link(title=str(exam_info.contents[0]),
                                link=BASE_URL + exam_info['href'])
        else:
            return ""

    return [
        exam_info_helper(each_class) for each_class in class_basic_info
    ]


def get_time_info(class_basic_info: list) -> List[str]:
    """Get class time information.

    :param class_basic_info: A list of class basic information.
    :return: A list of lists, where each each contains class time information.
    """
    def time_info_helper(each_class: list) -> str:
        """Get the class time information.

        :param each_class: information of one class.
        :return: a list of class time information.
        """
        return "<br>".join(
            [" ".join(content.replace("\n", "").split())
             for index, content in enumerate(each_class[4].contents)
             if index % 4 == 0]
        )

    return [
        time_info_helper(each_class=each_class)
        for each_class in class_basic_info
    ]


def get_location_info(class_basic_info: list) -> List[str]:
    """Get class location information.

    :param class_basic_info: A list of class basic information.
    :return: A list of lists, where each each contains class loc information.
    """
    def location_info_helper(each_class: list) -> str:
        """Get the class time information.

        :param each_class: information of one class.
        :return: a list of class time information.
        """
        return " ".join(
            [" ".join(content.replace("\n", "").split())
             for index, content in enumerate(each_class[4].contents)
             if index % 4 != 0 and index % 2 == 0]
        )

    return [
        location_info_helper(each_class=each_class)
        if location_info_helper(each_class=each_class) is not None else ""
        for each_class in class_basic_info
    ]


def get_instructor_info(class_basic_info: list) -> List[str]:
    """Get class instructor information.

    :param class_basic_info: A list of class basic information.
    :return: A list of list of class instructor(s) information.
    """
    def instructor_info_helper(each_class: list) -> str:
        """Get the class instructor information.

        :param each_class: information of one class.
        :return: a list of class information.
        """
        instructor_info = each_class[5].find_all("a")
        return "<br>".join(
            [to_html_link(title=str(each_class_info.contents[0]),
                          link=each_class_info['href'])
             if instructor_info else "DEPT"
             for each_class_info in instructor_info]
        )

    return [
        instructor_info_helper(each_class) for each_class in class_basic_info
    ]


def get_connection_info(each_class: BeautifulSoup) -> str:
    """Get class connection information.

    :param each_class: A beautiful soup object that contains class information.
    :return: A list of class connection information.
    """
    connection_info = each_class[9].find_all("a")
    return " ".join(
        [to_html_link(title=str(each_class_info.contents[0]),
                      link=BASE_URL + each_class_info['href'])
         for each_class_info in connection_info if connection_info]
    )


def get_hidden_days_info(class_times: List[str]) -> List[str]:
    """Get hidden class information time.

    :param class_times: List of class times.
    :return: List of strings with substituted full week day names.
    """
    def hidden_days_info_helper(class_time: str) -> str:
        """Hide values helper.

        :param class_time: list of time of each class.
        :return: a string that contains exact class day time.
        """
        for original, replace in TIME_FILTER.iteritems():
            class_time = class_time.replace(original, replace)

        return class_time

    return [hidden_days_info_helper(class_time=class_time)
            for class_time in class_times]


def get_seats_info(seat_max: str,
                   seat_taken: str,
                   seat_available: str,
                   seat_wait: str) -> str:
    """Convert seats info to HTML format.

    :param seat_max: Number of max seats of the class.
    :param seat_taken: Number of taken seats of the class.
    :param seat_available: Number of available seats of the class.
    :param seat_wait: Number of wait list of the class.
    :return: A HTML formatted string holds all input information.
    """
    return f"{seat_max} {seat_taken} {seat_available} {seat_wait}"


def refine_class_info(class_info_list: list, subject: str) -> pd.DataFrame:
    """Refine class information from the web page.

    :param class_info_list: A list that contains all class web pages.
    :param subject: Name of the subject.
    :return: A pandas data frame that has all class information.
    """
    # Set data frame that holds all class information.
    class_info_frame = pd.DataFrame(
        columns=["", "Add", "Subject", "Course Number", "Title", "Time", "CRN",
                 "Location", "Instructor", "Exam", "Foundation", "Division",
                 "Area", "Connection", "Seat", "Textbook", "Special", "Hidden"]
    )

    # Get class seats information and store in the data frame..
    class_seats_info = [each_class[-1].find_all("td")
                        for each_class in class_info_list]

    class_info_frame["Seat"] = [
        get_seats_info(
            seat_max=str(each_class[1].contents[0]),
            seat_taken=str(each_class[2].contents[0]),
            seat_available=str(each_class[3].contents[0]),
            seat_wait=str(each_class[4].contents[0])
        )
        if each_class else ""
        for each_class in class_seats_info]

    # Get class special information, if any stores in the data frame.
    class_info_frame["Special"] = [
        each_class[1].find_all("td")[1].contents[0].replace("\n", "")
        if len(each_class) > 2 else ""
        for each_class in class_info_list
    ]

    # Get class basic information.
    class_basic_info = [each_class[0].find_all("td")
                        for each_class in class_info_list]

    # Set all basic information.
    class_info_frame[""] = SHOW_DETAIL
    class_info_frame["Add"] = TO_CALENDAR

    class_info_frame["Subject"] = subject

    class_info_frame["Course Number"] = \
        get_number_info(class_basic_info=class_basic_info)

    class_info_frame["Exam"] = \
        get_exam_info(class_basic_info=class_basic_info)

    class_info_frame["Title"] = [str(each_class[2].contents[0])
                                 for each_class in class_basic_info]

    class_info_frame["CRN"] = [str(each_class[3].contents[0])
                               for each_class in class_basic_info]

    class_info_frame["Time"] = \
        get_time_info(class_basic_info=class_basic_info)

    class_info_frame["Location"] = \
        get_location_info(class_basic_info=class_basic_info)

    class_info_frame["Instructor"] = \
        get_instructor_info(class_basic_info=class_basic_info)

    class_info_frame["Foundation"] = \
        [each_class[6].contents[0].replace("\n", "")
         for each_class in class_basic_info]

    class_info_frame["Division"] = \
        [each_class[7].contents[0].replace("\n", "")
         for each_class in class_basic_info]

    class_info_frame["Area"] = \
        [each_class[8].contents[0].replace("\n", "")
         for each_class in class_basic_info]

    class_info_frame["Connection"] = \
        [get_connection_info(each_class=each_class)
         for each_class in class_basic_info]

    class_info_frame["Textbook"] = \
        [to_html_link(title="Textbook",
                      link=each_class[10].find("a")['href'])
         for each_class in class_basic_info]

    class_info_frame["Hidden"] = \
        get_hidden_days_info(class_info_frame["Time"])

    return class_info_frame


def get_specific_class_info(subject: str, semester: str) -> pd.DataFrame:
    """Return all class information for one subject within a semester.

    :param subject: A subject from subjects fetched.
    :param semester: A semester from semesters fetched.
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


def save_one_semester(semester_name: str, semester_value: str):
    """Get class information for one semester.

    :param semester_name: Name of the desired semester to be fetched.
    :param semester_value: HTML value of the desired semester to be fetched.
    """
    # Fetch all subject names.
    subjects = fetch_subjects()

    # Get information for all classes within the semester.
    all_class = \
        [get_specific_class_info(subject=subject_value,
                                 semester=semester_value)
         for subject_value in subjects.values]

    # Concatenate all data frames together to one.
    semester_frame = pd.DataFrame(pd.concat(all_class, ignore_index=True))

    # Save it as a pickle file.
    semester_frame.to_pickle(f"course_data/pickle_data/{semester_name}.pkl")


def save_all_semesters():
    """Get class information for all existing subjects."""
    semesters = fetch_semesters()
    for semester_name, semester_value in semesters.iteritems():
        save_one_semester(semester_name=semester_name,
                          semester_value=semester_value)
