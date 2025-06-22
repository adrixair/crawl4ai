import sys
import os

# Ajouter le dossier ./python au sys.path (chemin relatif depuis app.py)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'python')))

from flask import Flask, render_template, request
from googleS import run_google_search

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


@app.route('/google_search', methods=['GET', 'POST'])
def google_search():
    url_list = []  # ✅ Initialisation de la liste d'URLs

    if request.method == 'POST':
        # ✅ Récupération des données POST
        keywords_raw = request.form.get('keywords', '')
        country = request.form.get('country', '')
        language = request.form.get('language', '')
        num_results = request.form.get('num_results', '3')
        message = "Form data saved successfully ✅"

        # ✅ Conversion du textarea keywords en liste
        query_list = [kw.strip() for kw in keywords_raw.splitlines() if kw.strip()]

        # ✅ Appel de ta fonction de recherche Google
        url_list = run_google_search(
            query_list=query_list,
            lang=language,
            region=country,
            num_results=int(num_results),
            advanced=False
        )

        # ✅ Console log pour vérifier
        print("🌐 Google Search completed. URL list:")
        for url in url_list:
            print(f"➡️ {url}")

        # ✅ Optionnel : Sauvegarde dans un fichier
        with open('search_logs.txt', 'a', encoding='utf-8') as f:
            f.write(f"Keywords:\n{keywords_raw}\nCountry: {country}\nLanguage: {language}\nResults: {num_results}\n")
            f.write(f"URLs Found:\n" + "\n".join(url_list) + "\n" + "-"*40 + "\n")

    # ✅ Toujours retourner le template avec les valeurs du formulaire et la liste d'URLs (même vide)
    return render_template('GoogleDeepSearchS.html',
                           keywords_raw=keywords_raw,
                           country=country,
                           language=language,
                           num_results=num_results,
                           message=message,
                           url_list=url_list)


if __name__ == "__main__":
    app.run(debug=True)