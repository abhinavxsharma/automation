import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]
        print("URL:", page.url)
        print("Title:", await page.title())
        
        # Check active card title or elements
        elements = await page.locator("h2, h3, h4").all_text_contents()
        print("Headings:", [e.strip() for e in elements if e.strip()])
        
        # Check buttons
        buttons = await page.locator("button").all_text_contents()
        print("Buttons:", [b.strip() for b in buttons if b.strip()][:15])

if __name__ == "__main__":
    asyncio.run(main())
