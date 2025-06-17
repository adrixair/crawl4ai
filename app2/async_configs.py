import requests

# Remplace directement par ta clé (à garder secrète si tu partages le code !)
API_KEY = "AIzaSyB-6LLZqKdMTd6c55tjyw4SugoC9v1xYas"
CX      = "TON_CX_ICI"  # identifiant du moteur personnalisé

def google_search(query: str, num: int = 100):
    """
    Récupère jusqu’à `num` résultats pour la recherche `query`.
    Google ne renvoie que 10 résultats par appel, on pagine.
    """
    results = []
    for start in range(1, num, 10):
        params = {
            "key": API_KEY,
            "cx": CX,
            "q": query,
            "start": start
        }
        resp = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
        data = resp.json()
        for item in data.get("items", []):
            results.append({
                "title":   item.get("title"),
                "link":    item.get("link"),
                "snippet": item.get("snippet")
            })
        if len(data.get("items", [])) < 10:
            break
    return results

if __name__ == "__main__":
    query = "architecture Sao Paulo"
    hits = google_search(query, num=100)
    print(f"Récupéré {len(hits)} résultats :\n")
    for i, h in enumerate(hits, 1):
        print(f"{i:02d}. {h['title']}")
        print(f"    Lien   : {h['link']}")
        print(f"    Snippet: {h['snippet']}\n")