import os
import json
import csv
import google.generativeai as genai
import time
from google.genai.errors import ServerError
import datetime
import copy
import argparse

# ===== Debug switches =====
DEBUG_VERBOSE = True          # messages de progression
DEBUG_GEMINI_RESPONSE = False  # réponses brutes et JSON nettoyé
# ==========================

# --- Gemini API key rotation ---
API_KEYS = [
    "AIzaSyACw763HszxKbP-PtEgf8GElg6BctlwmfE",  # Adrien
]

_current_key_index = 0

def next_key():
    """Advance to the next API key in a circular fashion."""
    global _current_key_index
    _current_key_index = (_current_key_index + 1) % len(API_KEYS)
    return API_KEYS[_current_key_index]

def strip_json_fences(text):
    """Remove surrounding Markdown JSON code fences if present."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    if text.endswith("```"):
        text = text[:-len("```")].strip()
    return text

# Dossier contenant les fichiers JSON (modifie ce chemin si besoin)
INPUT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../output"))

# Colonnes du fichier de sortie
fieldnames = [
    "company_name", "company_website", "contact_email", "contact_phone",
    "contact_place_street", "contact_place_city", "contact_place_state", "contact_place_country",
    "contact_place_postal_code", "social_links"
]

def parse_address(address):
    """
    Extrait les champs d'adresse depuis:
      • un dict (format attendu) ou
      • une liste de dicts (Gemini peut renvoyer plusieurs adresses).
    Dans le cas d'une liste, on prend la première entrée.
    Si des champs sont manquants, on renvoie des chaînes vides.
    """
    if isinstance(address, list) and address:
        address = address[0]  # première adresse si plusieurs
    if not isinstance(address, dict):
        address = {}
    return (
        address.get("street", ""),
        address.get("city", ""),
        address.get("state", ""),
        address.get("country", ""),
        address.get("postal_code", "")
    )

def load_and_extract(filepath):
    if DEBUG_VERBOSE:
        print(f"Debug: loading and extracting {filepath}")
    with open(filepath, encoding="utf-8") as f:
        raw = strip_json_fences(f.read())
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"Debug: JSON decode error in {filepath}: {e}")
            raise

    # Préserver les données originales avant enrichissement
    original_data = copy.deepcopy(data)

    prompt = (
        "Voici des données extraites depuis un site web d’entreprise, brutes (tu peux effectuer une recherche Web rapide si nécessaire) :\n\n"
        f"{json.dumps(original_data, ensure_ascii=False, indent=2)}\n\n"
        "Merci d’analyser ces informations et de me retourner un JSON enrichi, "
        "avec les champs suivants :\n"
        "- website\n"
        "- contact_email (une liste de toutes les adresses email trouvées, au format standard)\n"
        "- contact_phone (une liste de tous les numéros de téléphone trouvés, au format E.164, sans espaces ni séparateurs)\n"
        "- address : un objet {street, city, state, country, postal_code} complet, utilisant les informations disponibles pour combler les éventuels manques.\n"
        "- social_links (une liste de liens sociaux, sans barres verticales comme séparateurs)\n\n"
        "Donne-moi uniquement un objet JSON bien formaté, sans autre texte."
    )

    retry_delay = 5
    enriched = None
    while True:
        try:
            genai.configure(api_key=API_KEYS[_current_key_index])
            # --- Appel simple sans outil Google Search ---
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(contents=prompt)
            if DEBUG_GEMINI_RESPONSE:
                print(f"Debug: Gemini response text for {filepath}: {response.text}")
            raw_response = strip_json_fences(response.text)
            if DEBUG_GEMINI_RESPONSE:
                print(f"Debug: stripped fences, raw response text: {raw_response}")
            enriched = json.loads(raw_response)
            if DEBUG_GEMINI_RESPONSE:
                print(f"Debug: enriched JSON for {filepath}: {enriched}")
            # Success: exit loop
            break
        except Exception as e:
            msg = str(e)
            # Always rotate key and retry
            new_key = next_key()
            if DEBUG_VERBOSE:
                print(f"Debug: rotated API key to index {_current_key_index} ({new_key}) due to error: {msg}")
            if DEBUG_VERBOSE:
                print(f"Retrying {filepath} in {retry_delay} seconds...")
            time.sleep(retry_delay)
            # continue loop to retry indefinitely
            continue
    # End loop

    website = enriched.get("website", "")
    emails = enriched.get("contact_email", "")
    if isinstance(emails, list):
        emails = " | ".join(emails)

    phones = enriched.get("contact_phone", "")
    if isinstance(phones, list):
        phones = " | ".join(phones)

    address_dict = enriched.get("address", "")
    social_links = enriched.get("social_links", [])
    if isinstance(social_links, dict):
        social_links = [str(social_links)]
    if isinstance(social_links, list):
        social_links = " | ".join(social_links)

    street, city, state, country, postal_code = parse_address(address_dict)

    return {
        "company_name": website.replace("https://", "").replace("www.", "").split('/')[0],
        "company_website": website,
        "contact_email": emails,
        "contact_phone": phones,
        "contact_place_street": street,
        "contact_place_city": city,
        "contact_place_state": state,
        "contact_place_country": country,
        "contact_place_postal_code": postal_code,
        "social_links": social_links
    }

def batch_process(limit=None):
    json_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".json") and not f.endswith(".md.json")]
    if limit is not None:
        json_files = json_files[:limit]
    total_files = len(json_files)
    rows = []
    for idx, filename in enumerate(json_files, start=1):
        filepath = os.path.join(INPUT_FOLDER, filename)
        if DEBUG_VERBOSE:
            print(f"Debug: processing candidate JSON file: {filename} ({idx}/{total_files})")
        # skip empty files
        if os.path.getsize(filepath) == 0:
            if DEBUG_VERBOSE:
                print(f"Debug: skipping empty file {filename}")
            continue
        try:
            row = load_and_extract(filepath)
            if row:
                rows.append(row)
                if DEBUG_VERBOSE:
                    print(f"Debug: successfully processed {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    if not rows:
        print("Aucun fichier JSON valide traité.")
        return

    # Générer un nom de fichier CSV unique avec timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"./apollo_formatted_output_{timestamp}.csv"

    with open(output_csv, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Export Apollo terminé : {output_csv} avec {len(rows)} lignes.")
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Gemini JSON outputs into a CSV.")
    parser.add_argument("--limit", type=int, default=3,
                        help="Maximum number of JSON files to process (default: all).")
    args = parser.parse_args()
    batch_process(limit=args.limit)