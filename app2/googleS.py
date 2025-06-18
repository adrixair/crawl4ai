#https://pypi.org/project/googlesearch-python/

from googlesearch import search

def run_google_search(query, lang="fr", region="fr", num_results=10, advanced=False):
    results = search(query, unique=True, lang=lang, region=region, advanced=advanced, sleep_interval=5, num_results=num_results)
    return list(results)

def main():
    query = "Google"
    urls = run_google_search(query, lang="fr", region="fr", num_results=10, advanced=False)
    print(urls)

if __name__ == "__main__":
    main()