import asyncio
import os
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import CrawlerRunConfig, CacheMode
from pathlib import Path

async def convert_file_to_markdown(input_file, output_file):
    try:
        # Lire directement le contenu brut (HTML inclus dans PHP, HTML, etc.)
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()

        raw_url = f"raw:{html_content}"

        config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=raw_url, config=config)
            if result.success:
                with open(output_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(result.markdown)
                print(f"✅ Converted: {input_file} → {output_file}")
            else:
                print(f"❌ Failed: {input_file} - {result.error_message}")

    except Exception as e:
        print(f"❌ Error reading {input_file}: {e}")

async def process_directory(input_dir, output_dir):
    extensions = ['.php', '.html', '.css', '.js', '.txt']  # Types de fichiers à convertir
    os.makedirs(output_dir, exist_ok=True)
    tasks = []

    for root, _, files in os.walk(input_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                input_file_path = Path(root) / file
                relative_path = Path(root).relative_to(input_dir)
                output_subdir = Path(output_dir) / relative_path
                os.makedirs(output_subdir, exist_ok=True)

                output_file_path = output_subdir / (file + ".md")

                # Lancer uniquement la conversion en Markdown, pas de copie des originaux
                tasks.append(convert_file_to_markdown(input_file_path, output_file_path))

    await asyncio.gather(*tasks)

def main():
    default_input = "/Users/adrien/Downloads/G108-main/Lab10"
    default_output = "/Users/adrien/Downloads/G108-main/Lab10-MD"

    print(f"📂 Chemin source par défaut : {default_input}")
    print(f"💾 Chemin de sortie par défaut : {default_output}")

    input_dir = input(f"👉 Dossier source (laisser vide pour défaut) : ").strip() or default_input
    output_dir = input(f"👉 Dossier sortie (laisser vide pour défaut) : ").strip() or default_output

    if not os.path.isdir(input_dir):
        print("❌ Le dossier source n'existe pas.")
        return

    asyncio.run(process_directory(input_dir, output_dir))

if __name__ == "__main__":
    main()