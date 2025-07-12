
from urllib.parse import quote
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.filters import FilterChain, ContentTypeFilter
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

def build_people_url(base_handle: str, title_kw: str = "") -> str:
    """
    Construit l'URL de la page /people d'une entreprise LinkedIn avec un filtre optionnel.
    """
    base_url = f"https://www.linkedin.com{base_handle}people/"
    if title_kw.strip():
        return f"{base_url}?keywords={quote(title_kw)}"
    return base_url

async def main(url: str):
    """
    Scanne une seule page LinkedIn /people/:
    - clique sur 'Show more results' jusqu'à disparition du bouton
    - imprime le markdown généré ou le HTML brut
    """
    # Facilité pour futures évolutions
    filter_chain = FilterChain([ContentTypeFilter(allowed_types=["text/html"])])
    keyword_scorer = KeywordRelevanceScorer(keywords=["contato", "contact"], weight=0.7)

    config = CrawlerRunConfig(
        exclude_all_images=True,
        exclude_external_links=False,
        exclude_external_images=True,
        wait_for_images=True,
        scan_full_page=False,
        scroll_delay=0.5,
        # Exemple de deep crawl désactivé pour une page unique
        # deep_crawl_strategy=BestFirstCrawlingStrategy(
        #     max_depth=2,
        #     max_pages=10,
        #     include_external=False,
        #     filter_chain=filter_chain,
        #     url_scorer=keyword_scorer
        # ),
        cache_mode=CacheMode.BYPASS,
        scraping_strategy=LXMLWebScrapingStrategy(),
        stream=True,
        verbose=True,
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(
                threshold=0.45,
                threshold_type="fixed",
                min_word_threshold=0
            ),
            options={
                "citations": True,
                "ignore_links": True,
                "skip_internal_links": True,
                "ignore_images": True,
                "ignore_tables": True,
                "protect_links": True,
                "include_sup_sub": True
            }
        ),
        magic=True,
        simulate_user=True,
        override_navigator=True,
        click=[{
            "selector": ".artdeco-button--secondary",
            "delay": 1,
            "times": 20
        }],
        wait_for=".org-people-profile-card__card-spacing",
        delay_before_return_html=2
    )

    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        async for result in await crawler.arun(url, config=config):
            if not result.success:
                print("Crawl error:", result.error_message)
                return
            # Affiche le markdown si existant, sinon le HTML
            if result.markdown:
                print(result.markdown)
            else:
                print(result.html)

if __name__ == "__main__":
    # Exemple d'utilisation
    base = "/company/sanofi/"
    kw = "Brazil"  # laisse "" pour aucun filtre
    target_url = build_people_url(base, kw)
    asyncio.run(main(target_url))
