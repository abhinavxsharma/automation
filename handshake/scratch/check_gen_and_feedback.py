import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        page = browser.contexts[0].pages[0]
        
        # Check text in the page
        body_text = await page.evaluate("() => document.body ? document.body.innerText : ''")
        lines = body_text.split('\n')
        
        # Look for Block 1 / Block 2 status
        print("=== Checking Generation Status ===")
        for i, line in enumerate(lines):
            if "Block 1" in line or "Block 2" in line or "Generating" in line or "boxed" in line:
                print(f"L{i}: {line}")
                
        # Check feedback items in sidebar
        print("\n=== Feedback Sidebar Items ===")
        fb_buttons = await page.locator('button:has-text("Needs attention"), button:has-text("All")').all()
        print(f"Feedback tab buttons: {len(fb_buttons)}")
        
        cards = await page.locator('[data-testid*="feedback"], .rounded-lg, .border').all()
        # Look for any text with 'Finding number'
        findings = await page.locator('text=Finding number').all()
        print(f"Total findings on screen: {len(findings)}")

if __name__ == '__main__':
    asyncio.run(main())
