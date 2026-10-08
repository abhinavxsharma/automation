import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const h = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(el => el.innerText.trim()).filter(Boolean);
            const btns = Array.from(document.querySelectorAll('button, a')).map(el => ({
                tag: el.tagName,
                text: el.innerText.trim(),
                aria: el.getAttribute('aria-label'),
                href: el.getAttribute('href')
            })).filter(b => b.text || b.aria);
            
            return {
                headings: h.slice(0, 10),
                buttons: btns.slice(0, 20)
            };
        }''')
        print("Headings:", info['headings'])
        print("Buttons:")
        for b in info['buttons']:
            print(" -", b)

if __name__ == "__main__":
    asyncio.run(main())
