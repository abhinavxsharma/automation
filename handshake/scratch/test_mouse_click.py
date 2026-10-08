import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click Continue at (770, 735)
        print("Clicking at (770, 735)...", flush=True)
        await page.mouse.click(770, 735)
        await asyncio.sleep(2.0)
        
        # Check current cards
        card_text = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            return card ? card.innerText.slice(0, 300).replace(/\\n+/g, ' ') : 'No card';
        }''')
        print("Card text after mouse click:", card_text, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
