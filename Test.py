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
    This function will extract class information from the given web page content.
    :param web_content: A string that contains web page information.
    :return: A list of lists, where each list holds information for one class.
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
    class_index = [index for index, row in enumerate(class_rows) if row.find("a")]

    combined_classes = [class_rows[class_index[index]: class_index[index + 1]]
                        for index, _ in enumerate(class_index[:-1])]
    combined_classes.append(class_rows[class_index[-1]:])

    return combined_classes

def refine_class_info(class_info_list: list, subject: str):
    class_basic_info = [class_info[0].find_all("td")
                        for class_info in class_info_list]

    class_info_frame = pd.DataFrame(
        0,
        index=np.arange(len(class_info_list)),
        columns=["Subject", "number", "exam", "title", "CRN", "time",
                 "location", "instructor", "foundation", "division", "area",
                 "connection", "textbook", "special_info"]
    )


class_list = extract_class_info(grub_web_content("BIO"))

class_info = class_list[-1]
class_basic_info = class_info[0].find_all("td")

base_url = "https://weblprod1.wheatonma.edu"

number_info = class_basic_info[0].find("a")
number = ClassNumber(num=number_info.contents[0].string,
                     link=base_url + number_info['href'])

exam_info = class_basic_info[1].find("a")
exam = ClassExam(letter=exam_info.contents[0].string,
                 link=base_url + exam_info['href'])

title = class_basic_info[2].contents[0].string

CRN = class_basic_info[3].contents[0].string

time = class_basic_info[4].contents[0]

location = class_basic_info[4].contents[2]

instructors_info = class_basic_info[5].find_all("a")
instructor = [ClassInstructor(name=info.contents[0].string,
                              link=info['href'])
              for info in instructors_info]

foundation = class_basic_info[6].contents[0].string

division = class_basic_info[7].contents[0].string

area = class_basic_info[8].contents[0].string

connection_info = class_basic_info[9].find("a")
if connection_info:
    connection = ClassConx(num=connection_info.contents[0].string,
                           link=base_url + connection_info['href'])
else:
    connection = ClassConx(num="", link="")

textbook = class_basic_info[10].find("a")['href']

print(number.num, '\n', number.link)
print(exam.letter, '\n', exam.link)
print(title)
print(CRN)
print(time)
print(location)
print(instructor[0].name)
print(instructor[0].link)
print(foundation)
print(division)
print(area)
print(connection.num, '\n', connection.link)
print(textbook)

# TODO: Careful about LAB. How to deal with them?