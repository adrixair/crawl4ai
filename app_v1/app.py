from flask import Flask, render_template

# Configure Flask to use the standard `templates` and `static` folders
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/GoogleDeepSearchS.html")
def google_deep_search_page():
    return render_template("GoogleDeepSearchS.html")

@app.route("/404.html")
def documentation():
    return render_template("404.html"),404

if __name__ == "__main__":
    app.run(debug=True)
