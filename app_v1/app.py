from flask import Flask, render_template, request
from python.googleS import run_google_search

app = Flask(__name__, template_folder="src")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/documentation")
def documentation():
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)