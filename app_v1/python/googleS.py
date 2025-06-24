#https://pypi.org/project/googlesearch-python/

from googlesearch import search

#def run_google_search(query, lang="fr", region="fr", num_results=10, advanced=False):
 #   results = search(query, unique=True, lang=lang, region=region, advanced=advanced, sleep_interval=5, num_results=num_results)
  #  return list(results)



def run_google_search(query_list, lang="fr", region="fr", num_results=10, advanced=False):
    """
    Prend une liste de requêtes (query_list) et retourne une liste unique d'URLs.
    """
    all_urls = []

    for query in query_list:
        print(f"🔍 Searching Google for: '{query}'")
        try:
            urls_for_query = search(query, unique=True, lang=lang, region=region, advanced=advanced, sleep_interval=5, num_results=num_results)
            all_urls.extend(urls_for_query)
        except Exception as e:
            print(f"❌ Error during search for query '{query}': {e}")

    # Supprimer les doublons tout en gardant l'ordre initial
    unique_urls = list(dict.fromkeys(all_urls))
    cleaned_urls = [url for url in unique_urls if url.startswith("http")]

    print(f"🌐 Total unique URLs found: {len(cleaned_urls)}")
    return cleaned_urls