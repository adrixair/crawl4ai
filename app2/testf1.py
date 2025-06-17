import os
import asyncio
import json
import re
import time
from typing import List, Dict

from pydantic import BaseModel, Field
from bs4 import BeautifulSoup

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMConfig,
)

from crawl4ai.content_filter_strategy import PruningContentFilter, LLMContentFilter
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.filters import FilterChain, DomainFilter, URLPatternFilter, ContentTypeFilter
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy, LLMExtractionStrategy
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

#Main Crawler Function
async def main():

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
        deep_crawl_strategy=BestFirstCrawlingStrategy(
            max_depth=2,
            max_pages=50,
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
                "body_width": 90,          # largeur de paragraphe
                "ignore_links": False,     # supprime les liens cliquables
                "skip_internal_links": True, # ignore les liens internes
                "ignore_images": True,     # supprime toutes les images
                "ignore_tables": True,     # supprime tables <table>
                "protect_links": True      # garde l’ancre brute sans http://
            }
        ),
    )

    ### Execute the crawl
    results = []

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        async for result in await crawler.arun("https://www.workally.com.br", config=config):
            results.append(result)
        print(results)

    # Combine all page markdowns
    combined_markdown = "\n\n".join([res.markdown for res in results if res.markdown])

if __name__ == "__main__":
    asyncio.run(main())



