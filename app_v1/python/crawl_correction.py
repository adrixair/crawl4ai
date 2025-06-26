import pandas as pd
from pathlib import Path
from urllib.parse import urlparse
import asyncio

import json
import time

import time
import traceback
from google import genai
from google.genai.errors import ClientError, ServerError

# --- Gemini API key rotation ---
API_KEYS = [
    "AIzaSyDPKtNEHkYLTxyro_sChX4DkaO3c4U4l9o", #ezer
    "AIzaSyBvMWoY-AZLUlTt8LCl5j1LWnW_o-Cqvws", #contato
    "AIzaSyDl7WFqRKh5X7UHgFlXH-Y_HdhrSwEj-bM", #Adrien
    "AIzaSyBDboCr6mYKJ0GpKckUdbuBPn4mSN3oFLk",


]
_current_key_index = 0

def next_key():
    global _current_key_index
    _current_key_index = (_current_key_index + 1) % len(API_KEYS)
    return API_KEYS[_current_key_index]

def get_client():
    return genai.Client(api_key=API_KEYS[_current_key_index])


from main import main  # Importer la fonction main depuis le fichier main.py
from gemini_markdown import gminimarkdown  # importe la fonction de recherche Gemini


OUTPUT_DIR = Path(__file__).parent.parent / "output"

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

    out_path = OUTPUT_DIR / f"{urlparse(url).netloc.replace('www.', '')}.md"
    output_json_path = OUTPUT_DIR / f"{urlparse(url).netloc.replace('www.', '')}-gmini-result.json"

    # Skip social media links and remove any existing files
    banned_domains = (
        "instagram.com",
        "twitter.com",
        "facebook.com",
        "reddit.com",
        "youtube.com",
        "youtu.be",
        "tripadvisor.com",
        "airbnb.com",
        "booking.com",
        "vrbo.com",
        "tripadvisor.com.br",
        "amazon.com.br",
        "airbnb.com.br",
        "booking.com.br",
        "vrbo.com.br",
        "tripadvisor.fr",
        "airbnb.fr",
        "leboncoin.fr",
        "seloger.com",
        "pap.fr",
        "logic-immo.com",
    )
    netloc = urlparse(url).netloc.lower().replace("www.", "")
    if any(netloc.endswith(dom) for dom in banned_domains):
        if out_path.exists():
            out_path.unlink()
        if output_json_path.exists():
            output_json_path.unlink()
        print(f"⚠️ {url} est un lien de médias sociaux, suppression des fichiers et skipping.")
        return

    # Vérifier si le markdown existant est suffisamment long (>=500 car.) et le JSON existe
    if out_path.exists():
        existing_md = out_path.read_text() or ""
        if len(existing_md) >= 500 and output_json_path.exists():
            no_results_file = OUTPUT_DIR / "no_results_sites.txt"
            if no_results_file.exists():
                lines = no_results_file.read_text().splitlines()
                if url in lines:
                    lines.remove(url)
                    no_results_file.write_text("\n".join(lines))
            print(f"✅ Fichiers valides déjà existants pour {url}, skipping.")
            return
        # sinon, supprimer markdown trop court ou JSON manquant pour nouvelle tentative
        print(f"⚠️ Markdown existant trop court (<500 car.) ou JSON manquant pour {url}, suppression pour nouvelle tentative.")
        out_path.unlink()
        if output_json_path.exists():
            output_json_path.unlink()

    try:
        markdown_content = await main(url)
        out_path.write_text(markdown_content or "")

        # Vérifier la longueur du Markdown
        length = len(markdown_content or "")
        if length < 500:
            print(f"⚠️ Markdown trop court ({length} caractères) pour {url}, suppression et ajout aux non-traités.")
            if out_path.exists():
                out_path.unlink()
            if output_json_path.exists():
                output_json_path.unlink()
            no_results_file = OUTPUT_DIR / "no_results_sites.txt"
            with open(no_results_file, "a", encoding="utf-8") as f:
                f.write(url + "\n")
            return

        # Générer le JSON via Gemini avec rotation des clés
        output_json_path.parent.mkdir(parents=True, exist_ok=True)
        retry_delay = 5
        for attempt in range(len(API_KEYS)):
            try:
                gmini_result = gminimarkdown(prompt_template, url, markdown_content)
                output_json_path.write_text(gmini_result or "")
                print(f"→ Markdown enregistré dans {out_path}")
                print(f"→ Résultat Gemini enregistré dans {output_json_path}")
                no_results_file = OUTPUT_DIR / "no_results_sites.txt"
                if no_results_file.exists():
                    lines = no_results_file.read_text().splitlines()
                    if url in lines:
                        lines.remove(url)
                        no_results_file.write_text("\n".join(lines))
                break
            except ClientError as ce:
                print("Debug: ClientError encountered, full traceback:")
                traceback.print_exc()
                print(f"⚠️  Clé utilisée lors de l’erreur : {API_KEYS[_current_key_index]}")
                next_key()  # avance à la clé suivante
                print(f"Debug: quota or client error ({ce}), clé changée à index {_current_key_index}. Nouvelle tentative dans {retry_delay}s.")
                time.sleep(retry_delay)
                continue
            except ServerError as se:
                print("Debug: ServerError encountered, full traceback:")
                traceback.print_exc()
                print(f"⚠️  Clé utilisée lors de l’erreur : {API_KEYS[_current_key_index]}")
                next_key()  # avance à la clé suivante
                print(f"Debug: serveur surchargé ou quota épuisé ({se}), clé changée à index {_current_key_index}. Nouvelle tentative dans {retry_delay}s.")
                time.sleep(retry_delay)
                continue

    except Exception as e:
        print(f"❌ Erreur lors du traitement de {url} : {e}")

if __name__ == "__main__":
    # Dédupliquer les URLs dans no_results_sites.txt si le fichier existe
    no_results_file = OUTPUT_DIR / "no_results_sites.txt"
    if no_results_file.exists():
        lines = no_results_file.read_text().splitlines()
        unique_lines = sorted(set(line for line in lines if line.strip()))
        no_results_file.write_text("\n".join(unique_lines))

    # Process all Markdown files in the output directory
    md_files = sorted((OUTPUT_DIR).glob("*.md"))
    total = len(md_files)
    for idx, md_path in enumerate(md_files, start=1):
        url = md_path.stem if md_path.stem.startswith("http") else "https://" + md_path.stem
        remaining = total - idx
        print(f"\n>>> ({idx}/{total}) Processing URL: {url} | Remaining: {remaining}")
        try:
            asyncio.run(process_site(url))
        except Exception as e:
            print(f"❌ Erreur générale pour {url} : {e}")
