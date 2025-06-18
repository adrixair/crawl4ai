import pandas as pd
import sys
import os
from pathlib import Path
from urllib.parse import urlparse
import asyncio
import json
import ast


sys.path.append(Path(__file__).parent.as_posix()) # Ajoute le répertoire parent au chemin de recherche
OUTPUT_DIR = Path(__file__).parent / "crawl_results" # Répertoire de sortie pour les résultats du crawl
OUTPUT_DIR.mkdir(exist_ok=True) # Crée le répertoire s'il n'existe pas

from main import main  # Importer la fonction main depuis le fichier main.py
from googleS import run_google_search  # importe la fonction de recherche Google
from gemini_markdown import gminimarkdown  # importe la fonction de recherche Gemini

query = "arquiteto sao paulo" # requête pour la recherche Google
urls = run_google_search(query, lang="fr", region="br", num_results=10, advanced=False) # liste des URLs à crawler
#urls = ["https://www.workally.com.br"]

prompt_template = """
Vous êtes un assistant spécialisé dans l'extraction de contacts et de réseaux sociaux à partir de contenu Markdown provenant d'un sites web.
Objectif : retourner un JSON structuré avec les champs suivants :
- website : URL principale (domaine racine) du site analysé.
- emails : liste des adresses email principales de contact trouvées.
- phone_numbers : liste des numéros de téléphone de contact.
- addresses : liste des adresses postales ou physiques identifiées.
- social_links : liste des URLs officielles du site pour ces plateformes ou services : LinkedIn, Instagram, Facebook, Twitter/X, YouTube, WhatsApp Web, API WhatsApp Business, et tout autre endpoint API officiel détecté (REST, GraphQL, etc.).

Contraintes :
- Uniquement les informations appartenant au site cible (pas de données de sites tiers).
- Éliminer les doublons dans chaque champ.
- Si le site contient des liens vers des API publiques (ex : WhatsApp API, GraphQL, etc.), incluez-les dans social_links.

Exemple de structure JSON attendue :

{
    "website": "https://www.exemple.com",
    "emails": ["contact@exemple.com", "info@exemple.com"],
    "phone_numbers": ["+33 1 23 45 67 89"],
    "addresse": ["123 Rue Exemple, Paris, France"],
    "social_links": [
        "https://www.linkedin.com/company/exemple",
        "https://www.instagram.com/exemple",
        "https://www.facebook.com/exemple",
        "https://twitter.com/exemple",
        "https://www.youtube.com/c/exemple",
        "https://api.whatsapp.com/send?phone=123456789"
    ]
}
"""

async def run_batch(urls: list[str]) -> None:

    gemini_results = []

    for url in urls:
        print(f"\n=== Crawl : {url} ===")
        markdownd = await main(url)
        out_path = OUTPUT_DIR / f"{urlparse(url).netloc.replace('www.', '')}.md"
        out_path.write_text(markdownd or "")

        gmini_result = gminimarkdown(prompt_template, url, markdownd)
        output_json_path = OUTPUT_DIR / f"{urlparse(url).netloc.replace('www.', '')}-gmini-result.json"
        output_json_path.parent.mkdir(parents=True, exist_ok=True)
        output_json_path.write_text(gmini_result or "")
        print(f"→ Résultat Gemini enregistré dans {output_json_path}")

        gemini_results.append(gmini_result)
      

    clean_results = []

    for result in gemini_results:
        try:
            # Remove markdown formatting like ```json ... ```
            cleaned = result.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[len("```json"):].strip()
            if cleaned.startswith("```"):
                cleaned = cleaned[len("```"):].strip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3].strip()

            json_obj = json.loads(cleaned)
            clean_results.append(json_obj)
        except Exception as e:
            print(f"Erreur de parsing sur un résultat Gemini : {e}")
            clean_results.append({"error": "Invalid JSON structure", "raw_result": result})

    final_output_path = OUTPUT_DIR / "gemini_results.json"
    final_output_path.write_text(json.dumps(clean_results, ensure_ascii=False, indent=2))
    print(f"→ Tous les résultats Gemini rassemblés proprement dans {final_output_path}")

    # Export to Excel
    df = pd.json_normalize(clean_results)
    excel_output_path = OUTPUT_DIR / "gemini_results.xlsx"
    df.to_excel(excel_output_path, index=False)
    print(f"→ Résultats Gemini exportés dans {excel_output_path}")

    # Open the Excel file automatically (for MacOS)
    os.system(f"open '{excel_output_path}'")
       

if __name__ == "__main__":
    asyncio.run(run_batch(urls))
