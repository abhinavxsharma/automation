import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            if (!card) return 'No card';
            const btns = Array.from(card.querySelectorAll('button')).map(b => ({
                text: b.textContent.trim(),
                disabled: b.disabled,
                type: b.type,
                outer: b.outerHTML
            }));
            return {
                cardHtml: card.innerHTML.slice(0, 500),
                btns
            };
        }''')
        print("Intro card info:", info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
