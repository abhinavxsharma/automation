import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        print("Active Page URL:", page.url)
        print("Active Page Title:", await page.title())

if __name__ == "__main__":
    asyncio.run(main())
