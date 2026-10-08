import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Check current URL
        print("Current URL:", page.url)
        
        # Let's inspect what task is on dashboard or if we can navigate to task 71654a38 or 1520c7f4
        info = await page.evaluate('''() => {
            const banner = document.querySelector('[class*="banner"], [role="alert"], [class*="alert"]');
            const cards = Array.from(document.querySelectorAll('*')).filter(el => {
                const t = el.innerText || '';
                return t.includes('Model Response 1 final answer') || t.includes('Both model responses must genuinely fail');
            });
            return {
                bannerText: banner ? banner.innerText : null,
                foundText: cards.length > 0 ? cards[0].innerText : null
            };
        }''')
        print("Banner info:", info)

if __name__ == "__main__":
    asyncio.run(main())
