import os
import json
import csv
import google.generativeai as genai
import time
from google.genai.errors import ServerError
import datetime
import copy
import argparse
import googlemaps

# --- Google Maps API for geocoding ---
import googlemaps
# Clé API Google Maps pour géocodage : remplace par ta propre clé
MAPS_API_KEY = "AIzaSyC7c1m_Jyz3uw6lbIQUNuH3e6o0NKc_8hk"
# Client Google Maps
gmaps_client = googlemaps.Client(key=MAPS_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")
# --- Gemini API key rotation ---
API_KEYS = [
    "AIzaSyABPqpjksAXPTWLpOEGNTKGP8ApGRYk090",  # Adrien
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

# --- Helpers for geocoding ---
def parse_address_components(components):
    """Parse Google Maps address_components into street, city, state, country, postal_code."""
    street = city = state = country = postal_code = ""
    for comp in components:
        types = comp.get("types", [])
        if "street_number" in types:
            street = comp.get("long_name", "") + (" " + street if street else "")
        if "route" in types:
            street = (street + " " + comp.get("long_name")) if street else comp.get("long_name")
        if "locality" in types:
            city = comp.get("long_name", "")
        if "administrative_area_level_1" in types:
            state = comp.get("short_name", "")
        if "country" in types:
            country = comp.get("long_name", "")
        if "postal_code" in types:
            postal_code = comp.get("long_name", "")
    return street, city, state, country, postal_code

def geocode_company(company_name, website_url):
    """Use Google Maps to geocode a company by name and website."""
    try:
        # Recherche textuelle combinant nom et site
        query = f"{company_name} site:{website_url}"
        # Lance une recherche de lieu
        places = gmaps_client.places(query=query)
        results = places.get("results", [])
        if results:
            place_id = results[0].get("place_id")
            details = gmaps_client.place(place_id=place_id, fields=["address_components"])
            comps = details.get("result", {}).get("address_components", [])
            return parse_address_components(comps)
    except Exception as e:
        print(f"Debug: erreur geocode_company pour {company_name}: {e}")
    return "", "", "", "", ""

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
    Extrait les champs d'adresse d'un dict retourné par Gemini :
    address est un dict contenant keys street, city, state, country, postal_code.
    """
    return (
        address.get("street", ""),
        address.get("city", ""),
        address.get("state", ""),
        address.get("country", ""),
        address.get("postal_code", "")
    )

def load_and_extract(filepath):
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
    # Géocodage Google Maps sans écraser les données existantes
    addr = data.get("address", {})
    geo_street = geo_city = geo_state = geo_country = geo_postal = ""
    if not addr.get("street") or not addr.get("city") or not addr.get("postal_code"):
        company_name = data.get("website", filepath).replace("https://", "").replace("www.", "").split("/")[0]
        geo_street, geo_city, geo_state, geo_country, geo_postal = geocode_company(company_name, data.get("website", ""))
    geo_address = {
        "street": geo_street,
        "city": geo_city,
        "state": geo_state,
        "country": geo_country,
        "postal_code": geo_postal
    }
    # Inclure l'adresse géocodée dans les données d'entrée
    data["geo_address"] = geo_address

    prompt = (
        "Voici des données extraites depuis un site web d’entreprise, brutes :\n\n"
        f"{json.dumps(original_data, ensure_ascii=False, indent=2)}\n\n"
        "Voici également les données géolocalisées obtenues via Google Maps, sans écraser les données originales :\n\n"
        f"{json.dumps(data['geo_address'], ensure_ascii=False, indent=2)}\n\n"
        "Merci d’analyser ces deux sources d’informations et de me retourner un JSON enrichi, "
        "avec les champs suivants :\n"
        "- website\n"
        "- contact_email (une liste de toutes les adresses email trouvées, au format standard)\n"
        "- contact_phone (une liste de tous les numéros de téléphone trouvés, au format E.164, sans espaces ni séparateurs)\n"
        "- address : un objet {street, city, state, country, postal_code} complet, utilisant les informations originales et géocodées pour combler les manques.\n"
        "- social_links (une liste de liens sociaux, sans barres verticales comme séparateurs)\n\n"
        "Donne-moi uniquement un objet JSON bien formaté, sans autre texte."
    )

    retry_delay = 5
    enriched = None
    while True:
        try:
            genai.configure(api_key=API_KEYS[_current_key_index])
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(
                contents=prompt
            )
            print(f"Debug: Gemini response text for {filepath}: {response.text}")
            raw_response = strip_json_fences(response.text)
            print(f"Debug: stripped fences, raw response text: {raw_response}")
            enriched = json.loads(raw_response)
            print(f"Debug: enriched JSON for {filepath}: {enriched}")
            # Success: exit loop
            break
        except Exception as e:
            msg = str(e)
            # Always rotate key and retry
            new_key = next_key()
            print(f"Debug: rotated API key to index {_current_key_index} ({new_key}) due to error: {msg}")
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
        print(f"Debug: processing candidate JSON file: {filename} ({idx}/{total_files})")
        # skip empty files
        if os.path.getsize(filepath) == 0:
            print(f"Debug: skipping empty file {filename}")
            continue
        try:
            row = load_and_extract(filepath)
            if row:
                rows.append(row)
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
    parser.add_argument("--limit", type=int, default=None,
                        help="Maximum number of JSON files to process (default: all).")
    args = parser.parse_args()
    batch_process(limit=args.limit)