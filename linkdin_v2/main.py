import asyncio
import os
from urllib.parse import urlparse, parse_qs
import re
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.deep_crawling.filters import FilterChain, ContentTypeFilter
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy

# Helper function to slugify URL into directory-friendly string
def slugify_url(url):
    parsed = urlparse(url)
    # Expect path like /company/{name}/people
    parts = parsed.path.strip('/').split('/')
    company = parts[1] if len(parts) > 1 else parts[0]
    # Extract the 'keywords' parameter
    qs = parse_qs(parsed.query)
    keyword = qs.get('keywords', [''])[0]
    slug = f"{company}_{keyword}"
    # Sanitize and lowercase
    slug = re.sub(r'[^a-zA-Z0-9_]+', '_', slug)
    return slug.lower()

async def main():
    browser_config = BrowserConfig(
        headless=False,
        verbose=True,
        use_managed_browser=True,
        browser_type="chromium",
        user_data_dir="/Users/adrien/.crawl4ai/profiles/Martin"
    )

    # Create a sophisticated filter chain
    filter_chain = FilterChain([
        ContentTypeFilter(allowed_types=["text/html"])
    ])

    run_config = CrawlerRunConfig(
        excluded_tags=['form', 'header', 'script', 'style'],
        process_iframes=True,
        remove_overlay_elements=True,
        cache_mode=CacheMode.ENABLED,
        scan_full_page=True,
        scroll_delay=0.5,
        scraping_strategy=LXMLWebScrapingStrategy(),
        stream=True,
        verbose=True,
        markdown_generator=DefaultMarkdownGenerator(content_source="cleaned_html", content_filter=PruningContentFilter(
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
        override_navigator=True
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        url = "https://www.linkedin.com/company/sanofi/people/?keywords=Brazil"
        result = await crawler.arun(
            url=url,
            config=run_config
        )

        if result.success:
            print("=== MARKDOWN RESULT ===")
            print(result.markdown)

            if result.media.get("images"):
                for image in result.media["images"]:
                    print(f"[IMG] {image.get('src')}")

            if result.links.get("internal"):
                for link in result.links["internal"]:
                    print(f"[INTERNAL LINK] {link.get('href')}")

            # Build slug and output directory based on URL
            slug = slugify_url(url)
            output_dir = os.path.join("output", slug)
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
            output_file = os.path.join(output_dir, f"{slug}.md")
            # Replace existing file if present
            if os.path.exists(output_file):
                os.remove(output_file)
            # Write markdown to file
            with open(output_file, "w", encoding="utf-8") as md_file:
                md_file.write(result.markdown)
            print(f"✅ Markdown saved to {output_file}")
        else:
            print(f"❌ Crawl failed: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())
