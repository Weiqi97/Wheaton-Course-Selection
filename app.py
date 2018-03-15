from flask import Flask, render_template, request
from data_fetcher import fetch_semesters, fetch_subjects

app = Flask(__name__)
app.debug = True


@app.route("/", methods=["GET"])
def drop_down_selections():
    subjects = fetch_subjects()
    semesters = fetch_semesters()
    return render_template("test.html",
                           subjects=subjects,
                           semesters=semesters)


@app.route("/", methods=["POST"])
def sth():
    semester = request.form["semesters"]
    subjects = request.form.getlist("subjects")
    print(semester, subjects)
    return render_template("test.html")


if __name__ == "__main__":
    app.run()
