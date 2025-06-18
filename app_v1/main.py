import asyncio

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.filters import FilterChain, ContentTypeFilter
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

#Main Crawler Function
async def main(url):

    ### Create a sophisticated filter chain
    filter_chain = FilterChain([
        ContentTypeFilter(allowed_types=["text/html"])
    ])

    ### Create a relevance scorer
    keyword_scorer = KeywordRelevanceScorer(
        keywords=["contato","contact"],
        weight=0.7
    )

    ### Set up the configuration

    browser_cfg = BrowserConfig(headless=True)

    config = CrawlerRunConfig(
        exclude_all_images=True,
        exclude_external_links=False,
        exclude_external_images=True,
        deep_crawl_strategy=BestFirstCrawlingStrategy(
            max_depth=2,
            max_pages=10,
            include_external=False,
            filter_chain=filter_chain,
            url_scorer=keyword_scorer
        ),
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
                "citations": True,         # ajoute des citations numérotées
                #"body_width": 90,          # largeur de paragraphe
                "ignore_links": True,     # supprime les liens cliquables
                "skip_internal_links": True, # ignore les liens internes
                "ignore_images": True,     # supprime toutes les images
                "ignore_tables": True,     # supprime tables <table>
                "protect_links": True ,     # garde l’ancre brute sans http://
                "include_sup_sub": True 
            }
        ),
    )

    ### Execute the crawl
    results = []
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        async for result in await crawler.arun(url, config=config):
            if not result.success:
                print("Crawl error:", result.error_message)
                return
            if result.markdown:
                external_links = result.links.get("external", [])
                if external_links:
                    formatted_links = []
                    for item in external_links:
                        # item peut être soit un dict (cas Crawl4AI) soit déjà une chaîne
                        href = item.get("href") if isinstance(item, dict) else str(item)
                        # Nettoie les liens mailto pour ne garder que l’adresse e‑mail
                        if href.startswith("mailto:"):
                            href = href.replace("mailto:", "")
                        formatted_links.append(f"- {href}")
                    external_links_md = "\n\n# Liens externes trouvés\n" + "\n".join(formatted_links)
                else:
                    external_links_md = ""
                results.append(result.markdown + external_links_md)
    return "\n".join(results)
