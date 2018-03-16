from flask import Flask, render_template, request

from data_fetcher import fetch_semesters, fetch_subjects

app = Flask(__name__)
app.debug = True
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
