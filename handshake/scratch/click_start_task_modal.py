import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        btn = page.locator("button:has-text('Start task')").first
        print("Start task button visible:", await btn.is_visible(), flush=True)
        await btn.click()
        await asyncio.sleep(4.0)
        
        print("URL now:", page.url, flush=True)
        print("Title:", await page.title(), flush=True)

if __name__ == "__main__":
    asyncio.run(main())
