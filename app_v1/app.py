from flask import Flask, render_template, request
from python.googleS import run_google_search

# Configure Flask to use the standard `templates` and `static` folders
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/sidebar.html")
def sidebar():
    """Serve the sidebar snippet used via fetch() on the frontend."""
    return render_template("sidebar.html")

@app.route("/documentation")
def documentation():
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
