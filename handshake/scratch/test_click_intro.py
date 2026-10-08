import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        btn = page.locator("div.rosetta-card button[aria-label='Continue']").first
        print("Button visible:", await btn.is_visible(), flush=True)
        await btn.click()
        await asyncio.sleep(1.5)
        
        info = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            const toast = document.querySelector('[role="status"], [role="alert"], .toast, div[class*="toast"]');
            return {
                toast: toast ? toast.innerText : null,
                cardText: card ? card.innerText.slice(0, 200).replace(/\\n+/g, ' ') : null
            };
        }''')
        print("After click:", info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
