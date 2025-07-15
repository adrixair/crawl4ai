import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    # Configuration avec profil persistant Chromium
    browser_config = BrowserConfig(
        headless=False,
        verbose=True,
        use_managed_browser=True,
        browser_type="chromium",
        user_data_dir="/Users/adrien/.crawl4ai/profiles/Martin"
    )

    run_config = CrawlerRunConfig(
        word_count_threshold=10,
        excluded_tags=['form', 'header'],
        exclude_external_links=True,
        process_iframes=True,
        remove_overlay_elements=True,
        cache_mode=CacheMode.ENABLED
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://www.linkedin.com/company/sanofi/people/?keywords=Brazil",
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
        else:
            print(f"❌ Crawl failed: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())
