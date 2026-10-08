import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        btns = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('button, a')).map(b => ({
                tag: b.tagName,
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                className: b.className,
                disabled: b.disabled,
                type: b.type
            })).filter(b => b.text || b.aria);
        }''')
        print(f"Total buttons/links: {len(btns)}")
        for b in btns:
            if any(k in (b['text'] + str(b['aria'])).lower() for k in ['submit', 'finish', 'complete', 'save', 'exit', 'pause', 'done']):
                print(" ->", b)

if __name__ == "__main__":
    asyncio.run(main())
