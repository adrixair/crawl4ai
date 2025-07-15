import asyncio
import threading
import sys
from playwright.async_api import async_playwright

# Fonction pour écouter la touche 'q' dans le terminal
def wait_for_q(loop):
    print("➡️  Appuie sur 'q' puis Entrée pour fermer le navigateur et sauvegarder le profil.")
    for line in sys.stdin:
        if line.strip().lower() == 'q':
            loop.call_soon_threadsafe(loop.stop)
            break

async def open_profile():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="/Users/adrien/.crawl4ai/profiles/prof",
            headless=False
        )
        page = await context.new_page()
        await page.goto("https://www.google.com")

        # Lance un thread pour écouter la touche 'q'
        loop = asyncio.get_event_loop()
        threading.Thread(target=wait_for_q, args=(loop,), daemon=True).start()

        print("🧭 Navigateur ouvert. Configure ton profil...")
        await asyncio.Event().wait()  # Attend que l’utilisateur appuie sur 'q'

        await context.close()
        print("✅ Profil sauvegardé et navigateur fermé.")

asyncio.run(open_profile())