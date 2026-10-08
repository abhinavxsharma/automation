import asyncio
import sys
import json
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        blocks_data = await page.evaluate('''() => {
            const blockEls = Array.from(document.querySelectorAll('[data-block-id]'));
            return blockEls.map(b => {
                const id = b.getAttribute('data-block-id');
                const inputs = Array.from(b.querySelectorAll('input, textarea, select')).map(inp => ({
                    tag: inp.tagName,
                    type: inp.type,
                    value: inp.value,
                    checked: inp.checked,
                    required: inp.required
                }));
                const text = b.innerText.slice(0, 150).replace(/\\n+/g, ' ');
                const hasCard = !!b.querySelector('div.rosetta-card');
                return {
                    id,
                    hasCard,
                    text,
                    inputs
                };
            });
        }''')
        print(f"Total blocks in DOM: {len(blocks_data)}")
        for b in blocks_data:
            print(f"[{b['id']}] card={b['hasCard']} | text: {b['text'][:60]}")
            if b['inputs']:
                print(f"   inputs: {b['inputs']}")

if __name__ == "__main__":
    asyncio.run(main())
