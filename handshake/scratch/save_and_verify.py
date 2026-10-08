import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Check toggle button state
        toggle_btn = page.locator("button[aria-label='View task without markdown or Latex formatting']").first
        if await toggle_btn.is_visible():
            print("Toggling back to formatted view...", flush=True)
            await toggle_btn.click()
            await asyncio.sleep(1.0)
            
        # Click Save
        print("Clicking Save button...", flush=True)
        save_btn = page.locator("button:has-text('Save')").first
        await save_btn.click()
        await asyncio.sleep(2.0)
        
        # Verify save toast or state
        info = await page.evaluate('''() => {
            const toasts = Array.from(document.querySelectorAll('[role="status"], [role="alert"], div[class*="toast"]')).map(t => t.innerText);
            const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Save') || b.innerText.includes('Saved'));
            return {
                toasts,
                saveBtnText: saveBtn ? saveBtn.innerText.trim() : null
            };
        }''')
        print("Save info:", info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
