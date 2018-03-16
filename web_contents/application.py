from flask import Flask, render_template, request
from web_contents.data.data_fetcher import fetch_semesters, fetch_subjects, \
    fetch_foundations, fetch_divisions, fetch_areas
from web_contents.data.data_reader import read_data

app = Flask(__name__)
app.debug = True


@app.route("/", methods=["GET"])
def drop_down_selections():
    semesters = fetch_semesters()
    subjects = fetch_subjects()
    foundations = fetch_foundations()
    divisions = fetch_divisions()
    areas = fetch_areas()

    return render_template("index.html",
                           semesters=semesters,
                           subjects=subjects,
                           foundations=foundations,
                           divisions=divisions,
                           areas=areas)


@app.route("/", methods=["POST"])
def return_table_values():
    semester = request.form["semester"]
    subjects = request.form.getlist("subjects")
    foundation = request.form["foundation"]
    division = request.form["division"]
    area = request.form["area"]

    selected_data = read_data(semester=semester,
                              subjects=subjects,
                              foundation=foundation,
                              division=division,
                              area=area)

    return render_template("index.html",
                           selected_data=selected_data)


if __name__ == "__main__":
    app.run()
