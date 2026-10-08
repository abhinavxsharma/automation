import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click Continue on dashboard
        btn = page.locator("button:has-text('Continue')").first
        print("Clicking Continue on dashboard...", flush=True)
        await btn.click()
        await asyncio.sleep(3.0)
        
        print("URL now:", page.url, flush=True)
        print("Title:", await page.title(), flush=True)
        
        # Check active card or modal
        card_info = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            const dialog = document.querySelector('div[role="dialog"]');
            return {
                cardText: card ? card.innerText.slice(0, 300).replace(/\\n+/g, ' ') : 'No card',
                dialogText: dialog ? dialog.innerText.slice(0, 300).replace(/\\n+/g, ' ') : 'No dialog'
            };
        }''')
        print("State on enter:\n", card_info)

if __name__ == "__main__":
    asyncio.run(main())
