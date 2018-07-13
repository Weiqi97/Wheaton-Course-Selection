"""This is the flask application that connects backend and frontend."""

from flask import Flask, render_template, request
from contents.data.data_reader import read_data, read_semesters, \
    read_subjects, read_foundations, read_divisions, read_areas, \
    read_current_semester

app = Flask(__name__)
app.debug = True


@app.route("/", methods=["GET"])
def main():
    """Render the main HTML page.

    Get the data for all the select drop downs.
    :return: A rendered template with desired information.
    """
    return render_template(
        "index.html",
        fetched_areas=read_areas(),
        fetched_subjects=read_subjects(),
        fetched_semesters=read_semesters(),
        fetched_divisions=read_divisions(),
        fetched_foundations=read_foundations(),
        current_semester=read_current_semester()
    )


@app.route("/course_table", methods=["POST"])
def get_all_class():
    """Get all course information.

    :return: A html formatted table.
    """
    return read_data(
        area=request.json["area"],
        division=request.json["division"],
        subjects=request.json["subjects"].split(","),
        semester=request.json["semester"],
        foundation=request.json["foundation"]
    )


if __name__ == "__main__":
    app.run(threaded=True)
