from flask import Flask, render_template, request

from data_fetcher import fetch_semesters

app = Flask(__name__)
app.debug = True


@app.route("/", methods=["GET"])
def drop_down():
    semesters = fetch_semesters()
    return render_template("test.html",
                           semesters=semesters)


@app.route("/", methods=["POST"])
def sth():
    A = request.form["STH"]
    print("DONE")


if __name__ == "__main__":
    app.run()
