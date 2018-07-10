from flask import Flask, render_template, request
from contents.data.data_reader import read_data, read_semesters, \
    read_subjects, read_foundations, read_divisions, read_areas, \
    read_current_semester

app = Flask(__name__)
app.debug = True


@app.route("/", methods=["GET", "POST"])
def drop_down_selections():
    fetched_semesters = read_semesters()
    fetched_subjects = read_subjects()
    fetched_foundations = read_foundations()
    fetched_divisions = read_divisions()
    fetched_areas = read_areas()
    fetched_current_semester = read_current_semester()
    selected_data = read_data(semester=fetched_current_semester,
                              subjects=["%"],
                              foundation="%",
                              division="%",
                              area="%")

    if request.method == "GET":
        return render_template("index.html",
                               current_semester=fetched_current_semester,
                               fetched_semesters=fetched_semesters,
                               fetched_subjects=fetched_subjects,
                               fetched_foundations=fetched_foundations,
                               fetched_divisions=fetched_divisions,
                               fetched_areas=fetched_areas,
                               selected_data=selected_data)

    if request.method == "POST":
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
                               semester=semester,
                               fetched_semesters=fetched_semesters,
                               fetched_subjects=fetched_subjects,
                               fetched_foundations=fetched_foundations,
                               fetched_divisions=fetched_divisions,
                               fetched_areas=fetched_areas,
                               selected_data=selected_data)


if __name__ == "__main__":
    app.run(threaded=True)
