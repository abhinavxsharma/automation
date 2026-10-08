import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            // Find the blocks related to prompt, image, and model responses
            const blocks = Array.from(document.querySelectorAll('[data-block-id]')).map(b => {
                const id = b.getAttribute('data-block-id');
                const text = b.innerText.slice(0, 150).replace(/\\n+/g, ' ');
                const btns = Array.from(b.querySelectorAll('button')).map(btn => ({
                    text: btn.innerText.trim(),
                    aria: btn.getAttribute('aria-label')
                })).filter(btn => btn.text || btn.aria);
                return { id, text, btns };
            });
            return blocks;
        }''')
        print(f"Total blocks in task: {len(info)}")
        for b in info:
            print(f"[{b['id']}] {b['text'][:80]} | btns: {b['btns']}")

if __name__ == "__main__":
    asyncio.run(main())
