import asyncio
import sys
import json
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        cards = await page.evaluate('''() => {
            const cardEls = Array.from(document.querySelectorAll('div.rosetta-card'));
            return cardEls.map((c, i) => {
                const h = c.querySelector('h1, h2, h3, h4, h5, h6');
                const text = c.innerText.slice(0, 150).replace(/\\n+/g, ' ');
                const inputs = Array.from(c.querySelectorAll('input, textarea')).map(inp => ({
                    type: inp.type,
                    value: inp.value.slice(0, 50)
                }));
                const buttons = Array.from(c.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
                
                // Get blockId if available
                const blockWrapper = c.closest('[data-block-id]');
                const blockId = blockWrapper ? blockWrapper.getAttribute('data-block-id') : null;
                
                return {
                    index: i,
                    heading: h ? h.innerText.trim() : null,
                    text: text,
                    blockId: blockId,
                    inputs: inputs,
                    buttons: buttons
                };
            });
        }''')
        print(f"Total cards: {len(cards)}")
        for c in cards:
            print(f"[{c['index']}] blockId: {c['blockId']} | heading: {c['heading']} | buttons: {c['buttons']}")
            print(f"     text: {c['text'][:100]}")
            if c['inputs']:
                print(f"     inputs: {c['inputs']}")

if __name__ == "__main__":
    asyncio.run(main())
