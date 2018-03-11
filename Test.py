# coding=utf-8

import mechanicalsoup
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from typing import List, NamedTuple

# Leave some constant here
base_url = "https://weblprod1.wheatonma.edu"


# TODO: Careful about LAB. How to deal with them?
class ClassNumber(NamedTuple):
    """Struct for class number information."""
    num: str
    link: str


class ClassExam(NamedTuple):
    """Struct for class exam information."""
    letter: str
    link: str


class ClassInstructor(NamedTuple):
    """Struct for class instructor information."""
    name: str
    link: str


class ClassConx(NamedTuple):
    """Struct for class connection information."""
    num: str
    link: str


# TODO: Think about if we want to make this a class object.
# TODO: This function will need semester parameter.
def grub_web_content(subject: str) -> str:
    """
    This function submit a form to search based on users request.
    :param subject: Desired subject users want to search for.
    :return: A string that contains web page information.
    """
    # Set the course search web page.
    url = "https://weblprod1.wheatonma.edu/PROD/bzcrschd.P_ListSection"

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

    # Submit form.
    response = browser.submit_selected()

    # TODO: Remove this, leave here for testing purpose.
    # browser.launch_browser()

    return response.text


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

    combined_classes = [class_rows[class_index[index]: class_index[index + 1]]
                        for index, _ in enumerate(class_index[:-1])]
    combined_classes.append(class_rows[class_index[-1]:])

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
        columns=["Subject", "number", "exam", "title", "CRN", "time",
                 "location", "instructor", "foundation", "division", "area",
                 "connection", "textbook", "special_info"]
    )

    # Set all the subject name
    class_info_frame["Subject"] = subject

    # This section will set the numbers
    def _number_info_helper(class_info: list):
        number_info = class_info[0].find("a")
        return ClassNumber(num=number_info.contents[0].string,
                           link=base_url + number_info['href'])

    number_infos = [_number_info_helper(class_info)
                    for class_info in class_basic_info]
    class_info_frame["number"] = number_infos

    # This section will set the exams.
    def _exam_info_helper(class_info: list):
        exam_info = class_info[1].find("a")
        if exam_info.contents:
            return ClassExam(letter=exam_info.contents[0].string,
                             link=base_url + exam_info['href'])
        else:
            return ClassExam(letter="", link="")

    class_info_frame["exam"] = [_exam_info_helper(class_info)
                                for class_info in class_basic_info]

    # This section will set the titles.
    class_info_frame["title"] = [class_info[2].contents[0].string
                                 for class_info in class_basic_info]

    # This section will set the CRN.
    class_info_frame["CRN"] = [class_info[3].contents[0].string
                               for class_info in class_basic_info]

    # This section will set the time.
    class_info_frame["time"] = [
        class_info[4].contents[0].string.replace('\n', '')
        for class_info in class_basic_info]
    # adjust time styles
    class_info_frame["time"] = [" ".join(time.split())
                                for time in class_info_frame["time"]]

    # This section will set the location.
    class_info_frame["location"] = [
        class_info[4].contents[2].string.replace('\n', '')
        for class_info in class_basic_info]

    # This section will set the instructor(s).
    def _instructor_info_helper(class_info: list):
        instructor_info = class_info[5].find_all("a")

        return [ClassInstructor(name=info.contents[0].string,
                                link=info['href'])
                if instructor_info else
                [ClassInstructor(name="DEPT",
                                 link="")]
                for info in instructor_info]

    class_info_frame["instructor"] = [_instructor_info_helper(class_info)
                                      for class_info in class_basic_info]

    return class_info_frame


class_infoss = extract_class_info(grub_web_content("BIO"))
class_frame = refine_class_info(class_infoss, "BIO")
class_exam = [CRN for CRN in class_frame['instructor']]
print(class_exam)
print("DONE")
