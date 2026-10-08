import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click Confirm time
        print("Clicking Confirm time...", flush=True)
        res = await page.evaluate('''() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Confirm time');
            if (btn) {
                btn.click();
                return 'Clicked Confirm time';
            }
            return 'Confirm time button not found';
        }''')
        print("Click result:", res, flush=True)
        await asyncio.sleep(5.0)
        
        print("\nPage URL now:", page.url, flush=True)
        print("Page Title:", await page.title(), flush=True)
        
        # Check text or status
        info = await page.evaluate('''() => {
            const h = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(el => el.innerText.trim()).filter(Boolean);
            const body = document.body ? document.body.innerText.slice(0, 500).replace(/\\n+/g, ' -- ') : '';
            return {
                headings: h,
                body
            };
        }''')
        print("Headings:", info['headings'])
        print("Body snippet:", info['body'][:300])

if __name__ == "__main__":
    asyncio.run(main())
