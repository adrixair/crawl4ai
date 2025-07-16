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
        wait_for_images=True,             # Wait for images to fully load
        scan_full_page=True,              # Force full-page scrolling for lazy loads
        scroll_delay=0.5,                   # Delay between scroll steps

        deep_crawl_strategy=BestFirstCrawlingStrategy(
            max_depth=2,
            max_pages=30,
            include_external=False,
            filter_chain=filter_chain,
            url_scorer=keyword_scorer
        ),
        cache_mode=CacheMode.ENABLED,
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
        magic=True,
        simulate_user=True,
        override_navigator=True,
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


    # Clean up browser contexts and cache after each crawl
    import shutil
    import os
    try:
        # Clear any Playwright browser storage/cache folders if they exist
        playwright_cache_path = os.path.expanduser("~/.cache/ms-playwright")
        if os.path.exists(playwright_cache_path):
            shutil.rmtree(playwright_cache_path)
            print(f"✅ Playwright cache folder cleared: {playwright_cache_path}")
    except Exception as cleanup_error:
        print(f"⚠️ Error while clearing Playwright cache: {cleanup_error}")
    # Clean up crawl4ai internal cache if it exists
    try:
        crawl4ai_cache_path = os.path.expanduser("~/.cache/crawl4ai")
        if os.path.exists(crawl4ai_cache_path):
            shutil.rmtree(crawl4ai_cache_path)
            print(f"✅ Crawl4AI cache folder cleared: {crawl4ai_cache_path}")
    except Exception as cleanup_error:
        print(f"⚠️ Error while clearing Crawl4AI cache: {cleanup_error}")
        
    return "\n".join(results)
