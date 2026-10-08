import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const resolveBtns = Array.from(document.querySelectorAll('button[aria-label="Resolve"]')).map(b => ({
                text: b.innerText,
                parentText: b.closest('li, div[class*="comment"], div[class*="item"]')?.innerText?.slice(0, 100)?.replace(/\\n+/g, ' ')
            }));
            const disagreeBtns = Array.from(document.querySelectorAll('button[aria-label="Disagree"]')).map(b => ({
                text: b.innerText,
                parentText: b.closest('li, div[class*="comment"], div[class*="item"]')?.innerText?.slice(0, 100)?.replace(/\\n+/g, ' ')
            }));
            return { resolveBtns, disagreeBtns };
        }''')
        print("Resolve buttons:")
        for b in info['resolveBtns']:
            print(f"  {b['parentText']}")
        print("\nDisagree buttons:")
        for b in info['disagreeBtns']:
            print(f"  {b['parentText']}")

if __name__ == "__main__":
    asyncio.run(main())
