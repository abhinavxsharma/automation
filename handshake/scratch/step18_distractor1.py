import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click Continue on the intro card
        res = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            if (!card) return 'No card';
            const btn = Array.from(card.querySelectorAll('button')).find(b => b.textContent.trim() === 'Continue');
            if (!btn) return 'No continue button';
            btn.click();
            return 'Clicked Continue';
        }''')
        print("Click intro result:", res, flush=True)
        await asyncio.sleep(1.5)
        
        # Check Distractor 1 card
        info = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            if (!card) return 'No card';
            const h = card.querySelector('h1, h2, h3, h4, h5, h6');
            return {
                heading: h ? h.innerText.trim() : null,
                text: card.innerText.slice(0, 300).replace(/\\n+/g, ' '),
                inputs: Array.from(card.querySelectorAll('input, textarea')).map(inp => ({
                    tag: inp.tagName,
                    type: inp.type,
                    val: inp.value,
                    placeholder: inp.placeholder
                })),
                buttons: Array.from(card.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean)
            };
        }''')
        print("Distractor 1 card info:", info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
