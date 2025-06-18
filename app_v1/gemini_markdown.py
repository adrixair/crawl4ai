from google import genai
import time
from google.genai.errors import ServerError

def gminimarkdown(prompt_template: str, url: str, markdown_content: str) -> str:
    client = genai.Client(api_key="AIzaSyAl_bK7SZR2-TZXHiJi8X7v-6cNnaMev-Y")
    full_prompt = prompt_template + "\n\nURL de recherche:\n" + url + "\n\n" + markdown_content

    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=full_prompt
            )
            return response.text
        except ServerError as e:
            if "503" in str(e) and attempt < max_retries:
                print(f"Serveur Gemini surchargé (503). Tentative {attempt}/{max_retries}. Nouvelle tentative dans {retry_delay} secondes...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print(f"Erreur Gemini non récupérable ou nombre de tentatives dépassé : {e}")
                return f"Erreur Gemini : {str(e)}"
