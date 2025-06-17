#https://pypi.org/project/googlesearch-python/

from googlesearch import search
def print_google_results(query: str, num: int = 100, *, unique: bool = True, lang: str = "en", region: str = None):
    """
    Lance une recherche Google et affiche chaque URL dans le terminal.

    :param query: chaîne de recherche
    :param num: nombre maximum de résultats à récupérer (10 par défaut, jusqu'à 100+)
    :param unique: True pour éliminer les doublons
    :param lang: code langue (ex. "fr", "en")
    :param region: code pays (ex. "us", "fr")
    """
    # search() renvoie un itérateur de chaînes (URLs) par défaut
    results = search(
        query,
        num_results=num,
        unique=unique,
        lang=lang,
        region=region,
    )

    for url in results:
        print(url)

if __name__ == "__main__":
    # Exemple : récupérer et afficher les 100 premiers résultats pour "architecture São Paulo"
    print_google_results("workally", num=10, lang="pt", region="br")