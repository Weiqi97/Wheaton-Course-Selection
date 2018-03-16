from flask import Flask, render_template, request
from web_contents.data.data_fetcher import fetch_semesters, fetch_subjects, \
    fetch_foundations, fetch_divisions, fetch_areas, fetch_intmajors

app = Flask(__name__)
app.debug = True


@app.route("/", methods=["GET"])
def drop_down_selections():
    semesters = fetch_semesters()
    subjects = fetch_subjects()
    foundations = fetch_foundations()
    divisions = fetch_divisions()
    areas = fetch_areas()
    intmajors = fetch_intmajors()

    return render_template("index.html",
                           semesters=semesters,
                           subjects=subjects,
                           foundations=foundations,
                           divisions=divisions,
                           areas=areas,
                           intmajors=intmajors)


@app.route("/", methods=["POST"])
def sth():
    semester = request.form["semester"]
    subjects = request.form.getlist("subject")
    foundation = request.form["foundation"]
    division = request.form["division"]
    area = request.form["area"]
    intmajor = request.form["intmajor"]

    print(semester, subjects)
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
