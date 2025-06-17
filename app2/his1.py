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

# Data model for LLM schema extraction
class CompanyInfo(BaseModel):
    company_name: str = Field(..., description="Nom de l'entreprise")
    social_links: List[str] = Field(..., description="URL des réseaux sociaux (LinkedIn, Instagram, Facebook, etc.)")
    email_addresses: List[str] = Field(..., description="Adresse(s) e-mail détectée(s)")
    address: str = Field(..., description="Adresse physique de l'entreprise")
    website: str = Field(..., description="Lien du site web de l'entreprise")

# Social Media Domains
SOCIAL_DOMAINS = (
    "facebook.com", "instagram.com", "linkedin.com",
    "twitter.com", "x.com", "youtube.com", "whatsapp.com"
)

def is_social(url: str) -> bool:
    return any(dom in url for dom in SOCIAL_DOMAINS)



#Main Crawler Function
async def main():

    ### Define the LLM extraction strategy
    llm_strategy = LLMExtractionStrategy(
            llm_config = LLMConfig(provider="gemini/gemini-2.0-flash", api_token="AIzaSyAl_bK7SZR2-TZXHiJi8X7v-6cNnaMev-Y"),
            schema=CompanyInfo.model_json_schema(),
            extraction_type="schema",
            instruction=(
                "À partir du markdown ci-dessous, extrait les informations suivantes et "
                "retourne-les sous forme de JSON conforme au schéma CompanyInfo : "
                "nom de l'entreprise, liste des liens de réseaux sociaux (LinkedIn, Instagram, Facebook, etc.), "
                "liste des adresses e-mail, adresse physique, et lien du site web."
            ),
            chunk_token_threshold=1000,
            overlap_rate=0.0,
            apply_chunking=True,
            input_format="markdown",   # or "html", "fit_markdown"
            extra_args={"temperature": 0.0, "max_tokens": 800}
        )
    
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
        #extraction_strategy=llm_strategy, #llm
        stream=True,
        verbose=True,

        markdown_generator=DefaultMarkdownGenerator(
        content_filter=
        PruningContentFilter(
            threshold=0.45,
            threshold_type="fixed",
            min_word_threshold=0
        ),
        
        options={
            "citations": True,         # ajoute des citations numérotées
            "body_width": 90,          # largeur de paragraphe
            "ignore_links": False,      # supprime les liens cliquables
            "ignore_images": True,     # supprime toutes les images
            "ignore_tables": True,     # supprime tables <table>
            "protect_links": True      # garde l’ancre brute sans http://
        }
        ),
    )

    ### Execute the crawl
    results = []
    social_links = []

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        async for result in await crawler.arun("https://www.workally.com.br", config=config):
            results.append(result)
            # Collect social media URLs
            for link in result.links.get("internal", []) + result.links.get("external", []):
                href = (link.get("href") or "").strip()
                if is_social(href):
                    social_links.append(href)

    # Combine all page markdowns and append social links
    combined_markdown = "\n\n".join([res.markdown for res in results if res.markdown])
    if social_links:
        combined_markdown += "\n\n" + "\n".join(sorted(set(social_links)))

    print("\n=== combined_markdown ===")
    print(combined_markdown)
    print("\n=== combined_markdown ===")

    curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=GEMINI_API_KEY" \
        -H 'Content-Type: application/json' \
        -X POST \
        -d '{
            "contents": [
            {
                "parts": [
                {
                    "text": "Explain how AI works in a few words"
                }
                ]
            }
            ]
    }'

    print("\n=== Combined LLM extraction result ===")
    print(combined_result.extracted_content)


    # ─── Display combined extraction and usage ───
    if combined_result.extracted_content:
        combined_data = json.loads(combined_result.extracted_content)
        print("Combined extracted items:", combined_data)
    else:
        print("No extracted content returned by LLM.")

    # Display LLM usage stats
    llm_strategy.show_usage()
    

if __name__ == "__main__":
    asyncio.run(main())
    



