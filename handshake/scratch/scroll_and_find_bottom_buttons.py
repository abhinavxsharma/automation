import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Scroll to bottom
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1.0)
        
        # Also check any scrolling containers inside main
        info = await page.evaluate('''() => {
            const bottomElements = Array.from(document.querySelectorAll('button, div[class*="bottom"], div[class*="footer"], footer')).map(el => {
                const rect = el.getBoundingClientRect();
                return {
                    tag: el.tagName,
                    text: el.innerText?.trim(),
                    aria: el.getAttribute('aria-label'),
                    y: Math.round(rect.y),
                    h: Math.round(rect.height),
                    w: Math.round(rect.width)
                };
            }).filter(el => el.text || el.aria);
            
            return {
                scrollY: window.scrollY,
                scrollHeight: document.body.scrollHeight,
                bottomElements: bottomElements.slice(-20)
            };
        }''')
        print(f"Scroll Y: {info['scrollY']}, Height: {info['scrollHeight']}")
        print("Bottom elements:")
        for el in info['bottomElements']:
            print(" -", el)

if __name__ == "__main__":
    asyncio.run(main())
