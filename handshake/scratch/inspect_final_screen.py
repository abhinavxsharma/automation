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
            const btns = Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                className: b.className
            })).filter(b => b.text || b.aria);
            
            return {
                cardText: card ? card.innerText.slice(0, 500).replace(/\\n+/g, ' ') : 'No card',
                allButtons: btns
            };
        }''')
        print("Card text:", info['cardText'], flush=True)
        print("\nAll buttons on page:")
        for b in info['allButtons']:
            print(f"  text: '{b['text']}' | aria: '{b['aria']}' | class: '{b['className'][:50]}'")

if __name__ == "__main__":
    asyncio.run(main())
