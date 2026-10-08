import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click Save progress & exit
        res = await page.evaluate('''() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save progress & exit');
            if (btn) {
                btn.click();
                return 'Clicked Save progress & exit';
            }
            return 'Button not found';
        }''')
        print("Click result:", res, flush=True)
        await asyncio.sleep(4.0)
        
        print("URL now:", page.url, flush=True)
        print("Title now:", await page.title(), flush=True)

if __name__ == "__main__":
    asyncio.run(main())
