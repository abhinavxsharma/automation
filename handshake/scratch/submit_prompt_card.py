import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        page = browser.contexts[0].pages[0]
        
        # Click the submit button inside the editor card
        submit_btn = page.locator('button[aria-label="Submit"]')
        print("Clicking Submit button on prompt card...")
        await submit_btn.click()
        await asyncio.sleep(2)
        
        # Check if there is a confirmation modal dialog
        dialog = page.locator('[role="dialog"]')
        if await dialog.count() > 0 and await dialog.is_visible():
            print("Confirmation dialog appeared:")
            print(await dialog.inner_text())
            # Find confirm button
            confirm_btn = dialog.locator('button:has-text("Delete"), button:has-text("Confirm"), button:has-text("Continue"), button:has-text("Submit")').first
            if await confirm_btn.is_visible():
                print(f"Clicking confirm button: {await confirm_btn.inner_text()}")
                await confirm_btn.click()
                await asyncio.sleep(2)
                
        # Take screenshot of page after submitting
        await page.screenshot(path='handshake/scratch/after_prompt_submit.png')
        print("Saved after_prompt_submit.png")

if __name__ == '__main__':
    asyncio.run(main())
