import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Check text around option 0
        opt0 = page.locator("text='Label–element or axis mis-binding'").first
        count = await opt0.count()
        print("Option 0 count:", count)
        if count > 0:
            print("Clicking option 0...")
            await opt0.click()
            await asyncio.sleep(0.5)
            
        # Check the Continue button inside the Error Type card
        continue_btn = page.locator("button:has-text('Continue')").first
        print("Continue button exists:", await continue_btn.is_visible())
        
        # Click continue
        await continue_btn.click()
        await asyncio.sleep(1.0)
        
        # Check current headings to see if we moved to next step
        headings = await page.locator("h2, h3, h4").all_text_contents()
        print("Headings after click:", [h.strip() for h in headings if h.strip()])

if __name__ == "__main__":
    asyncio.run(main())
