from flask import Flask, render_template, request, jsonify
import asyncio
from xt import run_batch  # on adapte run_batch pour qu’il prenne en argument une liste de keywords
from googleS import run_google_search

# Serve static assets under app_v1/static/ and templates from app_v1/templates
app = Flask(
    __name__,
    static_folder="../static",
    static_url_path="/static",
    template_folder="../templates",
)

@app.route("/", methods=["GET"])
def index():
    # Page principale
    return render_template("index.html")

@app.route("/google_search", methods=["POST"])
def google_search():
    # Récupère les données du formulaire
    keywords = request.form["keywords"].splitlines()
    num_results = int(request.form["num_results"])
    lang = request.form["language"]
    country = request.form["country"]

    all_results = {}
    for kw in keywords:
        urls = run_google_search(kw.strip(), lang=lang, region=country, num_results=num_results, advanced=False)
        all_results[kw] = urls

    return jsonify(all_results)

@app.route("/run_crawl", methods=["POST"])
def run_crawl():
    data = request.get_json()
    urls = data.get("urls", [])
    # On exécute votre fonction run_batch de manière asynchrone
    asyncio.run(run_batch(urls))
    return jsonify({"status": "finished", "crawled": len(urls)})

if __name__ == "__main__":
    app.run(debug=True)
