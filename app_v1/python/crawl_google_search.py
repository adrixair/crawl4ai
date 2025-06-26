import pandas as pd
from pathlib import Path
from urllib.parse import urlparse
import asyncio
import json
import traceback

import time
from google import genai
from google.genai.errors import ClientError, ServerError

# --- Gemini API key rotation ---
API_KEYS = [
    "AIzaSyDPKtNEHkYLTxyro_sChX4DkaO3c4U4l9o",
    "AIzaSyAl_bK7SZR2-TZXHiJi8X7v-6cNnaMev-Y",
    "AIzaSyABPqpjksAXPTWLpOEGNTKGP8ApGRYk090",
    "AIzaSyBKym2yV21Pe0XOw_HziG02r8AN0uXjFLY",
    "AIzaSyAjRWfrypGrgLZqLaXh97z5s8Ryiht6rgY",
    "AIzaSyBrhIctdOK8mRwTUIp3OE05NuaBtD6cgVI",
]
_current_key_index = 0

def next_key():
    global _current_key_index
    _current_key_index = (_current_key_index + 1) % len(API_KEYS)
    return API_KEYS[_current_key_index]

def get_client():
    """Return a genai client using the current API key."""
    return genai.Client(api_key=API_KEYS[_current_key_index])


from main import main  # Importer la fonction main depuis le fichier main.py
from googleS import run_google_search  # importe la fonction de recherche Google
from gemini_markdown import gminimarkdown  # importe la fonction de recherche Gemini


# Définir OUTPUT_DIR et le chemin du fichier texte contenant les URLs
OUTPUT_DIR = Path(__file__).parent / ".." / "output"
text_file_path = OUTPUT_DIR / "google_urls_result_SP.txt"

# --- Load no_results_sites.txt and skip URLs listed there ---
no_results_file = OUTPUT_DIR / "no_results_sites.txt"
# Ensure the file exists
if not no_results_file.exists():
    no_results_file.touch()
# Load URLs to skip
with no_results_file.open("r", encoding="utf-8") as f:
    no_results_sites = {line.strip() for line in f if line.strip()}

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
- Si aucune information n’est disponible (aucun email, téléphone, adresse ou lien social), retourner quand même un JSON vide avec les bons champs et des listes vides, comme dans l’exemple.

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

async def process_site(url: str) -> None:
    """Crawl a single URL, save its Markdown and Gemini JSON, nothing else."""
    print(f"\n=== Crawl : {url} ===")

    # Skip banned domains
    banned_domains = (
        "instagram.com",
        "twitter.com",
        "facebook.com",
        "reddit.com",
        "youtube.com",
        "youtu.be",
        "tripadvisor.com",
        "tripadvisor.com.br",
        "tripadvisor.fr",
        "airbnb.com",
        "airbnb.com.br",
        "airbnb.fr",
        "booking.com",
        "booking.com.br",
        "vrbo.com",
        "vrbo.com.br",
        "leboncoin.fr",
        "seloger.com",
        "pap.fr",
        "logic-immo.com",
    )
    netloc = urlparse(url).netloc.lower().replace("www.", "")
    if any(netloc.endswith(dom) for dom in banned_domains):
        print(f"⚠️ Domaine banni détecté pour {url}, skipping.")
        return

    out_path = OUTPUT_DIR / f"{urlparse(url).netloc.replace('www.', '')}.md"
    output_json_path = OUTPUT_DIR / f"{urlparse(url).netloc.replace('www.', '')}-gmini-result.json"

    # Skip if both files already exist
    if out_path.exists() and output_json_path.exists():
        print(f"✅ Fichiers déjà existants pour {url}, skipping.")
        return

    try:
        markdown_content = await main(url)
        out_path.write_text(markdown_content or "")

        if markdown_content:
            output_json_path.parent.mkdir(parents=True, exist_ok=True)
            retry_delay = 5
            # Rotate through keys until one succeeds
            for attempt in range(len(API_KEYS)):
                try:
                    # Ensure gminimarkdown uses the current key
                    gminimarkdown.client = get_client()
                    gmini_result = gminimarkdown(prompt_template, url, markdown_content)
                    output_json_path.write_text(gmini_result or "")
                    print(f"→ Résultat Gemini enregistré dans {output_json_path}")
                    break
                except (ClientError, ServerError) as e:
                    print(f"Debug: Gemini error ({e}), rotating key and retrying in {retry_delay}s.")
                    traceback.print_exc()
                    next_key()
                    time.sleep(retry_delay)
                    continue
            else:
                print(f"❌ Tous les clés API épuisées pour {url}.")
        else:
            print(f"❌ Aucun contenu Markdown récupéré pour {url}.")
            error_result = json.dumps(
                {"website": url, "error": "No Markdown content from crawl."},
                ensure_ascii=False,
                indent=2,
            )
            output_json_path.write_text(error_result)

    except Exception as e:
        print(f"❌ Erreur lors du traitement de {url} : {e}")

if __name__ == "__main__":
    if text_file_path.exists():
        with open(text_file_path, "r") as file:
            urls = [line.strip() for line in file if line.strip()]
        # Skip URLs listed in no_results_sites
        urls = [url for url in urls if url not in no_results_sites]
        for url in urls:
            try:
                asyncio.run(process_site(url))
            except Exception as e:
                print(f"❌ Erreur générale pour {url} : {e}")
    else:
        print(f"❌ Fichier texte non trouvé : {text_file_path}")
