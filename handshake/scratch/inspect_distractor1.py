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
            const inputs = Array.from(card.querySelectorAll('input, textarea')).map(inp => ({
                tag: inp.tagName,
                type: inp.type,
                name: inp.name,
                id: inp.id,
                value: inp.value,
                placeholder: inp.placeholder
            }));
            const buttons = Array.from(card.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
            return {
                text: card.innerText.slice(0, 300).replace(/\\n+/g, ' '),
                inputs,
                buttons
            };
        }''')
        print("Distractor 1 card details:", info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
