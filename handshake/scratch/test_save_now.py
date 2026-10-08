import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Dismiss any toast if present
        await page.evaluate('''() => {
            const closeBtn = document.querySelector('button[aria-label="Close error"], button[aria-label="Dismiss"]');
            if (closeBtn) closeBtn.click();
        }''')
        await asyncio.sleep(1.0)
        
        # Click Save
        print("Clicking Save button...", flush=True)
        save_btn = page.locator("button:has-text('Save')").first
        await save_btn.click()
        await asyncio.sleep(2.0)
        
        # Check toasts / messages
        toasts = await page.evaluate('''() => {
            const allToasts = Array.from(document.querySelectorAll('[role="status"], [role="alert"], div[class*="toast"]')).map(t => t.innerText.slice(0, 150));
            return allToasts;
        }''')
        print("Toasts after Save:", toasts, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
