import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        res = await page.evaluate('''() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Start timer');
            if (btn) {
                btn.click();
                return 'Clicked Start timer';
            }
            return 'Start timer not found';
        }''')
        print("Start timer result:", res, flush=True)
        await asyncio.sleep(2.0)
        
        print("URL now:", page.url, flush=True)
        print("Title:", await page.title(), flush=True)
        
        # Check if dialog is gone and what card is on screen
        info = await page.evaluate('''() => {
            const dialog = document.querySelector('div[role="dialog"]');
            const card = document.querySelector('div.rosetta-card');
            return {
                hasDialog: !!dialog,
                cardText: card ? card.innerText.slice(0, 300).replace(/\\n+/g, ' ') : 'No card'
            };
        }''')
        print("State now:", info)

if __name__ == "__main__":
    asyncio.run(main())
