import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click the radio button input directly using force=True
        print("Clicking radio 0 directly via locator...")
        radio = page.locator("#radio-00289b96-5d4f-4efc-821c-14dd0cb7ae0a-0")
        await radio.click(force=True)
        await asyncio.sleep(0.5)
        
        # Click continue button
        print("Clicking Continue button...")
        continue_btn = page.locator("button:has-text('Continue')").first
        await continue_btn.click()
        await asyncio.sleep(1.5)
        
        # Check current headings to see if we moved to next step!
        headings = await page.locator("h2, h3, h4").all_text_contents()
        print("Headings after continue:", [h.strip() for h in headings if h.strip()])

if __name__ == "__main__":
    asyncio.run(main())
