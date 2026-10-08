import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button, a')).map(b => ({
                tag: b.tagName,
                text: b.innerText.trim(),
                href: b.getAttribute('href')
            })).filter(b => b.text || b.href);
            
            return {
                title: document.title,
                url: window.location.href,
                headings: Array.from(document.querySelectorAll('h1, h2, h3, h4, h5')).map(h => h.innerText.trim()),
                buttons: btns
            };
        }''')
        print("Page info:\n", info)

if __name__ == "__main__":
    asyncio.run(main())
