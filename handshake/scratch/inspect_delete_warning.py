import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click Start timer if visible to dismiss timer modal
        start_btn = page.locator("button:has-text('Start timer')").first
        if await start_btn.is_visible():
            print("Clicking Start timer to dismiss modal...")
            await start_btn.click()
            await asyncio.sleep(1.0)
            
        # Now inspect the card
        info = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            if (!card) return 'No card';
            
            const btns = Array.from(card.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label')
            }));
            
            return {
                text: card.innerText.replace(/\\n+/g, ' '),
                btns
            };
        }''')
        print("Card info:\n", info)

if __name__ == "__main__":
    asyncio.run(main())
