import sys
from pathlib import Path
from urllib.parse import urlparse
import asyncio

# Ajoute le dossier courant (app2) au PYTHONPATH pour permettre l'import local
sys.path.append(Path(__file__).parent.as_posix())

from main import main  # importe la coroutine de crawl définie dans app2/main.py

# Liste d'URLs de départ
URLS = [
    "https://www.workally.com.br",
]

OUTPUT_DIR = Path(__file__).parent / "crawl_results"
OUTPUT_DIR.mkdir(exist_ok=True)

async def run_batch(urls: list[str]) -> None:
    
    for url in urls:
        print(f"\n=== Crawl : {url} ===")
        pages = await main(url) 
        domain = urlparse(url).netloc.replace("www.", "")
        out_path = OUTPUT_DIR / f"{domain}.md"
        out_path.write_text("\n".join(pages) if pages else "")
        print(f"→ {len(pages)} page(s) enregistrée(s) dans {out_path}")

if __name__ == "__main__":
    asyncio.run(run_batch(URLS))